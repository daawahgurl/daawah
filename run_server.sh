
#!/usr/bin/env bash
# Run locally (mac / linux)
python -m venv venv -p python3 || true
source venv/bin/activate
pip install -r requirements.txt
python app.py
