import json
import zlib
from functools import wraps
import logging
import traceback as tb

from flask import make_response
from werkzeug.exceptions import HTTPException
import pandas as pd

from tshistory import util


def has_formula():
    try:
        import tshistory_formula.api
    except ImportError:
        return False
    return True


def has_supervision():
    try:
        import tshistory_supervision.api
    except ImportError:
        return False
    return True


def handler():
    classes = []
    if has_supervision():
        from tshistory_supervision.tsio import timeseries as tss
        classes.append(tss)
    if has_formula():
        from tshistory_formula.tsio import timeseries as tsf
        classes.append(tsf)
    from tshistory.tsio import timeseries as tsb
    classes.append(tsb)

    if len(classes) <= 2:
        return classes[0]

    class timeseries(tss, tsf):
        pass
    return timeseries


def utcdt(dtstr):
    return pd.Timestamp(dtstr)


def todict(dictstr):
    if dictstr is None:
        return None
    return json.loads(dictstr)


def enum(*enum):
    " an enum input type "

    def _str(val):
        if val not in enum:
            raise ValueError(f'Possible choices are in {enum}')
        return val
    _str.__schema__ = {'type': 'enum'}
    return _str


L = logging.getLogger('tshistory_rest')

def onerror(func):
    @wraps(func)
    def wrapper(*a, **k):
        try:
            return func(*a, **k)
        except Exception as err:
            if isinstance(err, HTTPException):
                raise
            L.exception('oops')
            tb.print_exc()
            response = make_response(str(err))
            response.headers['Content-Type'] = 'text/plain'
            response.status_code = 418
            return response

    return wrapper


def series_response(format, series, metadata, code):
    if format == 'json':
        if series is not None:
            response = make_response(
                series.to_json(orient='index',
                               date_format='iso')
            )
        else:
            response = make_response('null')
        response.headers['Content-Type'] = 'text/json'
        response.status_code = code
        return response

    assert format == 'tshpack'
    response = make_response(
        util.pack_series(metadata, series)
    )
    response.headers['Content-Type'] = 'application/octet-stream'
    response.status_code = code
    return response

