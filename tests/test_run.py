import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def run_cmd(cmd):
    result = subprocess.run(cmd, cwd=ROOT, shell=True, text=True,
                            stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    return result.returncode, result.stdout


def test_help():
    code, out = run_cmd("go run ./cmd/kentavra/main.go help")
    assert code == 0
    assert "Usage" in out


def test_version():
    code, out = run_cmd("go run ./cmd/kentavra/main.go version")
    assert code == 0
    assert "Kentavra version" in out


def test_env_format():
    env_path = ROOT / "kentavra" / "env"
    content = env_path.read_text()
    assert not content.rstrip().endswith("root")
    assert content.endswith("\n")
