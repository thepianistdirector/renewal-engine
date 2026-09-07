import unittest

from renewal_engine.discovery import discover
from renewal_engine.transformation import transform, patch


def program(call="p.readfp(stream, filename=source)", imp="import configparser", ctor="configparser.ConfigParser()"):
    return ("def load(stream, source):\n    " + imp + "\n    p = " + ctor + "\n    " + call + "\n    return p\n").encode()


class RecipeTests(unittest.TestCase):
    def test_exact_patch_and_unrelated_bytes(self):
        original = b'# p.readfp is a comment\ntext = "readfp(filename=)"\n' + program()
        result = transform(original, discover(original))
        self.assertEqual(result, original.replace(b'p.readfp(stream, filename=source)', b'p.read_file(stream, source=source)'))
        self.assertEqual(transform(result, discover(result)), result)
        self.assertIn('-    p.readfp', patch(original, result, 'example.py'))

    def test_alias_and_keyword_mapping(self):
        original = program('p.readfp(fp=stream, filename=source)', 'from configparser import ConfigParser as CP', 'CP()')
        result = transform(original, discover(original))
        self.assertIn(b'p.read_file(f=stream, source=source)', result)
        for call in ['p.readfp(stream)', 'p.readfp(stream, source)', 'p.readfp(fp=stream)']:
            with self.subTest(call=call):
                d=discover(program(call));self.assertTrue(d.edits)

    def test_unsupported_never_changes(self):
        variants = [
            program('p.readfp(*stream)'), program('p.readfp(stream, **source)'),
            program('p.readfp(stream, source=source)'), program('p.readfp()'),
            program('p.readfp(stream, filename=get_name())'),
            program('p.readfp(stream, source, filename=source)'),
            program('p.readfp(stream, fp=stream)'), program(ctor='Other()'),
            program(ctor='configparser.ConfigParser(strict=False)'),
            program().replace(b'p.readfp', b'q.readfp'),
            program().replace(b'    p.readfp', b'    p = Other()\n    p.readfp'),
            program().replace(b'    p.readfp', b'    if source:\n        p.readfp'),
            b'@decorate\n' + program(),
            program().replace(b'def load(stream, source)',b'def load(stream, source, configparser)'),
            b'configparser.ConfigParser = Other\n' + program(),
            b'import configparser\nconfigparser.__dict__["ConfigParser"] = Other\n' + program(),
            b'setattr(configparser, "ConfigParser", Other)\n' + program(),
            program().replace(b'import configparser',b'import other as configparser'),
            b'class Other:\n    def readfp(self, stream): pass\nobj=Other()\nobj.readfp(stream)\n',
        ]
        for source in variants:
            with self.subTest(source=source):
                d=discover(source);self.assertFalse(d.edits);self.assertEqual(transform(source,d),source)
                self.assertTrue(all(f.status == 'REVIEW NEEDED' for f in d.findings))

    def test_utf8_crlf_and_multiline_offsets(self):
        original = '# café\n'.encode() + program('p.readfp(\n        stream,\n        filename=source\n    )')
        original = original.replace(b'\n', b'\r\n')
        result=transform(original,discover(original))
        self.assertEqual(result,original.replace(b'p.readfp',b'p.read_file').replace(b'filename=',b'source='))

    def test_shadow_and_encoding_refusal(self):
        self.assertFalse(discover(program(), shadowed=True).edits)
        for source in [b'# coding: latin-1\n# caf\xe9\n'+program(), b'def invalid(', b'\xef\xbb\xbf'+program()]:
            d=discover(source);self.assertFalse(d.edits);self.assertTrue(d.findings)

    def test_changed_source_invalidates_edits(self):
        source=program();d=discover(source)
        with self.assertRaisesRegex(ValueError,'precondition'):
            transform(b'\n'+source,d)
        with self.assertRaisesRegex(ValueError,'digest precondition'):
            transform(source.replace(b'configparser',b'other_module'),d)

    def test_support_belongs_to_exact_call(self):
        source=program('p.readfp(stream); q.readfp(stream)')
        d=discover(source)
        self.assertEqual([f.status for f in d.findings],['SUPPORTED','REVIEW NEEDED'])
        source=program().replace(b'\n',b'\r')
        d=discover(source)
        self.assertEqual([f.status for f in d.findings],['SUPPORTED'])
        self.assertIn(b'p.read_file',transform(source,d))

    def test_no_final_newline_patch(self):
        source=program().rstrip(b'\n');candidate=transform(source,discover(source))
        self.assertIn('\\ No newline at end of file',patch(source,candidate,'fixture.py'))


if __name__ == '__main__':
    unittest.main()
