'''
Schema definitions for FITS Headers.

See section 4 of the FITS Standard:
https://fits.gsfc.nasa.gov/standard40/fits_standard40aa-le.pdf
'''
from datetime import date, datetime
from .exceptions import (
    RequiredMissing, WrongType, WrongPosition, AdditionalHeaderCard,
    WrongValue,
)
import re
from collections.abc import Iterable
from astropy.io import fits
import logging

from .utils import log_or_raise


log = logging.getLogger(__name__)


HEADER_ALLOWED_TYPES = (str, bool, int, float, complex, date, datetime)
TABLE_KEYWORDS = {'TTYPE', 'TUNIT', 'TFORM', 'TSCAL', 'TZERO', 'TDISP', 'TDIM'}
IGNORE = TABLE_KEYWORDS


class HeaderCard:
    '''
    Schema for the entry of a FITS header

    Attributes
    ----------
    keyword: str
        override the keyword given as the class member name,
        useful to define keywords containing hyphens or starting with numbers
    required: bool
        If this card is required
    allowed_values: instance of any in ``HEADER_ALLOWED_TYPES`` or iterable of that
        If specified, card must have on of these values
    position: int or None
        if not None, the card must be at this position in the header,
        starting with the first card at 0
    type: one or a tuple of the types in ``HEADER_ALLOWED_TYPES``
    empty: True, False or None
        If True, value must be empty, if False must not be empty,
        if None, no check if a value is present is performed
    case_insensitive: True
        match str values case insensitively
    '''
    def __init__(
        self, keyword=None, *, required=True,
        allowed_values=None, position=None, type_=None,
        empty=None, case_insensitive=True,
    ):
        self.keyword = None
        if keyword is not None:
            self.__set_name__(None, keyword)

        self.required = required
        self.position = position
        self.empty = empty
        self.case_insensitive = case_insensitive

        vals = allowed_values
        if vals is not None:
            if not isinstance(vals, Iterable) or isinstance(vals, str):
                vals = {vals}
            else:
                vals = set(vals)

            if self.case_insensitive:
                vals = set(v.upper() if isinstance(v, str) else v for v in vals)

            if not all(isinstance(v, HEADER_ALLOWED_TYPES) for v in vals):
                raise ValueError(f'Values must be instances of {HEADER_ALLOWED_TYPES}')

        self.type = type_
        if type_ is not None:
            if isinstance(type_, Iterable):
                self.type = tuple(set(type_))

            # check that value and type match if both supplied
            if vals is not None:
                if any(not isinstance(v, type_) for v in vals):
                    raise TypeError(f'`values` must be of type `type_`({type_}) or None')
        else:
            # if only value is supplied, deduce type from value
            if vals is not None:
                self.type = tuple(set(type(v) for v in vals))

        self.allowed_values = vals

    def __set_name__(self, owner, name):
        if self.keyword is None:
            if len(name) > 8:
                raise ValueError('FITS header keywords must be 8 characters or shorter')

            if not re.match(r'^[A-Z0-9\-_]{1,8}$', name):
                raise ValueError(
                    'FITS header keywords must only contain'
                    ' ascii uppercase, digit, _ or -'
                )
            self.keyword = name

    def validate(self, card, pos, onerror='raise'):
        '''Validate an astropy.io.fits.card.Card'''
        valid = True
        k = self.keyword

        if self.position is not None and self.position != pos:
            valid = False
            msg = (
                f'Expected card {k} at position {self.position}'
                f' but found at {pos}'
            )
            log_or_raise(msg, WrongPosition, log, onerror=onerror)

        if self.type is not None and not isinstance(card.value, self.type):
            valid = False
            msg = (
                f'Header keyword {k} has wrong type {type(card.value)}'
                f', expected one of {self.type}'
            )
            log_or_raise(msg, WrongType, log, onerror=onerror)

        if self.allowed_values is not None:
            if self.case_insensitive and isinstance(card.value, str):
                val = card.value.upper()
            else:
                val = card.value
            if val not in self.allowed_values:
                log_or_raise(
                    f'Possible values for {k!r} are {self.allowed_values}'
                    f', found {card.value!r}',
                    WrongValue,
                    log,
                    onerror=onerror
                )

        has_value = not (card.value is None or isinstance(card.value, fits.Undefined))
        if self.empty is True and has_value:
            log_or_raise(
                f'Card {k} is required to be empty but has value {card.value}',
                WrongValue, log, onerror,
            )

        if self.empty is False and not has_value:
            log_or_raise(f'Card {k} exists but has no value', WrongValue, log, onerror)

        return valid


class HeaderSchemaMeta(type):
    def __new__(cls, name, bases, dct):
        dct['__cards__'] = {}
        dct['__slots__'] = tuple()

        for base in reversed(bases):
            if issubclass(base, HeaderSchema):
                dct['__cards__'].update(base.__cards__)

        for k, v in dct.items():
            if isinstance(v, HeaderCard):
                k = v.keyword or k  # use user override for keyword if there
                dct['__cards__'][k] = v

        new_cls = super().__new__(cls, name, bases, dct)
        return new_cls


class HeaderSchema(metaclass=HeaderSchemaMeta):
    '''
    Schema definition for the header of a FITS HDU

    To be added as `class __header_schema__(HeaderSchema)` to HDU schema classes.

    Add `Card` class members to define the schema.


    Example
    -------
    >>> from fits_schema.binary_table import BinaryTable, Int32
    >>> from fits_schema.header import HeaderSchema, HeaderCard
    >>>
    >>> class Events(BinaryTable):
    ...    EVENT_ID = Int32()
    ...
    ...    class __header_schema__(HeaderSchema):
    ...        HDUCLASS = HeaderCard(required=True, allowed_values="Events")
    '''
    # define some common header keywords
    EXTEND   = HeaderCard(type_=bool, required=False)
    ORIGIN   = HeaderCard(type_=str, required=False)
    TELESCOP = HeaderCard(type_=str, required=False)
    INSTRUME = HeaderCard(type_=str, required=False)
    OBSERVER = HeaderCard(type_=str, required=False)
    OBJECT   = HeaderCard(type_=str, required=False)
    AUTHOR   = HeaderCard(type_=str, required=False)
    REFERENC = HeaderCard(type_=str, required=False)
    COMMENT  = HeaderCard(type_=str, required=False)
    HISTORY  = HeaderCard(type_=str, required=False)
    CREATOR  = HeaderCard(type_=str, required=False)
    PROGRAM  = HeaderCard(type_=str, required=False)

    # see table 22 of https://fits.gsfc.nasa.gov/standard40/fits_standard40aa-le.pdf
    DATE     = HeaderCard(type_=str, required=False)
    DATE_OBS = HeaderCard(keyword='DATE-OBS', type_=str, required=False)
    DATE_BEG = HeaderCard(keyword='DATE-BEG', type_=str, required=False)
    DATE_AVG = HeaderCard(keyword='DATE-AVG', type_=str, required=False)
    DATE_END = HeaderCard(keyword='DATE-END', type_=str, required=False)

    MJD_OBS  = HeaderCard(keyword='MJD-OBS', type_=float, required=False)
    MJD_BEG  = HeaderCard(keyword='MJD-BEG', type_=float, required=False)
    MJD_AVG  = HeaderCard(keyword='MJD-AVG', type_=float, required=False)
    MJD_END  = HeaderCard(keyword='MJD-END', type_=float, required=False)

    # time definition
    MJDREF   = HeaderCard(type_=float, required=False)
    MJDREFI  = HeaderCard(type_=int, required=False)
    MJDREFF  = HeaderCard(type_=float, required=False)
    JDREF    = HeaderCard(type_=float, required=False)
    JDREFI   = HeaderCard(type_=int, required=False)
    JDREFF   = HeaderCard(type_=float, required=False)
    DATEREF  = HeaderCard(type_=float, required=False)

    # start / end time relative to reference time
    TSTART   = HeaderCard(type_=float, required=False)
    TSTOP    = HeaderCard(type_=float, required=False)

    @classmethod
    def validate_header(cls, header: fits.Header, onerror='raise'):

        required = {k for k, c in cls.__cards__.items() if c.required}
        missing = required - set(header.keys())

        # first let's test for any missing required keys
        if missing:
            log_or_raise(
                f"Header is missing the following required keywords: {missing}",
                RequiredMissing, log=log, onerror=onerror,
            )

        # no go through each of the header items and validate them with the schema
        for pos, card in enumerate(header.cards):
            kw = card.keyword
            if kw not in cls.__cards__:
                if kw.rstrip('0123456789') not in IGNORE:
                    log_or_raise(
                        f'Unexpected header card "{str(card).strip()}"',
                        AdditionalHeaderCard,
                        log=log,
                        onerror=onerror
                    )
                continue

            cls.__cards__[card.keyword].validate(card, pos, onerror)

    @classmethod
    def update(cls, other_schema):
        cls.__cards__.update(other_schema.__cards__)
