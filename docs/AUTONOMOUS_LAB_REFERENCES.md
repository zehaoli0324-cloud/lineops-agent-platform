# 自动化实验室参考文献与 LineOps 模块映射

2026-11-17 · 为下一阶段实施提供参考

这里区分论文报道的工作与我们建议迁移的设计。文献不等于已接入依赖，也不构成 LineOps 已完成真实设备控制、具备科研发现能力或获得工业覆盖率的证据。

## 1 ChemOS 2.0：模块化编排架构

**ChemOS 2.0: An orchestration architecture for chemical self-driving laboratories.** Matter 7, 2959–2977 (2024). DOI: [10.1016/j.matt.2024.04.022](https://doi.org/10.1016/j.matt.2024.04.022)。

论文介绍面向化学自驱动实验室的编排架构，协调模块通信、数据交换与指令管理，将实验规划、仪器、数据库和计算连接起来。

建议迁移：独立运行内核、稳定通信契约、设备适配和数据服务，支撑 WP2/WP4。阅读时重点看架构分层与 Figure 1 的功能划分。不要将其对实验室的适配结果直接解释为任意工业设备兼容性。

## 2 HELAO-async：独立工作流与共享资源

**Orchestrating nimble experiments across interconnected labs.** Digital Discovery 2, 1806–1812 (2023). DOI: [10.1039/D3DD00166K](https://doi.org/10.1039/D3DD00166K)。[出版社全文入口](https://pubs.rsc.org/en/content/articlehtml/2023/dd/d3dd00166k)。

论文讨论多实验流程独立启停且共享仪器资源的问题，使用 Python 异步编程，将资源管理器和实验编排器抽象为 FastAPI 服务。

建议迁移：把任务执行、设备资源与编排分开，为 WP3 的异步队列及后续多设备资源预约提供参考。它不自动证明我们的系统具备跨系统 exactly-once、检查点恢复或实时调度保证，这些仍需单独设计和验证。

## 3 Coscientist：语言模型与真实工具

**Autonomous chemical research with large language models.** Nature 624, 570–578 (2023). DOI: [10.1038/s41586-023-06792-0](https://doi.org/10.1038/s41586-023-06792-0)。

论文中的 Coscientist 将语言模型与文献/设备文档检索、代码执行和实验自动化工具结合，展示实验规划、执行和分析任务。

建议迁移：围绕真实工具回执开展取证与决策，支撑 WP1 的模型闭环；将模型版本、工具交互和结果保存在可检查轨迹中。我们的动作前置条件、权限和恢复判据继续由程序约束，不因使用语言模型而取消。

## 4 XDL / Chemputer：从任务描述到设备执行

**A universal system for digitization and automatic execution of the chemical synthesis literature.** Science 370, 101–108 (2020). DOI: [10.1126/science.abc2986](https://doi.org/10.1126/science.abc2986)。[作者机构保存的论文](https://www.chem.gla.ac.uk/cronin/images/pubs/Mehr-ScienceOct2020.pdf)。

论文将文献合成过程转化为可编辑、可编译执行的描述，再驱动自动化合成。

建议迁移：WP2 区分“采集、暂停、维护、恢复、验证”等任务语义与具体设备/API/参数单位，降低协调器对设备协议的耦合。这里借鉴中间表示和编译分层思想，不计划直接把化学语言当作工业运维通用协议。

## 5 A-Lab：执行、表征与后续决策闭环

**An autonomous laboratory for the accelerated synthesis of inorganic materials.** Nature 624, 86–91 (2023). DOI: [10.1038/s41586-023-06734-w](https://doi.org/10.1038/s41586-023-06734-w)。

原始版本标题使用“novel materials”；当前论文网页已更新。作者更正发表于 2026-01-19：[10.1038/s41586-025-09992-y](https://doi.org/10.1038/s41586-025-09992-y)。引用成果范围、目标数和成功数时应核对更新版，不沿用旧摘要数字。

论文连接方案提出、机器人合成、XRD 表征与后续实验选择，利用测量结果调整后续方案。

建议迁移：WP1/WP3 中分开保存命令、回执、动作后观测和最终验证。维修工具返回成功不能直接等同设备恢复；结果有歧义时保留未确定或移交。材料合成成功率不能迁移为设备运维成功率。

## 6 ORGANA：感知、规划与任务执行衔接

**ORGANA: A robotic assistant for automated chemistry experimentation and characterization.** Matter 8, 101897 (2025). DOI: [10.1016/j.matt.2024.10.015](https://doi.org/10.1016/j.matt.2024.10.015)。[作者实验室出版物入口](https://rvl.cs.toronto.edu/publications/)。

DOI 含 2024，正式卷期年份为 2025。论文将自然语言交互、规划、感知与机器人实验操作结合，并考虑任务调度与并行执行。

建议迁移：研究用户目标如何形成可执行任务，以及感知、计划和资源如何协调，支撑 WP1/WP2 和后续资源调度。当前只在软件产线验证接口，不复制或声称已实现机器人操作能力。

## 阅读产出

每篇阅读后记录：论文解决的问题、模块边界、观测/指令/回执对象、控制与数据路径、异常和人工介入边界、数据及代码可得性。将建议映射到具体工作包与测试，而不是仅把论文名称加在架构图上。以上六篇尚未作为本仓库依赖安装或复现。
