import requests
from typing import List, Dict, Any, Optional

class UgDomainRegistryClient:
    """
    UG ccTLD Registry API Client
    Base URL: https://new.registry.co.ug/api/v2
    """

    def __init__(self, api_key: Optional[str] = None, base_url: str = "https://new.registry.co.ug/api/v2", timeout: int = 30):
        self.api_key = api_key
        self.base_url = base_url.rstrip("/")
        self.timeout = timeout

    def _headers(self, auth_required: bool = True) -> Dict[str, str]:
        headers = {"Content-Type": "application/json"}
        if auth_required:
            if not self.api_key:
                raise ValueError("API key is required for this operation. Set REGISTRY_API_KEY in your .env or pass api_key to the client.")
            headers["Authorization"] = f"Bearer {self.api_key}"
        return headers

    def _get(self, path: str, json_body: Optional[Dict[str, Any]] = None, auth_required: bool = False) -> Dict[str, Any]:
        url = f"{self.base_url}{path}"
        resp = requests.get(url, json=json_body, headers=self._headers(auth_required), timeout=self.timeout)
        return self._handle_response(resp)

    def _post(self, path: str, payload: Dict[str, Any], auth_required: bool = True) -> Dict[str, Any]:
        url = f"{self.base_url}{path}"
        resp = requests.post(url, json=payload, headers=self._headers(auth_required), timeout=self.timeout)
        return self._handle_response(resp)

    @staticmethod
    def _handle_response(resp: requests.Response) -> Dict[str, Any]:
        try:
            data = resp.json()
        except ValueError:
            resp.raise_for_status()
            return {"status": "error", "message": resp.text}

        if not resp.ok:
            message = data if isinstance(data, dict) else {"message": str(data)}
            raise requests.HTTPError(f"HTTP {resp.status_code}: {message}", response=resp)
        return data

    def check_availability(self, domains: List[str]) -> Dict[str, Any]:
        payload = {"domains": [{"name": d} for d in domains]}
        return self._get("/domains/check-availability", json_body=payload, auth_required=False)

    def whois(self, domain: str) -> Dict[str, Any]:
        payload = {"domain_name": domain}
        return self._get("/domains/whois", json_body=payload, auth_required=False)

    def register_domain(self, domain: str, period: int) -> Dict[str, Any]:
        payload = {"domain_name": domain, "period": int(period)}
        return self._post("/domains/register", payload, auth_required=True)

    def modify_domain(self, domain: str, contacts: Dict[str, Any], nameservers: Dict[str, Any]) -> Dict[str, Any]:
        payload = {"domain_name": domain, "contacts": contacts, "nameservers": nameservers}
        return self._post("/domains/modify", payload, auth_required=True)

    def renew_domain(self, domain: str, period: int) -> Dict[str, Any]:
        payload = {"domain_name": domain, "period": int(period)}
        return self._post("/domains/renew", payload, auth_required=True)

    def request_transfer(self, domain: str) -> Dict[str, Any]:
        payload = {"domain_name": domain}
        return self._post("/domains/request-transfer", payload, auth_required=True)

    def confirm_transfer(self, domain: str, transfer_id: int) -> Dict[str, Any]:
        payload = {"domain_name": domain, "transfer_id": int(transfer_id)}
        return self._post("/domains/confirm-transfer", payload, auth_required=True)

    def lock_domain(self, domain: str) -> Dict[str, Any]:
        payload = {"domain_name": domain}
        return self._post("/domains/lock", payload, auth_required=True)

    def unlock_domain(self, domain: str) -> Dict[str, Any]:
        payload = {"domain_name": domain}
        return self._post("/domains/unlock", payload, auth_required=True)
