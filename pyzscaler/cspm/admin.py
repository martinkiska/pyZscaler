from restfly.endpoint import APIEndpoint


class AdminAPI(APIEndpoint):
    def get_tenant(self, tenant_id):
        return self._get(f"tenant/{tenant_id}/details")
