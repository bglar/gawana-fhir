from fhir_server.api import api_v1
from .views import (
    healthcareservice_list, healthcareservice_detail,
    location_list, location_detail,
    patient_list, patient_detail,
    practitioner_list, practitioner_detail,
    organization_list, organization_detail
)

# HealthcareService
api_v1.add_url_rule('/HealthcareService',
                    view_func=healthcareservice_list,
                    methods=['GET', 'POST', 'PUT', 'DELETE'])

api_v1.add_url_rule('/HealthcareService/_history',
                    view_func=healthcareservice_list,
                    methods=['GET'])

api_v1.add_url_rule('/HealthcareService/<fhirop:operation>',
                    view_func=healthcareservice_list,
                    methods=['POST'])

api_v1.add_url_rule('/HealthcareService/<string:key>',
                    view_func=healthcareservice_detail,
                    methods=['GET', 'PUT', 'DELETE', 'POST'])

api_v1.add_url_rule('/HealthcareService/<string:key>/<fhirop:operation>',
                    view_func=healthcareservice_list,
                    methods=['POST'])

api_v1.add_url_rule('/HealthcareService/<key>/_history/<vid>',
                    view_func=healthcareservice_detail,
                    methods=['GET', 'PUT'])

api_v1.add_url_rule('/HealthcareService/<key>/_history',
                    view_func=healthcareservice_detail,
                    methods=['GET'])

# Location
api_v1.add_url_rule('/Location',
                    view_func=location_list,
                    methods=['GET', 'POST', 'PUT', 'DELETE'])

api_v1.add_url_rule('/Location/_history',
                    view_func=location_list,
                    methods=['GET'])

api_v1.add_url_rule('/Location/<fhirop:operation>',
                    view_func=location_list,
                    methods=['POST'])

api_v1.add_url_rule('/Location/<string:key>',
                    view_func=location_detail,
                    methods=['GET', 'PUT', 'DELETE', 'POST'])

api_v1.add_url_rule('/Location/<string:key>/<fhirop:operation>',
                    view_func=location_list,
                    methods=['POST'])

api_v1.add_url_rule('/Location/<key>/_history/<vid>',
                    view_func=location_detail,
                    methods=['GET', 'PUT'])

api_v1.add_url_rule('/Location/<key>/_history',
                    view_func=location_detail,
                    methods=['GET'])

# Patient
api_v1.add_url_rule('/Patient',
                    view_func=patient_list,
                    methods=['GET', 'POST', 'PUT', 'DELETE'])

api_v1.add_url_rule('/Patient/_history',
                    view_func=patient_list,
                    methods=['GET'])

api_v1.add_url_rule('/Patient/<fhirop:operation>',
                    view_func=patient_list,
                    methods=['POST'])

api_v1.add_url_rule('/Patient/<string:key>',
                    view_func=patient_detail,
                    methods=['GET', 'PUT', 'DELETE', 'POST'])

api_v1.add_url_rule('/Patient/<string:key>/<fhirop:operation>',
                    view_func=patient_list,
                    methods=['POST'])

api_v1.add_url_rule('/Patient/<key>/_history/<vid>',
                    view_func=patient_detail,
                    methods=['GET', 'PUT'])

api_v1.add_url_rule('/Patient/<key>/_history',
                    view_func=patient_detail,
                    methods=['GET'])

# Organization
api_v1.add_url_rule('/Organization',
                    view_func=organization_list,
                    methods=['GET', 'POST', 'PUT', 'DELETE'])

api_v1.add_url_rule('/Organization/_history',
                    view_func=organization_list,
                    methods=['GET'])

api_v1.add_url_rule('/Organization/<fhirop:operation>',
                    view_func=organization_list,
                    methods=['POST'])

api_v1.add_url_rule('/Organization/<string:key>',
                    view_func=organization_detail,
                    methods=['GET', 'PUT', 'DELETE', 'POST'])

api_v1.add_url_rule('/Organization/<string:key>/<fhirop:operation>',
                    view_func=organization_list,
                    methods=['POST'])

api_v1.add_url_rule('/Organization/<key>/_history/<vid>',
                    view_func=organization_detail,
                    methods=['GET', 'PUT'])

api_v1.add_url_rule('/Organization/<key>/_history',
                    view_func=organization_detail,
                    methods=['GET'])

# Practitioner
api_v1.add_url_rule('/Practitioner',
                    view_func=practitioner_list,
                    methods=['GET', 'POST', 'PUT', 'DELETE'])

api_v1.add_url_rule('/Practitioner/_history',
                    view_func=practitioner_list,
                    methods=['GET'])

api_v1.add_url_rule('/Practitioner/<fhirop:operation>',
                    view_func=practitioner_list,
                    methods=['POST'])

api_v1.add_url_rule('/Practitioner/<string:key>',
                    view_func=practitioner_detail,
                    methods=['GET', 'PUT', 'DELETE', 'POST'])

api_v1.add_url_rule('/Practitioner/<string:key>/<fhirop:operation>',
                    view_func=practitioner_list,
                    methods=['POST'])

api_v1.add_url_rule('/Practitioner/<key>/_history/<vid>',
                    view_func=practitioner_detail,
                    methods=['GET', 'PUT'])

api_v1.add_url_rule('/Practitioner/<key>/_history',
                    view_func=practitioner_detail,
                    methods=['GET'])
