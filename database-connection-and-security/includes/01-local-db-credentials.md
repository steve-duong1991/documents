# Local Database Credentials

> **Note:** This section is a **local dev template** — host, username, and paths are machine-specific. Replace them for your environment. Production connection patterns start in [§2 Production security](02-prod-db-security.md).

> **Related:** Production baseline → [§2 Production security](02-prod-db-security.md) · Pattern picker → [§13 Decision guide](13-decision-guide.md) · Never use local auth in prod → [§00 Overview](00-overview.md)

> **Environment:** macOS · Homebrew · PostgreSQL 17  
> **Last updated:** June 2026

## Connection details

| Setting | Value |
|---------|-------|
| **Host** | `localhost` (or `127.0.0.1`) |
| **Port** | `5432` |
| **Database** | `postgres` |
| **Username** | `steveduong` |
| **Password** | *(none — not required for local connections)* |
| **SSL** | Not required locally |

## Connection strings

**URI format:**

```
postgresql://steveduong@localhost:5432/postgres
```

**JDBC (Java / Spring Boot):**

```
jdbc:postgresql://localhost:5432/postgres
```

**Environment variables:**

```bash
export PGHOST=localhost
export PGPORT=5432
export PGDATABASE=postgres
export PGUSER=steveduong
# PGPASSWORD is not set — local auth uses trust
```

## Quick connect

```bash
pg-start          # start PostgreSQL (manual, on-demand)
psql postgres     # connect to default database
pg-stop           # stop when done
```

## Shell aliases

Defined in `~/.zshrc`:

| Alias | Command |
|-------|---------|
| `pg-start` | `pg_ctl -D /opt/homebrew/var/postgresql@17 start` |
| `pg-stop` | `pg_ctl -D /opt/homebrew/var/postgresql@17 stop` |
| `pg-status` | `pg_ctl -D /opt/homebrew/var/postgresql@17 status` |

## Install paths

| Item | Path |
|------|------|
| Binaries | `/opt/homebrew/opt/postgresql@17/bin` |
| Data directory | `/opt/homebrew/var/postgresql@17` |
| Config | `/opt/homebrew/var/postgresql@17/pg_hba.conf` |

## Authentication (local only)

Local connections use **`trust`** authentication — no password is required:

```
local   all   all                 trust
host    all   all   127.0.0.1/32    trust
host    all   all   ::1/128         trust
```

> **Note:** This setup is for **local development only**. Do not use `trust` auth in production.

## Optional: set a password

If a GUI tool requires a password field:

```bash
psql postgres -c "ALTER USER steveduong PASSWORD 'your_password';"
```

## Start behaviour

PostgreSQL is **not** set to auto-start on macOS boot.

- Do **not** use `brew services start postgresql@17` (runs in background + auto-start on login).
- Use `pg-start` / `pg-stop` manually when needed.

## Common mistakes

| Mistake | Fix |
|---------|-----|
| Copy local connection string to production | Use [§5](05-secret-manager-password.md) or cloud IAM(Identity and Access Management) patterns |
| Commit `.env` with `DATABASE_URL` | Platform secrets / CI variables only |
| Use `brew services` when manual start is intended | `pg-start` / `pg-stop` per project convention |
| Expose Postgres on `0.0.0.0` for convenience | Localhost only in dev |
