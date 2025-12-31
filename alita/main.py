
from alita.agent import run_agent

def main():
    print("Alita Linux AI Agent (v0.6.4)")
    while True:
        try:
            q = input("> ")
            if q in ("exit","quit"):
                break
            print(run_agent(q))
        except Exception as e:
            print(f"⚠️ 内部错误已捕获（未退出）: {e}")
