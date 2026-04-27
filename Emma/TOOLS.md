# TOOLS.md - Local Notes

Skills define _how_ tools work. This file is for _your_ specifics — the stuff that's unique to your setup.

## What Goes Here

Things like:

- Camera names and locations
- SSH hosts and aliases
- Preferred voices for TTS
- Speaker/room names
- Device nicknames
- Composio CLI configurations
- Email and cloud service access
- Anything environment-specific

### Composio CLI Configuration

**Location:** Installed globally via npm: `npm install -g @composio/cli`

**Configuration Details:**
- **CLI Tool:** `composio` command available system-wide
- **Authentication:** Uses OAuth tokens stored in `~/.composio/config.json`
- **Tool Discovery:** Built-in search and discovery capabilities
- **Status:** ✅ Installed and working

**How to Use Composio CLI:**

```bash
# Search for available tools
composio search gmail

# List available connections
composio connections list

# Connect a new service
composio link gmail

# Execute a tool
composio execute GMAIL_SEND_EMAIL -d '{
  "to": "faisal.homodi@gmail.com",
  "subject": "Test Email",
  "body": "Hello from Composio!"
}'

# Get tool schema
composio execute GMAIL_SEND_EMAIL --get-schema

# Dry run (see what would be executed)
composio execute GMAIL_SEND_Tools --dry-run -d '{
  "to": "faisal.homodi@gmail.com",
  "subject": "Test Email",
  "body": "Hello from Composio!"
}'
```

**How to Verify Connection:**
Run `composio connections list` to see all connected services and their status.

**Available Tools (100+):**
- **Gmail:** `GMAIL_SEND_EMAIL`, `GMAIL_CREATE_DRAFT`, `GMAIL_FIND_EMAIL`, etc.
- **Google Calendar:** `GOOGLE_CALENDAR_CREATE_EVENT`, `GOOGLE_CALENDAR_FIND_EVENTS`, etc.
- **Google Drive:** `GOOGLE_DRIVE_UPLOAD_FILE`, `GOOGLE_DRIVE_FIND_FILE`, `GOOGLE_DRIVE_CREATE_FOLDER`, etc.
- **Dropbox:** `DROPBOX_UPLOAD_FILE`, `DROPBOX_FIND_FILE`, `DROPBOX_CREATE_FOLDER`, etc.
- **Many more services:** GitHub, Slack, Notion, Twitter, Salesforce, etc.

### Service Access via Composio

**Primary Services:**
- **Gmail (email):** Use `GMAIL_*` tools for email operations
- **Google Drive (gdrive):** Use `GOOGLE_DRIVE_*` tools for file operations  
- **Google Calendar (gcalendar/gcal):** Use `GOOGLE_CALENDAR_*` tools for calendar operations
- **Dropbox:** Use `DROPBOX_*` tools for storage and file operations

**Tool Usage Pattern:**
- Structured JSON parameters with clear schema
- Built-in validation and error handling
- Native CLI interface with auto-completion
- Real-time event listening capabilities
- Comprehensive logging and debugging

### Secrets Configuration

**Location:** `/home/faisal/.openclaw/secrets.json`
**Composio Configuration:** Stored in `~/.composio/config.json` with OAuth tokens
**Format:** JSON configuration with service connections
**Status:** ✅ Configured and working

### Composio CLI Integration

**Location:** Global installation via npm
**Configuration:** Managed through `composio` CLI commands
**Tool Registration:** Built-in tool discovery and execution
**Service Management:** Direct CLI interface with OAuth authentication

## Examples

```markdown
### Cameras

- living-room → Main area, 180° wide angle
- front-door → Entrance, motion-triggered

### SSH

- home-server → 192.168.1.100, user: admin
- composio-demo → Example server for Composio testing

### TTS

- Preferred voice: "Nova" (warm, slightly British)
- Default speaker: Kitchen HomePod

### Secrets

- Location: `/home/faisal/.openclaw/secrets.json` (managed by OpenClaw)
- Format: JSON with service sections (channels, gateway, profiles, ngrok, gmail, github, composio)
- Contains: Ngrok auth token, Gmail OAuth tokens, API keys, auth tokens
- DO NOT commit - this file is already outside the workspace git repo
- Reference: `mem/SECRETS.md` for full documentation

### Composio

- **Gmail:** Connected via OAuth for email operations
- **Google Drive:** Connected for file upload/download operations
- **Dropbox:** Connected for file storage operations
- **Configuration:** Managed through `~/.composio/config.json`
- **Usage:** `composio execute TOOL_NAME -d '{"param": "value"}'`

## Why Separate?

Skills are shared. Your setup is yours. Keeping them apart means you can update skills without losing your notes, and share skills without leaking your infrastructure.

---

Add whatever helps you do your job. This is your cheat sheet.
