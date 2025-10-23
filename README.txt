
RefutingPaulianity Contact App - Ready to Deploy
-----------------------------------------------

What this package contains:
- app.py                : Flask backend (receives submissions, stores to SQLite, and emails to you)
- config.py             : Optional local config (place your Gmail app password here for local testing)
- templates/refutingpaulianity.html : Your website HTML (modified so the contact form submits to the backend)
- requirements.txt      : Python packages
- run_server.sh/.bat    : Helper scripts to run locally
- README.txt            : this file

------------ QUICK LOCAL RUN (Windows / Mac / Linux) ------------
1) Make sure you have Python 3.8+ installed.
2) Open a terminal and go to the project folder.
3) (Optional but recommended) Create a virtual environment:
   python -m venv venv
   On mac/linux: source venv/bin/activate
   On windows: venv\Scripts\activate
4) Install requirements:
   pip install -r requirements.txt
5) (OPTION A: Use environment variables) Set environment variables before running:
   - EMAIL_USER = daawahgurl@gmail.com
   - EMAIL_PASS = <your 16-character Gmail App Password>
   Example (mac/linux):
       export EMAIL_USER="daawahgurl@gmail.com"
       export EMAIL_PASS="your_app_password_here"
   Example (Windows PowerShell):
       $env:EMAIL_USER = "daawahgurl@gmail.com"
       $env:EMAIL_PASS = "your_app_password_here"

   (OPTION B: Or put credentials into config.py for local testing - not recommended for public use)
6) Run the server:
   python app.py
7) Open your browser at: http://127.0.0.1:5000/
8) Submit a question. Then visit: http://127.0.0.1:5000/admin/questions to view saved items.

------------ DEPLOY TO RENDER.COM ------------
1) Create a new Git repo from this folder (recommended) or upload the ZIP to Render.
2) Create a new Web Service on Render and connect your repo (or upload ZIP).
3) In Render, set these Environment Variables (in your service settings):
   - EMAIL_USER = daawahgurl@gmail.com
   - EMAIL_PASS = <your 16-character Gmail App Password>
4) Build Command: pip install -r requirements.txt
   Start Command: gunicorn app:app
5) Deploy. Render will run the app and expose it publicly.
6) Your admin view will be at: https://<your-render-url>/admin/questions

------------ NOTES & SECURITY ------------
- This demo stores submissions in a SQLite file named 'questions.db' in the project folder.
- The admin page (/admin/questions) is NOT protected by a password in this demo. Before making the site public, secure it with HTTP basic auth, a login, or similar.
- Use environment variables for EMAIL_USER and EMAIL_PASS; never commit real passwords into public repos.
- Gmail: you must enable 2-Step Verification and create an 'App Password' in your Google account. Do NOT use your regular Gmail password.
- If you get SMTP errors on Render, double-check EMAIL_PASS and that your Gmail account allows SMTP via app passwords.

------------ HELP ------------
If you want, I can also push this to a GitHub repo for you or provide step-by-step Render deployment commands.
