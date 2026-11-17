# 工业团队与相邻制造研究

调研日期：2026-11-17。范围：与设备取证、诊断、维护流程、技能执行和视觉反馈相关的公开资料。

这是方向调研，不是完整市场普查。论文、机构报道、官方产品说明与合作公告分别记录；厂商表述不是独立效果验收。材料只说明相关团队的公开工作，不表示对方在招募、寻求合作或已授权联系。

## 1. Siemens Senseye：状态监测与维修指导

来源：[IND-01](sources.md#ind-01-siemens-senseye)，官方新闻及产品文档。

公开工作：Senseye 结合设备数据和预测性维护，扩展生成式 AI 维修指导。官方产品资料将预测性维护工具定位为咨询性状态监测；Maintenance Copilot 使用历史知识向用户提供指导。

LineOps 可借鉴：把设备状态、历史知识和维修流程放在统一上下文中；明确“给建议”“执行操作”“完成维修”的产品边界。

证据边界：现有材料不能证明无人值守维修闭环或任意设备的自主控制能力。

## 2. Augury + Rockwell Automation：诊断进入维护流程

来源：[IND-02](sources.md#ind-02-augury--rockwell)，Augury 官方产品说明及 Rockwell 合作公告。

公开工作：Augury 以可靠性、维护、运营等角色组织 Agent 工作流，描述维护窗口、工单和作业建议等能力。2026-07-23 的 Rockwell 公告提出与 Fiix CMMS、FactoryTalk Optix 等结合，连接诊断、维护规划和执行。

LineOps 可借鉴：把“移交”做成有设备身份、证据、原因、未完成动作及后续要求的业务对象；未来接 CMMS 时保留外部工单身份。

证据边界：合作公告不等于全部集成已交付，不能据此报告自动维修成功率或现场收益。

## 3. Aitomatic OpenSSA：领域知识与专业 Agent

来源：[IND-03](sources.md#ind-03-aitomatic-openssa)，官方方案页与开源仓库。

公开工作：OpenSSA 面向工业问题求解，采用 DANA 神经符号架构，强调领域知识、分层规划及 Observe-Orient-Decide-Act。

LineOps 可借鉴：将设备手册、故障树和操作规程作为规划依据；可以比较纯模型规划与知识约束规划，而非只比较角色数量。

证据边界：开源框架与方案定位不证明设备执行约束、崩溃恢复或特定现场效果；引入代码前核对版本、许可与实际维护情况。

## 4. 中控 SUPCON TPT：流程工业时序与工具编排

来源：[IND-04](sources.md#ind-04-supcon-tpt)，官方中文与全球站。

公开工作：TPT 平台描述预测、评估、控制、优化、工业时间序列和工具编排能力，官网列举流程工业应用。

LineOps 可借鉴：逐步明确压力、流量等测点、单位、采样时间及工况，把时间关系作为诊断依据。新增观测需要能帮助区分原因。

证据边界：官网案例属于厂商描述；流程工业优化与离散工位维修并非同一任务，不能直接迁移其应用效果。

## 5. Xia 等的生产系统研究：语义操作连接实体实验产线

来源：[IND-05](sources.md#ind-05-production-system-microservices)，Yuchen Xia、Jize Zhang、Nasser Jazdi、Michael Weyrich，2024 年预印本。

公开工作：*Incorporating Large Language Models into Production Systems for Enhanced Task Automation and Flexibility* 将原子操作建模为微服务，通过数字孪生提供语义上下文，并在实验室模块化生产设施上实现案例。

LineOps 可借鉴：Agent 选择任务语义，适配器处理底层设备操作；用设备能力和当前状态约束可执行计划。

证据边界：实体实验室案例与长期工厂商业部署分别看待；生产编排成功也不自动等于故障维修成功。

## 6. 技能化制造多 Agent：OPC UA、MCP 与 MQTT

来源：[IND-06](sources.md#ind-06-skill-based-multi-agent-manufacturing)，Kay Köhle、Darko Anicic、Thomas A. Runkler、René Graf，2026-10-01 提交。

公开工作：*LLM-Driven Multi-Agent Control for Skill-Based Smart Manufacturing* 将模块技能通过 OPC UA 暴露，使用 MCP 工具服务器、MQTT 通信与实时状态，比较集中编排、点对点及单体架构；实验涉及六模块工厂仿真和静默硬件故障。

LineOps 可借鉴：比较同一任务上的协作结构；把静默失败、实时状态和重新规划纳入测试。协议选择服务于能力表达及反馈，不以协议数量作为研究贡献。

证据边界：主要评测环境是仿真，不是工厂长期生产记录；不同挑战上的结果也不支持简单宣布多 Agent 总体占优。本知识库不摘录成功率数字，后续需按任务、预算和重复运行细读。

## 7. CMU 视觉纠正 3D 打印：接近点胶的反馈任务

来源：[IND-07](sources.md#ind-07-cmu-visual-3d-printing)，CMU 2026-02-06 研究报道；Amir Barati Farimani、Yayati Jadhav 等。

公开工作：报道介绍结合逐层图像、视觉语言模型、规划和设备命令的多 Agent 系统，用于发现打印缺陷并调整后续操作。

LineOps 可借鉴：重点研究可见质量缺陷、动作参数、后续观测的对应关系。点胶也可从局部视觉异常开始，检验处置是否改善新产生的胶路。

证据边界：本轮读取的是学校研究报道，尚未完成期刊全文、代码和跨设备实验核查；不能将模块化描述视为任意设备适配已验证。

## 8. SMIA：工业资产的能力与技能描述

来源：[IND-08](sources.md#ind-08-smia)，2025 年论文。

公开工作：*Self-configurable Manufacturing Industrial Agents (SMIA): a standardized approach for digitizing manufacturing assets* 结合 AAS、能力-技能-服务及语义描述组织制造资产 Agent。

LineOps 可借鉴：为适配器声明设备身份、能力、参数模式与调用接口；后续再评估是否需要采用既有工业语义标准。

证据边界：当前仅核对题录和摘要层信息，未完成全文复现；单场景阶段不必先实施完整 AAS 栈。

## 对我们的取舍

| 当前问题 | 优先参考 | 应产出的项目证据 |
| --- | --- | --- |
| 视觉缺陷如何形成可行动任务 | CMU 视觉打印；点胶工艺知识 | 可区分工艺故障与观测退化的任务卡 |
| 设备能力如何表达 | Xia 等；技能化制造；SMIA | 稳定动作对象、参数与前置条件 |
| 诊断如何进入维护流程 | Senseye；Augury + Rockwell | 可人工接续的工单与证据 |
| 专家知识如何约束推理 | OpenSSA | 同任务上的知识约束对照实验 |
| 如何使用过程时间关系 | SUPCON TPT | 有测点和时间语义的公开观测 |

初步判断：相邻系统已经覆盖维护助手、生产编排、视觉纠正和资产语义。LineOps 的待验证价值应具体落在“取证是否减少无效维修、动作后是否可靠复核、执行中断时能否避免盲目重做”上。调研范围不足以证明这些能力构成市场空白或研究首创。
