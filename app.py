from flask import Flask, request, jsonify
from flask_cors import CORS
import requests
from bs4 import BeautifulSoup
import time

app = Flask(__name__)
CORS(app)

BASE_URL = "https://dirbs.pta.gov.pk/drs/auth/register_individual"

@app.route("/verify", methods=["POST"])
def verify():
    data = request.json

    phones = data.get("phones", [])
    cnic = data.get("cnic")

    if not phones or not cnic:
        return jsonify({"error": "phones and cnic required"}), 400

    results = []

    for phone in phones:
        payload = {
            "purpose": "foreigners_temporary_unblocking",
            "user_type_of_individual": "local",
            "first_name": "Ali Raza",
            "phone": phone,
            "email": "bii3267c17185@gmail.com",
            "city_id": "36",
            "address": "PO 424 JB Chak 426 JB kahna Quetta Teh gujra dist TT Singh",
            "cnic_number": cnic,
            "passport_number": "LD6801861",
            "password_for_edit_profile": "TestPassword123",
            "confirm_password_for_edit_profile": "TestPassword123"
        }

        try:
            r = requests.post(
                BASE_URL,
                data=payload,
                headers={
                    "User-Agent": "Mozilla/5.0 (Linux; Android 10)",
                    "Content-Type": "application/x-www-form-urlencoded"
                },
                timeout=20
            )

            soup = BeautifulSoup(r.text, "html.parser")
            toast = soup.select_one(".toast-message")

            msg = toast.text.strip() if toast else "No message found"

            if "Provided Cell number is not issued against given CNIC" in msg:
                status = "Wrong Number ❌"
            elif "already exists in system" in msg:
                status = "Verified ✅"
            else:
                status = msg

            results.append({
                "phone": phone,
                "message": status
            })

            time.sleep(1)  # safe delay

        except Exception as e:
            results.append({
                "phone": phone,
                "error": str(e)
            })

    return jsonify(results)

if __name__ == "__main__":
    app.run()
