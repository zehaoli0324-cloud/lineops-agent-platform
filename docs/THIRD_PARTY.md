# 第三方依赖与参考工作台

2026 年 11 月 15 日。采用 Git 子模块保存未经修改的上游源码指针，不复制进自有模块，也不自动安装运行。

| 状态 | 项目 | 位置或入口 | 用途 |
| --- | --- | --- | --- |
| 已选并固定源码版本 | FUXA | third_party/FUXA | 工作台、设备图、标签、趋势和告警 |
| 已选并固定源码版本 | Neuroptica | third_party/neuroptica | 小型光学神经网络功能仿真 |
| 计划运行时依赖 | Eclipse Mosquitto | https://mosquitto.org/ | MQTT 状态发布订阅，不需要在本仓库复制源码 |
| 参考，不纳入默认依赖 | ThingsBoard CE | https://github.com/thingsboard/thingsboard | 设备与遥测平台、规则链 |
| 参考，不纳入默认依赖 | Atlas CMMS | https://github.com/Grashjs/cmms | 工单、资产与维修业务 |
| 参考，不纳入默认依赖 | Frigate | https://github.com/blakeblackshear/frigate | 摄像头、视频与事件证据 |
| 参考，不纳入默认依赖 | Node RED | https://github.com/node-red/node-red | 事件连接器和流程接线 |
| 光学备选，不纳入默认依赖 | Photontorch | https://github.com/flaport/photontorch | 光子电路仿真 |
| 光学备选，不纳入默认依赖 | TorchONN | https://github.com/JeremieMelo/pytorch-onn | 光学模型训练与协同设计 |
| 架构估算参考 | ScopeX SimPhony | https://github.com/ScopeX-ASU/SimPhony | 系统架构、能耗与面积等模型估算 |

## 固定版本

- FUXA：`af0ec56e8d729c271885fbba2872f55975f6d246`，核对该提交的 README 与 LICENSE。
- Neuroptica：`7bc3c152f2713780b88e701744b0541175b12111`，核对该提交的 README 与 LICENSE。
- 两个选定子模块各自保留上游 MIT 许可文件和归属。它们的许可不代表所有参考工具采用相同许可，也不代表数据、权重或产品名称可以任意使用。
- 这是源码接入，不等于依赖安装、服务部署、模型映射或端到端测试已经完成。

## 获取与检查

首次克隆主仓库时可使用 `git clone --recurse-submodules <主仓库地址>`。

已有主仓库执行 `git submodule update --init --recursive`。Git 会签出主仓库记录的固定提交；不要为了更新依赖直接追踪上游最新提交。

之后使用 `git submodule status` 检查固定版本。安装与启动按各上游对应版本文档进行，并根据本机 OS、CPU 和 Python 或 Node 版本验证；当前未执行安装或运行。

## 比赛来源记录

第三方原库是现成工具，不计为参赛原创实现。选择和记录技术栈与赛前实现自己的参赛代码分开。比赛项目的适配器、FUXA 场景配置、模拟器、Agent 和评测实现留到正式窗口；参赛时按最终 brief 再核对来源和时间要求。
