from sqlalchemy import Column
from sqlalchemy.orm import validates
from sqlalchemy_utils import CompositeArray as Array

from fhir_server.configs import (
    ISSUE_SEVERITY_URL,
    ISSUE_TYPE_URL,
    OPERATION_OUTCOME_URL,
)
from fhir_server.elements import primitives, Field, complex
from fhir_server.resources.domainresource import DomainResource
from fhir_server.elements.base.backboneelement import BackboneElement


class OperationOutcomeIssue(BackboneElement):
    """ A single issue associated with the action.

    An error, warning or information message that results from a system action.
    """

    def element_properties(self):
        elm = super().element_properties()
        elm.extend(
            [
                Field("code", {"mini": 1, "maxi": 1}, primitives.CodeField, None),
                # Error or warning code.
                Field("severity", {"mini": 1, "maxi": 1}, primitives.CodeField, None),
                # fatal | error | warning | information.
                Field(
                    "diagnostics", {"mini": 0, "maxi": 1}, primitives.StringField, None
                ),
                # Additional diagnostic information about the issue.
                Field(
                    "location", {"mini": 0, "maxi": -1}, primitives.StringField, None
                ),
                # XPath of element(s) related to issue.
                Field(
                    "expression", {"mini": 0, "maxi": -1}, primitives.StringField, None
                ),
                # FluentPath of element(s) related to issue
                Field(
                    "details",
                    {"mini": 0, "maxi": 1},
                    complex.CodeableConceptField(),
                    None,
                )
                # Additional details about the error.
            ]
        )
        return elm


OperationOutcomeIssueField = OperationOutcomeIssue()


class OperationOutcome(DomainResource):
    """ Information about the success/failure of an action.

    A collection of error, warning or information messages that result from a
    system action.
    """

    issue = Column(Array(OperationOutcomeIssueField()))
    # A single issue associated with the action.

    # @validates('issue')
    # def validate_issue(self, key, issue):
    #     for data in issue:
    #         code = data.get('code')
    #         msg = 'operation outcome code'
    #         self.code_fields_validator(code, ISSUE_TYPE_URL, msg)
    #
    #         severity = data.get('severity')
    #         msg = 'operation outcome severity'
    #         self.code_fields_validator(severity, ISSUE_SEVERITY_URL, msg)
    #
    #         details = data.get('details')
    #         msg = 'operation outcome details'
    #         self.code_fields_validator(details, OPERATION_OUTCOME_URL, msg)
    #
    #     return issue

    def _resource_summary(self):
        summary_fields = ["id", "meta", "issue"]
        return {"repr": "%r" % self.issue, "fields": summary_fields}

    def __repr__(self):
        return "<OperationOutcome %r>" % self.id
