from sqlalchemy_utils import register_composites

from fhir_server.resources.infrastructure.operationoutcome import (
    OperationOutcome)


class TestOperationOutcome(object):
    id = "1"
    issue = [{
        "code": "invalid",
        "severity": "error",
        "diagnostics": "some exception explanation",
        "location": ["/Patient/name", "/Patient/gender"],
        "expression": ["/Patient/name", "/Patient/gender"],
        "details": {
            "text": "text",
            "coding": [
                {
                    "code": "MSG_CANT_PARSE_CONTENT",
                    "display": "display",
                    "system": "http://testing.test.com",
                    "userSelected": "True",
                    "version": "2.3"
                }]
        }
    }]

    def test_operationoutcome_repr(self):
        data = OperationOutcome(
            id=self.id,
            issue=self.issue
        )

        assert str(data) == "<OperationOutcome '1'>"

    def test_save_operationoutcome(self, session):
        data = OperationOutcome(
            id=self.id,
            issue=self.issue
        )
        session.add(data)
        session.commit()
        register_composites(session.connection())
        get = session.query(OperationOutcome).first()
        assert get.id == '1'
        assert get.issue[0].code == 'invalid'
