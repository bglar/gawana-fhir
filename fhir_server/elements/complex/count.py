#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  FHIR 1.0.2.7202 (http://hl7.org/fhir/StructureDefinition/Count)
#  Date: 2016-03-18.


from .quantity import Quantity


class Count(Quantity):
    """ A count of a discrete element (no unit).

    There SHALL be a code with a value of "1" if there is a value and it SHALL
    be an expression of length.  If system is present, it SHALL be UCUM.  If
    present, the value SHALL a whole number.
    """

    def element_properties(self):
        """
        Extend quantity complex type removing the unit field.
        """
        elm = super().element_properties()
        elm = [e for e in elm if not(e.name == 'unit')]

        return elm


CountField = Count()
