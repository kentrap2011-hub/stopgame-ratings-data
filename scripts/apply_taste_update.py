import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PROFILE = ROOT / "gaming_taste_live.json"
REQUEST = ROOT / ".github" / "taste_update_request.json"


def load(path):
    with path.open("r", encoding="utf-8") as f:
        return json.load(f)


def save(path, data):
    with path.open("w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
        f.write("\n")


profile = load(PROFILE)
request = load(REQUEST)
if not request.get("pending"):
    print("No pending taste update")
    raise SystemExit(0)

request_id = request["request_id"]
applied = profile.setdefault("applied_update_ids", [])
if request_id in applied:
    request["pending"] = False
    save(REQUEST, request)
    print("Update already applied")
    raise SystemExit(0)

for op in request.get("operations", []):
    kind = op["op"]
    path = op.get("path", [])
    if kind == "append":
        cur = profile
        for key in path[:-1]:
            cur = cur.setdefault(key, {})
        arr = cur.setdefault(path[-1], [])
        arr.append(op["value"])
    elif kind == "set":
        cur = profile
        for key in path[:-1]:
            cur = cur.setdefault(key, {})
        cur[path[-1]] = op["value"]
    elif kind == "replace_matching":
        cur = profile
        for key in path[:-1]:
            cur = cur.setdefault(key, {})
        arr = cur.setdefault(path[-1], [])
        match = op["match"]
        replaced = False
        for i, item in enumerate(arr):
            if isinstance(item, dict) and all(item.get(k) == v for k, v in match.items()):
                arr[i] = op["value"]
                replaced = True
                break
        if not replaced:
            raise ValueError(f"No matching list item for {match}")
    else:
        raise ValueError(f"Unsupported op: {kind}")

profile["updated_at"] = request.get("updated_at", profile.get("updated_at"))
applied.append(request_id)
request["pending"] = False
save(PROFILE, profile)
save(REQUEST, request)
print(f"Applied taste update {request_id}")
