#!/usr/bin/env python3
import json
import re
import sys

SENSITIVE_PATH_RE = re.compile(
    r"""(?ix)
    (?:^|[/\\])\.env(?:\.[\w-]+)?$ |
    (?:^|[/\\])\.env(?:\.[\w-]+)? |
    credentials |
    id_rsa$ | id_ed25519$ | id_dsa$ | id_ecdsa$ |
    \.pem$ | \.key$ |
    (?:^|[/\\])\.aws[/\\] |
    (?:^|[/\\])\.ssh[/\\] |
    secrets?(?:\.\w+)?$
    """
)

SECRET_PATTERNS = [
    re.compile(r"AKIA[0-9A-Z]{16}"),
    re.compile(r"sk-[A-Za-z0-9]{20,}"),
    re.compile(r"sk_live_[A-Za-z0-9]{10,}"),
    re.compile(r"gh[pousr]_[A-Za-z0-9]{20,}"),
    re.compile(r"Bearer\s+[A-Za-z0-9\-._~+/]{10,}=*", re.IGNORECASE),
    re.compile(r"[\w.+-]+@[\w-]+\.[\w.-]+"),
]


def deny(reason):
    print(json.dumps({
        "hookSpecificOutput": {
            "hookEventName": "PreToolUse",
            "permissionDecision": "deny",
            "permissionDecisionReason": reason,
        }
    }))
    sys.exit(0)


def allow_with_redacted_command(tool_input, redacted_command):
    updated = dict(tool_input)
    updated["command"] = redacted_command
    print(json.dumps({
        "hookSpecificOutput": {
            "hookEventName": "PreToolUse",
            "permissionDecision": "allow",
            "updatedInput": updated,
        }
    }))
    sys.exit(0)


def redact(text):
    redacted = text
    found = False
    for pattern in SECRET_PATTERNS:
        if pattern.search(redacted):
            found = True
            redacted = pattern.sub("[REDACTED]", redacted)
    return redacted, found


def main():
    try:
        payload = json.load(sys.stdin)
    except (json.JSONDecodeError, ValueError):
        sys.exit(0)

    tool_name = payload.get("tool_name", "")
    tool_input = payload.get("tool_input", {}) or {}

    if tool_name == "Read":
        file_path = tool_input.get("file_path", "")
        if file_path and SENSITIVE_PATH_RE.search(file_path):
            deny(f"Blocked reading a file that looks like a secrets/credentials file: {file_path}")
        sys.exit(0)

    if tool_name == "Bash":
        command = tool_input.get("command", "")
        if not command:
            sys.exit(0)

        if SENSITIVE_PATH_RE.search(command):
            deny("Blocked a command that appears to reference a secrets/credentials file.")

        redacted_command, found = redact(command)
        if found:
            allow_with_redacted_command(tool_input, redacted_command)

        sys.exit(0)

    sys.exit(0)


if __name__ == "__main__":
    main()
