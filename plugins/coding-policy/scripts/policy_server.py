#!/usr/bin/env python3
"""Small, dependency-free, read-only MCP stdio server for the demo policy catalog."""
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
VERSION = json.loads((ROOT / ".codex-plugin/plugin.json").read_text())["version"]
PROTOCOLS = ("2024-11-05", "2025-03-26", "2025-06-18", "2025-11-25")
ANNOTATIONS = {"readOnlyHint": True, "destructiveHint": False,
               "idempotentHint": True, "openWorldHint": False}
TOOLS = [
    {"name": "get_policy", "description": "Read the versioned Cyberdyne shared workflow or review policy. Repository AGENTS.md owns domain rules.",
     "inputSchema": {"type": "object", "properties": {"topic": {"type": "string", "enum": ["workflow", "review"]}},
                     "required": ["topic"], "additionalProperties": False}, "annotations": ANNOTATIONS},
    {"name": "get_pr_template", "description": "Read the fallback Cyberdyne PR template. Prefer a repository's own template when present.",
     "inputSchema": {"type": "object", "properties": {}, "additionalProperties": False}, "annotations": ANNOTATIONS}
]


class RpcError(Exception):
    def __init__(self, code, message):
        self.code, self.message = code, message


def dispatch(method, params):
    if method == "initialize":
        requested = params.get("protocolVersion")
        return {"protocolVersion": requested if requested in PROTOCOLS else PROTOCOLS[-1],
                "capabilities": {"tools": {"listChanged": False}},
                "serverInfo": {"name": "cyberdyne-policy", "version": VERSION}}
    if method == "ping":
        return {}
    if method == "tools/list":
        return {"tools": TOOLS}
    if method != "tools/call":
        raise RpcError(-32601, "Method not found")
    name, args = params.get("name"), params.get("arguments", {})
    if not isinstance(args, dict):
        raise RpcError(-32602, "arguments must be an object")
    if name == "get_policy":
        if set(args) != {"topic"} or args["topic"] not in ("workflow", "review"):
            raise RpcError(-32602, "topic must be workflow or review; no extra arguments")
        filename = args["topic"] + ".md"
    elif name == "get_pr_template":
        if args:
            raise RpcError(-32602, "get_pr_template accepts no arguments")
        filename = "pr-template.md"
    else:
        raise RpcError(-32602, "Unknown tool")
    try:
        content = (ROOT / "policy" / filename).read_text()
    except OSError:
        return {"isError": True, "content": [{"type": "text", "text": "Bundled policy unavailable; inspect the plugin installation."}]}
    return {"content": [{"type": "text", "text": f"Source: coding-policy {VERSION}/policy/{filename}\n\n{content}"}], "isError": False}


def handle(line):
    request_id = None
    try:
        try:
            message = json.loads(line)
        except json.JSONDecodeError:
            raise RpcError(-32700, "Parse error")
        if not isinstance(message, dict) or message.get("jsonrpc") != "2.0" or not isinstance(message.get("method"), str):
            raise RpcError(-32600, "Invalid Request")
        if "id" not in message:
            return None
        request_id = message["id"]
        if isinstance(request_id, bool) or not isinstance(request_id, (str, int)):
            request_id = None
            raise RpcError(-32600, "Invalid request id")
        params = message.get("params", {})
        if not isinstance(params, dict):
            raise RpcError(-32602, "params must be an object")
        return {"jsonrpc": "2.0", "id": request_id, "result": dispatch(message["method"], params)}
    except RpcError as error:
        return {"jsonrpc": "2.0", "id": request_id, "error": {"code": error.code, "message": error.message}}


def main():
    for line in sys.stdin:
        reply = handle(line)
        if reply is not None:
            print(json.dumps(reply), flush=True)


if __name__ == "__main__":
    main()
