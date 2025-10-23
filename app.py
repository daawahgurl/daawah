from flask import Flask, render_template, request, jsonify, send_from_directory
import sqlite3
from datetime import datetime
import os
import smtplib
from email.message import EmailMessage

# --- Configuration ---
# The app will read email credentials from environment variables:
#   EMAIL_USER  -> your Gmail address (example: daawahgurl@gmail.com)
#   EMAIL_PASS  -> your Gmail App Password (16 chars)
# For local convenience you can also put values in config.py (see README).
try:
    import config as _cfg  # optional local config file (not required)
except Exception:
    _cfg = None

EMAIL_USER = os.environ.get("EMAIL_USER") or (getattr(_cfg, "EMAIL_USER", None) if _cfg else None)
EMAIL_PASS = os.environ.get("EMAIL_PASS") or (getattr(_cfg, "EMAIL_PASS", None) if _cfg else None)

DB_PATH = os.path.join(os.path.dirname(__file__), "questions.db")

app = Flask(__name__, static_folder='static', template_folder='templates')

def init_db():
    with sqlite3.connect(DB_PATH) as conn:
        conn.execute(\"\"\"
            CREATE TABLE IF NOT EXISTS questions (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                question TEXT NOT NULL,
                email TEXT,
                submitted_at TEXT NOT NULL
            )
        \"\"\")
    print("Database initialized:", DB_PATH)

@app.route("/")
def home():
    return render_template("refutingpaulianity.html")

@app.route("/submit_question", methods=["POST"])
def submit_question():
    data = request.get_json(force=True)
    question = (data.get("question") or "").strip()
    email = (data.get("email") or "").strip() or None

    if not question:
        return jsonify({"message": "Please type a question before submitting."}), 400

    submitted_at = datetime.utcnow().isoformat()

    with sqlite3.connect(DB_PATH) as conn:
        conn.execute(
            "INSERT INTO questions (question, email, submitted_at) VALUES (?, ?, ?)",
            (question, email, submitted_at)
        )

    # Send an email copy if credentials available
    if EMAIL_USER and EMAIL_PASS:
        try:
            send_email_to_owner(question, email)
        except Exception as e:
            # don't expose SMTP errors to the user; log and continue
            print("Warning: failed to send email:", e)

    return jsonify({"message": "✅ Thank you! Your question has been saved and emailed."})

@app.route("/admin/questions")
def admin_questions():
    # Note: This endpoint is not password-protected in this demo.
    # When you publish this site, you MUST protect it (basic auth or admin login).
    with sqlite3.connect(DB_PATH) as conn:
        rows = conn.execute("SELECT id, question, email, submitted_at FROM questions ORDER BY submitted_at DESC").fetchall()

    html = ["<html><head><meta charset='utf-8'><title>Submitted Questions</title></head><body>"]
    html.append("<h2>Submitted Questions</h2>")
    html.append("<p><em>Tip: protect this page before making the site public.</em></p>")
    html.append("<table border='1' cellpadding='8' cellspacing='0'>")
    html.append("<tr><th>ID</th><th>Submitted At (UTC)</th><th>Email (if provided)</th><th>Question</th></tr>")
    for qid, question, email, ts in rows:
        safe_q = (question.replace('<','&lt;').replace('>','&gt;'))
        safe_e = (email or '—').replace('<','&lt;').replace('>','&gt;')
        html.append(f"<tr><td>{qid}</td><td>{ts}</td><td>{safe_e}</td><td>{safe_q}</td></tr>")
    html.append("</table>")
    html.append("</body></html>")
    return "\\n".join(html)

def send_email_to_owner(question, sender_email):
    owner = EMAIL_USER
    msg = EmailMessage()
    msg["Subject"] = "New Question from Website"
    msg["From"] = owner
    msg["To"] = owner
    body = f"New question submitted on your site:\\n\\nQuestion:\\n{question}\\n\\nSender email: {sender_email or 'Not provided'}\\n\\nTime (UTC): {datetime.utcnow().isoformat()}"
    msg.set_content(body)

    # Gmail SMTP (SSL)
    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as smtp:
        smtp.login(EMAIL_USER, EMAIL_PASS)
        smtp.send_message(msg)

if __name__ == "__main__":
    init_db()
    # In production (Render) you'll use a different start command (see README).
    app.run(host="0.0.0.0", port=5000, debug=True)
