__version__ = '0.1.1'

import orjson
import hashlib

import pydantic
import typing


async def hash(obj: typing.Any, default: typing.Optional[typing.Callable] = None) -> bytes:
    def _default(o: object):
        default(o)
        if isinstance(o, pydantic.BaseModel):
            return o.dict()
        raise TypeError

    return hashlib.sha1(orjson.dumps(
        obj, default=_default,
        option=orjson.OPT_STRICT_INTEGER | orjson.OPT_NAIVE_UTC | orjson.OPT_NON_STR_KEYS | orjson.OPT_PASSTHROUGH_SUBCLASS | orjson.OPT_SERIALIZE_NUMPY | orjson.OPT_SORT_KEYS)).digest()
