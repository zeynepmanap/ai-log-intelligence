from flask import Flask, render_template, request, send_file
import requests
import json
import re
import io

app = Flask(__name__)

OLLAMA_URL = "http://localhost:11434/api/generate"
MODEL_NAME = "llama3"


# -----------------------------
# Utility Functions
# -----------------------------

def extract_json(text):
    match = re.search(r"\{.*\}", text, re.DOTALL)
    if match:
        return match.group(0)
    return None


def calculate_severity_stats(log_text):
    text = log_text.lower()
    return {
        "error": text.count("error"),
        "critical": text.count("critical"),
        "warning": text.count("warning"),
        "info": text.count("info"),
    }


def detect_security_threats(log_text):
    text = log_text.lower()
    threats = []

    if "failed login" in text:
        threats.append("Possible brute force attack")

    if "unauthorized" in text:
        threats.append("Unauthorized access attempt")

    if "sql syntax" in text or "sql injection" in text:
        threats.append("Possible SQL injection attempt")

    if "too many requests" in text:
        threats.append("Potential rate limit abuse")

    return threats


def calculate_system_risk(stats, log_text, threats):
    if stats["critical"] > 0:
        return "High"

    if len(threats) > 0:
        return "High"

    if stats["error"] >= 3:
        return "Medium"

    if stats["warning"] >= 5:
        return "Medium"

    return "Low"


def calculate_confidence(stats, threats):
    score = 40
    score += stats["error"] * 5
    score += stats["critical"] * 15
    score += len(threats) * 10
    return min(score, 100)


# -----------------------------
# AI Analysis
# -----------------------------

def analyze_with_ai(log_text):

    prompt = f"""
You are a senior DevOps and Security log analysis expert.

Return ONLY valid JSON.

JSON format:

{{
  "summary": "...",
  "root_cause": "...",
  "risk_level": "Low/Medium/High",
  "recommendations": ["...", "..."]
}}

Logs:
{log_text}
"""

    response = requests.post(
        OLLAMA_URL,
        json={
            "model": MODEL_NAME,
            "prompt": prompt,
            "stream": False
        }
    )

    data = response.json()
    ai_text = data.get("response", "")

    json_text = extract_json(ai_text)

    if json_text:
        try:
            return json.loads(json_text)
        except:
            pass

    return {
        "summary": "AI output could not be parsed.",
        "root_cause": ai_text,
        "risk_level": "Low",
        "recommendations": ["Model output not valid JSON."]
    }


# -----------------------------
# Routes
# -----------------------------

@app.route("/", methods=["GET", "POST"])
def index():

    analysis = None
    stats = None
    threats = None
    system_risk = None
    confidence = None

    if request.method == "POST":
        file = request.files.get("logfile")

        if file:
            log_text = file.read().decode("utf-8")

            stats = calculate_severity_stats(log_text)
            threats = detect_security_threats(log_text)
            system_risk = calculate_system_risk(stats, log_text, threats)
            confidence = calculate_confidence(stats, threats)

            analysis = analyze_with_ai(log_text)

    return render_template(
        "index.html",
        analysis=analysis,
        stats=stats,
        threats=threats,
        system_risk=system_risk,
        confidence=confidence
    )


@app.route("/download", methods=["POST"])
def download():
    data = request.form.get("analysis_json")
    buffer = io.BytesIO()
    buffer.write(data.encode("utf-8"))
    buffer.seek(0)
    return send_file(
        buffer,
        as_attachment=True,
        download_name="analysis.json",
        mimetype="application/json"
    )


if __name__ == "__main__":
    app.run(debug=True)
