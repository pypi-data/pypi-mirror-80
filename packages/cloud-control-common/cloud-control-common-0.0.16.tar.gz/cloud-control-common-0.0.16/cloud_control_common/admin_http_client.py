import requests
from requests import auth

from cloud_control_common.cloud_control_exception import CloudControlException
from cloud_control_common.config import api_urls, context_path, admin_api_version, admin_path


class AdminHttpClient:

    def __init__(self, geo, credentials):
        self._session = requests.Session()
        self._session.auth = auth.HTTPBasicAuth(credentials.get_username(), credentials.get_password())
        self._session.verify = True
        self._session.headers = {'Content-Type': 'application/json'}
        self.host = api_urls.get(geo)
        self.geo = geo

    def get(self, path, **kwargs):
        response = self._session.get('{0}{1}'.format(self._get_base_path(), path))
        if response.status_code != 200:
            self._report_error_status(response)
        else:
            return response.json()

    def _get_base_path(self):
        return '{0}/{1}/{2}/{3}'.format(self.host, context_path, admin_api_version, admin_path)

    def _report_error_status(self, response):
        if response.status_code == 401:
            raise CloudControlException(
                'Supplied credentials are incorrect or user is not associated with this geo {0}.'.format
                (self.geo), response)
        else:
            raise CloudControlException(
                'API call to {0} failed with status code {1}'.format(response.request.url, response.status_code),
                response)
