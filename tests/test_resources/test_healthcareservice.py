from unittest.mock import patch

from fhir_server.resources.identification.healthcareservice import HealthcareService


class TestHealthcareService(object):
    id = "1"
    implicitRules = "https://gawana-fhir.constraints.co.ke/rules"
    language = "EN"
    identifier = [
        {
            "system": "system",
            "use": "secondary",
            "value": "value111",
            "assigner": {"reference": "reference url", "display": "Patient X"},
            "type": {
                "text": "text",
                "coding": [
                    {
                        "code": "UDI",
                        "display": "display",
                        "system": "http://testing.test.com",
                        "userSelected": "True",
                        "version": "2.3",
                    }
                ],
            },
            "period": {"start": "2011-05-24", "end": "2011-06-24"},
        }
    ]
    providedBy = {
        "display": "display",
        "reference": "http://spark.furore.com/fhir/Organization/1",
    }
    serviceCategory = {
        "text": "text",
        "coding": [
            {
                "code": "6",
                "display": "display",
                "system": "http://testing.test.com",
                "userSelected": "True",
                "version": "2.3",
            }
        ],
    }
    serviceType = [
        {
            "text": "text",
            "coding": [
                {
                    "code": "4",
                    "display": "display",
                    "system": "http://testing.test.com",
                    "userSelected": "True",
                    "version": "2.3",
                }
            ],
        }
    ]
    specialty = [
        {
            "text": "text",
            "coding": [
                {
                    "code": "394592004",
                    "display": "display",
                    "system": "http://testing.test.com",
                    "userSelected": "True",
                    "version": "2.3",
                }
            ],
        }
    ]
    location = [
        {"display": "display", "reference": "http://spark.furore.com/fhir/Location/1"}
    ]
    serviceName = "Test Service"
    comment = "Some Health care service comment"
    extraDetails = "extraDetails"
    photo = {}
    telecom = [
        {
            "rank": 2,
            "system": "phone",
            "use": "work",
            "value": "+254712122988",
            "period": {"start": "2011-05-24", "end": "2011-06-24"},
        }
    ]
    coverageArea = [
        {"display": "display", "reference": "http://spark.furore.com/fhir/Location/1"}
    ]
    serviceProvisionCode = [
        {
            "text": "text",
            "coding": [
                {
                    "code": "cost",
                    "display": "display",
                    "system": "http://testing.test.com",
                    "userSelected": "True",
                    "version": "2.3",
                }
            ],
        }
    ]
    eligibility = {
        "text": "text",
        "coding": [
            {
                "code": "area",
                "display": "display",
                "system": "http://testing.test.com",
                "userSelected": "True",
                "version": "2.3",
            }
        ],
    }
    eligibilityNote = "eligibilityNote"
    programName = ["programName1", "programName2"]
    characteristic = [
        {
            "text": "text",
            "coding": [
                {
                    "code": "area",
                    "display": "display",
                    "system": "http://testing.test.com",
                    "userSelected": "True",
                    "version": "2.3",
                }
            ],
        }
    ]
    referralMethod = [
        {
            "text": "text",
            "coding": [
                {
                    "code": "mail",
                    "display": "display",
                    "system": "http://testing.test.com",
                    "userSelected": "True",
                    "version": "2.3",
                }
            ],
        }
    ]
    publicKey = "publicKey"
    appointmentRequired = True
    notAvailable = {}
    availableTime = [
        {
            "daysOfWeek": ["mon"],
            "allDay": True,
            "availableStartTime": "11:22:00",
            "availableEndTime": "11:22:00",
        }
    ]
    availabilityExceptions = "availabilityExceptions"

    @patch("fhir_server.helpers.validations.requests.get")
    def test_healthcareservice_repr(self, mock_get):
        mock_get.return_value.json.return_value = {
            "count": 1,
            "data": [
                {"code": "secondary"},
                {"code": "UDI"},
                {"code": "6"},
                {"code": "4"},
                {"code": "394592004"},
                {"code": "work"},
                {"code": "cost"},
                {"code": "area"},
                {"code": "mail"},
                {"code": "mon"},
            ],
        }
        data = HealthcareService(
            id=self.id,
            implicitRules=self.implicitRules,
            language=self.language,
            serviceName=self.serviceName,
            comment=self.comment,
            extraDetails=self.extraDetails,
            eligibilityNote=self.eligibilityNote,
            programName=self.programName,
            publicKey=self.publicKey,
            appointmentRequired=self.appointmentRequired,
            availabilityExceptions=self.availabilityExceptions,
            identifier=self.identifier,
            availableTime=self.availableTime,
            referralMethod=self.referralMethod,
            serviceProvisionCode=self.serviceProvisionCode,
            specialty=self.specialty,
            serviceType=self.serviceType,
            serviceCategory=self.serviceCategory,
        )

        assert str(data) == "<HealthcareService 'Test Service'>"
