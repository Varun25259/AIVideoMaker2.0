AI Video Maker — Upgraded Full Source Package
---------------------------------------------
This upgraded package contains advanced features (implemented as safe stubs for experimental parts).

Important notes:
- This package is SOURCE code. To produce a Windows .exe, use GitHub Actions (workflow included) or build locally with PyInstaller.
- Do NOT commit API keys or OAuth client_secrets.json to GitHub. Keep them local after install.
- Place a sample.mp4 file in the project root to test local generation quickly.

Build with GitHub Actions:
1) Upload all files to your GitHub repo root (or create new repo).
2) Ensure .github/workflows/windows-build.yml is present.
3) Go to Actions -> Windows Build -> Run workflow -> Download artifact -> Run exe.

Local build:
1) Install Python 3.10+, FFmpeg and add FFmpeg to PATH.
2) python -m venv venv; Activate the venv.
3) pip install -r requirements.txt
4) pyinstaller --noconfirm --clean --onefile src/main_gui.py --name AIVideoMaker
5) dist\AIVideoMaker.exe will be produced.

If you want, I can now help you upload this package to GitHub (step-by-step) and run the build, and if errors appear, paste the logs here and I'll fix them.
