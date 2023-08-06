# 储存单位
import asyncio
import os
import platform
import re

# 文件大小单位
import traceback
from functools import wraps

import requests
from aiohttp import ClientProxyConnectionError

from re_common.baselibrary.utils.core.requests_core import MsgCode

SUFFIX = ['B', 'KB', 'MB', 'GB', 'TB', 'PB', 'EB', 'ZB', 'YB']
# 系统的分割符
__os_sep__ = "\\" if platform.system() == 'Windows' else os.sep
# 标准文件名正着
_filename_ascii_strip_re = re.compile(r'[^A-Za-z0-9_.-]')
# windows的设备文件
_windows_device_files = ('CON', 'AUX', 'COM1', 'COM2', 'COM3', 'COM4', 'LPT1',
                         'LPT2', 'LPT3', 'PRN', 'NUL')

import warnings


# https://blog.csdn.net/qq_39314099/article/details/83822593
def deprecated(message):
    def deprecated_decorator(func):
        @wraps(func)
        def deprecated_func(*args, **kwargs):
            warnings.warn("{} is a deprecated function. {}".format(func.__name__, message),
                          category=DeprecationWarning,
                          stacklevel=2)
            warnings.simplefilter('default', DeprecationWarning)
            return func(*args, **kwargs)

        return deprecated_func

    return deprecated_decorator


def request_try_except(func):
    @wraps(func)
    def wrapTheFunction(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except requests.exceptions.ReadTimeout as e:
            dicts = {"code": MsgCode.TIME_OUT_ERROR,
                     "msg": "time out, {}".format(repr(e))}
            return False, dicts
        except requests.exceptions.ProxyError as e:
            dicts = {"code": MsgCode.PROXY_ERROR,
                     "msg": "proxy error, {}".format(repr(e))}
            return False, dicts
        except:
            dicts = {"code": MsgCode.ON_KNOW,
                     "msg": traceback.format_exc()}
            return False, dicts

    return wrapTheFunction


def aiohttp_try_except(func):
    @wraps(func)
    async def wrapTheFunction(*args, **kwargs):
        try:
            return await func(*args, **kwargs)
        except ClientProxyConnectionError as e:
            dicts = {"code": MsgCode.PROXY_ERROR,
                     "msg": "proxy error, {}".format(repr(e))}
            return False, dicts
        except asyncio.exceptions.TimeoutError as e:
            dicts = {"code": MsgCode.TIME_OUT_ERROR,
                     "msg": "time out, {}".format(repr(e))}
            return False, dicts
        except Exception as e:
            dicts = {"code": MsgCode.ON_KNOW,
                     "msg": traceback.format_exc()}
            return False, dicts

    return wrapTheFunction
