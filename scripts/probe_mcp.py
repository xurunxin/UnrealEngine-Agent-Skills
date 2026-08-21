from __future__ import annotations

import argparse
import json
import sys
import urllib.error
import urllib.request
from dataclasses import dataclass
from typing import Any

PROTOCOL_VERSION = "2025-06-18"


@dataclass
class Response:
    payload: dict[str, Any] | None
    session_id: str | None
    status: int


def parse_payload(raw: bytes, content_type: str) -> dict[str, Any] | None:
    text = raw.decode("utf-8", errors="replace").strip()
    if not text:
        return None
    if "text/event-stream" in content_type:
        payloads = []
        for line in text.splitlines():
            if line.startswith("data:"):
                data = line[5:].strip()
                if data:
                    payloads.append(json.loads(data))
        return payloads[-1] if payloads else None
    return json.loads(text)


def post(url: str, message: dict[str, Any], timeout: float, session_id: str | None = None) -> Response:
    headers = {
        "Content-Type": "application/json",
        "Accept": "application/json, text/event-stream",
        "MCP-Protocol-Version": PROTOCOL_VERSION,
        "User-Agent": "ue5-agent-skills-probe/0.1.0",
    }
    if session_id:
        headers["Mcp-Session-Id"] = session_id
    request = urllib.request.Request(
        url,
        data=json.dumps(message).encode("utf-8"),
        headers=headers,
        method="POST",
    )
    with urllib.request.urlopen(request, timeout=timeout) as response:
        content_type = response.headers.get("Content-Type", "")
        return Response(
            payload=parse_payload(response.read(), content_type),
            session_id=response.headers.get("Mcp-Session-Id") or session_id,
            status=response.status,
        )


def main() -> int:
    parser = argparse.ArgumentParser(description="Read-only initialize/tools-list probe for a local MCP endpoint.")
    parser.add_argument("--url", default="http://127.0.0.1:8000/mcp")
    parser.add_argument("--timeout", type=float, default=10.0)
    parser.add_argument("--json", action="store_true")
    parser.add_argument("--expect-meta-tools", action="store_true", help="Require list_toolsets, describe_toolset, and call_tool.")
    args = parser.parse_args()

    if not (args.url.startswith("http://127.0.0.1:") or args.url.startswith("http://localhost:")):
        print("Refusing to probe a non-loopback URL. Use a separately reviewed client for remote MCP.", file=sys.stderr)
        return 2

    try:
        initialize = post(
            args.url,
            {
                "jsonrpc": "2.0",
                "id": 1,
                "method": "initialize",
                "params": {
                    "protocolVersion": PROTOCOL_VERSION,
                    "capabilities": {},
                    "clientInfo": {"name": "ue5-agent-skills-probe", "version": "0.1.0"},
                },
            },
            args.timeout,
        )
        if not initialize.payload or "result" not in initialize.payload:
            raise RuntimeError(f"initialize did not return a result: {initialize.payload}")

        # Notification has no id; a 202/204 or empty response is valid.
        post(
            args.url,
            {"jsonrpc": "2.0", "method": "notifications/initialized", "params": {}},
            args.timeout,
            initialize.session_id,
        )
        listed = post(
            args.url,
            {"jsonrpc": "2.0", "id": 2, "method": "tools/list", "params": {}},
            args.timeout,
            initialize.session_id,
        )
        tools = (listed.payload or {}).get("result", {}).get("tools", [])
        names = [str(item.get("name")) for item in tools]
        expected = {"list_toolsets", "describe_toolset", "call_tool"}
        missing = sorted(expected - set(names)) if args.expect_meta_tools else []
        result = {
            "ok": not missing,
            "url": args.url,
            "protocol_version": initialize.payload["result"].get("protocolVersion"),
            "server_info": initialize.payload["result"].get("serverInfo"),
            "session_id_present": bool(initialize.session_id),
            "tool_count": len(names),
            "tools": names,
            "missing_expected_meta_tools": missing,
        }
    except (urllib.error.URLError, urllib.error.HTTPError, TimeoutError, ValueError, RuntimeError, json.JSONDecodeError) as exc:
        print(f"MCP probe failed: {exc}", file=sys.stderr)
        return 1

    if args.json:
        print(json.dumps(result, ensure_ascii=False, indent=2))
    else:
        print(f"MCP initialize PASS: {result['server_info']}")
        print(f"tools/list PASS: {result['tool_count']} tool(s)")
        for name in result["tools"]:
            print(f"- {name}")
        if missing:
            print(f"Missing expected meta-tools: {', '.join(missing)}", file=sys.stderr)
    return 0 if result["ok"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
