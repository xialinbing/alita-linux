# Alita

**Alita** 是一个 **Linux 系统排障 AI Agent**，
采用 **人始终在回路（Human-in-the-loop）** 的设计理念，
用于 **通过对话方式辅助定位系统问题**，而不是自动化执行。

> 核心原则：
> **AI 负责思考与分析，人负责决策与执行。**

---

## ✨ 特性概览

* ✅ 原生 Shell 执行（bash），行为等同手动输入
* ✅ 4 阶段排障模型（思考 → 执行 → 分析 → 推荐）
* ✅ 命令 **必须人工确认（yes）** 才会执行
* ✅ 执行结果 **自动分析（只读）**
* ✅ 自动推荐下一步命令，但 **不会自动执行**
* ✅ 强制简体中文输出（命令除外）
* ❌ 不自动修复
* ❌ 不自动 sudo
* ❌ 不自动循环执行

---

## 🧠 4 阶段工作模型（核心设计）

```
① THINK
   AI 理解问题，推荐 1 条最优诊断命令（不执行）

② EXECUTE
   用户确认 yes → Shell 原样执行

③ ANALYZE
   AI 自动分析刚才的命令输出（只读）

④ RECOMMEND
   AI 推荐 1 条下一步诊断命令（不执行）
   等待用户再次确认
```

> ⚠️ **任何命令都不会在未确认的情况下执行**

---

## 📦 安装

### 1. 下载

```bash
curl -LO <alita-linux-v0.6.4.tar.gz>
tar -xzf alita-linux-v0.6.4.tar.gz
cd alita-linux
```

### 2.（可选）使用虚拟环境

```bash
python3 -m venv venv
source venv/bin/activate
pip install -e .
```

### 3. 启动

```bash
alita
```

---

## ⚙️ 环境变量配置（LLM）

Alita 本身不绑定具体模型，可通过兼容 Anthropic / LiteLLM 的接口使用。

```bash
export ANTHROPIC_BASE_URL=https://<your-endpoint>
export ANTHROPIC_API_KEY=sk-xxxx
export ANTHROPIC_MODEL=<model-name>
```

示例（LiteLLM）：

```bash
export ANTHROPIC_BASE_URL=https://litellm.example.com/
export ANTHROPIC_MODEL=us.anthropic.claude-sonnet-4
```

---

## 🖥 使用示例

### 例 1：CPU 使用率高

```
> cpu 使用率有点高
```

Alita 输出：

```
当前需要先确认哪些进程占用了大量 CPU。

建议执行命令:
  top -b -n 1 | head -20
是否执行？(yes/no)
```

```
> yes
```

执行完成后，Alita 会 **自动分析结果**：

```
—— 分析 ——
- PID 56030 的 Java 进程占用了约 3.4 个 CPU 核
- system CPU 偏高，可能与 GC 或线程竞争有关

—— 建议的下一步（未执行） ——
top -H -p 56030 -bn1 | head -30
是否执行这一步？(yes/no)
```

---

## 🛡️ 安全模型说明

Alita **不依赖字符白名单或命令过滤**，安全边界基于以下原则：

* 所有命令 **必须人工确认**
* 使用当前用户权限执行
* 不自动 sudo
* 不写系统、不修改配置
* 命令行为完全可见、可预期

> **如果你不愿意在 shell 里手动敲的命令，
> 也不应该在 Alita 里输入 yes。**

---

## 📁 项目结构

```
alita/
├── agent.py    # 状态机与阶段控制
├── llm.py      # LLM 调用（THINK / ANALYZE / RECOMMEND）
├── exec.py     # Shell 执行器（bash -lc）
└── main.py     # CLI 入口
```

---

## 🚧 非目标（刻意不做）

* ❌ 自动修复
* ❌ 自动 kill / restart
* ❌ 自动 sudo
* ❌ 无人值守运行
* ❌ 生产变更工具

Alita 的定位是：
**“一个始终可控的排障助手，而不是运维机器人。”**

---

## 📜 License

MIT License（或按你的实际选择）

---

## 🙋 FAQ

**Q：Alita 会不会乱跑命令？**
A：不会。所有命令都需要你输入 `yes`。

**Q：可以直接输入命令吗？**
A：可以，Alita 会询问是否执行。

**Q：分析和推荐是自动的吗？**
A：分析和推荐是自动的，执行永远不是。

---

## 🧭 适用场景

* 系统性能排查
* Java / JVM 资源问题
* Linux 进程 / 内存 / IO 分析
* 值班 / On-call 辅助排障

---

**Alita = 人控 + AI 辅助 + Shell 原生**

如果你认同这个理念，它会是一个非常可靠的工具。
