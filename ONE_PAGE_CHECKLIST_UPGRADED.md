ONE-PAGE CHECKLIST — Upgraded Build & Run

1) Download and extract package to a folder (e.g., C:\AIVideoMakerUpgraded).
2) Option A - GitHub Actions (recommended):
   - Create a GitHub repo and upload all files (do NOT upload keys).
   - Actions -> Windows Build -> Run workflow -> Download artifact when complete.
3) Option B - Local build:
   - Install Python 3.10+, FFmpeg (PATH), and create a venv.
   - pip install -r requirements.txt
   - pyinstaller --onefile src\main_gui.py --name AIVideoMaker
   - Run dist\AIVideoMaker.exe and provide API keys in Setup tab.
4) Place sample.mp4 in project root for quick testing.
5) For YouTube upload: create OAuth credentials (Desktop app) in Google Cloud Console and place client_secrets.json in app folder after installation.
