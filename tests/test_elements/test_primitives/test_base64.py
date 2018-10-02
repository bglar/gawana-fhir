import base64
import sys

import pytest
from fhir_server.elements.primitives import Base64Field


class TestBase64Field(object):
    raw_data = 'my raw string'
    large_data = 'datag212' * 100000000
    encoded = base64.b64encode(bytes(raw_data, 'utf-8'))

    def test_b64_encodes_data(self):
        result = Base64Field().process_bind_param(self.raw_data, 'postgres')
        assert result != self.raw_data
        assert result == self.encoded

    def test_b64_dencodes_data(self):
        result = Base64Field().process_result_value(self.encoded, 'postgres')
        assert result != self.encoded
        assert result == self.raw_data

    def test_b64_dencodes_raw_data(self):
        result = Base64Field().process_result_value(self.raw_data, 'postgres')
        assert result != self.encoded
        assert result == self.raw_data

    def test_b64_None(self):
        result = Base64Field().process_result_value(None, 'postgres')
        assert result is None

        bind = Base64Field().process_bind_param(None, 'postgres')
        assert bind is None

    # TODO Optimize this test and get rid of `pragma no cover` from::
    #   fhir_server/elements/primitives.py:385
    #
    # def test_data_not_more_than_250mb(self):
    #     size = sys.getsizeof(self.large_data)
    #     assert size > 262144000
    #
    #     with pytest.raises(TypeError) as excinfo:
    #         Base64Field().process_bind_param(self.large_data, 'postgres')
    #
    #     assert 'Base64 value must not exceed 250MB' in str(excinfo.value)
