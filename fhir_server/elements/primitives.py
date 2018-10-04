import sys
from decimal import Decimal
import re
import pytz
from datetime import time, datetime
from time import gmtime, strftime
import base64
import bleach
from sqlalchemy import types


def regex_checker(some_str, regex):
    pattern = re.compile(regex)
    if pattern.fullmatch(str(some_str)):
        return True
    else:
        return False


def validate_local_times(value):
    date_obj = value
    seperator = ['+', '-', 'Z']

    if isinstance(value, str):
        for sep in seperator:
            value = (value.split(sep))[0]

        try:
            date_obj = datetime.strptime(value, '%Y-%m-%dT%H:%M:%S')
        except Exception:
            pass

        try:
            date_obj = datetime.strptime(value, '%Y-%m-%dT%H:%M')
        except Exception:
            pass

    if isinstance(date_obj, datetime):
        strftime("%Z", gmtime())
        for zone in pytz.all_timezones:
            tz = pytz.timezone(zone)
            try:
                tz.localize(date_obj, is_dst=None)
            except Exception:
                raise pytz.exceptions.AmbiguousTimeError(
                    'Ambiguous Time Error for %s' % value)


class BooleanField(types.TypeDecorator):
    """
    true or false values (0 and 1 are not valid values) and
    should cater for optional boolean fields """
    impl = types.Boolean

    def process_bind_param(self, value, dialect):
        # Override to exclude 1s and 0s
        if str(value) in ['1', '0']:
            raise TypeError(
                '{} is an invalid value for the fhir boolean field'.format(
                    value))
        return value

    def process_result_value(self, value, dialect):
        # Do nothing here
        return value


class IntegerField(types.INTEGER):
    """A signed 32-bit integer (for larger values, use decimal)"""


class UnsignedIntField(types.TypeDecorator):
    """Any non-negative integer (e.g. >= 0)
    regex: [0-9]+
    """

    impl = types.Integer

    def process_bind_param(self, value, dialect):
        if value is not None:
            if value < 0:
                raise TypeError(
                    'Value %s must be an int greater than or equal 0' % value)

        return value

    def process_result_value(self, value, dialect):
        # Do nothing here
        return value


class PositiveIntField(UnsignedIntField):
    """Any positive integer (e.g. > 0)
    regex: [1-9][0-9]*
    """

    impl = types.Integer

    def process_bind_param(self, value, dialect):
        if value is not None:
            if value <= 0:
                raise TypeError(
                    'Value %s must be a positive integer greater than 0' % (
                        value))
        return value


class DecimalField(types.TypeDecorator):
    """
    Rational numbers that have a decimal representation.
    Note: decimals may not use exponents, and leading 0 digits are not allowed
    """
    impl = types.Numeric

    def process_bind_param(self, value, dialect):
        decimal_val = value

        if value:
            try:
                decimal_val = Decimal(str(value))
            except Exception:
                raise ValueError('Invalid literal for Decimal: %s' % value)

        return decimal_val

    def process_result_value(self, value, dialect):
        # Do nothing here
        return value


class StringField(types.TypeDecorator):
    """
    A sequence of Unicode characters. Note that strings SHALL NOT exceed 1MB
    in size """

    impl = types.UnicodeText

    def process_bind_param(self, value, dialect):
        size = sys.getsizeof(value)  # Returns size of the string in bytes

        if isinstance(value, bytes):
            raise TypeError('This field expects unicode string'
                            ' but an encoded string was given')

        if size > 1048576:
            raise TypeError('String value must not exceed 1MB')

        return value

    def process_result_value(self, value, dialect):
        # Do nothing here
        return value


class InstantField(types.TypeDecorator):
    """ An instant in time - known at least to the second and always
    includes a time zone.

    Note: This is intended for precisely observed times (typically
    system logs etc.), and not human-reported times - for them, use
    date and dateTime. instant is a more constrained dateTime. This
    type is for system times, not human times (see date and
    dateTime below).
    """

    impl = types.DateTime(timezone=True)

    def process_bind_param(self, value, dialect):
        regex = ('-?[0-9]{4}(-(0[1-9]|1[0-2])(-(0[0-9]|[1-2][0-9]|3[0-1])'
                 'T([01][0-9]|2[0-3]):[0-5][0-9](:[0-5][0-9])?(\.[0-9]+)?'
                 '(Z|(\+|-))((0[0-9]|1[0-3])[0-5][0-9]|1400)?)?)?')

        if value is not None:
            if isinstance(value, datetime):
                value = datetime.strftime(value, '%Y-%m-%dT%H:%M:%S%z')

            if not (regex_checker(value, regex)):
                raise TypeError('The Instant %s is invalid' % value)

        return value

    def process_result_value(self, value, dialect):
        # Do nothing here
        return value


class DateField(types.TypeDecorator):
    """
    A date, or partial date (e.g. just year or year + month) as used
    in human communication.

    There is no time zone. Dates SHALL be valid dates.
    date is a union of the w3c schema types date, gYearMonth, and gYear
    """
    impl = types.Date

    def process_bind_param(self, value, dialect):
        regex = '-?[0-9]{4}(-(0[1-9]|1[0-2])(-(0[0-9]|[1-2][0-9]|3[0-1]))?)?'

        if value is not None:
            if not (regex_checker(value, regex)):
                raise TypeError(
                    'The Date %s is invalid' % value)

        return value

    def process_result_value(self, value, dialect):
        # Do nothing here
        return value


class DateTimeField(types.TypeDecorator):
    """ A date, date-time or partial date (e.g. just year or year + month)
    as used in human communication.

    If hours and minutes are specified, a time zone SHALL be populated.
    Seconds must be provided due to schema type constraints but may be
    zero-filled and may be ignored. Dates SHALL be valid dates.
    The time "24:00" is not allowed
    """
    impl = types.DateTime(timezone=True)

    def process_bind_param(self, value, dialect):
        regex = ('-?[0-9]{4}(-(0[1-9]|1[0-2])(-(0[0-9]|[1-2][0-9]|3[0-1])'
                 '(T([01][0-9]|2[0-3]):[0-5][0-9](:[0-5][0-9])?(\.[0-9]+)?'
                 '(Z|(\+|-)((0[0-9]|1[0-3]):[0-5][0-9]|14:00)))?)?)?')

        if value is not None:
            if not (regex_checker(value, regex)):
                raise TypeError('The DateTime %s is invalid' % value)

            validate_local_times(value)

        return value

    def process_result_value(self, value, dialect):
        # Do nothing here
        return value


class TimeField(types.TypeDecorator):
    """ A time during the day, with no date specified (can be converted
    to a Duration since midnight). Seconds must be provided due to schema
    type constraints but may be zero-filled and may be ignored. The time
    "24:00" is not allowed, and neither is a time zone
    """
    impl = types.Time

    def process_bind_param(self, value, dialect):
        regex = '([01][0-9]|2[0-3]):[0-5][0-9]:[0-5][0-9](\.[0-9]+)?'
        res_value = value

        if value is not None:
            try:
                if isinstance(value, str):
                    time_obj = time(*map(int, value.split(':')))
                    res_value = time_obj.strftime("%H:%M:%S")
                elif isinstance(value, time):
                    res_value = value.strftime("%H:%M:%S")

            except Exception:
                raise ValueError("Time field expects valid str or time object "
                                 "but %s was given" % (type(value)))

            else:
                if not (regex_checker(res_value, regex)):
                    raise TypeError('The Time %s is invalid' % value)

        return res_value

    def process_result_value(self, value, dialect):
        # Do nothing here
        return value


# class URIField(types.TypeDecorator):
class URIField(types.UserDefinedType):
    """
    A Uniform Resource Identifier Reference (RFC 3986 ).
    Note: URIs are case sensitive. """
    impl = types.UnicodeText

    def get_col_spec(self, **kw):
        return 'URI'

    def bind_processor(self, dialect):
        def process(value):
            return value

        return process

    def result_processor(self, dialect, coltype):
        def process(value):
            return value

        return process


class OIDField(URIField):
    """
    An OID represented as a URI (RFC 3001): urn:oid:1.2.3.4.5
    """

    def bind_processor(self, dialect):
        def process(value):
            regex = 'urn:oid:[0-2](\.[1-9]\d*)+'

            if value is not None:
                if not (regex_checker(value, regex)):
                    raise TypeError('This OID is invalid')
            return value

        return process


class IdField(types.TypeDecorator):
    """
    Any combination of upper or lower case ASCII letters
    ('A'..'Z', and 'a'..'z', numerals ('0'..'9'), '-' and '.', with a length
    limit of 64 characters. (This might be an integer, an un-prefixed OID,
    UUID or any other identifier pattern that meets these constraints.)
    """

    impl = types.UnicodeText

    def process_bind_param(self, value, dialect):
        regex = '[A-Za-z0-9\-\.]{1,64}'

        if value is not None:
            if len(value) > 64:
                raise ValueError('Id field cannot be more than 64 characters')

            if len(value) < 1:
                raise ValueError('Id must have at least 1 character')

            if not (regex_checker(value, regex)):
                raise TypeError('Id: {} is not a valid id'.format(value))

        return value

    def process_result_value(self, value, dialect):
        # Do nothing here
        return value


class CodeField(StringField):
    """
    Indicates that the value is taken from a set of controlled strings defined
    elsewhere (see Using codes for further discussion). Technically, a code is
    restricted to a string which has at least one character and no leading or
    trailing whitespace, and where there is no whitespace other than single
    spaces in the contents
    """

    def process_bind_param(self, value, dialect):
        size = sys.getsizeof(value)  # Returns size of the string in bytes
        regex = '[^\s]+([\s]+[^\s]+)*'

        if value is not None:
            if size > 1048576:
                raise TypeError('Code value must not exceed 1MB')

            if not (regex_checker(value, regex)):
                raise TypeError(f'This Code: {value} is invalid')

            if re.search(r"(\s\s)+", value):
                raise TypeError('Code must not have a whitespace more '
                                'than a single character')

        return value


class Base64Field(types.TypeDecorator):  # TODO test for all edge cases
    """
    A stream of bytes, base64 encoded (RFC 4648)
    """
    impl = types.UnicodeText

    def process_bind_param(self, value, dialect):
        if value is not None and not isinstance(value, bytes):
            raw_byte = value.encode()
            print(raw_byte)
            value = base64.b64encode(raw_byte)
            size = sys.getsizeof(value)  # Returns size in bytes
            if size > 262144000:  # pragma: no cover
                raise TypeError('Base64 value must not exceed 250MB')

        return value

    def process_result_value(self, value, dialect):
        db_val = value
        if not value:
            return value

        if type(value) is str:
            db_val = base64.b64encode(bytes(value, 'utf-8'))

        decoded = base64.b64decode(db_val)
        string = decoded.decode('utf-8')
        return string


class MarkdownField(types.TypeDecorator):
    """
    A string that may contain markdown syntax for optional
    processing by a markdown presentation engine """

    impl = types.UnicodeText

    def process_bind_param(self, value, dialect):
        allowed_tags = ['a', 'abbr', 'acronym', 'b', 'blockquote', 'code',
                        'em', 'i', 'li', 'ol', 'pre', 'strong', 'ul',
                        'h1', 'h2', 'h3', 'p']

        result = bleach.clean(
            value, tags=allowed_tags, strip=True
        )

        return result

    def process_result_value(self, value, dialect):
        # Do nothing
        return value
