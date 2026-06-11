---
title: "Agentic Engineering 22 条技巧 (Matt Van Horn, 2026.06)"
created: 2026-06-10
updated: 2026-06-10
type: concept
tags: [agentic-engineering, ai-coding, workflow, planning, context, multi-agent, skill-automation, voice-input, remote-work, productivity, claude-code, codex]
sources: [raw/articles/agentic-engineering-tips-2026.md]
methods: [ce-plan, ce-brainstorm, ce-work, plan-md, voice-to-llm, tmux-multi-agent, last30days, raw-transcript-input, human-signal, printing-press, skill-scaffolding]
confidence: medium
---

# Agentic Engineering 22 条技巧 — Matt Van Horn (2026.06)

> **来源：** [X/@mvanhorn](https://x.com/mvanhorn/status/2061877533885473181) | 整理：Datawhale  
> **作者背景：** last30days (2.7 万星)、PrintingPress (4k+ 星)、Python/Go/GStack/Paperclip 顶级贡献者

---

## 核心内容

22 条经验浓缩成 5 条核心原则：

| # | 原则 | 一句话 |
|---|------|--------|
| 1 | **先规划，再动手** | 有想法→`/ce-plan`→plan.md→`/ce-work`。plan 是 agent 的 leash |
| 2 | **上下文决定差距** | 截图、issue、Slack、原始会议录音、十年笔记→稳定流进 agent |
| 3 | **人往上移** | 人做调度：给信号、给判断、给品味、给取舍。Agent 提供产量 |
| 4 | **Agent 从助手变执行层** | 远程控制+邮箱入口+登录态+真实服务接口=真正干活 |
| 5 | **小心 build 成瘾** | Agent 反馈太快像打游戏，越 build 越嗨，人和关系容易丢 |

---

## 22 条技巧拆解

### 一、先规划，再动手 (01-03)

| # | 技巧 | 要点 |
|---|------|------|
| 01 | `/ce-plan` 生成 plan.md | 接 GitHub issue、截图、设计稿、Slack、脑暴图。模糊想法用 `/ce-brainstorm` 先聊清 |
| 02 | plan.md 是给 agent 看的 | "Plans are for agents, you silly human." 扫一眼标题→`/ce-work`。不懂追问 TLDR/eli5 |
| 03 | 同一条 loop 用于所有脑力工作 | 战略文档、产品 spec、竞品分析、board update |

→ 与 Hermes 的 `[[plan]]` skill 同个模式：先计划再执行。

### 二、怎么高效喂活给 agent (04-09)

| # | 技巧 | 要点 |
|---|------|------|
| 04 | **语音做主输入** | Mac: Monologue/WisprFlow。手机: Apple 自带听写。鹅颈麦常驻桌上 |
| 05 | **同时开 4-6 个 tmux** | 一个写 plan、一个 build、一个跑研究、一个修 bug。多线程调度 agent |
| 06 | 新终端默认直达 Claude Code | Ghostty launcher 脚本，打开就是 Claude Code |
| 07 | **远程控制+邮箱入口** | `remoteControlAtStartup: true`。AgentMail 收邮件→新任务入口 |
| 08 | 跳过权限确认 | `bypassPermissions` + 白名单 Bash/Read/Write/Edit |
| 09 | **Claude 管 plan，Codex 管 build** | 三种交接：IDE extension、`/ce-work --codex`、PrintingPress Codex 模式。Codex: reasoning xhigh + fast on；Claude: reasoning xhigh + fast off |

### 三、上下文决定一切 (10-15)

| # | 技巧 | 要点 |
|---|------|------|
| 10 | `/ce-plan` 前先 `/last30days` | 并行搜 Reddit/X/YouTube/HN/GitHub/Web。选库前、做 feature 前、见合伙人前 |
| 11 | **原始 transcript 直接扔进去** | 不要替模型总结。Granola 录音→raw transcript→`/ce-plan turn into proposal` |
| 12 | **人给信号 (Human Signal)** | Agent 提供产量，人提供品味。"第二版接近了""先处理最大风险""这段太长" |
| 13 | 视频也走同一条 loop | HyperFrames：HTML→script.md→agent 渲染 MP4。GIF 上传 catbox |
| 14 | **笔记做成 agent 知识库** | Bear+BearCLI / Obsidian / gbrain / supermemory。本质是 Personal RAG |
| 15 | 随时随地工作的硬件 | Mac mini+Mosh+tmux+Hermes+OpenClaw。AgentCookie 同步 cookies |

→ 14 和 15 直接关联 llm-wiki：[[obsidian-integration]]、Hermes 远程工作模式。

### 四、让 agent 走出终端 (16-20)

| # | 技巧 | 要点 |
|---|------|------|
| 16 | plan.md 给 agent，Proof 给同事 | Proof 生成链接→inline comment→评论流回 agent loop |
| 17 | **任何做两次的事写成 skill** | "Anything I do more than twice, I turn into a skill." 不从头写，先读一个跑通的 skill 再 scaffold |
| 18 | 开源贡献进同一条 loop | 找自己天天用的工具→找真实缺口→`/ce-plan+/ce-work`。PR 只是进门，Discord 里建立关系 |
| 19 | M5 Max+64GB 也扛不住 | 6 个 Claude 会话+Codex→电池撑一小时。随身 Anker、车载充电器、禁止休眠 |
| 20 | PrintingPress | 把网页手动操作包装成 CLI→agent 带登录态调用。配套 AgentCookie |

→ 17 直接关联 Hermes 的 skill 系统。20 的 "CLI 包装真实服务" 模式可迁移到 Hermes 的 tool 开发。

### 五、最后提醒 (21-22)

| # | 技巧 | 要点 |
|---|------|------|
| 21 | Agent 很容易上瘾 | "Building with agents is the greatest video game ever made." 休息+出门+和爱的人说话 |
| 22 | 这篇文章本身就这么写的 | Claude Code+Monologue 语音→agent 改写→last30days 提供材料→Proof review。只剩 Talk/Plan/Build |

---

## 核心知识点

1. **research → plan → build → review 流水线**：不是某个环节快，是全流程快
2. **上下文是核心竞争力**：能把什么喂进去，决定了 agent 能产出什么
3. **人做调度，agent 做执行**：给信号、给判断、给品味——不是代码 review，是方向 review
4. **skill 是积累资产**：做两次就写成 skill。不从头写，先读一个跑通的再 scaffold
5. **警惕 build 成瘾**：反馈越快越危险，人和关系比 code 重要

---

## 可迁移知识

| 知识 | 如何迁移到 Hermes |
|------|-------------------|
| plan→build loop | 用 [[plan]] skill：先 /plan 再执行 |
| 语音输入 | 配置语音转文字→直接喂给 Hermes |
| 多 tmux 并行 | 用 `delegate_task` 或 `terminal(background=true)` 并行跑多任务 |
| 原始 transcript 直接喂 | 不总结，把 raw text 直接给 Hermes 处理 |
| Skill 脚手架 | "look at [existing skill] and help me make one like this for [x]" |
| 上下文是核心 | 截图、链接、文件→直接贴进对话 |
| CLI 包装服务 | Hermes tool 开发：把服务 API 包装成 tool |

---

## 关联

- [[zhang2020-phylstm-analysis]] — 论文分析需要上下文（论文本身+关联论文）
- [[wang2023-pinn-spurious-analysis]] — 交叉引用提升 wiki 价值的案例
- Hermes: `plan` skill — plan→build loop 的 Hermes 实现
- Hermes: skill 系统 — "做两次写成 skill" 的落地方式
