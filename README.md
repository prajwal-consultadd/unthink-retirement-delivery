python3 -m venv .venv
source .venv/bin/activate

pip install -r requirements.txt

python app.py
python -m clay.sync_google_sheet_to_potential_users
python -m documents.get_potential_linkedin_users
