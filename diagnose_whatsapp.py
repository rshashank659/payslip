# diagnose_whatsapp.py
import os
import requests
from dotenv import load_dotenv

load_dotenv()

PHONE_NUMBER_ID = os.getenv("WA_PHONE_NUMBER_ID")
ACCESS_TOKEN    = os.getenv("WA_ACCESS_TOKEN")
TEST_PHONE      = "919632212016"  # GAGAN H's number with country code

print("="*60)
print("WHATSAPP DIAGNOSTICS")
print("="*60)
print(f"Phone Number ID : {PHONE_NUMBER_ID}")
print(f"Token (first 20): {ACCESS_TOKEN[:20] if ACCESS_TOKEN else 'MISSING'}...")
print()

headers = {
    "Authorization": f"Bearer {ACCESS_TOKEN}",
    "Content-Type": "application/json"
}

# ── TEST 1: Token valid? ──
print("TEST 1: Checking token...")
r = requests.get(
    f"https://graph.facebook.com/v19.0/{PHONE_NUMBER_ID}",
    headers=headers
)
print(f"  Status: {r.status_code}")
print(f"  Response: {r.json()}")
print()

# ── TEST 2: Phone number registered? ──
print("TEST 2: Checking phone number status...")
r = requests.get(
    f"https://graph.facebook.com/v19.0/{PHONE_NUMBER_ID}?fields=display_phone_number,verified_name,status,quality_rating",
    headers=headers
)
data = r.json()
print(f"  Status: {r.status_code}")
print(f"  Phone: {data.get('display_phone_number')}")
print(f"  Name: {data.get('verified_name')}")
print(f"  Status: {data.get('status')}")
print(f"  Quality: {data.get('quality_rating')}")
print()

# ── TEST 3: Template exists and approved? ──
print("TEST 3: Checking template status...")
WABA_ID = os.getenv("WA_BUSINESS_ACCOUNT_ID")
r = requests.get(
    f"https://graph.facebook.com/v19.0/{WABA_ID}/message_templates?name=payslip_notification",
    headers=headers
)
print(f"  Status: {r.status_code}")
data = r.json()
if "data" in data and data["data"]:
    t = data["data"][0]
    print(f"  Template name: {t.get('name')}")
    print(f"  Template status: {t.get('status')}")
    print(f"  Category: {t.get('category')}")
else:
    print(f"  Response: {data}")
print()

# ── TEST 4: Send a plain text message (no PDF) ──
print("TEST 4: Sending plain template message (no PDF)...")
payload = {
    "messaging_product": "whatsapp",
    "to": TEST_PHONE,
    "type": "template",
    "template": {
        "name": "payslip_notification",
        "language": {"code": "en"},
        "components": [
            {
                "type": "body",
                "parameters": [
                    {"type": "text", "text": "Test Employee"},
                    {"type": "text", "text": "March 2026"}
                ]
            }
        ]
    }
}
r = requests.post(
    f"https://graph.facebook.com/v19.0/{PHONE_NUMBER_ID}/messages",
    headers=headers,
    json=payload
)
print(f"  Status: {r.status_code}")
print(f"  Response: {r.json()}")
print()

print("="*60)
print("Share this output to diagnose the issue")
print("="*60)