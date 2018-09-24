import re
import base64
import hashlib
import requests
import warnings
import mimetypes

from language_tags import tags
import jwt
from pycountry import countries

from fhir_server.configs.constants import SANCTIONED_CODE_URLS
from .xhtml_validator import xhtml_validator
from .reference_validator import validate_reference
from fhir_server.configs import (
    ADDRESS_USE_URL, ADDRESS_TYPE_URL,
    QUANTITY_COMPARATOR_URL, HUMANNAME_USE_URL,
    UNITS_OF_TIME_URL, EVENT_TIMING_URL, TIMING_ABBREVIATION_URL,
    CONTACT_POINT_SYSTEM_URL, CONTACT_POINT_USE_URL,
    SIGNATURE_TYPE_URL, IDENTIFIER_TYPE_URL, IDENTIFIER_USE_URL,
    UCUM_SYSTEM_URI, AGE_UNITS_URL, NARRATIVE_STATUS_URL,
    SIGNATURE_MIME_TYPES, CONTACT_ENTITY_TYPE_URL,

    VALID_ATTACHMENT_EXTENSIONS
)


class CompositeValidator(object):
    def __init__(self, name, columns, values):
        self.columns = columns
        self.values = values
        self.name = name

        self.validator_dispatch()

    def validator_dispatch(self):
        """Dispatch method"""
        method_name = 'validate_' + self.name

        # Get the method from 'self'. Default to a lambda.
        method = getattr(self, method_name, lambda: "nothing")
        return method()

    def validate_valuesets(self, url, response):
        resp = requests.get(url)
        if not (resp.json()['count'] == 1):
            raise TypeError(
                'The %s must be defined in %s' % (
                    response, url.split('?')[0]))

    def validate_fhir_range(self):
        if (self.values.__getattribute__('high')) and (
                self.values.__getattribute__('low')):

            if self.values.low.value > self.values.high.value:
                raise ValueError('low_val cannot be > than high_val')

            if not (self.values.low.unit == self.values.high.unit):
                raise ValueError('units for low and high should match')

            if not (self.values.low.code == self.values.high.code):
                raise ValueError('codes for low and high should match')

            if not (self.values.low.system == self.values.high.system):
                raise ValueError('systems for low and high should match')

        return self.values

    def validate_fhir_attachment(self):
        errors = []
        if self.values.data:
            if not self.values.contentType:
                errors.append(
                    'content_type must be populated if data is provided')

            mimetypes.init()
            mime = mimetypes.guess_extension(str(self.values.contentType))

            if not (mime in VALID_ATTACHMENT_EXTENSIONS):
                errors.append(
                    'The uploaded file type not supported')

        if self.values.language:
            if not tags.check(self.values.language):
                errors.append(
                    'the language code must be valid')

        if self.values.hash and self.values.data:
            byte_data = self.values.data
            d_hash = base64.b64decode(byte_data)
            valid_hash = hashlib.sha1(d_hash).digest()
            if not self.values.hash == valid_hash:
                errors.append(
                    'the hash must be a base64 sha-1 hash of the data')

        if len(errors) > 0:
            raise ValueError(errors)

        return self.values

    def validate_fhir_simplequantity(self):
        if self.values.code:
            if not self.values.system:
                raise ValueError(
                    'system must be specified if code is provided')

        if self.values.system:
            if not self.values.system == UCUM_SYSTEM_URI:
                msg = (
                    'Your are using a different unit of measure system. %s is'
                    ' recommended' % UCUM_SYSTEM_URI)
                warnings.warn(msg, UserWarning)

        return self.values

    def validate_fhir_quantity(self):
        self.validate_fhir_simplequantity()
        if self.values.comparator:
            url = QUANTITY_COMPARATOR_URL + '?code=' + self.values.comparator
            self.validate_valuesets(url, 'quantity comparator')

        return self.values

    def validate_fhir_age(self):
        self.validate_fhir_quantity()
        if self.values.code:
            url = AGE_UNITS_URL + '?code=' + self.values.code
            self.validate_valuesets(url, 'age units')

        return self.values

    def validate_fhir_count(self):
        return self.validate_fhir_quantity()

    def validate_fhir_money(self):
        self.validate_fhir_quantity()
        if self.values.value:
            if not self.values.code:
                raise ValueError(
                    'code must be specified if value is provided')
        return self.values

    def validate_fhir_distance(self):
        return self.validate_fhir_quantity()

    def validate_fhir_duration(self):
        self.validate_fhir_quantity()
        if self.values.code:
            url = UNITS_OF_TIME_URL + '?code=' + self.values.code
            self.validate_valuesets(url, 'duration units')

        return self.values

    def validate_fhir_period(self):
        return self.values

    def validate_fhir_humanname(self):
        valid_text = []

        def check_for_white_spaces(name, value):
            if re.search(r"(\s)+", value):
                raise TypeError('%s in name must not have a whitespace' % name)

            valid_text.append(value)

        if self.values.prefix:
            for val in self.values.prefix:
                check_for_white_spaces('prefix', val)

        if self.values.family:
            for val in self.values.family:
                check_for_white_spaces('family', val)

        if self.values.given:
            for val in self.values.given:
                check_for_white_spaces('given', val)

        if self.values.suffix:
            for val in self.values.suffix:
                check_for_white_spaces('suffix', val)

        if self.values.text:
            words = self.values.text.split()
            for word in words:
                if word not in valid_text:
                    raise TypeError(
                        'text must be composed of the other name attributes')

        if self.values.use:
            url = HUMANNAME_USE_URL + '?code=' + self.values.use
            self.validate_valuesets(url, 'humanname use')

        return self.values

    def validate_fhir_timing(self):
        errors = []
        if self.values.repeat:
            if self.values.repeat.duration and not (
                    self.values.repeat.durationUnits):
                errors.append(
                    'durationUnits must be present for the duration provided')

            if self.values.repeat.periodMax:
                if not self.values.repeat.period:
                    errors.append(
                        'If there is a periodMax, there must be a period')
                if self.values.repeat.periodMax < 0:
                    errors.append(
                        'periodMax SHALL be a non-negative value')

            if self.values.repeat.period:
                if not self.values.repeat.periodUnits:
                    errors.append(
                        'periodUnits must be present for the period provided')
                if self.values.repeat.period < 0:
                    errors.append('period SHALL be a non-negative value')

            if self.values.repeat.frequency and self.values.repeat.when:
                errors.append('Either frequency or when can exist, not both')

            if self.values.repeat.durationMax:
                if not self.values.repeat.duration:
                    errors.append(
                        'If there is a durationMax, there must be a duration')
                if self.values.repeat.durationMax < 0:
                    errors.append('durationMax SHALL be a non-negative value')

            if self.values.repeat.duration and (
                    self.values.repeat.duration < 0):
                errors.append('duration SHALL be a non-negative value')

            if self.values.repeat.durationUnits:
                url = UNITS_OF_TIME_URL + '?code=' + (
                    self.values.repeat.durationUnits)
                self.validate_valuesets(url, 'timing durationUnits')

            if self.values.repeat.periodUnits:
                url = UNITS_OF_TIME_URL + '?code=' + (
                    self.values.repeat.periodUnits)
                self.validate_valuesets(url, 'timing periodUnits')

            if self.values.repeat.when:
                url = EVENT_TIMING_URL + '?code=' + self.values.repeat.when
                self.validate_valuesets(url, 'timing when')

        if self.values.code and self.values.code.coding:
            url = TIMING_ABBREVIATION_URL + '?code='
            for i, val in enumerate(self.values.code.coding):
                get_url = url + self.values.code.coding[i].code
                self.validate_valuesets(get_url, 'timing code')

        if len(errors) > 0:
            raise TypeError(errors)

        return self.values

    def validate_fhir_sampleddata(self):
        if re.search(r"(\s\s)+", self.values.data):
            raise TypeError(
                'data in sampleddata must not have more than 1 whitespace')

        regex = '^([0-9.][E|U|L| ]*)*$'
        if not re.fullmatch(regex, self.values.data):
            raise TypeError(
                'Data should be composed of decimal values with spaces,'
                ' or "E" | "U" | "L')

        return self.values

    def validate_fhir_contactpoint(self):
        if self.values.system:
            url = CONTACT_POINT_SYSTEM_URL + '?code=' + self.values.system
            self.validate_valuesets(url, 'contactpoint system')

        if self.values.use:
            url = CONTACT_POINT_USE_URL + '?code=' + self.values.use
            self.validate_valuesets(url, 'contactpoint use')

        return self.values

    def validate_fhir_address(self):
        if self.values.type:
            url = ADDRESS_TYPE_URL + '?code=' + self.values.type
            self.validate_valuesets(url, 'address type')

        if self.values.use:
            url = ADDRESS_USE_URL + '?code=' + self.values.use
            self.validate_valuesets(url, 'address use')

        if self.values.country:
            country_code = self.values.country

            # Check that the code is a recommended ISO 3166 3letter code
            try:
                countries.get(alpha3=country_code)
            except Exception:
                msg = ('This country code is not recommended. '
                       'Please use an ISO 3166 3letter country code')
                warnings.warn(msg, UserWarning)

        return self.values

    def validate_fhir_signature(self):
        url = SIGNATURE_TYPE_URL + '?code='

        for val in self.values.type:
            get_url = url + val.code
            self.validate_valuesets(get_url, 'signature code')

        if not (self.values.contentType in SIGNATURE_MIME_TYPES):
            raise ValueError(
                'The signature content type should be one of'
                ' %s' % SIGNATURE_MIME_TYPES)

        try:
            jwt.decode(self.values.blob, verify=False)
        except Exception:
            raise jwt.exceptions.DecodeError(
                'The blob provided is not a valid jwt encoded signature')

        return self.values

    def validate_fhir_identifier(self):
        if self.values.type and self.values.type.coding:
            url = IDENTIFIER_TYPE_URL + '?code='
            for i, val in enumerate(self.values.type.coding):
                get_url = url + self.values.type.coding[i].code
                self.validate_valuesets(get_url, 'identifier type')

        if self.values.use:
            url = IDENTIFIER_USE_URL + '?code=' + self.values.use
            self.validate_valuesets(url, 'identifier use')

        return self.values

    def validate_fhir_narrative(self):
        url = NARRATIVE_STATUS_URL + '?code=' + self.values.status
        self.validate_valuesets(url, 'narrative status')

        xhtml_validator.reset()
        xhtml_validator.feed(self.values.div)
        xhtml_validator.close()

        return self.values

    def validate_fhir_reference(self):
        if self.values.reference:
            validate_reference(self.values.reference)

    def validate_fhir_organizationcontact(self):
        if self.values.purpose:
            codings = self.values.purpose.coding
            for coding in codings:
                url = CONTACT_ENTITY_TYPE_URL + '?code=' + coding.code
                self.validate_valuesets(url, 'organization contact type')

    def validate_fhir_coding(self):
        if self.values.system:
            if self.values.system not in SANCTIONED_CODE_URLS:
                raise ValueError(
                    'The provided system uri is not a sanctioned uri. '
                    'Use a sanctioned uri from '
                    '[http://hl7.org/fhir/terminologies-systems.html]')
