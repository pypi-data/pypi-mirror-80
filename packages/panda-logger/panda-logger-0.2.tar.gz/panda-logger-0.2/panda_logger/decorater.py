import json
from functools import wraps
import time

from . import logger

__all__ = ['log_request_and_response']

FORMAT_LOG_REQUEST_AND_RESPONSE = '[request={}][response={}][elapsed={}ms]'


def log_request_and_response(view_func):
    @wraps(view_func)
    def log(*args, **kwargs):
        request = args[0]
        request_dict = getattr(request, request.method).dict()
        start = time.time()
        response = view_func(*args, **kwargs)
        elapsed = int((time.time() - start) * 1000)
        response_dict = json.loads(response.getvalue())
        message = FORMAT_LOG_REQUEST_AND_RESPONSE.format(
            request_dict, response_dict, elapsed)
        logger.patch(lambda r: r.update(name=view_func.__module__,
                                        function=view_func.__name__,
                                        line=view_func.__code__.co_firstlineno)
                     ).info(message)
        return response

    return log


if __name__ == "__main__":
    pass
