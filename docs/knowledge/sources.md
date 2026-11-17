# 来源目录

整理日期：2026-11-17。以下为项目讨论使用的一手资料入口。链接可访问不代表全文已读，官方描述不代表独立验证，公开代码也不代表已在本项目复现。

本轮通过公开检索核对论文题录/摘要、部分公开材料、机构报道和官方仓库。部分出版社页面有 403 或 Cookie 跳转；未获取全文的条目不标为全文精读。沿用原参考页的题录信息已注明；后续引用实验数字应再次核对原文。

## 自动化实验室

### LAB-01 ChemOS 2.0

- 题名：*ChemOS 2.0: An orchestration architecture for chemical self-driving laboratories*。
- 年份与来源：2024，Matter 7，2959-2977；[DOI](https://doi.org/10.1016/j.matt.2024.04.022)。
- [出版页](https://www.sciencedirect.com/science/article/pii/S2590238524001954)；[作者代码](https://github.com/malcolmsimgithub/ChemOS2.0)。
- 核验深度：题录、摘要及仓库说明；出版社正文访问受限。代码为演示及定制参考，未安装复现。
- 用途：模块编排、错误注入、并行模拟。

### LAB-02 HELAO-async

- 题名：*Orchestrating nimble experiments across interconnected labs*。
- 年份与来源：2023，Digital Discovery 2，1806-1812；[DOI](https://doi.org/10.1039/D3DD00166K)。
- [出版页](https://pubs.rsc.org/en/content/articlehtml/2023/dd/d3dd00166k)。
- 核验深度：题录和公开检索信息；正文直接读取返回 403，尚需全文核查。
- 用途：异步工作流、设备服务与共享资源。

### LAB-03 AlabOS

- 作者线索：Yuxing Fei、Gerbrand Ceder 等；2024 年预印本。
- [arXiv:2405.13930](https://arxiv.org/abs/2405.13930)；[作者机构 PDF](https://ceder.berkeley.edu/publications/2024_Yuxing_AlabOS.pdf)。
- 核验深度：摘要及公开论文任务、资源与异常处理材料；未复现。
- 用途：资源所有权、任务状态、可恢复异常及人工介入。

### LAB-04 Coscientist

- 题名：*Autonomous chemical research with large language models*。
- 年份与来源：2023，Nature 624，570-578；[DOI](https://doi.org/10.1038/s41586-023-06792-0)。
- [出版页](https://www.nature.com/articles/s41586-023-06792-0)。
- 核验深度：沿用原参考页题录及公开摘要；本轮正文访问遇到身份/Cookie 跳转，未重核实验细节。
- 用途：模型结合设备文档、工具执行与反馈。

### LAB-05 XDL / Chemputer

- 题名：*A universal system for digitization and automatic execution of the chemical synthesis literature*。
- 年份与来源：2020，Science 370，101-108；[DOI](https://doi.org/10.1126/science.abc2986)。
- [作者机构 PDF](https://www.chem.gla.ac.uk/cronin/images/pubs/Mehr-ScienceOct2020.pdf)。
- 核验深度：题录与概述沿用 [原参考页](../AUTONOMOUS_LAB_REFERENCES.md)；本轮未重新精读全文。
- 用途：过程表达、任务编译与设备实现分层。

### LAB-06 A-Lab

- 当前参考题名：*An autonomous laboratory for the accelerated synthesis of inorganic materials*。
- 年份与来源：2023，Nature 624，86-91；[DOI](https://doi.org/10.1038/s41586-023-06734-w)。
- [出版页](https://www.nature.com/articles/s41586-023-06734-w)；[作者更正 DOI](https://doi.org/10.1038/s41586-025-09992-y)。
- 核验深度：题录、更正入口及标题说明沿用原参考页；本轮正文读取受 Cookie 跳转限制，未重新核验更正细节。本知识库不引用成功数或成功率。
- 用途：执行、表征和后续决策闭环；注意修订版本。

### LAB-07 ORGANA

- 题名：*ORGANA: A robotic assistant for automated chemistry experimentation and characterization*。
- 年份与来源：2024 年预印本；Matter 8，101897（2025）；[DOI](https://doi.org/10.1016/j.matt.2024.10.015)。
- [arXiv:2401.06949](https://arxiv.org/abs/2401.06949)；[项目页](https://ac-rad.github.io/organa/)。
- 核验深度：公开摘要和项目概述，期刊题录沿用原参考页；未复现机器人系统。
- 用途：目标澄清、视觉反馈、调度和人在环。

## 工业产品与制造研究

### IND-01 Siemens Senseye

- 类型：官方产品说明、服务文档和新闻。
- [2025 年维护方案公告](https://press.siemens.com/jp/en/pressrelease/pr-20250324)。
- [Senseye 产品数据表，2025-11](https://cache.industry.siemens.com/dl/files/319/109955319/att_1350959/v1/109955319_Senseye-product-sheet-V1.6_Nov25-2.pdf)。
- [Maintenance Essentials 文档，2025-11](https://cache.industry.siemens.com/dl/files/942/109997942/att_1351423/v1/109997942_Senseye_Maintenance_Essentials_Documentation_Nov25_v1.0.pdf)。
- 核验深度：官方资料检索及定位说明；无独立现场验收。
- 用途：预测性维护、咨询性状态监测、历史知识与维修指导。

### IND-02 Augury + Rockwell

- 类型：厂商产品资料及合作公告。
- [Augury Industrial AI Workforce](https://www.augury.com/industrial-ai/)。
- [角色型 Agent 工作流](https://www.augury.com/blog/work-transformation-2/role-based-ai-agents-manufacturing/)。
- [Rockwell 合作公告，2026-07-23](https://www.rockwellautomation.com/en-us/company/news/press-releases/rockwell-automation-and-augury-partner-to-improve-industrial-performance-with-agentic-ai.html)。
- 核验深度：官方公开描述；合作宣布与具体集成交付、现场效果分别看待。
- 用途：诊断、维护计划、工单和业务系统衔接。

### IND-03 Aitomatic OpenSSA

- 类型：官方方案与开源框架。
- [官方方案](https://www.aitomatic.com/solutions)；[OpenSSA 仓库](https://github.com/aitomatic/openssa)。
- 核验深度：方案定位、仓库说明及架构概述；未安装或运行。
- 用途：工业领域知识、神经符号专业 Agent、分层规划。

### IND-04 SUPCON TPT

- 类型：官方产品与应用场景描述。
- [中文站](https://supcontpt.supcon.com/)；[全球站 TPT2](https://global.supcon.com/digital/tpt)。
- 核验深度：官网定位与公开场景；未取得独立验收数据。
- 用途：工业时序、预测/评估/控制/优化和工具编排。

### IND-05 Production system microservices

- 题名：*Incorporating Large Language Models into Production Systems for Enhanced Task Automation and Flexibility*。
- 作者：Yuchen Xia、Jize Zhang、Nasser Jazdi、Michael Weyrich；2024 年预印本。
- [arXiv:2407.08550](https://arxiv.org/abs/2407.08550)。
- 核验深度：摘要及实验室模块化生产案例概述；未复现。
- 用途：语义上下文、原子操作微服务与实体实验设施。

### IND-06 Skill-based multi-agent manufacturing

- 题名：*LLM-Driven Multi-Agent Control for Skill-Based Smart Manufacturing*。
- 作者：Kay Köhle、Darko Anicic、Thomas A. Runkler、René Graf；2026-10-01 提交。
- [arXiv:2610.01364](https://arxiv.org/abs/2610.01364)。
- 核验深度：公开摘要与研究设置；主要实验为六模块工厂仿真，未复现。
- 用途：OPC UA 技能、MCP 工具、MQTT、架构对照及静默故障。

### IND-07 CMU visual 3D printing

- 类型：CMU 官方研究报道，2026-02-06；团队线索为 Amir Barati Farimani、Yayati Jadhav 等。
- [AI saves 3D prints](https://engineering.cmu.edu/news-events/news/2026/02/06-ai-saves-3d-prints.html)。
- 核验深度：学校报道；期刊全文、代码和跨设备实验尚待核查。报道提及 Additive Manufacturing，未补写未经核对的完整题录。
- 用途：视觉缺陷、Agent 规划、设备参数修改与后续反馈。

### IND-08 SMIA

- 题名：*Self-configurable Manufacturing Industrial Agents (SMIA): a standardized approach for digitizing manufacturing assets*，2025。
- [DOI](https://doi.org/10.1016/j.jii.2025.100915)。
- 核验深度：题录及摘要层检索；未全文精读或复现。
- 用途：AAS、能力-技能-服务和资产语义。

## 后续核查清单

- [ ] 获取 HELAO、Coscientist 等可公开全文，补充精读章节和图表笔记。
- [ ] 核对 A-Lab 更正原文，再决定是否引用具体实验结论。
- [ ] 精读技能化制造及 CMU 论文的任务、对照、预算、失败案例和代码。
- [ ] 核对拟采用开源项目的提交版本、依赖、许可与维护状态。
- [ ] 对厂商案例补充具体交付范围、现场条件和可取得的验收材料。
- [ ] 后续调研按相同问题更新，而非仅添加团队名称或产品宣传。
