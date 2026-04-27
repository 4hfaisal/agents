---
skill-kind: custom
owner: Faisal Al Homodi
created: 2026-04-04
last-updated: 2026-04-10
category: [portfolio, finance, mcp, agents]
name: portfolio-manager
description: Interact with Faisal's personal investment portfolio via the Portfolio Manager MCP server. Read holdings, P&L, WACC, contacts, and reports. Record transactions, update positions, add loans and contacts, and generate PDF/email reports. Also contains full deployment procedures for setting up the app from scratch on a new Linux (Debian/Ubuntu) server.
---

# Portfolio Manager Skill

## Overview

This skill covers two modes:

1. **Interact** — use the MCP server to read and update the portfolio (most common)
2. **Deploy** — install and run the full app stack on a new server from the GitHub repo

---

## Part A: Deployment (new server setup)

Use this when the portfolio app is not yet running on the target machine.

### A1 — Prerequisites check

Run these to confirm the environment:

```bash
# Check OS
cat /etc/os-release | grep -E "^(NAME|VERSION_ID)"

# Check Docker
docker --version 2>/dev/null || echo "Docker not installed"
docker compose version 2>/dev/null || echo "Docker Compose not installed"

# Check Git
git --version 2>/dev/null || echo "Git not installed"
```

### A2 — Install Docker (Debian/Ubuntu)

Skip if Docker is already installed. Run as root or with sudo:

```bash
# Remove any old versions
apt-get remove -y docker docker-engine docker.io containerd runc 2>/dev/null || true

# Install dependencies
apt-get update
apt-get install -y ca-certificates curl gnupg lsb-release

# Add Docker's official GPG key
install -m 0755 -d /etc/apt/keyrings
curl -fsSL https://download.docker.com/linux/$(. /etc/os-release && echo "$ID")/gpg \
  | gpg --dearmor -o /etc/apt/keyrings/docker.gpg
chmod a+r /etc/apt/keyrings/docker.gpg

# Add Docker repository
echo \
  "deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/docker.gpg] \
  https://download.docker.com/linux/$(. /etc/os-release && echo "$ID") \
  $(lsb_release -cs) stable" \
  | tee /etc/apt/sources.list.d/docker.list > /dev/null

# Install Docker Engine + Compose plugin
apt-get update
apt-get install -y docker-ce docker-ce-cli containerd.io docker-buildx-plugin docker-compose-plugin

# Start and enable Docker
systemctl start docker
systemctl enable docker

# Verify
docker --version
docker compose version
```

### A3 — Install Git

```bash
apt-get install -y git
git --version
```

### A4 — Clone the repository

The repo is at `https://github.com/4hfaisal/portfolio-manager.git`.

```bash
# Choose install location
INSTALL_DIR="/opt/portfolio-manager"

git clone https://github.com/4hfaisal/portfolio-manager.git "$INSTALL_DIR"
cd "$INSTALL_DIR"
```

### A5 — Configure environment

The app uses environment variables for credentials. A template is provided:

```bash
cd "$INSTALL_DIR"

# Copy the example env file to the project root (where docker-compose reads it)
cp backend/.env.example .env

# Review and optionally edit passwords
cat .env
# POSTGRES_USER=portfolio
# POSTGRES_PASSWORD=portfolio     ← change this for production
# POSTGRES_DB=portfolio
# BASE_CURRENCY=USD
# PRICE_REFRESH_INTERVAL_HOURS=3
```

To change a value:
```bash
sed -i 's/POSTGRES_PASSWORD=portfolio/POSTGRES_PASSWORD=YOUR_SECURE_PASSWORD/' .env
```

### A6 — Build and start all containers

```bash
cd "$INSTALL_DIR"

# Build the backend image (pulls Python 3.12-slim + installs all pip deps)
docker compose build

# Start all three services: db, backend, frontend
docker compose up -d

# Watch startup logs (Ctrl+C to stop following)
docker compose logs -f
```

Expected startup sequence:
1. `portfolio_db` starts and becomes healthy (PostgreSQL ready)
2. `portfolio_backend` runs `alembic upgrade head` (creates all tables), then starts uvicorn on port 8000
3. `portfolio_frontend` runs `npm install` then `npm run dev` on port 3000

The first start takes 3–5 minutes (npm install + Docker image layers).

### A7 — Verify the stack is running

```bash
# All three containers should show "Up"
docker compose ps

# Backend health check
curl -s http://localhost:8000/health
# Expected: {"status":"ok"}

# Portfolio summary (confirms DB + backend are connected)
curl -s http://localhost:8000/api/portfolio/summary
# Expected: JSON with total_value_usd, unrealized_pl_usd, etc.

# Frontend (may take a minute for Next.js to compile)
curl -s -o /dev/null -w "%{http_code}" http://localhost:3000
# Expected: 200
```

### A8 — Seed initial data (first run only)

If starting with an empty database, run the seed script to populate the portfolio structure:

```bash
docker exec portfolio_backend python seed.py
```

This creates the asset class hierarchy, accounts, and positions. **Only run once** — it is not idempotent.

### A9 — Common troubleshooting

| Symptom | Fix |
|---------|-----|
| `portfolio_backend` exits immediately | Check `docker compose logs backend` — usually a DB connection error; wait for DB to be healthy |
| `npm install` hangs in frontend | Run `docker compose restart frontend` — the cache flag in the Compose file handles permission issues |
| Port 3000 or 8000 already in use | `lsof -i :3000` or `lsof -i :8000` to find the process; kill it or change the port in `docker-compose.yml` |
| `alembic upgrade head` fails | DB may already be at latest — check `docker compose logs backend \| grep alembic` |
| Price data shows "no data" | Normal on first boot; the price updater runs after a 5-minute delay and the backfill runs in the background |
| Benchmark chart empty | Wait ~60s after startup; benchmark backfill runs in a background thread on boot |

### A10 — Expose the app externally (optional)

To make the app accessible from outside the server, set up a reverse proxy. Using nginx:

```bash
apt-get install -y nginx

cat > /etc/nginx/sites-available/portfolio << 'EOF'
server {
    listen 80;
    server_name your-domain-or-ip;

    # Frontend
    location / {
        proxy_pass http://localhost:3000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }

    # Backend API
    location /api/ {
        proxy_pass http://localhost:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
}
EOF

ln -s /etc/nginx/sites-available/portfolio /etc/nginx/sites-enabled/
nginx -t && systemctl reload nginx
```

### A11 — Update to latest version

```bash
cd "$INSTALL_DIR"

git pull origin main
docker compose build backend
docker compose up -d backend
```

The frontend container volume-mounts the source and uses `npm run dev`, so it picks up code changes automatically. The backend needs a rebuild when `requirements.txt` changes.

### A12 — MCP server setup (for agent access)

The MCP server allows AI agents to interact with the portfolio programmatically.

```bash
# Install Python 3.10+ (required by the MCP package)
apt-get install -y python3.11 python3.11-venv

# Create virtualenv for MCP server
cd "$INSTALL_DIR/mcp-server"
python3.11 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

# Test the MCP server connects to the backend
PORTFOLIO_API_URL=http://localhost:8000 python server.py
```

To register the MCP server in Claude Code (`.mcp.json` at project root):

```json
{
  "mcpServers": {
    "portfolio-manager": {
      "command": "/opt/portfolio-manager/mcp-server/venv/bin/python",
      "args": ["/opt/portfolio-manager/mcp-server/server.py"],
      "env": {
        "PORTFOLIO_API_URL": "http://localhost:8000"
      }
    }
  }
}
```

If the app is on a remote server, replace `http://localhost:8000` with `http://<server-ip>:8000`.

---

## Part B: Using the MCP Server

### B1 — Establish the endpoint

**Before using any tools, confirm the MCP server is reachable.**

Check context for:
- An explicit `PORTFOLIO_API_URL` or `MCP_URL`
- A running Docker stack on `localhost:8000`
- A previously confirmed endpoint in the conversation

**If no endpoint is in context, ask:**

> "To access the portfolio, I need the Portfolio Manager API URL.
> The default is `http://localhost:8000` if running locally, or a remote URL if hosted.
> What URL should I use?"

### B2 — Tool quick reference

See `references/tools.md` for full parameter and return-type documentation.

| Intent | Tool |
|--------|------|
| Portfolio health check | `get_summary` |
| Browse / search all positions | `get_holdings` |
| Drill into one position | `get_position(position_id)` |
| Search by name or ticker | `search_portfolio(q)` |
| Allocation breakdown | `get_allocation` |
| Performance vs benchmarks | `get_performance(days)` |
| Best / worst positions | `get_top_movers(limit)` |
| P&L by asset class | `get_pl_by_class` |
| Realized vs unrealized split | `get_realized_vs_unrealized` |
| Monthly income history | `get_income_by_period` |
| Currency exposure | `get_currency_exposure` |
| IRR for illiquid positions | `get_irr` |
| Recent transactions | `get_recent_transactions(limit)` |
| Alerts (stale prices, loans) | `get_alerts` |
| Cost of capital | `get_wacc` |
| All contacts | `list_contacts` |
| All loans | `list_loans` |
| PDF reports | `list_reports` |
| Email (HTML) reports | `list_email_reports` |
| Ingestion history | `list_ingestion_logs` |
| Current settings | `get_settings` |
| Record a buy/sell/dividend/etc | `add_transaction(...)` |
| Edit position data | `update_position(...)` |
| Add new position | `add_position(...)` |
| Add a loan | `add_loan(...)` |
| Add a contact | `add_contact(...)` |
| Generate PDF report | `generate_report` |
| Generate HTML email report | `generate_email_report` |
| Read HTML email report body | `get_email_report_content(filename)` |
| Change settings | `update_settings(...)` |

### B3 — Workflow patterns

#### Portfolio review / analysis
```
1. get_summary           → overall KPIs
2. get_allocation        → class weights
3. get_pl_by_class       → which classes are performing
4. get_top_movers        → standout positions
5. get_realized_vs_unrealized → cash vs paper gains
6. get_wacc              → hurdle rate context
7. get_alerts            → anything needing attention
```

#### Record a transaction
```
1. get_holdings or search_portfolio(q)  → find position_id
2. add_transaction(
     position_id=...,
     type="buy"|"sell"|"dividend"|"capital_call"|"nav_update"|...,
     date="YYYY-MM-DD",
     total_amount=...,
     quantity=...,   # optional but recommended
     price=...       # optional but recommended
   )
```

Transaction types:
- `buy` / `sell` — affects cost basis
- `dividend` / `distribution` / `interest` — income only, no cost basis change
- `capital_call` — cash deployed into PE/VC fund
- `nav_update` — new valuation for illiquid assets (PE, RE, mutual funds)
- `cost_entry` — manual cost entry for positions without price history

#### Update an illiquid position value
```
1. search_portfolio(q)   → find position_id
2. add_transaction(
     position_id=...,
     type="nav_update",
     date="YYYY-MM-DD",
     total_amount=<new_value_in_local_currency>
   )
```
Use `nav_update` over `update_position(current_value=...)` — it preserves the valuation history.

#### Send an email report
```
1. generate_email_report()              → creates HTML file, returns filename
2. get_email_report_content(filename)   → returns full HTML string
3. Send via your email tool with content_type="text/html"
```

#### Add a new investment
```
1. get_holdings           → find account_id under the right asset class
2. add_position(
     account_id=...,
     name="...",
     asset_type="pe"|"stock"|"etf"|...,
     cost_currency="USD"|"BHD"|"SAR"|"EUR",
     quantity=...,
     avg_cost_basis=...,
     first_acquired="YYYY-MM-DD"
   )
3. add_transaction(       → record the initial buy / capital call
     position_id=<returned id>,
     type="buy"|"capital_call",
     date=..., total_amount=..., currency=...
   )
```

#### Search before writing
Always search before creating to avoid duplicates:
```
1. search_portfolio(q="fund name or ticker")
2. If found → use returned position_id directly
3. If not found → add_position(...)
```

### B4 — Asset types reference

| Value | Meaning | Live price? |
|-------|---------|-------------|
| `stock` | Listed equity | Yes (Yahoo Finance) |
| `etf` | Exchange-traded fund | Yes (Yahoo Finance) |
| `mutual_fund` | Mutual / unit trust fund | Ticker if listed |
| `crypto` | Cryptocurrency | Yes (CoinGecko) |
| `real_estate` | Direct property | No — manual nav_update |
| `pe` | Private equity | No — manual nav_update |
| `vc` | Venture capital | No — manual nav_update |
| `private_credit` | Private credit / direct lending | No — manual nav_update |
| `gold` | Physical or paper gold | Yes (Yahoo Finance, GC=F) |

### B5 — Currencies

Supported: `USD`, `BHD`, `SAR`, `EUR`.
- BHD and SAR are pegged to USD (hardcoded).
- EUR rate is fetched from ECB at startup with a 1.08 fallback.
- All analytics output in USD regardless of position currency.

### B6 — Rules

- Always call `get_summary` first for a full portfolio review — it gives context for everything else.
- Use `get_holdings` or `search_portfolio` to resolve IDs before any write — never guess IDs.
- For illiquid positions, use `nav_update` transactions to record new valuations — preserves history.
- `generate_report` / `generate_email_report` do **not** send anything — they save files for an external delivery agent.
- When adding a contact, pass `link_to_position_id` or `link_to_account_id` to link in one step.
- `update_settings` changes take effect on the next container restart.

---

## Part C: Database Migration (copy data to a new server)

Use this when re-seeding produces incorrect numbers or you want to clone the exact live database state (including prices, snapshots, benchmarks, and all history) to another server. This is always preferred over re-seeding.

### C1 — Dump from the source server

```bash
# On the source server — dump to a binary file in the current directory
docker exec portfolio_db pg_dump -U portfolio -Fc portfolio > portfolio_backup.dump

# Verify it has content (should be several MB if data is populated)
ls -lh portfolio_backup.dump
```

### C2 — Transfer to the new server

```bash
# From the source server, SCP to the new server (replace NEW_SERVER_IP and user)
scp portfolio_backup.dump user@NEW_SERVER_IP:~/portfolio_backup.dump
```

If SCP is not available, upload via any file transfer method (SFTP, rsync, etc.).

A current dump is also committed to the GitHub repo at `backend/portfolio_backup.dump` and can be downloaded directly:

```bash
# On the new server — pull the repo and use the committed dump
cd ~/portfolio-manager
git pull
cp backend/portfolio_backup.dump ~/portfolio_backup.dump
```

### C3 — Restore on the new server

```bash
# Make sure the db container is running
cd ~/portfolio-manager
docker compose up -d db

# Wait for postgres to be ready
sleep 10

# Drop and recreate the database (clean slate)
docker exec portfolio_db psql -U portfolio -c "DROP DATABASE IF EXISTS portfolio;"
docker exec portfolio_db psql -U portfolio -c "CREATE DATABASE portfolio;"

# Restore — alembic schema is included in the dump
docker exec -i portfolio_db pg_restore -U portfolio -d portfolio < ~/portfolio_backup.dump

# Start the rest of the stack — alembic upgrade head will be a no-op
docker compose up -d
```

### C4 — Verify

```bash
# Check row counts
docker exec portfolio_db psql -U portfolio -d portfolio -c "
  SELECT 'positions'    AS tbl, count(*) FROM positions
  UNION ALL SELECT 'transactions',         count(*) FROM transactions
  UNION ALL SELECT 'accounts',             count(*) FROM accounts
  UNION ALL SELECT 'portfolio_snapshots',  count(*) FROM portfolio_value_snapshots;
"

# Check invested capital matches expected ~$1,638,258
curl -s http://localhost:8000/api/portfolio/summary | python3 -m json.tool | grep total_invested
```

### C5 — When to update the committed dump

After any significant data changes (new positions, bulk transactions, price backfill), regenerate and commit the dump:

```bash
# On the live server
docker exec portfolio_db pg_dump -U portfolio -Fc portfolio > backend/portfolio_backup.dump

# Commit and push
cd ~/portfolio-manager
git add backend/portfolio_backup.dump
git commit -m "chore: update db dump"
git push origin main
```
