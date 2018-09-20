import pytest

from sqlalchemy import Column
from sqlalchemy.exc import StatementError
from sqlalchemy_utils import register_composites

from fhir_server.elements import primitives
from fhir_server.elements.complex.timing import (
    TimingField, Timing as TimingDef)


class TestTiming(object):

    @pytest.fixture
    def TestTimingModel(self, Base):
        class TestTimingModel(Base):
            __tablename__ = 'test_timing'
            id = Column(primitives.IntegerField, primary_key=True)
            timing = Column(TimingField())
        return TestTimingModel

    def test_post_data(self, session, TestTimingModel):
        post = TestTimingModel(
            id=1,
            timing={
                'event': [
                    '2015-10-10T11:11:11+02:00',
                    '2015-10-10T11:12:11+02:00'
                ],
                'code': {
                    'text': 'text',
                    'coding': [{
                        'code': 'QOD',
                        'display': 'display',
                        'system': 'http://testing.test.com',
                        'userSelected': True,
                        'version': '2.3'
                    }]
                },
                'repeat': {
                    'count': 12,
                    'duration': 11.32,
                    'durationMax': 11.22,
                    'durationUnits': 'min',
                    'frequency': 3,
                    'frequencyMax': 5,
                    'period': 5.30,
                    'periodMax': 7.59,
                    'periodUnits': 'min',
                    'boundsPeriod': {
                        'start': '2015-10-10',
                        'end': '2015-11-11'
                    },
                    'boundsQuantity': {
                        'code': 'code',
                        'system': 'system',
                        'unit': 'kg',
                        'value': 2.400023,
                        'comparator': '<'
                    },
                    'boundsRange': {
                        'high': {
                            'code': 'code',
                            'system': 'system',
                            'unit': 'kg',
                            'value': 2.400023
                        },
                        'low': {
                            'code': 'code',
                            'system': 'system',
                            'unit': 'kg',
                            'value': 0.400023
                        }
                    }
                }
            }
        )

        session.execute("""
            CREATE TABLE test_timing (
                id INTEGER, timing fhir_timing);""")

        session.add(post)

        register_composites(session.connection())
        session.commit()
        get = session.query(TestTimingModel).first()
        assert get.id == 1
        assert get.timing.repeat.durationUnits == 'min'

    def test_post_if_missing_durationMax_and_periodMax(
            self, session, TestTimingModel):
        post = TestTimingModel(
            id=1,
            timing={
                'event': [
                    '2015-10-10T11:11:11+02:00',
                    '2015-10-10T11:12:11+02:00'
                ],
                'code': {
                    'text': 'text',
                    'coding': [{
                        'code': 'QOD',
                        'display': 'display',
                        'system': 'http://testing.test.com',
                        'userSelected': True,
                        'version': '2.3'
                    }]
                },
                'repeat': {
                    'count': 12,
                    'duration': 11.32,
                    'durationUnits': 'min',
                    'frequency': 3,
                    'frequencyMax': 5,
                    'period': 5.30,
                    'periodUnits': 'min',
                    'boundsPeriod': {
                        'start': '2015-10-10',
                        'end': '2015-11-11'
                    },
                    'boundsQuantity': {
                        'code': 'code',
                        'system': 'system',
                        'unit': 'kg',
                        'value': 2.400023,
                        'comparator': '<'
                    },
                    'boundsRange': {
                        'high': {
                            'code': 'code',
                            'system': 'system',
                            'unit': 'kg',
                            'value': 2.400023
                        },
                        'low': {
                            'code': 'code',
                            'system': 'system',
                            'unit': 'kg',
                            'value': 0.400023
                        }
                    }
                }
            }
        )

        session.execute("""
            CREATE TABLE test_timing (
                id INTEGER, timing fhir_timing);""")

        session.add(post)

        register_composites(session.connection())
        session.commit()
        get = session.query(TestTimingModel).first()
        assert get.id == 1
        assert get.timing.repeat.durationUnits == 'min'

    def test_post_fails_if_duration_present_but_no_durationUnits(
            self, session, TestTimingModel):
        post = TestTimingModel(
            id=1,
            timing={
                'event': [
                    '2015-10-10T11:11:11+02:00',
                    '2015-10-10T12:11:11+02:00'
                ],
                'code': {
                    'text': 'text',
                    'coding': [{
                        'code': 'QOD',
                        'display': 'display',
                        'system': 'http://testing.test.com',
                        'userSelected': True,
                        'version': '2.3'
                    }]
                },
                'repeat': {
                    'count': 12,
                    'duration': 11.32,
                    'durationMax': 11.22,
                    'frequency': 3,
                    'frequencyMax': 5,
                    'period': 5.30,
                    'periodMax': 7.59,
                    'periodUnits': 'min',
                    'boundsPeriod': {
                        'start': '2015-10-10',
                        'end': '2015-11-11'
                    },
                    'boundsQuantity': {
                        'code': 'code',
                        'system': 'system',
                        'unit': 'kg',
                        'value': 2.400023,
                        'comparator': '<'
                    },
                    'boundsRange': {
                        'high': {
                            'code': 'code',
                            'system': 'system',
                            'unit': 'kg',
                            'value': 2.400023
                        },
                        'low': {
                            'code': 'code',
                            'system': 'system',
                            'unit': 'kg',
                            'value': 0.400023
                        }
                    }
                }
            }
        )

        session.execute("""
            CREATE TABLE test_timing (
                id INTEGER, timing fhir_timing);""")

        session.add(post)
        with pytest.raises(StatementError) as excinfo:
            session.commit()
        assert ('durationUnits must be present for the duration '
                'provided') in str(excinfo.value)

    def test_post_fails_if_period_present_but_no_periodUnits(
            self, session, TestTimingModel):
        post = TestTimingModel(
            id=1,
            timing={
                'event': [
                    '2015-10-10T11:11:11+02:00',
                    '2015-10-10T10:11:11+02:00'
                ],
                'code': {
                    'text': 'text',
                    'coding': [{
                        'code': 'QOD',
                        'display': 'display',
                        'system': 'http://testing.test.com',
                        'userSelected': True,
                        'version': '2.3'
                    }]
                },
                'repeat': {
                    'count': 12,
                    'duration': 11.32,
                    'durationUnits': 'min',
                    'durationMax': 11.22,
                    'frequency': 3,
                    'frequencyMax': 5,
                    'period': 5.30,
                    'periodMax': 7.59,
                    'boundsPeriod': {
                        'start': '2015-10-10',
                        'end': '2015-11-11'
                    },
                    'boundsQuantity': {
                        'code': 'code',
                        'system': 'system',
                        'unit': 'kg',
                        'value': 2.400023,
                        'comparator': '<'
                    },
                    'boundsRange': {
                        'high': {
                            'code': 'code',
                            'system': 'system',
                            'unit': 'kg',
                            'value': 2.400023
                        },
                        'low': {
                            'code': 'code',
                            'system': 'system',
                            'unit': 'kg',
                            'value': 0.400023
                        }
                    }
                }
            }
        )

        session.execute("""
            CREATE TABLE test_timing (
                id INTEGER, timing fhir_timing);""")

        session.add(post)
        with pytest.raises(StatementError) as excinfo:
            session.commit()
        assert ('periodUnits must be present for the period '
                'provided') in str(excinfo.value)

    def test_post_fails_if_both_frequency_and_when_exists(
            self, session, TestTimingModel):
        post = TestTimingModel(
            id=1,
            timing={
                'event': [
                    '2015-10-10T11:11:11+02:00',
                    '2015-10-10T10:11:11+02:00'
                ],
                'code': {
                    'text': 'text',
                    'coding': [{
                        'code': 'QOD',
                        'display': 'display',
                        'system': 'http://testing.test.com',
                        'userSelected': True,
                        'version': '2.3'
                    }]
                },
                'repeat': {
                    'count': 12,
                    'duration': 11.32,
                    'durationUnits': 'min',
                    'durationMax': 11.22,
                    'frequency': 3,
                    'frequencyMax': 5,
                    'period': 5.30,
                    'periodMax': 7.59,
                    'periodUnits': 'min',
                    'when': 'WAKE',
                    'boundsPeriod': {
                        'start': '2015-10-10',
                        'end': '2015-11-11'
                    },
                    'boundsQuantity': {
                        'code': 'code',
                        'system': 'system',
                        'unit': 'kg',
                        'value': 2.400023,
                        'comparator': '<'
                    },
                    'boundsRange': {
                        'high': {
                            'code': 'code',
                            'system': 'system',
                            'unit': 'kg',
                            'value': 2.400023
                        },
                        'low': {
                            'code': 'code',
                            'system': 'system',
                            'unit': 'kg',
                            'value': 0.400023
                        }
                    }
                }
            }
        )

        session.execute("""
            CREATE TABLE test_timing (
                id INTEGER, timing fhir_timing);""")

        session.add(post)
        with pytest.raises(StatementError) as excinfo:
            session.commit()
        assert ('Either frequency or when can exist, not both') in str(
            excinfo.value)

    def test_duration_should_be_non_negative_value(
            self, session, TestTimingModel):
        post = TestTimingModel(
            id=1,
            timing={
                'event': [
                    '2015-10-10T11:11:11+02:00',
                    '2015-10-10T10:11:11+02:00'
                ],
                'code': {
                    'text': 'text',
                    'coding': [{
                        'code': 'QOD',
                        'display': 'display',
                        'system': 'http://testing.test.com',
                        'userSelected': True,
                        'version': '2.3'
                    }]
                },
                'repeat': {
                    'count': 12,
                    'duration': -11.32,
                    'durationUnits': 'min',
                    'durationMax': -11.22,
                    'frequency': 3,
                    'frequencyMax': 5,
                    'period': 5.30,
                    'periodMax': -7.59,
                    'periodUnits': 'min',
                    'when': 'WAKE',
                    'boundsPeriod': {
                        'start': '2015-10-10',
                        'end': '2015-11-11'
                    },
                    'boundsQuantity': {
                        'code': 'code',
                        'system': 'system',
                        'unit': 'kg',
                        'value': 2.400023,
                        'comparator': '<'
                    },
                    'boundsRange': {
                        'high': {
                            'code': 'code',
                            'system': 'system',
                            'unit': 'kg',
                            'value': 2.400023
                        },
                        'low': {
                            'code': 'code',
                            'system': 'system',
                            'unit': 'kg',
                            'value': 0.400023
                        }
                    }
                }
            }
        )

        session.execute("""
            CREATE TABLE test_timing (
                id INTEGER, timing fhir_timing);""")

        session.add(post)
        with pytest.raises(StatementError) as excinfo:
            session.commit()
        assert ('duration SHALL be a non-negative value') in str(excinfo.value)

    def test_period_should_be_non_negative_value(
            self, session, TestTimingModel):
        post = TestTimingModel(
            id=1,
            timing={
                'event': [
                    '2015-10-10T11:11:11+02:00',
                    '2015-10-10T10:11:11+02:00'
                ],
                'code': {
                    'text': 'text',
                    'coding': [{
                        'code': 'QOD',
                        'display': 'display',
                        'system': 'http://testing.test.com',
                        'userSelected': True,
                        'version': '2.3'
                    }]
                },
                'repeat': {
                    'count': 12,
                    'duration': 11.32,
                    'durationUnits': 'min',
                    'durationMax': 11.22,
                    'frequency': 3,
                    'frequencyMax': 5,
                    'period': -5.30,
                    'periodMax': 7.59,
                    'periodUnits': 'min',
                    'boundsPeriod': {
                        'start': '2015-10-10',
                        'end': '2015-11-11'
                    },
                    'boundsQuantity': {
                        'code': 'code',
                        'system': 'system',
                        'unit': 'kg',
                        'value': 2.400023,
                        'comparator': '<'
                    },
                    'boundsRange': {
                        'high': {
                            'code': 'code',
                            'system': 'system',
                            'unit': 'kg',
                            'value': 2.400023
                        },
                        'low': {
                            'code': 'code',
                            'system': 'system',
                            'unit': 'kg',
                            'value': 0.400023
                        }
                    }
                }
            }
        )

        session.execute("""
            CREATE TABLE test_timing (
                id INTEGER, timing fhir_timing);""")

        session.add(post)
        with pytest.raises(StatementError) as excinfo:
            session.commit()
        assert ('period SHALL be a non-negative value') in str(excinfo.value)

    def test_period_must_be_provided_if_periodMax_is_provided(
            self, session, TestTimingModel):
        post = TestTimingModel(
            id=1,
            timing={
                'event': [
                    '2015-10-10T11:11:11+02:00',
                    '2015-10-10T10:11:11+02:00'
                ],
                'code': {
                    'text': 'text',
                    'coding': [{
                        'code': 'QOD',
                        'display': 'display',
                        'system': 'http://testing.test.com',
                        'userSelected': True,
                        'version': '2.3'
                    }]
                },
                'repeat': {
                    'count': 12,
                    'duration': 11.32,
                    'durationUnits': 'min',
                    'durationMax': 11.22,
                    'frequency': 3,
                    'frequencyMax': 5,
                    'periodMax': 11.22,
                    'periodUnits': 'min',
                    'boundsPeriod': {
                        'start': '2015-10-10',
                        'end': '2015-11-11'
                    },
                    'boundsQuantity': {
                        'code': 'code',
                        'system': 'system',
                        'unit': 'kg',
                        'value': 2.400023,
                        'comparator': '<'
                    },
                    'boundsRange': {
                        'high': {
                            'code': 'code',
                            'system': 'system',
                            'unit': 'kg',
                            'value': 2.400023
                        },
                        'low': {
                            'code': 'code',
                            'system': 'system',
                            'unit': 'kg',
                            'value': 0.400023
                        }
                    }
                }
            }
        )

        session.execute("""
            CREATE TABLE test_timing (
                id INTEGER, timing fhir_timing);""")

        session.add(post)
        with pytest.raises(StatementError) as excinfo:
            session.commit()
        assert ('If there is a periodMax, there must be a period') in str(
            excinfo.value)

    def test_duration_must_be_provided_if_durationMax_is_provided(
            self, session, TestTimingModel):
        post = TestTimingModel(
            id=1,
            timing={
                'event': [
                    '2015-10-10T11:11:11+02:00',
                    '2015-10-10T10:11:11+02:00'
                ],
                'code': {
                    'text': 'text',
                    'coding': [{
                        'code': 'QOD',
                        'display': 'display',
                        'system': 'http://testing.test.com',
                        'userSelected': True,
                        'version': '2.3'
                    }]
                },
                'repeat': {
                    'count': 12,
                    'durationUnits': 'min',
                    'durationMax': 11.22,
                    'frequency': 3,
                    'frequencyMax': 5,
                    'period': 5.30,
                    'periodMax': 7.59,
                    'periodUnits': 'min',
                    'boundsPeriod': {
                        'start': '2015-10-10',
                        'end': '2015-11-11'
                    },
                    'boundsQuantity': {
                        'code': 'code',
                        'system': 'system',
                        'unit': 'kg',
                        'value': 2.400023,
                        'comparator': '<'
                    },
                    'boundsRange': {
                        'high': {
                            'code': 'code',
                            'system': 'system',
                            'unit': 'kg',
                            'value': 2.400023
                        },
                        'low': {
                            'code': 'code',
                            'system': 'system',
                            'unit': 'kg',
                            'value': 0.400023
                        }
                    }
                }
            }
        )

        session.execute("""
            CREATE TABLE test_timing (
                id INTEGER, timing fhir_timing);""")

        session.add(post)
        with pytest.raises(StatementError) as excinfo:
            session.commit()
        assert ('If there is a durationMax, there must be a duration') in str(
            excinfo.value)

    def test_post_fails_if_duration_unit_provided_is_not_in_valueset(
            self, session, TestTimingModel):
        post = TestTimingModel(
            id=1,
            timing={
                'event': [
                    '2015-10-10T11:11:11+02:00',
                    '2015-10-10T10:11:11+02:00'
                ],
                'code': {
                    'text': 'text',
                    'coding': [{
                        'code': 'QOD',
                        'display': 'display',
                        'system': 'http://testing.test.com',
                        'userSelected': True,
                        'version': '2.3'
                    }]
                },
                'repeat': {
                    'count': 12,
                    'duration': 11.32,
                    'durationMax': 11.22,
                    'durationUnits': 'mwezi',
                    'frequency': 3,
                    'frequencyMax': 5,
                    'period': 5.30,
                    'periodMax': 7.59,
                    'periodUnits': 'min',
                    'boundsPeriod': {
                        'start': '2015-10-10',
                        'end': '2015-11-11'
                    },
                    'boundsQuantity': {
                        'code': 'code',
                        'system': 'system',
                        'unit': 'kg',
                        'value': 2.400023,
                        'comparator': '<'
                    },
                    'boundsRange': {
                        'high': {
                            'code': 'code',
                            'system': 'system',
                            'unit': 'kg',
                            'value': 2.400023
                        },
                        'low': {
                            'code': 'code',
                            'system': 'system',
                            'unit': 'kg',
                            'value': 0.400023
                        }
                    }
                }
            }
        )

        session.execute("""
            CREATE TABLE test_timing (
                id INTEGER, timing fhir_timing);""")

        session.add(post)
        with pytest.raises(StatementError) as excinfo:
            session.commit()
        assert ('The timing durationUnits must be defined in') in str(
            excinfo.value)

    def test_post_fails_if_period_unit_provided_is_not_in_valueset(
            self, session, TestTimingModel):
        post = TestTimingModel(
            id=1,
            timing={
                'event': [
                    '2015-10-10T11:11:11+02:00',
                    '2015-10-10T10:11:11+02:00'
                ],
                'code': {
                    'text': 'text',
                    'coding': [{
                        'code': 'QOD',
                        'display': 'display',
                        'system': 'http://testing.test.com',
                        'userSelected': True,
                        'version': '2.3'
                    }]
                },
                'repeat': {
                    'count': 12,
                    'duration': 11.32,
                    'durationMax': 11.22,
                    'durationUnits': 'min',
                    'frequency': 3,
                    'frequencyMax': 5,
                    'period': 5.30,
                    'periodMax': 7.59,
                    'periodUnits': 'mwezi',
                    'boundsPeriod': {
                        'start': '2015-10-10',
                        'end': '2015-11-11'
                    },
                    'boundsQuantity': {
                        'code': 'code',
                        'system': 'system',
                        'unit': 'kg',
                        'value': 2.400023,
                        'comparator': '<'
                    },
                    'boundsRange': {
                        'high': {
                            'code': 'code',
                            'system': 'system',
                            'unit': 'kg',
                            'value': 2.400023
                        },
                        'low': {
                            'code': 'code',
                            'system': 'system',
                            'unit': 'kg',
                            'value': 0.400023
                        }
                    }
                }
            }
        )

        session.execute("""
            CREATE TABLE test_timing (
                id INTEGER, timing fhir_timing);""")

        session.add(post)
        with pytest.raises(StatementError) as excinfo:
            session.commit()
        assert ('The timing periodUnits must be defined in') in str(
            excinfo.value)

    def test_post_fails_if_when_value_provided_is_not_in_valueset(
            self, session, TestTimingModel):
        post = TestTimingModel(
            id=1,
            timing={
                'event': [
                    '2015-10-10T11:11:11+02:00',
                    '2015-10-10T10:11:11+02:00'
                ],
                'code': {
                    'text': 'text',
                    'coding': [{
                        'code': 'QOD',
                        'display': 'display',
                        'system': 'http://testing.test.com',
                        'userSelected': True,
                        'version': '2.3'
                    }]
                },
                'repeat': {
                    'count': 12,
                    'duration': 11.32,
                    'durationMax': 11.22,
                    'durationUnits': 'min',
                    'period': 5.30,
                    'periodMax': 7.59,
                    'periodUnits': 's',
                    'when': 'rrt',
                    'boundsPeriod': {
                        'start': '2015-10-10',
                        'end': '2015-11-11'
                    },
                    'boundsQuantity': {
                        'code': 'code',
                        'system': 'system',
                        'unit': 'kg',
                        'value': 2.400023,
                        'comparator': '<'
                    },
                    'boundsRange': {
                        'high': {
                            'code': 'code',
                            'system': 'system',
                            'unit': 'kg',
                            'value': 2.400023
                        },
                        'low': {
                            'code': 'code',
                            'system': 'system',
                            'unit': 'kg',
                            'value': 0.400023
                        }
                    }
                }
            }
        )

        session.execute("""
            CREATE TABLE test_timing (
                id INTEGER, timing fhir_timing);""")

        session.add(post)
        with pytest.raises(StatementError) as excinfo:
            session.commit()
        assert ('The timing when must be defined in') in str(
            excinfo.value)

    def test_post_fails_if_code_value_provided_is_not_in_valueset(
            self, session, TestTimingModel):
        post = TestTimingModel(
            id=1,
            timing={
                'event': [
                    '2015-10-10T11:11:11+02:00',
                    '2015-10-10T10:11:11+02:00'
                ],
                'code': {
                    'text': 'text',
                    'coding': [{
                        'code': 'HAIKO',
                        'display': 'display',
                        'system': 'http://testing.test.com',
                        'userSelected': True,
                        'version': '2.3'
                    }]
                },
                'repeat': {
                    'count': 12,
                    'duration': 11.32,
                    'durationMax': 11.22,
                    'durationUnits': 'min',
                    'period': 5.30,
                    'periodMax': 7.59,
                    'periodUnits': 's',
                    'when': 'WAKE',
                    'boundsPeriod': {
                        'start': '2015-10-10',
                        'end': '2015-11-11'
                    },
                    'boundsQuantity': {
                        'code': 'code',
                        'system': 'system',
                        'unit': 'kg',
                        'value': 2.400023,
                        'comparator': '<'
                    },
                    'boundsRange': {
                        'high': {
                            'code': 'code',
                            'system': 'system',
                            'unit': 'kg',
                            'value': 2.400023
                        },
                        'low': {
                            'code': 'code',
                            'system': 'system',
                            'unit': 'kg',
                            'value': 0.400023
                        }
                    }
                }
            }
        )

        session.execute("""
            CREATE TABLE test_timing (
                id INTEGER, timing fhir_timing);""")

        session.add(post)
        with pytest.raises(StatementError) as excinfo:
            session.commit()
        assert ('The timing code must be defined in') in str(
            excinfo.value)

    def test_post_data_with_null_timing_field(
            self, session, TestTimingModel):
        post = TestTimingModel(
            id=1,
            timing={}
        )

        session.execute("""
            CREATE TABLE test_timing (
                id INTEGER, timing fhir_timing);""")

        session.add(post)

        register_composites(session.connection())
        session.commit()
        get = session.query(TestTimingModel).first()
        assert get.id == 1
        assert get.timing.event is None

    @pytest.fixture
    def ProfiledTiming(self):
        class Timing(TimingDef):
            def element_properties(self):
                fields = super().element_properties()
                for field in fields:
                    if not field.name == 'when':
                        field.cardinality['mini'] = 1

                return fields

        return Timing()()

    @pytest.fixture
    def TestProfiledTiming(self, Base):
        class TestProfiledTiming(Base):
            __tablename__ = 'test_timing'
            id = Column(primitives.IntegerField, primary_key=True)
            timing = Column(self.ProfiledTiming())
        return TestProfiledTiming

    def test_nullable_change_to_false(self, session):
        fields = self.ProfiledTiming()
        repeat = [field for field in fields.columns if field.name == 'repeat']
        code = [field for field in fields.columns if field.name == 'code']
        event = [field for field in fields.columns if field.name == 'event']

        assert not repeat[0].nullable
        assert not code[0].nullable
        assert not event[0].nullable

    def test_post_data_fields_present(
            self, session, TestProfiledTiming):
        post = TestProfiledTiming(
            id=1,
            timing={
                'event': [
                    '2015-10-10T11:11:11+02:00',
                    '2015-10-10T10:11:11+02:00'
                ],
                'code': {
                    'text': 'text',
                    'coding': [{
                        'code': 'QOD',
                        'display': 'display',
                        'system': 'http://testing.test.com',
                        'userSelected': True,
                        'version': '2.3'
                    }]
                },
                'repeat': {
                    'count': 12,
                    'duration': 11.32,
                    'durationMax': 11.22,
                    'durationUnits': 'min',
                    'frequency': 3,
                    'frequencyMax': 5,
                    'period': 5.30,
                    'periodMax': 7.59,
                    'periodUnits': 'min',
                    'boundsPeriod': {
                        'start': '2015-10-10',
                        'end': '2015-11-11'
                    },
                    'boundsQuantity': {
                        'code': 'code',
                        'system': 'system',
                        'unit': 'kg',
                        'value': 2.400023,
                        'comparator': '<'
                    },
                    'boundsRange': {
                        'high': {
                            'code': 'code',
                            'system': 'system',
                            'unit': 'kg',
                            'value': 2.400023
                        },
                        'low': {
                            'code': 'code',
                            'system': 'system',
                            'unit': 'kg',
                            'value': 0.400023
                        }
                    }
                }
            }
        )

        session.execute("""
            CREATE TABLE test_timing (
                id INTEGER, timing fhir_timing);""")

        session.add(post)
        session.commit()
        register_composites(session.connection())
        get = session.query(TestProfiledTiming).first()
        assert get.id == 1
        assert get.timing.repeat.count == 12

    def test_fail_to_post_data_missing_fields(
            self, session, TestProfiledTiming):
        post = TestProfiledTiming(
            id=1,
            timing={}
        )

        session.execute("""
            CREATE TABLE test_timing (
                id INTEGER, timing fhir_timing);""")

        session.add(post)
        with pytest.raises(StatementError) as excinfo:
            session.commit()
        assert ('Field code in column fhir_timing not '
                'nullable') in str(excinfo.value)
        assert ('Field event in column fhir_timing not '
                'nullable') in str(excinfo.value)
        assert ('Field repeat in column fhir_timing not '
                'nullable') in str(excinfo.value)
