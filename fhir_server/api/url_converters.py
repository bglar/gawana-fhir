from werkzeug.routing import BaseConverter
from werkzeug.urls import url_quote


class FhirOperationsConverter(BaseConverter):
    def __init__(self, map):
        BaseConverter.__init__(self, map)
        self.regex = "\$([^/])+"

    def to_python(self, value):
        return value.replace("$", "")

    def to_url(self, value):
        return url_quote(value, charset=self.map.charset)
