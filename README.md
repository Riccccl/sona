# SONA Scraper

A Python automation tool that monitors the [SONA Systems](https://psywue.sona-systems.com/) research participation portal for newly available psychology studies and sends real-time Discord notifications when new ones appear.

## Features

- Automated web scraping of SONA study listings using Playwright (headless Chromium)
- Incremental diff detection — only new studies since the last run trigger a notification
- Discord webhook integration for instant alerts
- Persistent study cache with JSON serialization for stateful runs
- GitHub Actions workflow for manual or scheduled cloud execution

## Quick Start

### Prerequisites

- Python 3.11+
- A [Discord webhook URL](https://support.discord.com/hc/en-us/articles/228383668) for the channel you want notifications in
- SONA account credentials

### Installation

```bash
git clone https://github.com/Riccccl/sona.git
cd sona
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r requirements.txt
python -m playwright install chromium --with-deps --only-shell
```

### Environment Setup

Create a `.env` file in the project root (never commit this):

```
SONA_USERNAME=your_username
SONA_PASSWORD=your_password
DISCORD_WEBHOOK_URL=https://discord.com/api/webhooks/...
```

### Run

```bash
python main.py
```

The scraper logs in, fetches available studies, compares them against the last cached run, sends a Discord notification for each new study, and saves the updated cache.

## Deploying with GitHub Actions

1. Fork this repository
2. Add the following repository secrets (Settings → Secrets and variables → Actions):
   - `SONA_USERNAME`
   - `SONA_PASSWORD`
   - `DISCORD_WEBHOOK_URL`
3. Go to **Actions → SONA CI Workflow → Run workflow** to trigger manually

The workflow runs linting, type checking, and tests before executing the scraper. To add automatic hourly checks, add the following to `main.yml` under `on:`:

```yaml
schedule:
  - cron: '0 * * * *'
```

## Development

### Install dev dependencies

```bash
pip install -r requirements-dev.txt
```

### Run tests

```bash
python -m pytest tests/
```

### Lint

```bash
ruff check src/ main.py tests/
```

### Type check

```bash
mypy src/ main.py
```

## Architecture

See [CLAUDE.md](./CLAUDE.md) for a detailed breakdown of module responsibilities, data flow, data models, and known constraints.

## Roadmap

- [ ] AI-powered study summaries (Gemini 1.5 Flash / Groq integration)
- [ ] Error fallback notifications on scrape or webhook failure
- [ ] Rich Discord embeds with structured formatting
- [ ] Ntfy push notification support
- [ ] Scraping of previously registered studies

## License

MIT — see [LICENSE](./LICENSE)
