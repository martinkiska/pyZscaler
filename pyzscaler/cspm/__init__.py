import os

from pyzscaler.cspm.admin import AdminAPI
from pyzscaler.cspm.audit import AuditAPI
from pyzscaler.cspm.license import LicenseAPI
from pyzscaler.cspm.session import AuthenticatedSessionAPI
from pyzscaler.version import version
from restfly.session import APISession


class ZCSPM(APISession):
    """
    A Controller to access Endpoints in the Zscaler Cloud Security Posture Management (ZCSPM) API.

    The ZCSPM object stores the session token and simplifies access to CRUD options within the ZCSPM platform.

    Attributes:
        account_ids (list): A list of account ids from ZCSPM.
        app_id (str): The ZCSPM application id.
        app_secret (str): The ZCSPM application secret.
        subscription_id (str): The unique id for your ZCSPM subscription.
        subscription_key (str): The key for your ZCSPM subscription.
        license_id (str): The unique id for your ZCSPM license.

    """
    _vendor = "Zscaler"
    _product = "Cloud Security Posture Management"
    _build = version
    _box = True
    _box_attrs = {"camel_killer_box": True}
    _env_base = "ZCSPM"
    _api_domain = "api"

    def __init__(self, **kw):

        self._account_ids = kw.get(
            "account_ids", None
        )
        self._app_secret = kw.get(
            "app_secret", os.getenv(f"{self._env_base}_APP_SECRET")
        )
        self._app_id = kw.get(
            "app_id", os.getenv(f"{self._env_base}_APP_ID")
        )
        self._subscription_key = kw.get(
            "subscription_key", os.getenv(f"{self._env_base}_SUBSCRIPTION_KEY")
        )
        self.license_id = kw.get(
            "license_id", os.getenv(f"{self._env_base}_LICENSE_ID")
        )
        self.token_jar = []

        if kw.get("trial"):
            self._url = "https://trialapi.cloudneeti.com"
        else:
            self._url = "https://api.cloudneeti.com"

        super(ZCSPM, self).__init__(**kw)

    def _build_session(self, **kwargs) -> None:
        """Creates a ZCSPM API session."""

        super(ZCSPM, self)._build_session(**kwargs)

        token_response = self.session.create_token(
            app_id=self._app_id,
            license_id=self.license_id,
            app_secret=self._app_secret,
            subscription_key=self._subscription_key,
        )

        # Get a token for each account provided
        if self._account_ids:
            for account_id in self._account_ids:
                app_token_response = self.session.create_token(
                    app_id=self._app_id,
                    license_id=self.license_id,
                    app_secret=self._app_secret,
                    subscription_key=self._subscription_key,
                    account_id=account_id,
                )
                self.token_jar.append(
                    {
                        "account_id": account_id,
                        "account_token": app_token_response["result"]["token"],
                    }
                )

        if token_response["status_code"] == 200:
            self._session.headers.update(
                {
                    "Authorization": f"Bearer {token_response['result']['token']}",
                    "Ocp-Apim-Subscription-Key": self._subscription_key,
                }
            )
        return token_response["message"]

    @property
    def admin(self):
        """
        The interface object for the :ref:`ZCSPM Admin interface <zcspm-admin>`.

        """
        self._url = "https://trialapi.cloudneeti.com/enterprise/api"
        return AdminAPI(self)

    @property
    def audit(self):
        """
        The interface object for the :ref:`ZCSPM Aduit interface <zcspm-audit>`.

        """
        self._url = (
            f"https://trialapi.cloudneeti.com/audit/license/{self.license_id}/account"
        )
        return AuditAPI(self)

    @property
    def session(self):
        """
        The interface object for the :ref:`ZCSPM Session interface <zcspm-session>`.

        """
        return AuthenticatedSessionAPI(self)

    @property
    def license(self):
        """
        The interface object for the :ref:`ZCSPM License interface <zcspm-license>`.

        """
        self._url = (
            f"https://trialapi.cloudneeti.com/onboarding/license/{self.license_id}"
        )
        return LicenseAPI(self)
