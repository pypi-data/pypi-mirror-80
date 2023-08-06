"""
Helper functions for extracting values from fields.
"""

import hashlib
from sirad import config, Log
from datetime import datetime

debug = Log(__name__, "date").debug

_debug_threshold = 20
_debug_count = {}

def salted_hash(value, salt):
    if salt is None:
        k = value.encode("utf-8")
    else:
        k = (value + salt).encode("utf-8")
    return hashlib.sha1(k).hexdigest()

def standard_datetime(dobj):
    return datetime.strftime(dobj, config.DATE_FORMAT)

def date(raw, date_format, column):
    """
    Extract date from value given date format. If date
    can't be extracted, return empty string.
    """
    global _debug_thresholod, _debug_count
    dobj = None
    for fmt in date_format.split("|"):
        try:
            dobj = datetime.strptime(raw, fmt)
            break
        except ValueError:
            if _debug_count.get(column, 0) < _debug_threshold:
                debug("Unable to process '{}' value '{}' as date with format '{}'".format(column, raw, fmt))
                _debug_count[column] = _debug_count.get(column, 0) + 1
            pass
    if dobj is None:
        return ""
    else:
        return standard_datetime(dobj)

def data(raw, field):
    """
    Extract data value
    """
    if not field.data:
        return None
    if raw in config.NULL_VALUES:
        return ""
    else:
        if field.hash:
            return salted_hash(raw, config.get_option("DATA_SALT"))
        elif field.type == "date":
            if isinstance(raw, datetime):
                return standard_datetime(raw)
            else:
                return date(raw, field.format, field.name)
        else:
            return raw

def pii(raw, field):
    """
    Extract pii value
    """
    if not field.pii:
        return None
    if raw in config.NULL_VALUES:
        return ""
    else:
        if field.hash:
            return salted_hash(raw, config.get_option("PII_SALT"))
        elif field.type == "date":
            if isinstance(raw, datetime):
                return standard_datetime(raw)
            else:
                return date(raw, field.format, field.name)
        else:
            return raw
