import traceback
import warnings
from typing import Any, Type


def default_encoder(o: Any) -> Any:
    kind: Type[Any] = type(o)

    if issubclass(kind, BaseException):
        o: BaseException
        tb = o.__traceback__
        result = {
            "exception": o.__class__.__name__,
            "traceback": traceback.format_tb(tb),
            "message": str(o),
        }
        return result

    warnings.warn("Unable to serialize object: %r" % o, UserWarning)
    return repr(o)
