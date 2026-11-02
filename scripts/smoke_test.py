"""Demo API smoke test, Python stdlib only.

Run while API is started:
  python scripts/smoke_test.py --base-url http://127.0.0.1:8000
Reads STAYPILOT_API_KEY from environment. POST creates a new simulated ticket.
"""
import argparse
import json
import os
import sys
import urllib.error
import urllib.request
import uuid


def request(base, method, path, data=None, key=None):
    headers = {"Accept": "application/json"}
    if key:
        headers["X-API-Key"] = key
    payload = None
    if data is not None:
        headers["Content-Type"] = "application/json"
        payload = json.dumps(data, ensure_ascii=False).encode("utf-8")
    req = urllib.request.Request(base.rstrip("/") + path, data=payload, headers=headers, method=method)
    with urllib.request.urlopen(req, timeout=30) as response:
        return response.status, json.load(response)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--base-url", default="http://127.0.0.1:8000")
    args = parser.parse_args()
    key = os.environ.get("STAYPILOT_API_KEY")
    if not key:
        sys.exit("请先在当前终端设置 STAYPILOT_API_KEY，再运行此脚本。")
    try:
        code, result = request(args.base_url, "GET", "/health")
        assert code == 200 and result["ok"] is True
        print("[PASS] health:", result)
        item = {"request_id": "smoke-" + uuid.uuid4().hex[:10],
                "room_number": "1208", "category": "housekeeping",
                "summary": "模拟送两瓶水", "quantity": 2,
                "priority": "normal", "confirmed": True}
        code, created = request(args.base_url, "POST", "/tickets", item, key)
        assert code == 201 and created["ticket_id"].startswith("WO-")
        print("[PASS] create:", created["ticket_id"])
        code, fetched = request(args.base_url, "GET", "/tickets/" + created["ticket_id"], key=key)
        assert code == 200 and fetched["ticket_id"] == created["ticket_id"]
        print("[PASS] query:", fetched["status"], fetched["department"])
        print("全部通过。该请求产生了一条模拟工单。")
    except (urllib.error.HTTPError, urllib.error.URLError, AssertionError, KeyError) as exc:
        sys.exit("[FAIL] 接口验证失败：" + str(exc))

if __name__ == "__main__":
    main()
