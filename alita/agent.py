
from alita.llm import think_cmd, analyze_output, recommend_next
from alita.exec import run_command, looks_like_command

STATE = {
    "pending_cmd": None,
    "context": ""
}

def run_agent(q: str) -> str:
    q = q.strip()
    if not q:
        return ""

    if STATE["pending_cmd"]:
        if q.lower() in ("yes","y"):
            cmd = STATE["pending_cmd"]
            STATE["pending_cmd"] = None
            out = run_command(cmd)
            STATE["context"] += f"\n$ {cmd}\n{out}"

            try:
                analysis = analyze_output(out)
            except Exception as e:
                analysis = f"⚠️ 分析失败: {e}"

            try:
                next_cmd = recommend_next(STATE["context"])
            except Exception:
                next_cmd = None

            resp = out
            resp += "\n\n—— 分析 ——\n" + analysis
            if next_cmd:
                STATE["pending_cmd"] = next_cmd.strip()
                resp += (
                    "\n\n—— 建议的下一步（未执行） ——\n"
                    + next_cmd.strip()
                    + "\n是否执行这一步？(yes/no)"
                )
            return resp

        STATE["pending_cmd"] = None
        return "已取消执行。"

    if looks_like_command(q):
        STATE["pending_cmd"] = q.lstrip("!: ")
        return "检测到命令，是否执行？(yes/no)"

    chat, cmd = think_cmd(q, STATE["context"])
    out = chat or ""
    if cmd:
        STATE["pending_cmd"] = cmd
        out += (
            "\n\n建议执行命令:\n  "
            + cmd
            + "\n是否执行？(yes/no)"
        )
    return out or "（无输出）"
