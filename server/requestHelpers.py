from typing import Any, Union
from flask.wrappers import Request


def get_param(req: Request, param: str) -> Union[Any, None]:
    """ Returns the query param value from the request """
    return req.args.get(param)
