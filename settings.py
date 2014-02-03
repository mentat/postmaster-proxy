import logging


logging.basicConfig(level=logging.INFO)
logging.getLogger('suds.client').setLevel(logging.INFO)
logging.getLogger('suds.transport').setLevel(logging.INFO)
logging.getLogger('suds.xsd.schema').setLevel(logging.INFO)
logging.getLogger('suds.wsdl').setLevel(logging.INFO)
logging.getLogger('suds.resolver').setLevel(logging.INFO)
logging.getLogger('suds.xsd.query').setLevel(logging.INFO)
logging.getLogger('suds.xsd.basic').setLevel(logging.INFO)
logging.getLogger('suds.xsd.sxbasic').setLevel(logging.INFO)
logging.getLogger('suds.xsd.sxbase').setLevel(logging.INFO)
logging.getLogger('suds.xsd.deplist').setLevel(logging.INFO)
logging.getLogger('suds.xsd.doctor').setLevel(logging.INFO)
logging.getLogger('suds.xsd.query').setLevel(logging.INFO)
logging.getLogger('suds.xsd.schema').setLevel(logging.INFO)
logging.getLogger('suds.mx.literal').setLevel(logging.INFO)
logging.getLogger('suds.mx.core').setLevel(logging.INFO)
logging.getLogger('suds.sax.date').setLevel(logging.INFO)
logging.getLogger('suds.sax.parser').setLevel(logging.INFO)
logging.getLogger('suds.servicedefinition').setLevel(logging.INFO)
logging.getLogger('suds.sudsobject').setLevel(logging.INFO)
logging.getLogger('suds.transport.http').setLevel(logging.INFO)
logging.getLogger('suds.umx.typed').setLevel(logging.INFO)
logging.getLogger('suds.binding.marshaller').setLevel(logging.INFO)
logging.getLogger('suds.metrics').setLevel(logging.INFO)

# Secret key that must be in X-PM-Auth header of all incoming requests.
SECRET_KEY = 'blah'

# Carriers credentials
CARRIERS_TEST = {
    'stamps': {
        'integration_id': '33fb4597-0228-424c-9b33-9611d6949901',
        'username': 'mentat',
        'password': 'postage1',
    },
}
CARRIERS_LIVE = {
    'stamps': {
        'integration_id': '33fb4597-0228-424c-9b33-9611d6949901',
        'username': 'mentat',
        'password': 'postmaster411',
    },
}

# How often allow for refreshing authenticators?
STAMPS_REFRESH_COOLDOWN = 5 * 60 # 5 minutes
