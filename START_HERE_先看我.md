# StayPilot 完整项目起步包 | 首次使用先看这里

**目标：** 将 Dify + DeepSeek + RAG + FastAPI + SQLite 组合成可演示的酒店 AI 智能客服与工单助手。

本压缩包包含 **可运行、已设计测试用例的后端源码**、**可直接上传 Dify 的虚构酒店政策知识库**、**可粘贴 Dify Code 节点的 Python 代码**、**30 条中英文评测用例**、**产品需求文档**、**从零搭建教程**。**不包含已经发布好的 Dify Agent 或已配置模型/密钥的 DSL**，因为这些必须在你自己的 Dify 账号中连接。

## 推荐的第一条路径（Windows）

1. 安装 Python 3.11 或 3.12，VS Code，Git。
2. 在 VS Code 中打开解压后的根目录，打开终端执行：

```powershell
cd backend
py -3.11 -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
$env:STAYPILOT_API_KEY="REPLACE_WITH_YOUR_LONG_RANDOM_SECRET"
python -m uvicorn app:app --reload --port 8000
```

3. 浏览器打开 `http://127.0.0.1:8000/docs` 查看接口，访问 `http://127.0.0.1:8000/health` 验证服务。
4. 在**新终端**设置相同 `STAYPILOT_API_KEY`，然后回到项目根目录运行：

```powershell
python scripts/smoke_test.py --base-url http://127.0.0.1:8000
```

5. 按 `docs/从零到一搭建指南.md` 将后端部署成 HTTPS API，在 Dify 内配置 DeepSeek、知识库和 Chatflow。
6. 将 `knowledge/demo_hotel_policies.md` 上传 Dify 知识库，参考 `dify_snippets/` 配置 Code 节点。
7. 用 `tests/eval_cases.jsonl` 逐条验证，记录真实结果；再发布 Dify Web App。

**注意**：`smoke_test.py` 会真实创建一张**模拟**工单（并在本地库中留下一条记录）。重复执行会增加新工单。不要用真实客人信息。

## 文件速查

| 路径 | 作用 |
|---|---|
| `backend/app.py` | FastAPI + SQLite：创建、查询、变更工单状态 |
| `backend/requirements.txt` | 运行依赖 |
| `backend/requirements-dev.txt` | 本地自动测试依赖 |
| `backend/.env.example` | 环境变量模板（不是实际密钥） |
| `knowledge/demo_hotel_policies.md` | 中英双语的**虚构**酒店政策 |
| `dify_snippets/` | Dify 校验、确认后 payload 生成、成功响应解析 |
| `docs/从零到一搭建指南.md` | Dify 各节点连接与部署的完整中文教程 |
| `docs/PRD_MVP.md` | 简版产品需求文档 |
| `docs/接口设计及状态规则.md` | API、业务流程、错误处理与工单状态机 |
| `tests/eval_cases.jsonl` | 30 条合成用例 |
| `tests/test_backend.py` | 后端可自动运行的单元/接口测试 |
| `scripts/smoke_test.py` | 启动后的一键连通性检查与建单验证 |

## 项目范围及注意事项

- 使用的酒店、住客、房号、政策都是虚构的；不接入真实 PMS、预订、库存和员工系统。
- Dify Cloud **不能访问**你电脑上的 localhost；完整联动演示需部署为公网可访问的 HTTPS 接口。
- 密钥不要提交 GitHub、写入 README 或暴露给浏览器前端。公网 demo 后端仍不具备企业级限流、身份认证和租户隔离；仅用于短期学习演示。
- 未经用户确认不得创建工单；API 错误时不能编造成功工单号。
- Render 等平台的临时文件系统**不保证** SQLite 重启后持久化。面试演示前做一次 API 健康检查并准备模拟数据。
- 对外简历中只描述已实际搭建和测试完成的功能，测试指标必须使用真实测量结果。
