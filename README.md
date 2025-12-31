# Alita

**Alita** is a **human-in-the-loop Linux troubleshooting AI agent**.

It helps operators diagnose system issues through conversation,
while **keeping all execution decisions strictly under human control**.

> **AI analyzes and suggests. Humans decide and execute.**

---

## ✨ Features

* Native shell execution (`bash`)
* 4-phase troubleshooting workflow
* All commands require explicit confirmation (`yes`)
* Automatic analysis of command output (read-only)
* One-step command recommendation (never auto-executed)
* Designed for safety, transparency, and predictability

**Explicitly NOT a goal:**

* ❌ Auto-fix
* ❌ Auto-sudo
* ❌ Unattended execution
* ❌ Self-healing automation

---

## 🧠 4-Phase Workflow

```
1. THINK
   AI proposes ONE best diagnostic command (not executed)

2. EXECUTE
   Human confirms → command runs in shell

3. ANALYZE
   AI automatically explains the output (read-only)

4. RECOMMEND
   AI suggests ONE next command (not executed)
```

> Commands are never executed without explicit human approval.

---

## 📦 Installation (Git Repository)

```bash
git clone https://github.com/<your-org>/alita.git
cd alita
python3 -m venv venv
source venv/bin/activate
pip install -e .
```

Run:

```bash
alita
```

---

## ⚙️ LLM Configuration

Alita is model-agnostic and works with Anthropic-compatible APIs (including LiteLLM).

```bash
export ANTHROPIC_BASE_URL=https://<endpoint>
export ANTHROPIC_API_KEY=sk-xxxx
export ANTHROPIC_MODEL=<model-name>
```

---

## 🛡️ Safety Model

Alita does **not** rely on command filtering or allowlists.

Safety is achieved through:

* Explicit human confirmation
* Transparent shell execution
* Current user permissions
* No automatic privilege escalation

> If you would not type a command yourself, you should not confirm it in Alita.

---

## 📁 Project Structure

```
alita/
├── agent.py   # State machine & workflow control
├── llm.py     # THINK / ANALYZE / RECOMMEND logic
├── exec.py    # Shell executor (bash -lc)
└── main.py    # CLI entry point
```

---

## 🎯 Use Cases

* Linux performance troubleshooting
* CPU / memory / IO diagnostics
* JVM / Java process analysis
* On-call and incident response

---

**Alita = Human Control + AI Insight + Native Shell**

