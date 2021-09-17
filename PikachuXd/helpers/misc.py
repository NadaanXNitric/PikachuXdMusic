from functools import wraps
from time import time


def exec_time(func):
    @wraps(func)
    async def _time_it(*args, **kwargs):
        t1 = time()
        try:
            return await func(*args, **kwargs)
        finally:
            t2 = time()
            total = t2 - t1
            total = round(total, 3)
            print(f"{func.__name__} Tᴏᴏᴋ : {total} Sᴇᴄᴏɴᴅs")
            return _time_it
