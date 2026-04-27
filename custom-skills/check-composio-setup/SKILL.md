---
skill-kind: custom
owner: Faisal Al Homodi
created: 2026-04-26
category: [development, tools, composio]
---

# Composio CLI Verification and Installation

## Description
Checks if the Composio CLI is installed and functional. If missing or not working, it automatically installs the CLI and logs the installation steps.

## Prerequisites
- Internet connectivity
- Permissions to run shell commands (sudo may be required)

## Usage
```bash
# Run a quick check
check_composio_cli
```

## Procedure
1. **Check Presence**
   - `which composio` or `composio -v` to confirm CLI binary and version.
2. **Validate Connection**
   - Run `composio login --status` or attempt a simple tool execution.
3. **Install if Missing**
   - Run `curl -fsSL https://composio.dev/install | bash`.
4. **Post‑Install Verification**
   - Re‑run version check and attempt a lightweight tool call.

## Dependencies
- Bash
- `curl`
- `sudo` (if required for install)

## Logging
All install/download logs are appended to `logs/composio_cli_setup.log`.