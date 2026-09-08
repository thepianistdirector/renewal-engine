"""Unambiguous finite JSON for retained evidence and supplied observations."""
import json


def _object(pairs):
    result={}
    for key,value in pairs:
        if key in result:
            raise ValueError('duplicate JSON object key: '+key)
        result[key]=value
    return result


def _constant(value):
    raise ValueError('non-finite JSON number is not supported')


def loads(data):
    try:
        return json.loads(data,object_pairs_hook=_object,parse_constant=_constant)
    except RecursionError as exc:
        raise ValueError('JSON nesting exceeds supported bounds') from exc
