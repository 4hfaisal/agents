# Agent Config Sync Skill

Bidirectional synchronization of agent configuration files between local OpenClaw workspace and GitHub repository.

## Features

- **Push to GitHub**: Sync local agent files to GitHub repository
- **Pull from GitHub**: Sync agent files from GitHub to local workspace  
- **Selective Sync**: Sync specific agents or all agents at once
- **Git Integration**: Uses git for version control operations

## Usage

### Sync to GitHub
```bash
sync-to-github [agent-names...]
```

### Sync from GitHub
```bash
sync-from-github [agent-names...]
```

### List Agents
```bash
list-agents
```

## Supported Agents

- **Kodee**: Main AI assistant (includes openclaw.json)
- **KodeeSpark**: Spark variant
- **Emma**: Emma agent
- **Govy**: Govy agent

## Files Managed

- `openclaw.json` - Main configuration (Kodee only)
- `SOUL.md` - Agent identity and principles
- `TOOLS.md` - Local tool configurations
- `USER.md` - User information

## Setup

1. Clone the agents repository:
   ```bash
   git clone https://github.com/4hfaisal/agents.git
   ```

2. Ensure GitHub credentials are configured

3. Use the sync scripts as needed

## Examples

Sync Kodee files to GitHub:
```bash
sync-to-github kodee
```

Sync all agents from GitHub:
```bash
sync-from-github all
```

Check available agents:
```bash
list-agents
```

## Notes

- Kodee is the only agent that includes `openclaw.json`
- Other agents sync only `SOUL.md`, `TOOLS.md`, and `USER.md`
- Repository structure: `/agents/{agent-name}/`
- Scripts are located in `scripts/` directory