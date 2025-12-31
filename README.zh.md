# Alita

**Alita** 是一个 **以人为核心控制（Human-in-the-loop）** 的
**Linux 系统排障 AI Agent**。

它通过对话辅助你分析系统问题，
但**任何命令的执行权始终掌握在你手中**。

> **AI 负责分析与建议，人负责判断与执行。**

---

## ✨ 特性

* 原生 Shell 执行（bash），行为等同手动输入
* 4 阶段排障模型（思考 → 执行 → 分析 → 推荐）
* 所有命令必须人工确认（`yes`）
* 命令执行后自动分析结果（只读）
* 自动推荐下一步命令，但不会自动执行
* 强制简体中文输出（命令除外）

**刻意不做的事情：**

* ❌ 自动修复
* ❌ 自动 sudo
* ❌ 自动循环执行
* ❌ 无人值守运行

---

## 🧠 4 阶段工作模型（核心设计）

```
① THINK（思考）
   AI 理解问题，推荐 1 条最优诊断命令（不执行）

② EXECUTE（执行）
   用户确认 yes → Shell 原样执行

③ ANALYZE（分析）
   AI 自动解读命令输出（只读）

④ RECOMMEND（推荐）
   AI 推荐 1 条下一步诊断命令（不执行）
```

> ⚠️ **任何命令都不会在未确认的情况下执行**

---

## 📦 安装（Git 仓库方式）

```bash
git clone https://github.com/<your-org>/alita.git
cd alita
python3 -m venv venv
source venv/bin/activate
pip install -e .
```

启动：

```bash
alita
```

---

## ⚙️ LLM 环境变量配置

Alita 不绑定具体模型，支持 Anthropic / LiteLLM 风格接口。

```bash
export ANTHROPIC_BASE_URL=https://<你的接口地址>
export ANTHROPIC_API_KEY=sk-xxxx
export ANTHROPIC_MODEL=<模型名>
```

---

## 🖥 使用示例

```
> cpu 使用率有点高
```

Alita：

```
建议执行命令:
  top -b -n 1 | head -20
是否执行？(yes/no)
```

```
> yes
```

执行完成后，Alita 会自动分析结果：

```
—— 分析 ——
- Java 进程占用了多个 CPU 核心
- system CPU 偏高，可能与 GC 或线程竞争有关

—— 建议的下一步（未执行） ——
top -H -p <pid> -bn1 | head -30
是否执行这一步？(yes/no)
```

---

## 🛡️ 安全模型说明

Alita **不依赖字符白名单或命令过滤**。

安全边界来自：

* 人工确认（yes）
* 当前用户权限
* 不自动 sudo
* 不写系统、不修改配置

> **如果你不愿意在 shell 里手动敲的命令，也不应该在 Alita 中确认。**

---

## 📁 项目结构

```
alita/
├── agent.py   # 状态机与 4 阶段流程控制
├── llm.py     # LLM 调用（思考 / 分析 / 推荐）
├── exec.py    # Shell 执行器（bash -lc）
└── main.py    # CLI 入口
```

---

## 🧭 适用场景

* Linux 系统性能排查
* CPU / 内存 / IO 异常定位
* Java / JVM 资源问题分析
* 值班 / On-call 排障辅助

---

**Alita = 人控执行 + AI 分析 + 原生 Shell**

