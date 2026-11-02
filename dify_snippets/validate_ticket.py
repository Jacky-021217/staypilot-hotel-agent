"""Paste the main() function into a Dify Code node.
Declare inputs: room_number, category, summary, quantity (from Parameter Extractor).
Declare outputs: valid(Boolean), error(String), room_number(String),
category(String), summary(String), quantity(Number), preview(String).
"""
import re


def main(room_number=None, category=None, summary=None, quantity=None) -> dict:
    room = str(room_number or "").strip()
    cat = str(category or "").strip().lower()
    description = str(summary or "").strip()
    try:
        count = int(quantity) if quantity not in (None, "") else 1
    except (TypeError, ValueError):
        count = -1

    errors = []
    if not re.fullmatch(r"[0-9A-Za-z-]{2,8}", room):
        errors.append("请提供有效房号（2–8位字母、数字或连字符）")
    if cat not in ("housekeeping", "maintenance"):
        errors.append("无法确认服务类型（客房用品/设施维修）")
    if len(description) < 3 or len(description) > 500:
        errors.append("请描述具体需求（3–500字符）")
    if not 1 <= count <= 20:
        errors.append("数量须为1–20")

    name = {"housekeeping": "客房服务部", "maintenance": "工程维修部"}.get(cat, "待确认")
    preview = f"房号：{room or '未提供'}\n部门：{name}\n需求：{description or '未提供'}\n数量：{count if count > 0 else '待确认'}"
    return {
        "valid": not errors,
        "error": "；".join(errors),
        "room_number": room,
        "category": cat,
        "summary": description,
        "quantity": count,
        "preview": preview,
    }
