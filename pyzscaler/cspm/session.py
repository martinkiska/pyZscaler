from restfly.endpoint import APIEndpoint


class AuthenticatedSessionAPI(APIEndpoint):

    def create_token(self, app_id: str, app_secret: str, license_id: str, subscription_key: str, **kwargs):
        """
        Creates a session token for ZCSPM.

        Args:
            app_id (str):
            app_secret (str):
            license_id (str):
            subscription_key (str):
            **kwargs: Optional keyword args.

        Keyword Args:
            account_id (str):

        Returns:
            The authenticated session token for the credentials provided.

        """
        account_id = kwargs.get("account_id")
        payload = {"APIApplicationId": app_id, "Secret": app_secret}
        headers = {"Ocp-Apim-Subscription-Key": subscription_key}

        if account_id:
            return self._post(
                f"authorize/license/{license_id}/token?accountId={account_id}",
                headers=headers,
                json=payload,
            )
        else:
            return self._post(
                f"authorize/license/{license_id}/token", headers=headers, json=payload
            )
