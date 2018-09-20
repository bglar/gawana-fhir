#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  FHIR 1.0.2.7202 (http://hl7.org/fhir/StructureDefinition/Age)
#  Date: 2016-03-18.


from .quantity import Quantity


class Age(Quantity):
    """ A duration (length of time) with a UCUM code.

    There SHALL be a code if there is a value and it SHALL be an
    expression of time.  If system is present, it SHALL be UCUM.
    If value is present, it SHALL be positive.
    """


AgeField = Age()
