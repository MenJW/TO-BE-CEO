# Intelligent Brain Company

[English](README.md) | 简体中文

Intelligent Brain Company 是一个 AI 创业公司模拟器：你输入一个想法，系统会像一家公司一样经过研究组、各职能部门和董事会评审，最终给出结构化的 Go / Maybe / No-Go 结论，而不是只返回一段普通聊天回复。

这个仓库现在已经不只是概念骨架，而是一个可以直接演示的产品雏形。它包含 Web 控制台、基于 SQLite 的项目历史、计划版本 Diff、与各部门直接对话的聊天面板，以及把聊天内容提升为正式干预并触发重算的完整流程。

研究组、董事会和各部门在配置 OpenAI 兼容接口后可以使用真实 LLM；如果没有配置密钥，系统会自动回退到本地确定性生成，因此整个流程仍然可以完整运行并用于展示。

硬件、软件、设计、营销和财务部门都通过显式 JSON 合约输出结果，因此整体体验更像一个跨部门评审系统，而不是简单的角色扮演 Prompt。

## 30 秒能看懂什么

输入：

- 一个创业想法或产品想法
- 若干约束，例如预算、上线速度、目标市场

流程：

1. 研究组评估需求、竞争和风险。
2. 各部门输出带结构化工件的方案。
3. 董事会给出结论和推进条件。
4. 你可以和任意角色对话，并把某次对话提升为正式干预。

输出：

- Go、Maybe 或 No-Go 结论
- 五维评分卡：市场需求、技术可行性、执行复杂度、MVP 时效、商业化潜力
- 部门方案及其工件，例如 BOM 目标、软件边界、设计约束、渠道预算、资金规划
- 时间线、版本历史和计划 Diff

## 它和普通 LLM 聊天有什么区别

- 它保留项目状态，而不是一次性回答。
- 它把研究、部门评审和董事会决策拆成了显式阶段。
- 它支持人在流程中途干预，并能重算下游结论。
- 它把版本、聊天和时间线写入 SQLite，结果可追踪、可审计。

## 项目目标

很多多智能体项目最终停留在角色扮演或软件协作层面。这个项目的目标更具体：把 AI 组织成一家公司，让用户像 CEO 一样提交一个 idea，然后看到研究、部门评审、董事会决策和人工干预之后的完整执行建议。

核心产品假设是：

1. 用户提交一个想法。
2. 研究组评估可行性、市场需求、竞争和风险。
3. 每个部门生成多个可行方案。
4. 跨部门评审依赖关系和取舍。
5. 系统整合出一版统一计划。
6. 董事会决定是否推进，以及要附带哪些条件。
7. 用户可以在任意阶段插入干预并改变结果。

## 当前 MVP 范围

当前版本聚焦在一个新用户可以快速理解并直接体验的最小闭环：

- 想法、方案、评审、董事会决策和用户干预等领域模型
- 覆盖完整流程的公司级 Pipeline
- 研究、硬件、软件、设计、营销、财务等部门注册表
- 部门方案生成的结构化 JSON 合约
- 将 idea 转成结构化计划的 CLI
- 用于创建项目、生成计划、聊天和记录干预的 Flask API
- 可直接和研究组、董事会、各部门对话的聊天面板
- Go / Maybe / No-Go 评分卡
- 用 SQLite 持久化项目状态、任务历史、版本和聊天记录
- 部署、评估、架构和案例文档

当前实现刻意保持轻量，便于后续接入 AutoGen、CrewAI、LangGraph、Semantic Kernel 或自定义模型路由，而不必重写业务流程。

## 仓库结构

```text
.
├── docs/
│   ├── architecture.md
│   ├── baseline-comparison.md
│   ├── deployment.md
│   ├── execution-plan.md
│   ├── evaluation-rubric.md
│   ├── github-metadata.md
│   └── license-strategy.md
├── examples/
│   └── demo_cases/
│       ├── ai-interview-coach.md
│       ├── campus-secondhand-marketplace.md
│       ├── crossborder-product-selection.md
│       └── README.md
├── render.yaml
├── src/
│   └── intelligent_brain_company/
│       ├── api/
│       ├── agents/
│       ├── domain/
│       ├── interfaces/
│       ├── services/
│       ├── workflows/
│       ├── app.py
│       ├── config.py
│       └── wsgi.py
├── tests/
│   ├── test_api.py
│   └── test_pipeline.py
└── pyproject.toml
```

## 快速开始

```bash
python -m pip install -e .
ibc-plan "Build an electric tricycle" --constraint "Target price below 18000 CNY" --constraint "Designed for short-distance cargo delivery"
```

CLI 当前会生成一份确定性的计划草案。后续如果接入真实模型，可以把其中各阶段逐步替换成在线 Agent。

### API 模式

```bash
python -m pip install -e .[dev]
ibc-api
```

示例流程：

1. `POST /api/projects` 创建项目
2. `POST /api/planning/generate` 生成第一版计划
3. `POST /api/planning/interventions` 插入用户反馈并重算
4. `GET /api/projects/<project_id>` 查看项目状态
5. `POST /api/projects/<project_id>/chat` 与研究组、董事会或某个部门对话
6. `POST /api/projects/<project_id>/chat/promote` 将聊天内容提升为正式干预并触发重算

启动后打开 `http://127.0.0.1:8000`，可以创建项目、查看计划、查看时间线和阶段进度，并提交干预。

控制台还提供：

- 三个一键演示的 Demo 项目
- 方便快速理解结果的评分卡
- 和研究组、董事会、硬件、软件、设计、营销、财务直接对话的聊天面板
- 从聊天到正式干预再到版本重算的完整链路

## 内置 Demo 案例

控制台里的内置案例是为了让新用户在一分钟内看懂整个产品闭环：

1. AI 面试训练教练
2. 跨境电商选品助手
3. 校园二手交易平台

这些案例适合用来演示：创建项目、生成计划、查看评分卡、向某个部门追问、把对话提升为正式干预，然后比较前后版本差异。

## 文档与资产

- 部署说明：docs/deployment.md
- Baseline 对比：docs/baseline-comparison.md
- 评估 Rubric：docs/evaluation-rubric.md
- 架构说明：docs/architecture.md
- GitHub 元数据建议：docs/github-metadata.md
- Demo 案例：examples/demo_cases/

如果你想启用真实 LLM 评审，请在启动 API 前配置这些环境变量：

```bash
IBC_LLM_API_KEY=your_key
IBC_LLM_BASE_URL=https://your-openai-compatible-endpoint/v1
IBC_LLM_MODEL=your-model-name
```

## 架构方向

当前架构分成四层：

1. 领域层：稳定的业务对象和状态模型
2. 工作流层：公司式流程和阶段交接
3. 服务层：编排入口、存储和未来的模型适配器
4. 接口层：CLI、HTTP API 和 Web 控制台

之所以这样拆分，是因为这个项目真正的护城河不在某一个 Prompt，而在 AI 公司的运行机制：状态管理、评审规则、升级逻辑和人工干预能力。

## 推荐下一步里程碑

1. 把更多确定性部门输出替换成真实 Agent
2. 引入更细粒度的检查点和按依赖重算
3. 增强评估数据集和自动化质量回归
4. 为公开 Demo 增加认证、重置和观察能力
5. 补截图、GIF 和公开演示视频，让仓库更像可传播产品

## 许可证说明

当前仓库使用 Apache-2.0。

这和项目当前的开放策略一致：更利于商业合作、更容易降低贡献门槛，也更适合被集成到企业场景中。关于许可证选择的背景说明见 docs/license-strategy.md。