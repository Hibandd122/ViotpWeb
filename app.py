from flask import Flask, request, jsonify, make_response
from flask_cors import CORS
import requests

app = Flask(__name__)
CORS(app)  # cho phép tất cả domain truy cập

# URL gốc của host bạn
TARGET_API = "http://de28.spaceify.eu:25120/predict"

@app.route("/predict", methods=["POST"])
def predict_proxy():
    try:
        # nhận JSON từ client
        data = request.get_json()
        if not data or "image" not in data:
            return jsonify({"error": "Missing 'image' in payload"}), 400

        # gửi POST tới host HTTP gốc
        r = requests.post(TARGET_API, json=data)

        # trả nguyên text về client
        response = make_response(r.text, r.status_code)
        response.headers["Content-Type"] = r.headers.get("Content-Type", "text/plain")
        return response

    except Exception as e:
        return jsonify({"error": str(e)}), 500
