"""Push firebase/database.rules.json to the live Realtime Database.

Runs in GitHub Actions with the FIREBASE_SERVICE_ACCOUNT secret (the JSON key from
Firebase console > Project settings > Service accounts > Generate new private key).
Errors are reported as ::error:: annotations (never including the key itself).
"""
import json, os, sys

DB_URL = "https://revision-7914f-default-rtdb.firebaseio.com"


def fail(msg):
    print("::error title=Rules deploy::" + msg.replace("\n", " ")[:400])
    sys.exit(1)


raw = os.environ.get("SA", "").strip()
try:
    info = json.loads(raw)
except Exception as e:
    fail(f"The FIREBASE_SERVICE_ACCOUNT secret is not valid JSON ({type(e).__name__} at char "
         f"{getattr(e, 'pos', '?')} of {len(raw)}; starts with {raw[:1]!r}, ends with {raw[-1:]!r}). "
         "Paste the whole .json key file, from { to }.")
if not isinstance(info, dict) or info.get("type") != "service_account":
    fail("The secret is JSON but not a service account key (missing \"type\": \"service_account\").")
missing = [k for k in ("private_key", "client_email", "project_id") if not info.get(k)]
if missing:
    fail("The key file is missing: " + ", ".join(missing))
if info.get("project_id") != "revision-7914f":
    print(f"::warning::Key is for project {info.get('project_id')!r}, expected 'revision-7914f'.")

try:
    import requests
    from google.oauth2 import service_account
    from google.auth.transport.requests import Request
    cred = service_account.Credentials.from_service_account_info(
        info, scopes=["https://www.googleapis.com/auth/firebase.database",
                      "https://www.googleapis.com/auth/userinfo.email"])
    cred.refresh(Request())
except Exception as e:
    fail(f"Google sign-in with the key failed: {type(e).__name__}: {e}")

auth = {"Authorization": "Bearer " + cred.token}
body = open("firebase/database.rules.json", encoding="utf-8").read()
try:
    json.loads(body)
except Exception as e:
    fail(f"firebase/database.rules.json is not valid JSON: {e}")

r = requests.put(DB_URL + "/.settings/rules.json", data=body.encode(), headers=auth, timeout=30)
print("PUT", r.status_code)
if not r.ok:
    fail(f"Firebase refused the rules (HTTP {r.status_code}): {r.text[:250]}")
live = requests.get(DB_URL + "/.settings/rules.json", headers=auth, timeout=30)
ok = live.ok and json.loads(live.text) == json.loads(body)
print(("::notice title=Rules deploy::Rules are live." if ok else "::error title=Rules deploy::Rules were sent but the live copy doesn't match."))
sys.exit(0 if ok else 1)
