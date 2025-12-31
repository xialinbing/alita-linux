
import subprocess, re

def looks_like_command(s: str) -> bool:
    s = s.strip()
    if not s:
        return False
    if s.startswith(("! ", ": ")):
        return True
    if re.search(r"[\u4e00-\u9fff]", s):
        return False
    return True

def run_command(cmd: str) -> str:
    try:
        p = subprocess.run(
            ["bash", "-lc", cmd],
            capture_output=True,
            text=True,
            timeout=30
        )
        return (p.stdout + p.stderr).strip()
    except Exception as e:
        return f"⚠️ 命令执行失败: {e}"
