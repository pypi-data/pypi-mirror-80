"""
Memoization for Python, with optional TTL (measured in time or function call count) for the cached results.
"""


from sys import modules
from enum import Enum
import time


class TTLUnit(Enum):
    SECONDS = 'seconds'
    MINUTES = 'minutes'
    CALL_COUNT = 'call_count'


class Cache(dict):
    def add_data(self, hash, data, ttl=None, ttl_unit=TTLUnit.SECONDS):
        dataobj = {'data': data}
        if ttl is not None and ttl_unit is not None:
            dataobj['ttl'] = ttl
            dataobj['ttl_unit'] = ttl_unit
        if ttl_unit in (TTLUnit.MINUTES, TTLUnit.SECONDS):
            dataobj['timestamp'] = time.time()
        self[hash] = dataobj

    def get_data_if_cached(self, hash):

        if hash not in self:
            return None

        dataobj = self[hash]
        data = dataobj['data']

        if 'ttl' not in dataobj or 'ttl_unit' not in dataobj:
            return data

        if dataobj['ttl_unit'] == TTLUnit.CALL_COUNT:
            if dataobj['ttl'] <= 0:
                del self[hash]
                return None
            dataobj['ttl'] -= 1
            return data

        elif dataobj['ttl_unit'] in (TTLUnit.SECONDS, TTLUnit.MINUTES):
            ttl_seconds = dataobj['ttl'] if dataobj['ttl_unit'] == TTLUnit.SECONDS else 60.0 * dataobj['ttl']
            if time.time() - dataobj['timestamp'] < ttl_seconds:
                return data
            else:
                del self[hash]
                return None

        else:
            raise ValueError(f'Unknown ttl_unit: {dataobj["ttl_unit"]}')

    def clear_cache(self):
        self.clear()


this = modules[__name__]
this._cache = Cache()


def memoize(func=None, ttl=None, ttl_unit=None):
    if func is not None:
        def memoized_func(*args, **kwargs):
            invocation_string = '~'.join((
                func.__name__,
                '~'.join((str(arg) for arg in args)),
                '~'.join((f'{str(k)}:{str(v)}' for k, v in kwargs.items()))
            ))
            invocation_hash = hash(invocation_string)
            if (cached_data := this._cache.get_data_if_cached(invocation_hash)) is not None:
                return cached_data
            function_result = func(*args, **kwargs)
            this._cache.add_data(invocation_hash, function_result, ttl, ttl_unit)
            return function_result
        return memoized_func
    else:
        def decorator(func):
            if ttl <= 0:  # No decorating needed
                return func

            def memoized_func(*args, **kwargs):
                invocation_string = '~'.join((
                    func.__name__,
                    '~'.join((str(arg) for arg in args)),
                    '~'.join((f'{str(k)}:{str(v)}' for k, v in kwargs.items()))
                ))
                invocation_hash = hash(invocation_string)
                if (cached_data := this._cache.get_data_if_cached(invocation_hash)) is not None:
                    return cached_data
                function_result = func(*args, **kwargs)
                this._cache.add_data(invocation_hash, function_result, ttl, ttl_unit)
                return function_result
            return memoized_func
        return decorator
