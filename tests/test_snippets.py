from pathlib import Path
import importlib.util

ROOT = Path(__file__).resolve().parents[1]


def load_script(name):
    path = ROOT / "dify_snippets" / name
    spec = importlib.util.spec_from_file_location(name.replace(".py", ""), path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def test_ticket_validation():
    check = load_script("validate_ticket.py").main
    good = check(room_number="1208", category="housekeeping", summary="送两瓶水", quantity=2)
    assert good["valid"] and good["quantity"] == 2
    missing = check(room_number="", category="housekeeping", summary="送两瓶水", quantity=2)
    assert missing["valid"] is False
    assert "房号" in missing["error"]
    bad_count = check(room_number="1208", category="housekeeping", summary="送两瓶水", quantity=30)
    assert not bad_count["valid"]


def test_approved_payload():
    build = load_script("build_payload_after_approval.py").main
    result = build("1208", "maintenance", "空调不制冷", 1, "workflow-001")
    import json
    payload = json.loads(result["payload_json"])
    assert payload["request_id"] == "workflow-001"
    assert payload["confirmed"] is True


def test_response_validation():
    parse = load_script("parse_ticket_response.py").main
    assert parse('{"ticket_id":"WO-ABC12345","status":"open"}')["success"]
    assert parse('{"status":"open"}')["success"] is False
