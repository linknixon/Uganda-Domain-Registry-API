import os
from flask import Flask, render_template, request, redirect, url_for, flash
from dotenv import load_dotenv
from registry_client import UgDomainRegistryClient

load_dotenv()
API_KEY = os.getenv("REGISTRY_API_KEY")

app = Flask(__name__)
app.secret_key = os.getenv("FLASK_SECRET_KEY", "dev-secret")  # replace in production

client = UgDomainRegistryClient(api_key=API_KEY)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/check", methods=["POST"])
def check_domain():
    domains_raw = request.form.get("domains", "").strip()
    if not domains_raw:
        flash("Please enter at least one domain.")
        return redirect(url_for("index"))
    domains = [d.strip() for d in domains_raw.split(",") if d.strip()]
    try:
        result = client.check_availability(domains)
    except Exception as e:
        flash(str(e))
        return redirect(url_for("index"))
    return render_template("result.html", title="Domain Availability", result=result)

@app.route("/whois", methods=["POST"])
def whois_domain():
    domain = request.form.get("domain")
    if not domain:
        flash("Please enter a domain name.")
        return redirect(url_for("index"))
    try:
        result = client.whois(domain)
    except Exception as e:
        flash(str(e))
        return redirect(url_for("index"))
    return render_template("whois.html", title="WHOIS Lookup", result=result)

@app.route("/register", methods=["POST"])
def register_domain():
    domain = request.form.get("domain")
    period = request.form.get("period", 1)
    if not domain:
        flash("Domain is required.")
        return redirect(url_for("index"))
    try:
        result = client.register_domain(domain, int(period))
    except Exception as e:
        flash(str(e))
        return redirect(url_for("index"))
    return render_template("result.html", title="Domain Registration", result=result)

@app.route("/renew", methods=["POST"])
def renew_domain():
    domain = request.form.get("domain")
    period = request.form.get("period", 1)
    if not domain:
        flash("Domain is required.")
        return redirect(url_for("index"))
    try:
        result = client.renew_domain(domain, int(period))
    except Exception as e:
        flash(str(e))
        return redirect(url_for("index"))
    return render_template("result.html", title="Domain Renewal", result=result)

@app.route("/modify", methods=["POST"])
def modify_domain():
    domain = request.form.get("domain")
    contacts_json = request.form.get("contacts_json") or "{}"
    nameservers_json = request.form.get("nameservers_json") or "{}"
    if not domain:
        flash("Domain is required.")
        return redirect(url_for("index"))
    try:
        import json
        contacts = json.loads(contacts_json)
        nameservers = json.loads(nameservers_json)
    except Exception as e:
        flash(f"Invalid JSON: {e}")
        return redirect(url_for("index"))
    try:
        result = client.modify_domain(domain, contacts, nameservers)
    except Exception as e:
        flash(str(e))
        return redirect(url_for("index"))
    return render_template("result.html", title="Modify Domain", result=result)

@app.route("/request-transfer", methods=["POST"])
def request_transfer():
    domain = request.form.get("domain")
    if not domain:
        flash("Domain is required.")
        return redirect(url_for("index"))
    try:
        result = client.request_transfer(domain)
    except Exception as e:
        flash(str(e))
        return redirect(url_for("index"))
    return render_template("result.html", title="Request Domain Transfer", result=result)

@app.route("/confirm-transfer", methods=["POST"])
def confirm_transfer():
    domain = request.form.get("domain")
    transfer_id = request.form.get("transfer_id")
    if not domain or not transfer_id:
        flash("Domain and Transfer ID are required.")
        return redirect(url_for("index"))
    try:
        result = client.confirm_transfer(domain, int(transfer_id))
    except Exception as e:
        flash(str(e))
        return redirect(url_for("index"))
    return render_template("result.html", title="Confirm Domain Transfer", result=result)

@app.route("/lock", methods=["POST"])
def lock_domain():
    domain = request.form.get("domain")
    if not domain:
        flash("Domain is required.")
        return redirect(url_for("index"))
    try:
        result = client.lock_domain(domain)
    except Exception as e:
        flash(str(e))
        return redirect(url_for("index"))
    return render_template("result.html", title="Lock Domain", result=result)

@app.route("/unlock", methods=["POST"])
def unlock_domain():
    domain = request.form.get("domain")
    if not domain:
        flash("Domain is required.")
        return redirect(url_for("index"))
    try:
        result = client.unlock_domain(domain)
    except Exception as e:
        flash(str(e))
        return redirect(url_for("index"))
    return render_template("result.html", title="Unlock Domain", result=result)

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=int(os.getenv("PORT", 5000)))
