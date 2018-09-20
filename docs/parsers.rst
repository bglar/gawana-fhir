Parsers (JSON and XML)
======================

This module should involve the conversion of the bases FHIR specification files
from JSON/XML to Python type classes.

Python FHIR Parser (fhir-parser) by smart-on-fhir can be a helpful parser for this.
The parser downloads FHIR specification files, parses the profiles and represents
them as Python Class.

Another parser should be created that converts these Python Classes to ORM compliant
methods. This parser should be a hook to the fhir-parser.

