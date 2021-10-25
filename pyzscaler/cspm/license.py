from restfly.endpoint import APIEndpoint
from restfly.session import APISession


class LicenseAPI(APIEndpoint):
    def __init__(self, api: APISession):
        super().__init__(api)
        self.license_id = api.license_id

    def list_accounts(self):
        return self._get('licenseAccounts').result

    def list_licenses(self):
        return self._get(f"licenseAccounts?{self.license_id}").result

    def azure_account(self):
        return self._post(f"account/azure?{self.license_id}")
