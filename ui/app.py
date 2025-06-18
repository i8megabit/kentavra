from flask import Flask, render_template, request, jsonify
import subprocess
from pathlib import Path
import os

ROOT = Path(__file__).resolve().parents[1]
RUN_SCRIPT = ROOT / 'kentavra' / 'run'
ENV_FILE = ROOT / 'kentavra' / 'env'

# Extract version from env file
VERSION = 'unknown'
for line in ENV_FILE.read_text().splitlines():
    if line.startswith('VERSION='):
        VERSION = line.split('=')[1].strip().strip('"')
        break

app = Flask(__name__)


def run_command(cmd):
    try:
        result = subprocess.run([str(RUN_SCRIPT), *cmd.split()],
                                cwd=ROOT,
                                stdout=subprocess.PIPE,
                                stderr=subprocess.STDOUT,
                                text=True,
                                timeout=120)
        return result.stdout, result.returncode
    except Exception as e:
        return str(e), 1


@app.route('/')
def index():
    output, _ = run_command('status')
    return render_template('index.html', output=output, version=VERSION)


@app.route('/execute', methods=['POST'])
def execute():
    cmd = request.form.get('cmd', '')
    output, code = run_command(cmd)
    return jsonify({'code': code, 'output': output})


@app.route('/version')
def version():
    return jsonify({'version': VERSION})


if __name__ == '__main__':
    port = int(os.environ.get('UI_PORT', 5000))
    app.run(host='0.0.0.0', port=port)
