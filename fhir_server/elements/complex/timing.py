#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  FHIR 1.0.2.7202 (http://hl7.org/fhir/StructureDefinition/Timing)
#  Date: 2016-03-18.


from sqlalchemy import Column, ForeignKey
from fhir_server.elements import primitives
from fhir_server.elements.base.complex_element import ComplexElement, Field
from fhir_server.elements.complex.codeableconcept import CodeableConceptField
from fhir_server.elements.complex.period import PeriodField
from fhir_server.elements.complex.coding import CodingField
from fhir_server.elements.complex.duration import DurationField
from fhir_server.elements.complex.range import RangeField


class TimingRepeat(ComplexElement):
    """ When the event is to occur.

    A set of rules that describe when the event should occur.
    """

    def element_properties(self):
        elm = super().element_properties()
        elm.extend([
            Field('count', {'mini': 0, 'maxi': 1},
                  primitives.IntegerField, None),
            # Number of times to repeat.

            Field('duration', {'mini': 0, 'maxi': 1},
                  primitives.DecimalField, None),
            # How long when it happens.

            Field('durationMax', {'mini': 0, 'maxi': 1},
                  primitives.DecimalField, None),
            # How long when it happens (Max).

            Field('durationUnits', {'mini': 0, 'maxi': 1},
                  primitives.CodeField, None),
            # s | min | h | d | wk | mo | a - unit of time (UCUM).

            Field('frequency', {'mini': 0, 'maxi': 1},
                  primitives.IntegerField, None),
            # Event occurs frequency times per period.

            Field('frequencyMax', {'mini': 0, 'maxi': 1},
                  primitives.IntegerField, None),
            # Event occurs up to frequencyMax times per period.

            Field('period', {'mini': 0, 'maxi': 1},
                  primitives.DecimalField, None),
            # Event occurs frequency times per period.

            Field('periodMax', {'mini': 0, 'maxi': 1},
                  primitives.DecimalField, None),
            # Upper limit of period (3-4 hours).

            Field('periodUnits', {'mini': 0, 'maxi': 1},
                  primitives.CodeField, None),
            # s | min | h | d | wk | mo | a - unit of time (UCUM).

            Field('when', {'mini': 0, 'maxi': 1}, primitives.CodeField, None),
            # Regular life events the event is tied to.

            Field('boundsPeriod', {'mini': 0, 'maxi': 1}, PeriodField(), None),
            # Length/Range of lengths, or (Start and/or end) limits.

            Field('boundsQuantity', {'mini': 0, 'maxi': 1},
                  DurationField(), None),
            # Length/Range of lengths, or (Start and/or end) limits.

            Field('boundsRange', {'mini': 0, 'maxi': 1}, RangeField(), None)
            # Length/Range of lengths, or (Start and/or end) limits.
        ])
        return elm


TimingRepeatField = TimingRepeat()


class Timing(ComplexElement):
    """ A timing schedule that specifies an event that may occur multiple times.

    Specifies an event that may occur multiple times. Timing schedules are used
    to record when things are expected or requested to occur. The most common
    usage is in dosage instructions for medications. They are also used when
    planning care of various kinds.
    """

    def element_properties(self):
        elm = super().element_properties()
        elm.extend([
            Field('event', {'mini': 0, 'maxi': -1},
                  primitives.DateTimeField, None),
            # When the event occurs.

            Field('code', {'mini': 0, 'maxi': 1},
                  CodeableConceptField(), None),
            # QD | QOD | Q4H | Q6H | BID | TID | QID | AM | PM +.

            Field('repeat', {'mini': 0, 'maxi': 1}, TimingRepeatField(), None)
            # When the event is to occur
        ])
        return elm


TimingField = Timing()
