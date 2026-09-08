"""Trusted original AGPL fixture driver; invoked only by hardlink-demo."""
import contextlib
import io
import json
from pathlib import Path
import runpy
import sys
import warnings

case = json.loads(sys.stdin.read())
source = Path(case['source'])
target = Path(case['target'])
if case['source_exists']:
    source.write_bytes(bytes.fromhex(case['content_hex']))
if case['target_kind'] == 'file':
    target.write_bytes(b'existing destination')
elif case['target_kind'] == 'directory':
    target.mkdir()
module = runpy.run_path(sys.argv[1])
exception = None
stdout = io.StringIO()
with warnings.catch_warnings(record=True) as caught, contextlib.redirect_stdout(stdout):
    warnings.simplefilter('always')
    try:
        returned = module['link'](str(source), str(target))
    except Exception as error:
        returned = None
        exception = {'type':type(error).__name__, 'args':list(error.args),
                     'errno':getattr(error,'errno',None), 'filename':getattr(error,'filename',None),
                     'filename2':getattr(error,'filename2',None)}
print(json.dumps({'returned':returned,'stdout':stdout.getvalue(),'exception':exception,
                  'warnings':[{'category':type(w.message).__name__,'message':str(w.message),'lineno':w.lineno} for w in caught]}))
