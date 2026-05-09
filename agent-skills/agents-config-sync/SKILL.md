---
skill-kind: custom
owner: Faisal Al Homodi
created: 2026-04-27
last-updated: 2026-04-27
category: [development, tools, git, configuration]
name: agents-config-sync
description: Bidirectional sync of agent configuration files with GitHub
---

# Skill: Agent Config Sync

Sync agent configuration files bidirectionally between local OpenClaw workspace and GitHub repository.

## Description

This skill manages bidirectional synchronization of agent configuration files between the local OpenClaw workspace and a GitHub repository. It handles copying files to GitHub (push) and pulling updates from GitHub (pull) for specific agents.

## Usage

### Sync to GitHub (Push)
```bash
sync-to-github [agent-names...]
```

### Sync from GitHub (Pull)  
```bash
sync-from-github [agent-names...]
```

### List Available Agents
```bash
list-agents
```

## Files Managed

- `openclaw.json` - Agent configuration (only for Kodee)
- `SOUL.md` - Core identity and principles
- `TOOLS.md` - Local notes and tool configurations
- `USER.md` - User information

## Setup

1. Ensure GitHub repository is cloned locally
2. Configure GitHub personal access token in secrets
3. Set up git user credentials

## Examples

Sync Kodee files to GitHub:
```bash
sync-to-github kodee
```

Sync all agents from GitHub:
```bash
sync-from-github all
```

## Notes

- Kodee gets `openclaw.json` while other agents don't
- Repository structure: `/agents/{agent-name}/`
- Uses git for version control operations