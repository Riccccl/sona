# CLAUDE.md

## Project Overview

SONA Scraper monitors `https://psywue.sona-systems.com/` (a German university psychology study portal) for newly available research studies and sends Discord notifications when new ones appear. It is designed for manual or scheduled execution via GitHub Actions — not for continuous running.

**Run:** `python main.py`

---

## Architecture

### Module Responsibilities

| Module | Responsibility |
|---|---|
| `main.py` | Entry point. Validates env vars, wires all components, drives the main flow. |
| `src/models.py` | `Study` dataclass and `VPNType` / `VPN_*` program-type classes. |
| `src/scraper.py` | Playwright browser automation. Logs into SONA, navigates, and extracts study rows from HTML tables. |
| `src/StudyCache.py` | Reads/writes `cached_studies.json`. Returns an empty cache on first run (no file found). |
| `src/differ.py` | Compares old and new `StudyCache` instances. New studies identified by link URL, not title. |
| `src/discord_notifier.py` | Builds Discord webhook payloads and POSTs them. Handles message splitting at the 2000-char limit. |
| `src/text_formatter.py` | Stub formatting utilities. Body is commented out. Not called anywhere. Safe to expand. |

### Data Flow

```
Scraper.scrape_available_studies()
    -> list[Study]                           (live data from Playwright browser session)

StudyCache(studies=available_studies)        (new cache, in memory)
StudyCache.from_file("cached_studies.json")  (old cache from disk; empty StudyCache if file missing)

Differ(old, new).get_new_studies()
    -> list[Study]                           (studies whose .link is not in old cache)

send_study_notification(study, webhook_url)  (one POST per new study, 1s sleep between)

newStudyCache.to_file("cached_studies.json") (persist for next run)
```

---

## Setup and Development Commands

### Install

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python -m playwright install chromium --with-deps --only-shell
```

### Environment Variables

Create `.env` (gitignored):

```
SONA_USERNAME=your_username
SONA_PASSWORD=your_password
DISCORD_WEBHOOK_URL=https://discord.com/api/webhooks/...
```

All three are required. `main.py` raises `ValueError` immediately if any are absent.

### Run

```bash
python main.py
```

---

## Coding Conventions

- **Type hints** on every function signature (parameters and return type). This is a hard convention — do not omit them.
- **Private methods** use a single underscore prefix (`_method_name`).
- **German method names** are intentional. The portal UI is in German; method names mirror the actions they perform:
  - `_anmeldungsdialog_bedienen` — "handle login dialog"
  - `_in_available_studies_navigieren` — "navigate to available studies"
  - `_in_participated_studies_navigieren` — "navigate to participated studies"
  - Do not rename these.
- **Dataclasses** for simple data models (`Study`, `VPNType`).
- **Static factory methods** (`StudyCache.from_file()`) over bare constructors for deserialization.
- **Module-level constants** for magic values (e.g., `MAX_DISCORD_CONTENT_LENGTH = 2000`).
- No linter or formatter is configured. Follow existing style: 4-space indent, no trailing whitespace.

---

## Constraints and Gotchas

### Discord 2000-character limit
`_split_message()` in `discord_notifier.py` splits long messages correctly, but `send_study_notification()` does not call it — it passes the payload directly. If any roadmap feature (e.g., AI summary) adds substantial text to a notification, wire `_split_message` into `send_study_notification` before sending.

### Playwright runs headless
`Scraper` is always instantiated with `headless=True` in `main.py`. Do not change this for CI. For local debugging only, pass `headless=False` temporarily.

### Cache file is gitignored
`cached_studies.json` is excluded from git (see `.gitignore`). It is persisted between CI runs via GitHub Actions cache, not commits. Do not add it to version control. A missing or corrupt cache causes `StudyCache.from_file()` to silently return an empty cache — this means all currently live studies will be treated as new on that run and all will be notified.

### `scrape_participated_studies` is incomplete
The method exists in `Scraper` but produces `Study` objects with `short_description=""` and `link=self.website_link + ""` (i.e., just the root URL). It is not called in `main.py`. Do not rely on it until the link extraction is fixed.

### Error handling in `main.py` is a stub
The `except` block in `__main__` re-raises immediately with `raise e`. The commented `print` line suggests error-suppression was considered and rejected. Proper fallback handling is on the roadmap.

### `src/__init__.py` prints on import
Contains `print("src package loaded")`. This prints on every run. Harmless but worth noting if adding tests that capture stdout.

---

## Data Model Reference

### `Study` (dataclass, `src/models.py`)

| Field | Type | Notes |
|---|---|---|
| `title` | `str` | Study name from `cells[1] p strong` |
| `compensation` | `str` | From `span[id*="LabelCredits"]` (e.g., `"0.5 VP-Stunden"`) |
| `short_description` | `str` | From `span[id*="LabelStudyType"]` (e.g., `"Online"`) |
| `link` | `str` | `website_link + href` from `cells[1] a` |

Property: `gives_vph: bool` — `True` when `"vph"` appears (case-insensitive) in `compensation`.

### `cached_studies.json` Shape

```json
{
  "date_created": "2024-01-15T10:30:00.123456",
  "studies": [
    {
      "title": "Study Name",
      "compensation": "0.5 VP-Stunden",
      "short_description": "Online",
      "link": "https://psywue.sona-systems.com/exp.aspx?experiment_id=123"
    }
  ]
}
```

Serialized via `study.__dict__`. Deserialized via `Study(**item)`. Any extra keys in the JSON will cause a `TypeError` on deserialization.

### `VPNType` Subclasses

Defined in `src/models.py`. Not used in the active scraping flow. Represent academic program types at the university.

| Class | `name` | `long_name` | `required_amount` |
|---|---|---|---|
| `VPN_MP` | MP | Medienpsychologie | 4 |
| `VPN_KPNM` | KPNM | Kommunikationspsychologie und Neue Medien | 4 |
| `VPN_MWK` | MWK | Medien- und Wirtschaftskommunikation | 4 |
| `VPN_MI` | MI | Medieninformatik | 4 |
| `VPN_HCI` | HCI | Human-Computer Interaction | 4 |
| `VPN_PsyErgo` | PsyErgo | Psychologische Ergonomie | 4 |
| `VPN_MTS` | MTS | Mensch-Technik-Systeme | **2** |
| `VPN_FREE` | FREE | Freier Bereich | 4 |

---

## GitHub Actions Workflow

File: `.github/workflows/main.yml`

- **Trigger:** `workflow_dispatch` only (manual from GitHub UI or API). No scheduled cron.
- **Runner:** `ubuntu-latest`, Python 3.11.
- **Required secrets:** `SONA_USERNAME`, `SONA_PASSWORD`, `DISCORD_WEBHOOK_URL`.
- **Permissions:** `actions: write` — required for the "Delete old caches" step to call `gh cache delete`.

**Cache strategy:**
1. Restore `cached_studies.json` from the latest `cached-studies-*` cache before running.
2. After the run, delete all existing `cached-studies-*` cache entries (`continue-on-error: true` so it doesn't fail if none exist).
3. Save a fresh cache keyed to `cached-studies-<run_id>`.

This ensures only one cache entry is kept at a time.

**To add a scheduled trigger**, add a `schedule` block under `on:` alongside `workflow_dispatch`:

```yaml
on:
  workflow_dispatch:
  schedule:
    - cron: '0 * * * *'  # hourly, adjust as needed
```

---

## Roadmap (Planned Features)

Avoid designs that conflict with these upcoming additions:

| Feature | Notes |
|---|---|
| AI Summary | LLM-generated study summary before Discord notification. Will likely extend `_create_payload_from_study` or `text_formatter.py`. Needs an additional API key secret. |
| Error fallbacks | Graceful handling of scrape failures, webhook errors, or login failures without crashing. |
| Structured Outputs / Messages | Richer Discord message formatting (embeds, fields). Will replace plain-text payload in `_create_payload_from_study`. |
| Ntfy integration | Additional push notification channel. Will need a new notifier module parallel to `discord_notifier.py`. |
| Scraping participated studies | `scrape_participated_studies()` exists but link extraction is broken. Needs fixing before use. |
