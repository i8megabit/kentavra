import subprocess
import time
import requests
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def test_ui_version():
    proc = subprocess.Popen(['python', 'ui/app.py'], cwd=ROOT)
    time.sleep(2)
    try:
        r = requests.get('http://localhost:5000/version', timeout=5)
        assert r.status_code == 200
        assert 'version' in r.json()
    finally:
        proc.terminate()
        proc.wait()
