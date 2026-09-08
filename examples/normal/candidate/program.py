"""Original AGPL-3.0 ConfigParser migration fixture. See PROVENANCE.md."""

def load_default(stream, source):
    import configparser
    parser = configparser.ConfigParser()
    parser.read_file(stream)
    return parser


def load_positional(stream, source):
    from configparser import ConfigParser
    parser = ConfigParser()
    parser.read_file(stream, source)
    return parser


def load_keyword(stream, source):
    import configparser as config
    parser = config.ConfigParser()
    parser.read_file(f=stream, source=source)
    return parser
