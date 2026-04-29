<!-- Author: mikewang6700 -->
# LLMOps

LLMOps 是一个面向开发者与企业的本地化 LLM 运维与应用平台，旨在帮助构建、管理与部署基于大型语言模型（LLM）的应用和代理（Agent）。该仓库包含后端 API 服务、前端管理控制台、以及若干扩展与工具脚本。

**主要特性**
- **统一 API 层**：提供面向应用、会话、API Key 管理、模型接入、工作流与向量检索的 REST 接口。
- **多模型接入**：支持 OpenAI、Weaviate、DeepSeek、Moonshot、通义等多家模型/服务提供者的适配。 
- **向量数据库与检索**：集成 Weaviate（可替换）用于语义检索与知识库管理。
- **工作流与 Agent**：支持可视化工作流编辑、节点插件与自定义 Agent 应用。
- **前端管理 UI**：基于 Vite + Vue 3 的管理控制台（目录：`ui/`）。

**仓库结构（概览）**
- **`api/`**：后端服务代码（Flask/WSGI 风格）；配置、路由、模型、服务与扩展。
- **`ui/`**：前端源代码（Vue 3 + TypeScript），含构建与 Docker 配置。
- **`docker/`**：容器部署与 nginx 配置示例。
- **`scripts/`**：仓库维护脚本（例如历史清理说明、作者注释脚本）。

**快速开始（本地开发）**
1. 克隆仓库：

```bash
git clone https://github.com/mikewang6700/llmops
cd llmops
```

2. 创建 Python 虚拟环境并安装依赖：

```bash
python -m venv .venv
source .venv/bin/activate   # Linux / macOS
.\.venv\Scripts\activate  # Windows PowerShell
pip install -r requirements.txt
```

3. 配置环境变量：复制并编辑示例文件 `api/.env.example`，将密钥与配置写入运行环境（注意：切勿将真实密钥提交到仓库）。

4. 启动后端与前端（示例使用 Docker Compose）：

```bash
docker compose up --build
```

5. 访问管理 UI：打开 `http://localhost:3000`（端口依 `docker-compose` 配置而定）。

**常用文件与路径**
- 后端入口：[`api/app/http/app.py`](api/app/http/app.py#L1)
- 后端配置：[`api/config/default_config.py`](api/config/default_config.py#L1)
- 前端入口：[`ui/src/main.ts`](ui/src/main.ts#L1)


**如何贡献**
1. 提交 issue 讨论功能或 bug。
2. 新建分支并提交 PR，保持变更小而清晰。
3. 对提交中涉及配置或密钥的修改，请使用占位符或 environment 变量；不应将敏感信息提交到仓库。
