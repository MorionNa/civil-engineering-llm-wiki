# 📚 Senna's LLM Research Wiki

> 一个以物理信息机器学习（Physics-Informed ML）、物理仿真和 AI 工程为核心的公开知识库。基于 [Andrej Karpathy 的 LLM Wiki 模式](https://gist.github.com/karpathy/442a6bf555914893e9891c11519de94f)，由 Hermes Agent 协助构建。

## 📂 知识库结构

| 目录 | 内容 | 说明 |
|------|------|------|
| `raw/` | 原始来源 | 论文全文、公众号推文 OCR、视频转录 |
| `papers/` | 论文分析 | 通读论文全文后的深度拆解（12 维度 1+3 结构） |
| `entities/` | 实体定义 | 方法名、数据集、模型架构等术语解释 |
| `comparisons/` | 对比分析 | 跨论文跨方法对比 |
| `queries/` | 问答归档 | 有价值的问答记录 |
| `SCHEMA.md` | 知识库约定 | 标签规范、页面模板、质量控制规则 |

## 📄 当前内容

| 论文 | 会议/期刊 | 核心主题 |
|------|----------|---------|
| PhyLSTM (Zhang et al., 2020) | — | LSTM 替代有限元进行滞回响应预测 |
| When PINNs Go Wrong (Wang et al., 2023) | — | PINN 训练产生伪解的根本原因与修复 |

| 其他内容 | 类型 | 核心主题 |
|----------|------|---------|
| Agentic Engineering 22 Tips (Matt Van Horn, 2026) | 公众号推文 | Agent 工程最佳实践 |
| AVBD 物理仿真算法 (SIGGRAPH 2025) | B 站视频笔记 | 增强顶点块下降求解器 |

## 🧭 如何导航

所有页面使用 `[[wikilink]]` 双向链接。三个入口：

1. **从 [index.md](index.md) 开始** — 所有页面按类型索引
2. **从标签搜索** — 每个页面有 `tags: [...]` frontmatter
3. **跟踪交叉引用** — 页面底部的关联段落链接到相关知识

推荐用 [Obsidian](https://obsidian.md) 克隆后打开，可查看图谱视图。

## 🔧 工具链

- **OCR：** [RapidOCR](https://github.com/RapidAI/RapidOCR) — 离线中英文 OCR
- **转录：** [Kimi Code CLI](https://github.com/MoonshotAI/kimi-code) — 视频/音频内容分析
- **Agent：** [Hermes Agent](https://github.com/NousResearch/hermes-agent) — 知识库自动化维护

## 📜 许可

笔记内容（papers/、entities/、comparisons/、queries/）采用 [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/)。

raw/ 文件夹中的论文全文、推文转载等保留原作者权利。
