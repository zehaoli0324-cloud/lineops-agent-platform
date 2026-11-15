# FUXA / MQTT 接入说明

状态：已写桥接脚本与 Compose 草案；当前环境没有 Docker，未启动 broker 或 FUXA，未导出可导入的 FUXA 工程。

## 启动草案

先 `git submodule update --init --recursive`，再 `docker compose --profile industrial up --build`。FUXA 按主仓库 gitlink 固定源码构建；基础镜像标签和 npm 依赖未做完整可复现锁定，首次构建需联网。默认只启动 app 时运行 `docker compose up --build app`。以上部署命令未在本环境验证。

打开 `http://127.0.0.1:1881` 创建 MQTT 连接，broker 主机为 compose 服务名 `mqtt`，端口 1883。通过 `lineops/glue/state` 与 `lineops/filling/state` JSON 消息创建标签。根据 FUXA 固定版本编辑器核对 JSON 标签解析配置，不把下面映射表误当成现成 FUXA 配置文件。

| 标签 | 消息路径 | 说明 |
| --- | --- | --- |
| 当前事件 | incident_id | 审计关联 |
| 运行终态 | status | recovered / handed_off / stopped / failed |
| 模式 | mode | offline / llm |
| 供压 | telemetry.supply_pressure | 归一化模拟值 |
| 设备运行 | telemetry.running | 布尔值 |
| 测量值 | measurement.value | 图像无效时 null |
| 图像质量 | measurement.quality | valid / invalid |

桥接为只读轮询，每两秒发布最近已完成事件的最终验证状态，QoS 1，retain=true。首版事件执行期间 API 读操作等待设备锁；当前不是实时遥测桥，也不发送控制命令。桥重启会重新发布，消费者必须按 incident_id 去重。MQTT 客户端传输与 FUXA 标签绑定仍需实测。

Agent 证据页位于 `http://127.0.0.1:8000`。FUXA 画面可链接到该页面；当前没有嵌入或统一身份认证。FUXA 容器尚未配置工程持久化卷，在正式配置时按上游目录核对并增加。该服务只用于本机演示，无身份验证，不适合直接开放给其他网络。
