__version__ = '0.1.2'

import orjson
import hashlib

import pydantic
import typing


def _json_encoder(o: typing.Any):
    if isinstance(o, pydantic.BaseModel):
        return o.dict()
    raise TypeError


def hash(obj: typing.Any) -> bytes:
    return hashlib.sha1(orjson.dumps(
        obj, default=_json_encoder,
        option=orjson.OPT_STRICT_INTEGER | orjson.OPT_NAIVE_UTC | orjson.OPT_NON_STR_KEYS | orjson.OPT_SERIALIZE_NUMPY | orjson.OPT_SORT_KEYS)).digest()
