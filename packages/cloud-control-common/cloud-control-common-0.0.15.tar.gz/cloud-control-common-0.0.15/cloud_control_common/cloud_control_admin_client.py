from cloud_control_common.admin_http_client import AdminHttpClient
from cloud_control_common.config import get_organization_summary


class CloudControlAdminClient:

    def __init__(self, credentials, geo):
        self.credentials = credentials
        self.geo = geo
        self.http_client = AdminHttpClient(geo, self.credentials)

    def get_organization_summary(self, org_id):
        return self.http_client.get(get_organization_summary.format(org_id))
