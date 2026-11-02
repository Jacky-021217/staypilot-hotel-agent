"""Use ONLY on Human Input's Approve branch, just before HTTP Request.
Declare Code inputs room_number/category/summary/quantity from Validate node;
request_id from sys.workflow_run_id. Declare output payload_json(String).
"""
import json


def main(room_number: str, category: str, summary: str, quantity: int, request_id: str) -> dict:
    payload = {
        "request_id": request_id,
        "room_number": room_number,
        "category": category,
        "summary": summary,
        "quantity": int(quantity),
        "priority": "normal",
        "confirmed": True,
    }
    return {"payload_json": json.dumps(payload, ensure_ascii=False)}
