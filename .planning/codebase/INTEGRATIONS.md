# External Integrations

**Analysis Date:** 2026-03-25

## APIs & External Services

**No external API integrations detected.**

This is a standalone memory management system that operates entirely on local JSON files.

## Data Storage

**Databases:**
- None - JSON file-based storage

**File Storage:**
- Local filesystem: `.memory/` directory
  - `operations.json` - Operation history
  - `conclusions.json` - Analysis conclusions
  - `portfolio.json` - Portfolio information
  - `crisis_knowledge/index.json` - Crisis events index
  - `crisis_knowledge/events/*.json` - Individual crisis event details
  - `lessons_learned/index.json` - Lessons index
  - `lessons_learned/lessons/*.json` - Individual lesson details
  - `investment_patterns.json` - Investment patterns
  - `links.json` - Relationships between events/lessons

**Caching:**
- None

## Authentication & Identity

**Auth Provider:**
- None - no authentication system

## Monitoring & Observability

**Error Tracking:**
- None - basic print statements for user feedback

**Logs:**
- Console output only via `print()` statements

## CI/CD & Deployment

**Hosting:**
- Local execution only
- No server deployment

**CI Pipeline:**
- None detected

## Environment Configuration

**Required env vars:**
- None detected

**Secrets location:**
- None - no external service credentials

## Webhooks & Callbacks

**Incoming:**
- None

**Outgoing:**
- None

---

*Integration audit: 2026-03-25*