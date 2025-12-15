from flask import Flask, request, jsonify, render_template
import requests
from googletrans import Translator

app = Flask(__name__)

# -------------------------
# ✅ MICROSOFT TRANSLATOR
# -------------------------
MS_KEY = "79mDUFzRpPiRvHuThcQuKu5fE8pvmzkBxstRNU3pSumK3DRN6jjTJQQJ99BLACGhslBXJ3w3AAAbACOGmxBT"
MS_REGION = "centralindia"
MS_ENDPOINT = "https://api.cognitive.microsofttranslator.com/translate"

# -------------------------
# ✅ GOOGLETRANSLATE (FREE)
# -------------------------
google_translator = Translator()

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/translate", methods=["POST"])
def translate():
    data = request.get_json()
    text = data.get("text", "").strip()
    source = data.get("source", "auto")
    target = data.get("target")

    # ✅ Fallback for unsupported Chhattisgarhi
    if source == "hne":
        source = "hi"
    if target == "hne":
        target = "hi"

    # -------------------------
    # ✅ TRY MICROSOFT FIRST
    # -------------------------
    try:
        params = {
            "api-version": "3.0",
            "to": target
        }

        if source != "auto":
            params["from"] = source

        headers = {
            "Ocp-Apim-Subscription-Key": MS_KEY,
            "Ocp-Apim-Subscription-Region": MS_REGION,
            "Content-Type": "application/json"
        }

        body = [{"text": text}]

        response = requests.post(MS_ENDPOINT, params=params, headers=headers, json=body)
        result = response.json()

        if response.status_code == 200:
            translated = result[0]["translations"][0]["text"]
            return jsonify({"translation": translated, "engine": "microsoft"})
    except:
        pass

    # -------------------------
    # ✅ FALLBACK TO FREE GOOGLE TRANSLATE
    # -------------------------
    try:
        google_result = google_translator.translate(text, src=source if source != "auto" else None, dest=target)
        return jsonify({
            "translation": google_result.text,
            "engine": "google-free"
        })
    except Exception as e:
        return jsonify({"error": "Both Microsoft and Google failed: " + str(e)})

if __name__ == "__main__":
    app.run(debug=True)