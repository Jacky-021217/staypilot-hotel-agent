> **首次解压请优先阅读 [START_HERE_先看我.md](START_HERE_先看我.md)**（含最快启动和文件速查）。

# StayPilot — 酒店 AI 服务工单 Agent 起步包

> 面向 AI 产品经理求职的演示 MVP。知识库、业务规则、用例与工单均为虚构样例。**这不是已经完成的 Dify Agent**；需要按下列步骤自行搭建、测试并录制演示。

**从零搭建详细版：** [`docs/从零到一搭建指南.md`](docs/从零到一搭建指南.md)。Dify 代码节点可直接复制 `dify_snippets/` 下的两个 `main()` 函数。

## 目录
- `knowledge/demo_hotel_policies.md`：中英双语虚构酒店规则，可直接导入 Dify Knowledge。
- `backend/app.py`：可运行的简单 FastAPI + SQLite 工单 API。
- `backend/requirements.txt`：Python 依赖。
- `docs/PRD_MVP.md`：产品目标、用户角色、P0/P1、验收与指标。
- `docs/从零到一搭建指南.md`：详细安装、Dify 节点配置、Render 部署、测试与 GitHub 发布。
- `dify_snippets/`：可直接粘贴到 Dify Code 节点的字段验证与批准后 Payload 构造代码。
- `tests/eval_cases.jsonl`：30 条合成测试样例（中英文、服务、异常和复杂场景）。

## A. 最快 Dify 路线
1. 在 Dify 创建 `Chatflow`，连接已配置好的可用模型（如你现有的 DeepSeek 模型供应商）。
2. Knowledge 新建知识库并上传 `knowledge/demo_hotel_policies.md`。按检索模型实际可用性选择索引模式并测试召回。
3. Chatflow 添加 `Question Classifier`，分类：`faq`、`service`、`complaint`、`emergency`、`other`。明确分类边界。
4. `faq` → `Knowledge Retrieval` → `LLM`（引用检索内容，只回答有依据的信息）→ `Answer`。
5. `service` → `Parameter Extractor`，字段如 `room_number`、`category`、`summary`、`quantity`、`language`。加入 `If/Else` 验证缺失字段。
6. **获取确认**：可用 `Human Input` 节点显示确认表单，或者用 Chatflow Conversation Variables + Variable Assigner 实现多轮确认。确保“确认”不会被误认成一条新服务请求。确认信息和原始请求必须匹配。
7. 仅在明确确认后 `HTTP Request` → `POST /tickets`，设置 `X-API-Key`。接口成功后读取后端返回的 `ticket_id` 回复，其他情况提示失败或人工服务。
8. `complaint` 和 `emergency` 分支提供人工处理及紧急提示，不能假装已经联系真人。
9. 按 JSONL 案例测试并记录**实际**正确数、错误案例、修复前后指标。
10. Publish 发布可演示的 Web App，导出 DSL，截图工作流，放入 GitHub（去掉所有密钥与真实数据）。

**区别：** Chatflow + HTTP 的路线是“工作流编排的 Agentic 应用”；如希望简历严谨称 Tool Calling，必须确实由 Agent/工具调用功能完成动态工具选择，不应把普通 HTTP 节点一概描述为自主 Tool Calling。

## B. 本地运行工单 API（Windows PowerShell）
```powershell
cd backend
py -3.11 -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
$env:STAYPILOT_API_KEY="replace-with-a-long-secret"
uvicorn app:app --reload --port 8000
```
在浏览器打开 `http://127.0.0.1:8000/docs`，用 `POST /tickets` 进行本地测试。发送请求必须附 `X-API-Key`。示例 Body：
```json
{
  "request_id": "demo-req-001",
  "room_number": "1208",
  "category": "maintenance",
  "summary": "Air conditioner is not cooling",
  "quantity": 1,
  "priority": "normal",
  "confirmed": true
}
```
接口将返回真实生成的 `ticket_id`（不是固定的例子 ID），并保存到本地 SQLite。相同 `request_id` 可避免重复建单。请求未确认或字段缺失会返回错误。`PATCH /tickets/{ticket_id}` 可演示工单状态流转。

**注意：** Dify Cloud 无法直接请求你电脑本地的 `localhost`。要连接云端 Dify，需自行将 API 安全部署到公网可访问的 HTTPS 服务；或先用你自己创建的云端 Mock API 做早期演示（这种方式须如实标记为模拟，不等于已持久化到正式酒店系统）。不要向公网暴露无认证的 API。API Key 应存 Dify 的密钥配置中，不放在仓库或前端。

## C. 两个优先演示案例
- 用例一：`What time is breakfast?` → 查知识库 → 给出 06:30–10:00，并说明是演示酒店政策。
- 用例二：`Room 1208 AC isn't working` → 维修意图 → 参数抽取 → 显示确认 → 用户批准 → HTTP 创建 → 返回真实工单 ID → 查询状态。

## D. 适合 GitHub 的材料
- 项目 README、架构图、产品 PRD。
- Dify 导出的 DSL（不含 API Key）、工作流截图。
- 演示视频/动图、失败案例、评估表。
- 模型名称、版本、测试日期、测试用例规模和**实际**指标。

## E. 面试时须说明的边界
仅针对单个虚构酒店；不连接真实 PMS/SaaS、实时入住/库存、预订或酒店员工系统。工单接口模拟，但真实执行了 POST 并完成本地持久化；消息路由与确认规则需要你在 Dify 内实际实现并测试后才可在简历中写“已完成”。


## F. 可运行自动测试与补充资料

后端和 Dify Code 代码均配有本地测试。从项目根目录执行：

```powershell
python -m pip install -r backend/requirements-dev.txt
python -m pytest -q
```

其他新增内容：`scripts/smoke_test.py`（真实调用已启动 API）、`dify_snippets/parse_ticket_response.py`（解析成功编号）、`docs/接口设计及状态规则.md`（错误码、状态流转）、`docs/真实测试记录模板.csv`（记录真实评估结果）。
