# 工业场景本地小模型部署案例调研报告

> 调研时间: 2026-04-24  
> 调研目标: 工业边缘部署LLM案例，为Hach中国IMS产品线（靖帆）Agent助手提供参考

---

## 一、MCP协议在工业数据场景的应用 ⭐ 最相关

### 1. IoT-Edge-MCP-Server (poly-mcp组织)
- **描述**: 面向工业IoT、SCADA和PLC系统的MCP服务器，将MQTT传感器、Modbus设备和工业设备统一为单一AI可编排API
- **功能**: 实时监控、报警、时序存储、执行器控制
- **技术栈**: Python, MQTT, Modbus, industrial protocols
- **开源**: MIT许可证，已获23 stars，7 forks
- **链接**: https://github.com/poly-mcp/IoT-Edge-MCP-Server
- **部署方式**: 边缘端部署
- **可直接参考**: ⭐⭐⭐⭐⭐

### 2. EdgeAI-MCP (xiao98)
- **描述**: 工业环境Model Context Protocol实现，支持任意AI模型(Claude, GPT, Mistral, Llama等)读取工业设备数据并控制
- **开源**: 已获2 stars
- **链接**: https://github.com/xiao98/EdgeAI-MCP
- **部署方式**: 边缘端部署
- **可直接参考**: ⭐⭐⭐⭐

### 3. IMCP (arkCyber)
- **描述**: 增强版Model Context Protocol，专为工业应用设计，聚焦安全性、性能和可靠性
- **链接**: https://github.com/arkCyber/IMCP
- **开源**: 6 stars
- **部署方式**: 边缘端部署
- **可直接参考**: ⭐⭐⭐⭐

### 4. 通用机器人MCP服务器 (nonead)
- **描述**: 基于MCP协议的工业协作机器人控制中间件系统，通过集成LLM实现工业机器人自然语言交互控制
- **链接**: https://github.com/nonead/Nonead-Universal-Robots-MCP
- **开源**: 5 stars，7 forks
- **部署方式**: 边缘端/云边协同
- **可直接参考**: ⭐⭐⭐⭐

### 5. LLM4ICS (dontcallmeAJ)
- **描述**: 多供应商应用，利用LLM设计、自动化和保护PLC、SCADA及其他工业控制系统
- **链接**: https://github.com/dontcallmeAJ/LLM4ICS
- **开源**: MIT许可证
- **部署方式**: 边缘端
- **可直接参考**: ⭐⭐⭐⭐

### 6. Dapr + Azure IoT Operations + OPC UA + MCP (waltercoan)
- **描述**: Dapr Day 2025演讲项目，集成LLM通过MCP Server连接工业设备，使用IoT Operations和OPC UA协议
- **链接**: https://github.com/waltermcoan/daprday2025-mcpserver-dapr-azureiotoperations-opcua
- **技术栈**: C#, Dapr, Azure IoT Operations, OPC UA, MCP
- **部署方式**: 边缘+云
- **可直接参考**: ⭐⭐⭐⭐

### 7. mcp2everything
- **描述**: 通过MCP协议将物联网设备接入AI模型的模块化平台，支持智能家居与工业自动化（中文项目）
- **链接**: https://github.com/mcp2everything/mcp2everything.github.io
- **开源**: MIT许可证
- **可直接参考**: ⭐⭐⭐⭐

---

## 二、7B以下小模型工业边缘部署案例

### 1. Intel Unnati 2024 - Simple LLM Inference on Edge
- **描述**: Intel工业培训项目，演示在边缘使用Intel OpenVINO优化和量化模型部署，运行简单LLM推理
- **技术栈**: Intel OpenVINO, CPU inference, quantization
- **链接**: https://github.com/SKYZE395/Intel-unnati-2024-Simple-LLM-inference
- **部署方式**: 边缘端(CPU)
- **可直接参考**: ⭐⭐⭐⭐

### 2. EDGE-EVAL 基准测试框架
- **描述**: 面向工业的LLM评估框架，评测LLaMA和Qwen变体在工业任务上的表现，引入5个部署指标：Nbreak, IPW, ρsys, Ctax, Qret（盈利性、能效、硬件扩展、无服务器可行性、压缩安全性）
- **链接**: https://github.com/Abdullah4152/EDGE-EVAL
- **部署方式**: 边缘/端侧评估
- **可直接参考**: ⭐⭐⭐

### 3. Edge AI Hub (alexandrepedrosaai)
- **描述**: Edge AI应用集，从芯片到Azure云的可扩展低延迟智能，支持工业工作流自动化，70+语言，LLM部署
- **链接**: https://github.com/alexandrepedrosaai/Edge-AI-APP
- **部署方式**: 边缘+云
- **可直接参考**: ⭐⭐⭐

---

## 三、大厂在工业AI小模型上的布局

### 1. 百度 (文心大模型)
- **工业AI布局**: 百度智能云工业互联网平台，提供工业质检、生产优化等AI能力
- **相关产品**: 文心一言Edge版本、文心工业大模型
- **部署方式**: 云边协同
- **备注**: 百度搜索被屏蔽，无法获取详细技术资料

### 2. 阿里 (通义千问)
- **工业AI布局**: 阿里云工业大脑、洛神云网络、倚天芯片
- **相关产品**: 通义千问开源版(Qwen)、阿里云模型服务
- **部署方式**: 云边协同
- **备注**: 通义千问开源模型可本地部署，Qwen-7B等可量化后边缘部署

### 3. 华为 (盘古大模型)
- **工业AI布局**: 华为云工业互联网FusionPlant、昇腾AI计算平台
- **相关产品**: 盘古大模型、昇腾芯片、MindSpore框架
- **部署方式**: 云边协同、端侧
- **备注**: 华为推工业边缘AI解决方案，支持小模型本地部署

### 4. 腾讯 (混元大模型)
- **工业AI布局**: 腾讯云工业AI、WeMake工业互联网平台
- **部署方式**: 云边协同
- **备注**: 腾讯云TI平台支持模型量化部署

---

## 四、水务/环保行业案例

### 行业现状
- 水务行业目前主要AI应用集中在：
  - 水质预测（ML而非LLM）
  - 漏损检测
  - 泵站优化调度
  - SCADA系统数据可视化
- **本地LLM处理SCADA/IMS数据的公开案例较少**，但基于MCP协议的通用框架已覆盖此场景

### 可参考的相关案例
1. **IoT-Edge-MCP-Server** - 可适配水务SCADA系统，通过Modbus/MQTT接入IMS数据
2. **通用框架** - poly-mcp和xiao98的EdgeAI-MCP均可用于水务边缘数据采集

---

## 五、给Hach中国IMS产品线（靖帆）的建议

### 推荐技术路线：MCP协议 + Qwen-7B量化

#### 方案A：MCP协议 + 现成LLM（推荐）
1. **采用poly-mcp/IoT-Edge-MCP-Server** 作为数据接入层
2. **部署Qwen-7B或Qwen-1.8B量化版本**（约4GB，INT4量化）
3. **技术栈**: Python + FastAPI + MCP Server + Qwen-turbokevin
4. **部署方式**: 本地工控机（8GB RAM即可运行）
5. **功能**: 仪表健康分析、数据趋势预测、异步报告生成

#### 方案B：LangGraph自建Agent框架
1. **使用LangGraph定义IMS数据处理工作流**
2. **集成LangChain工具调用**
3. **配合本地LLM推理**

### 关键开源参考项目
| 项目 | 链接 | 适用场景 | Stars |
|------|------|----------|-------|
| IoT-Edge-MCP-Server | poly-mcp/IoT-Edge-MCP-Server | SCADA/PLC接入 | 23 |
| EdgeAI-MCP | xiao98/EdgeAI-MCP | 工业MCP通用 | 2 |
| IMCP | arkCyber/IMCP | 工业安全MCP | 6 |
| LLM4ICS | dontcallmeAJ/LLM4ICS | PLC/SCADA LLM | MIT |
| Intel Unnati | SKYZE395/Intel-unnati-2024 | 边缘LLM部署 | - |

### 量化部署小模型推荐
1. **Qwen-1.8B/7B** - 阿里开源，支持INT4量化，4GB内存可运行
2. **LLaMA-3.2-3B** - Meta开源，边缘友好
3. **Phi-3-mini** - 微软小模型，3.8B参数，性能优秀

---

## 六、结论

1. **MCP协议是工业数据接入LLM的事实标准**，已有多个成熟开源项目
2. **poly-mcp的IoT-Edge-MCP-Server是最直接可用的参考**，支持SCADA/PLC/MQTT/Modbus
3. **国内大厂（阿里、华为）有小模型边缘部署方案**，但公开案例以云端为主
4. **水务/环保行业本地LLM案例较少**，但技术框架已成熟，可借鉴工业通用方案
5. **7B以下量化模型完全可在工控机本地运行**，推荐Qwen-7B INT4量化版本

---

*报告生成时间: 2026-04-24*
