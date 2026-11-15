# LineOps Agent Platform

模块化工业设备运维平台，当前交付 v0.1 本机软件沙箱。点胶与灌装两条线共用事件管理、工具网关、执行轨迹、图像证据和恢复判据。

[HTML 架构图](docs/architecture.html) · [完整 Proposal](docs/PROPOSAL.html) · [实施规格](docs/SPECIFICATION.md) · [状态与验证](docs/STATUS.md) · [30 类场景](docs/SCENARIOS.md)


![论文式系统架构](docs/architecture-full.png)

[分层、因果与接口说明](docs/ARCHITECTURE.md) · [HTML 交互图](docs/architecture.html) · [矢量 PDF](docs/architecture-full.pdf)

## 运行首版

需要 Python 3.11+，当前测试 Python 3.12。克隆后在仓库根目录执行：

```bash
python -m venv .venv
source .venv/bin/activate
pip install -e .
lineops serve
```

Windows 将激活命令改为 `.venv\Scripts\activate`。打开 http://127.0.0.1:8000，选择产线、注入条件与运行模式。默认离线规则对照不需要模型密钥；它用于复现，不作为真实 LLM Agent 效果。FUXA 是后续并排接入的工业工作台，当前页面是独立证据控制台。

```bash
lineops suite
python -m unittest discover -s tests -v
lineops run --scene filling --fault supply
```

支持 normal / clog / supply / camera / persistent 五种注入。前四种条件在离线套件中结束为 recovered；persistent 保持暂停并建工单，结束为 handed_off。正常条件 recovered 表示通过恢复谓词，无维修动作，不计作成功维修。

## 真实模型工具调用

通过环境变量设置 `LINEOPS_API_KEY`、`LINEOPS_MODEL`，可选 `LINEOPS_LLM_URL`（完整 Chat Completions URL），再选择页面 llm 模式或：

```bash
lineops run --mode llm --scene glue --fault clog
```

配置参见 [.env.example](.env.example)，服务不会自动加载该文件。诊断、规划、验证角色按顺序使用 function tools；真实回执由运行器产生。模型读取图像测量结果和遥测，当前不直接向视觉语言模型发送图片。已验证协议 mock，尚无真实模型端点效果记录。

## 虚拟光学后端与 FUXA

```bash
git submodule update --init --recursive
pip install -e '.[optical]'
lineops optical-check
```

Neuroptica 8 端口 Reck 光学网络通过功能检查。它是独立未训练数值变换，尚未接入缺陷识别决策；不可将此结果解释成真实芯片速度、功耗或识别准确率。不可用时明确返回 numpy_identity fallback，替代变换不宣称等价。

FUXA 和 Neuroptica 固定为 Git 子模块；保留各自 MIT 许可与归属。[FUXA/MQTT 接入草案](docs/FUXA_INTEGRATION.md)包含 Compose 与只读桥接。当前环境没有 Docker，未验证 FUXA 部署、MQTT 传输或标签配置。

## 模块与扩展

- `lineops/simulator.py`：两种场景、状态变更和参数化渲染，隐藏故障不进入工具结果。
- `lineops/runtime.py`：任务生命周期、工具权限、步数预算、动作幂等、维护前暂停与强制复核。
- `lineops/store.py`：SQLite 事件、轨迹、PNG 和工单。重启后未完成任务标记 failed；尚不能恢复世界继续运行。
- `lineops/llm.py`：OpenAI 兼容工具调用，三角色按需读取、执行和验证。
- `lineops/api.py` 与 `static/index.html`：本机 API、操作者注入与证据页。
- `lineops/mqtt_bridge.py`：最近完成事件的只读 MQTT 发布草案。

新产线需实现渲染、测量与故障动作关系，并配置手册和阈值。两条已内置场景可在页面直接切换；首版未实现第三方热加载插件或任意设备仅改配置接入。

## 当前限制与下一步

图像分割采用合成图的 RGB 阈值，不是已训练工业视觉模型；模拟值无真实物理单位，三帧复核不是统计置信度。当前单进程同步运行、设备锁串行执行，没有多设备调度、跨进程锁、真实 PLC/CMMS 或身份认证。只在本机使用；页面显示会等待当前任务完成，停止请求在下一工具边界生效。

下一阶段依次接通真实模型并留存测试轨迹、实测 FUXA/MQTT、实现任务队列与重启恢复、丰富噪声及未见故障、建立真实设备只读试点。完整路线见 [ROADMAP](docs/ROADMAP.md)。

比赛项目 [lineops-agentware-2026](https://github.com/zehaoli0324-cloud/lineops-agentware-2026) 赛前只存文档和第三方指针，不复制本仓库实现。仓库名称暂沿用 LineOps（产线运维）；[命名备选](docs/NAMING.md)。
