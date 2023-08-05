import logging
import requests

from faceclient import httpclient
from faceclient import faces

LOG = logging.getLogger(__name__)
DEFAULT_BASE_URL = 'http://localhost:8082/api'


class Client(object):
    def __init__(self, base_url=DEFAULT_BASE_URL, **kwargs):
        session = requests.Session()

        http_client = httpclient.HTTPClient(
            base_url, session=session, **kwargs
        )
        self.http_client = http_client

        # Create all resource managers.
        self.faces = faces.FacesManager(http_client)
