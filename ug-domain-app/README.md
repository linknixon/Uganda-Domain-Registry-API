# UG Domain Manager (Flask + Python)

A minimal Flask web app that integrates with the **UG ccTLD Registry API** (`https://new.registry.co.ug/api/v2`) to:
- Check availability
- WHOIS lookup
- Register / Renew
- Modify (contacts & nameservers via JSON)
- Request & Confirm transfer
- Lock / Unlock

---

## 1) Prerequisites
- Python 3.9+
- Internet access to reach the Registry API
- An active **API key** from your registrar dashboard

---

## 2) Create and activate a Python virtual environment

### macOS / Linux
```bash
cd ug-domain-app
python3 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
```

### Windows (PowerShell)
```powershell
cd ug-domain-app
py -3 -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
```

> To deactivate later: `deactivate`

---

## 3) Install dependencies
```bash
pip install -r requirements.txt
```

---

## 4) Configure environment
Copy `.env.example` to `.env` and set your real values:
```
REGISTRY_API_KEY=your_real_api_key_here
FLASK_SECRET_KEY=dev-secret-change-me
PORT=5000
```

> **Never commit** your real `.env` to git.

---

## 5) Run the app (development)
Two options:

**A. Using Flask CLI**
```bash
export FLASK_APP=app.py            # Windows PowerShell: $env:FLASK_APP="app.py"
export FLASK_ENV=development       # Windows PowerShell: $env:FLASK_ENV="development"
flask run                          # default http://127.0.0.1:5000
```

**B. Using Python**
```bash
python app.py
```

App will start at `http://127.0.0.1:${PORT}` (default 5000).

---

## 6) Use the UI
Open the homepage and use the forms to:
- Check availability (comma-separated list)
- WHOIS
- Register / Renew (period in years)
- Modify (paste contacts and nameservers JSON)
- Transfer (request + confirm)
- Lock / Unlock

### Example JSON for Modify
**Contacts**:
```json
{
  "registrant": {
    "firstname": "John",
    "email": "john@example.com",
    "organization": "Example Org",
    "country": "UG",
    "city": "Kampala",
    "street_address": "Plot 123",
    "phone": "0771234567",
    "postal_code": "256",
    "fax": ""
  },
  "admin": {
    "firstname": "Jane",
    "lastname": "Doe",
    "email": "admin@example.com",
    "organization": "Example Org",
    "country": "UG",
    "city": "Kampala",
    "street_address": "Plot 123",
    "phone": "0771234567",
    "postal_code": "256",
    "fax": ""
  },
  "billing": { "firstname": "Jane", "lastname": "Doe", "email": "billing@example.com", "organization": "Example Org", "country": "UG", "city": "Kampala", "street_address": "Plot 123", "phone": "0771234567", "postal_code": "256", "fax": "" },
  "tech": { "firstname": "Jane", "lastname": "Doe", "email": "tech@example.com", "organization": "Example Org", "country": "UG", "city": "Kampala", "street_address": "Plot 123", "phone": "0771234567", "postal_code": "256", "fax": "" }
}
```

**Nameservers**:
```json
{
  "ns1": { "name": "ns1.example.com", "ip": "192.0.2.1" },
  "ns2": { "name": "ns2.example.com", "ip": "192.0.2.2" }
}
```

---

## 7) Troubleshooting
- **401 Unauthorized**: Check `REGISTRY_API_KEY` and that you’re hitting the correct environment.
- **4XX errors**: Validate required fields per endpoint. Ensure JSON structure matches the registry spec.
- **Timeouts**: Network/firewall issues, or API is slow. You can increase `timeout` in `registry_client.py` constructor.
- **GET with JSON body**: This client sends JSON in the body for the GET endpoints as indicated by the provided docs.

---

## 8) Production notes (brief)
- Run behind Gunicorn + Nginx or a PaaS.
- Set `DEBUG=False` and a strong `FLASK_SECRET_KEY`.
- Add validation, logging, and auth if exposing to end users.
