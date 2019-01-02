from datetime import date
from decimal import Decimal
from enum import Enum
from functools import wraps
from inspect import signature
from json import dumps, JSONEncoder
from time import mktime
from typing import Callable

from flask import current_app
from flask import make_response
from werkzeug.local import LocalProxy

from core.models.budget import Model

logger = LocalProxy(lambda: current_app.logger)


def unpack_args(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        for arg in args:
            if isinstance(arg, dict):
                kwargs.update(arg)
        transformer = ArgumentTransformer(kwargs, None, None, f, verbose=False)
        return f(**transformer.transform())

    return wrapper


@unpack_args
def pre_mapping(key_mappings: dict = None, value_mappings: dict = None, handler: Callable = None):
    def decorator(f):
        h = handler or f

        @wraps(f)
        def wrapper(*args, **kwargs):
            transformer = ArgumentTransformer(kwargs, key_mappings, value_mappings, h)
            return f(*args, **transformer.transform())

        return wrapper

    return decorator


def post_mapping(payload_type="JSON"):
    def decorator(f):
        @wraps(f)
        def wrapper(*args, **kwargs):
            payload = f(*args, **kwargs)
            if payload_type == "JSON":
                payload = dumps(payload, cls=CustomizeEncoder)
            else:
                raise Exception("Unsupported payload type", payload_type)
            return make_response(payload)

        return wrapper

    return decorator


class CustomizeEncoder(JSONEncoder):
    def default(self, o):
        if isinstance(o, Enum):
            return o.name
        if isinstance(o, Decimal):
            return float(o)
        if isinstance(o, date):
            return int(mktime(o.timetuple()) * 1000)
        if isinstance(o, set):
            return list(o)
        if isinstance(o, Model):
            return o.to_dict()
        if hasattr(o, '__dict__'):
            return o.__dict__
        return super().default(o)


class ArgumentTransformer:
    def __init__(self, kwargs, key_mappings, value_mappings, target_function, verbose=True):
        self.kwargs_items = kwargs.items()
        self.key_mappings = key_mappings
        self.value_mappings = value_mappings
        self.target_function_name = target_function.__name__
        self.filter_names = signature(target_function).parameters.keys()
        self.verbose = verbose

    def transform(self):
        self.log("Transforming payload: %s by mapping_d %s" % (self.kwargs_items, self.key_mappings))

        items = self.kwargs_items
        if self.key_mappings is not None:
            items = self.map_keys(items)
        if self.filter_names:
            items = filter(self.arg_filter, items)
        if self.value_mappings is not None:
            items = map(self.value_mapper, items)

        transformed = dict(items)
        self.log("Transformed payload: %s" % transformed)
        return transformed

    def map_keys(self, items):
        payload = dict(items)

        def map_key(key):
            if isinstance(key, str):
                return payload.get(key, None)
            elif isinstance(key, dict):
                return {map_key(k): map_key(v) for k, v in key.items()}
            elif isinstance(key, list):
                return [map_key(i) for i in key]
            else:
                raise Exception("Unknown mappings type for %s during context switching" % str(key))

        return map(lambda item: (item[0], map_key(item[1])), self.key_mappings.items())

    def arg_filter(self, args):
        return args[0] in self.filter_names

    def value_mapper(self, args):

        key, val = args
        if key not in self.value_mappings:
            return args
        mapper = eval(self.value_mappings[key])
        if val is not None:
            val = mapper(val)
        return key, val

    def log(self, *args):
        # TODO: setup logging configuration
        if self.verbose:
            print(*args)


# TODO: MOVE TO MODULE
def t_date(o):
    return date.fromtimestamp(int(o) / 1000)


def t_decimal(o):
    return Decimal(o)


def t_delta(d):
    from dateutil.relativedelta import relativedelta
    parameters = dict(zip(d.keys(), map(int, d.values())))
    return relativedelta(**parameters)


def t_nullable_id(i):
    return int(i) if str(i).strip().isdigit() else None


def to_single_dict(multi_dict):
    return {k: multi_dict.get(k) for k in multi_dict.keys()}
