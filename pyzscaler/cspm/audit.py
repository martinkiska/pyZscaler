from restfly.endpoint import APIEndpoint
from restfly.session import APISession


class AuditAPI(APIEndpoint):
    def __init__(self, api: APISession):
        super().__init__(api)
        self.token_jar = api.token_jar
        self.license_id = api.license_id

    def list_benchmarks(self, account_id: str):
        token = None
        # Get the token from the token jar

        for token in self.token_jar:
            if token["account_id"] == account_id:
                token = token["account_token"]

        if token is not None:
            headers = {
                "Authorization": f"Bearer {token}",
            }
            return self._get(f"{account_id}/benchmarks", headers=headers).result

        else:
            raise ValueError(
                f"No token found for account id: {account_id}, ensure you initialise ZCSPM with the account id."
            )

    def get_benchmark_summary(self, account_id: str, benchmark_id: str):
        token = None
        for item in self.token_jar:
            if item["account_id"] == account_id:
                token = item["account_token"]

        if token is not None:
            headers = {
                "Authorization": f"Bearer {token}",
            }
            return self._get(
                f"{account_id}/benchmark/{benchmark_id}/summary/?{self.license_id}",
                headers=headers,
            ).result
        else:
            raise ValueError(
                f"No token found for account id: {account_id}, ensure you initialise ZCSPM with the account id."
            )

    def get_health_status(self, account_id: str):
        token = None
        for item in self.token_jar:
            if item["account_id"] == account_id:
                token = item["account_token"]

        if token is not None:
            headers = {
                "Authorization": f"Bearer {token}",
            }
            return self._get(f"{account_id}/healthstatus", headers=headers)
        else:
            raise ValueError(
                f"No token found for account id: {account_id}, ensure you initialise ZCSPM with the account id."
            )
