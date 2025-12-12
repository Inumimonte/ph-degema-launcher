import streamlit as st
import requests, zipfile, io, os, runpy, sys, tempfile

# CONFIG: Set your real repo details
GITHUB_USER = "Inumimonte"
GITHUB_REPO = "ph-degema-dashboard"
BRANCH = "main"

ZIP_URL = f"https://github.com/{GITHUB_USER}/{GITHUB_REPO}/archive/refs/heads/{BRANCH}.zip"

st.title("Loading Dashboard…")
st.info("Fetching the full application from GitHub. Please wait...")

# Step 1: Download the zip file
try:
    r = requests.get(ZIP_URL, timeout=60)
    r.raise_for_status()
except Exception as e:
    st.error(f"Failed to download repository ZIP: {e}")
    st.stop()

# Step 2: Extract ZIP into a temporary folder
tmp_dir = tempfile.mkdtemp()
try:
    z = zipfile.ZipFile(io.BytesIO(r.content))
    z.extractall(tmp_dir)
except Exception as e:
    st.error(f"Failed to extract ZIP archive: {e}")
    st.stop()

# Step 3: Find the extracted folder
root_folder = None
for name in os.listdir(tmp_dir):
    path = os.path.join(tmp_dir, name)
    if os.path.isdir(path) and name.startswith(GITHUB_REPO):
        root_folder = path
        break

if root_folder is None:
    st.error("Could not find app folder inside ZIP.")
    st.stop()

# Step 4: Switch to that folder and run the REAL app.py
os.chdir(root_folder)
sys.path.insert(0, root_folder)

try:
    runpy.run_path(os.path.join(root_folder, "app.py"), run_name="__main__")
except Exception as e:
    st.error(f"Error while running real app.py: {e}")
    raise
