#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  FHIR 1.0.2.7202 (http://hl7.org/fhir/StructureDefinition/Distance)
#  Date: 2016-03-18.


from .quantity import Quantity


class Distance(Quantity):
    """ A measure of distance.

    There SHALL be a code if there is a value and it SHALL be an expression of
    length.  If system is present, it SHALL be UCUM.
    """


DistanceField = Distance()
