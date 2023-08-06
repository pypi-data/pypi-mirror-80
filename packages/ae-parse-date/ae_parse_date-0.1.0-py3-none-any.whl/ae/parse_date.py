"""
parse date strings more flexible and less strict
================================================

This module is pure python and has no namespace external dependencies.

The :func:`parse_date` helper function is converting a wide range
of date and datetime string literal formats into the built-in types
:class:`datetime.datetime` and :class:`datetime.date`.

This function extends (and fully replaces) Pythons standard method
:meth:`~datetime.datetime.strptime` and supports multiple date formats
which are much more flexible interpreted.
"""
import datetime
from typing import Any, Dict, Optional, Tuple, Union

from ae.base import DATE_ISO, DATE_TIME_ISO                 # type: ignore


__version__ = '0.1.0'


def parse_date(literal: str, *additional_formats: str, replace: Optional[Dict[str, Any]] = None,
               ret_date: Optional[bool] = False,
               dt_seps: Tuple[str, ...] = ('T', ' '), ti_sep: str = ':', ms_sep: str = '.', tz_sep: str = '+',
               ) -> Optional[Union[datetime.date, datetime.datetime]]:
    """ parse a date literal string, returning the represented date/datetime or None if date literal is invalid.

    This function checks/corrects the passed date/time literals for to support a wider range of ISO and additional
    date/time formats as Pythons :func:`~datetime.datetime.strptime`.

    .. hint::
        Pythons :meth:`~datetime.datetime.strptime` for to parse date and time strings into :class:`datetime.date`
        or :class:`datetime.datetime` objects is very strict and does not respect the formatting alternatives of
        ISO8601 (see https://bugs.python.org/issue15873 and https://github.com/boxed/iso8601).

    Additionally a :class:`datetime.date` object can be created/returned automatically if no time info
    is specified in the date string/literal (see :paramref:`~parse_date.ret_date` parameter).

    :param literal:             date literal string in the format of :data:`DATE_ISO`, :data:`DATE_TIME_ISO` or in
                                one of the additional formats passed into the
                                :paramref:`~parse_date.additional_formats` arguments.

    :param additional_formats:  additional date literal format string masks (supported mask characters are documented
                                at the `format` argument of the python method :meth:`~datetime.datetime.strptime`).

    :param replace:             dict of replace keyword arguments for :meth:`datetime.datetime.replace` call.
                                Pass e.g. dict(microsecond=0, tzinfo=None) for to set the microseconds of the
                                resulting date to zero and for to remove the timezone info.

    :param ret_date:            request return value type: True=datetime.date, False=datetime.datetime (the default)
                                or None=determine type from literal (short date if dt_seps are not in literal).

    :param dt_seps:             tuple of supported separator characters between the date and time literal parts.

    :param ti_sep:              separator character of the time parts (hours/minutes/seconds) in literal.

    :param ms_sep:              microseconds separator character.

    :param tz_sep:              time-zone separator character.

    :return:                    represented date/datetime or None if date literal is invalid.
    """
    lp_tz_sep = literal.rfind(tz_sep)
    lp_ms_sep = literal.rfind(ms_sep)
    lp_dt_sep = max((literal.find(_) for _ in dt_seps))
    if ret_date and lp_dt_sep != -1:
        literal = literal[:lp_dt_sep]       # cut time part if exists caller requested return of short date
        l_dt_sep = None
        l_time_sep_cnt = 0
    else:
        l_dt_sep = literal[lp_dt_sep] if lp_dt_sep != -1 else None
        l_time_sep_cnt = literal.count(ti_sep)
        if not 0 <= l_time_sep_cnt <= 2:
            return None

    if l_dt_sep:
        additional_formats += (DATE_TIME_ISO,)
    additional_formats += (DATE_ISO,)

    for mask in additional_formats:
        mp_dt_sep = max((mask.find(_) for _ in dt_seps))
        m_time_sep_cnt = mask.count(ti_sep)
        if lp_tz_sep == -1 and mask[-3] == tz_sep:
            mask = mask[:-3]                    # no timezone specified in literal, then remove '+%z' from mask
        if lp_ms_sep == -1 and mask.rfind(ms_sep) != -1:
            mask = mask[:mask.rfind(ms_sep)]    # no microseconds specified in literal, then remove '.%f' from mask
        if 1 <= l_time_sep_cnt < m_time_sep_cnt:
            mask = mask[:mask.rfind(ti_sep)]    # no seconds specified in literal, then remove ':%S' from mask
        if mp_dt_sep != -1:
            if l_dt_sep:
                m_dt_sep = mask[mp_dt_sep]
                if l_dt_sep != m_dt_sep:        # if literal uses different date-time-sep
                    mask = mask.replace(m_dt_sep, l_dt_sep)     # .. then replace in mask
            else:
                mask = mask[:mp_dt_sep]         # if no date-time-sep in literal, then remove time part from mask

        try:
            ret_val: Optional[Union[datetime.date, datetime.datetime]] = datetime.datetime.strptime(literal, mask)
        except ValueError:
            ret_val = None

        if ret_val is not None:
            if replace:
                ret_val = ret_val.replace(**replace)
            if ret_date or ret_date is None and l_dt_sep is None:
                ret_val = ret_val.date()        # type: ignore
            return ret_val

    return None
