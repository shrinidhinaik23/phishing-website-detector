from flask import Flask, request, jsonify
from backend import predict_url

app = Flask(__name__)

@app.route("/predict", methods=["POST"])
def predict():
    data = request.get_json()
    url = data.get("url", "").strip()

    if not url:
        return jsonify({"error": "URL is required"}), 400

    try:
        result = predict_url(url)

        prediction = result.get("prediction", "Suspicious")
        confidence = float(result.get("confidence", 0))
        risk_level = result.get("risk_level", "Medium")

        if prediction == "Phishing":
            status = "High Risk"
            high_risk = max(int(confidence), 75)
            suspicious = 100 - high_risk if high_risk < 90 else 15
            safe_score = max(100 - high_risk, 5)

        elif prediction == "Suspicious":
            status = "Suspicious"
            suspicious = max(int(confidence), 60)
            high_risk = max(suspicious - 25, 20)
            safe_score = max(100 - suspicious, 15)

        else:
            status = "Safe"
            safe_score = max(int(confidence), 80)
            suspicious = max(100 - safe_score - 5, 10)
            high_risk = max(100 - safe_score - suspicious, 5)

        return jsonify({
            "status": status,
            "high_risk": high_risk,
            "suspicious": suspicious,
            "safe_score": safe_score,
            "prediction": prediction,
            "confidence": confidence,
            "risk_level": risk_level
        })

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True, port=5000)