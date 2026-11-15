# LineOps Agent Platform

面向工业产线的模块化自主运维系统完整规划。

采用 FUXA 工作台、独立有状态产线模拟器、运行管理与多 Agent 服务和可替换计算后端。完整范围保留多设备、多产线、多模态、真实业务系统接入与光学计算研究，不受一次黑客松交付范围限制。

## 文档

- [完整项目规划](docs/PROPOSAL.md)
- [三十类候选场景](docs/SCENARIOS.md)
- [与比赛版本的范围对照](docs/SCOPE_MAP.md)

## 当前状态

2026 年 11 月 15 日：仅规划文档，尚未部署或实现验证。比赛版本使用独立仓库 lineops-agentware-2026；当前不包含参赛项目代码。

## 架构与第三方源码

![完整平台架构](docs/architecture.html)

- [架构图与模块职责](docs/ARCHITECTURE.md)
- [上游源码、固定版本与参考工作台](docs/THIRD_PARTY.md)
- [命名建议](docs/NAMING.md)

已选上游以 Git 子模块固定提交，运行 `git submodule update --init --recursive` 获取源码。当前没有安装或部署声明。


## 细化设计

- [可交互 HTML 架构图](docs/architecture.html)
- [Proposal HTML 阅读版](docs/PROPOSAL.html)
- [实施规格与验收](docs/SPECIFICATION.md)
