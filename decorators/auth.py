import time
import traceback
from functools import wraps
from fastapi_jwt_auth.exceptions import MissingTokenError, InvalidHeaderError

from exceptions.auth_exception import AuthExceptions
from exceptions.handled import HandledException


def timeit(func):
    @wraps(func)
    def timeit_wrapper(*args, **kwargs):
        start_time = time.perf_counter()
        result = func(*args, **kwargs)
        end_time = time.perf_counter()
        total_time = end_time - start_time
        return result, total_time
    return timeit_wrapper


def auth_handler(func):
    @wraps(func)
    def auth_handler_wrapper(*args, **kwargs):
        try:
            kwargs["Authorize"].jwt_required()
            result = func(*args, **kwargs)
        except (MissingTokenError, InvalidHeaderError):
            traceback.print_exc()
            raise AuthExceptions.UNAUTHORIZED
        except HandledException as e:
            raise e.args[0]
        return result
    return auth_handler_wrapper


# # @auth_handler2(AuthExceptions.UNAUTHORIZED)
# def auth_handler2(exception=None):
#     def decorator(func):
#         @wraps(func)
#         def auth_handler_wrapper(*args, **kwargs):
#             try:
#                 print(args)
#                 print(kwargs)
#                 kwargs["Authorize"].jwt_required()
#                 result = func(*args, **kwargs)
#             except (
#                     MissingTokenError,
#                     InvalidHeaderError,
#
#             ) as e:
#                 # traceback.print_exc()
#                 if exception:
#                     raise exception
#                 else:
#                     raise e
#             return result
#         return auth_handler_wrapper
#     return decorator
