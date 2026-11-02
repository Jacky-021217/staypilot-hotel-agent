"""Dify Code 节点：仅用于 HTTP 成功状态（201）后解析真实响应。

输入: response_body (String), 映射 HTTP Request.body
输出: success(Boolean), ticket_id(String), status(String), error(String)
当响应缺少编号时，不允许宣称创建成功。
"""
import json


def main(response_body):
    try:
        data = json.loads(response_body) if isinstance(response_body, str) else response_body
        if not isinstance(data, dict):
            raise ValueError("Response body must be an object")
        ticket_id = data.get("ticket_id")
        status = data.get("status", "")
        if not isinstance(ticket_id, str) or not ticket_id.startswith("WO-"):
            raise ValueError("Missing valid ticket id")
        return {"success": True, "ticket_id": ticket_id, "status": str(status), "error": ""}
    except (ValueError, TypeError, json.JSONDecodeError) as exc:
        return {"success": False, "ticket_id": "", "status": "", "error": str(exc)}
