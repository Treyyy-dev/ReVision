"""Push firebase/database.rules.json to the live Realtime Database.

Runs in GitHub Actions with the FIREBASE_SERVICE_ACCOUNT secret (the JSON key from
Firebase console > Project settings > Service accounts > Generate new private key).
"""
import json, os, sys
import requests
from google.oauth2 import service_account
from google.auth.transport.requests import Request

DB_URL = "https://revision-7914f-default-rtdb.firebaseio.com"
info = json.loads(os.environ["SA"])
cred = service_account.Credentials.from_service_account_info(
    info, scopes=["https://www.googleapis.com/auth/firebase.database",
                  "https://www.googleapis.com/auth/userinfo.email"])
cred.refresh(Request())
auth = {"Authorization": "Bearer " + cred.token}
body = open("firebase/database.rules.json", encoding="utf-8").read()
json.loads(body)  # fail early on a typo

r = requests.put(DB_URL + "/.settings/rules.json", data=body.encode(), headers=auth, timeout=30)
print("PUT", r.status_code, r.text[:300])
r.raise_for_status()
live = requests.get(DB_URL + "/.settings/rules.json", headers=auth, timeout=30)
ok = live.ok and json.loads(live.text) == json.loads(body)
print("Live rules match the repo:", ok)
sys.exit(0 if ok else 1)
