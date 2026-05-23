# DocVault Documentation Generator

[![GitHub Marketplace](https://img.shields.io/badge/Marketplace-DocVault%20Documentation%20Generator-24292e?style=flat&logo=github)](https://github.com/marketplace/actions/docvault-documentation-generator)

**DocVault** — AI-powered documentation for entire codebases, websites, and apps. Built on the [Cursor SDK](https://cursor.com/docs/sdk) (Composer 2.5).

Part of the [DocVault](https://github.com/nico-builds/docvault-app) product family on [nico.builds](https://github.com/nico-builds).

## Features

- Full project audit: architecture, APIs, guides, glossary
- Markdown docs under `.docvault/`
- **Optional `--ui`**: single-page HTML with **clickable TOC** (all sections on one page)
- Safe default: `plan` mode analyzes without writing files

## Prerequisites

- [Cursor API key](https://cursor.com/dashboard/integrations) → secret `CURSOR_API_KEY`

## Quick start

```yaml
name: DocVault docs

on:
  pull_request:
  workflow_dispatch:

permissions:
  contents: read

jobs:
  document:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - name: DocVault documentation (plan)
        uses: nico-builds/docvault-docs-action@v1
        with:
          cursor-api-key: ${{ secrets.CURSOR_API_KEY }}
          mode: plan
```

### Generate docs + project UI

```yaml
permissions:
  contents: write

jobs:
  document:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - uses: nico-builds/docvault-docs-action@v1
        with:
          cursor-api-key: ${{ secrets.CURSOR_API_KEY }}
          mode: write
          ui: 'true'
          audience: both

      - uses: actions/upload-artifact@v4
        with:
          name: docvault
          path: .docvault/
```

Serve `.docvault/ui/index.html` at `/docs` in your app.

## Inputs

| Input | Default | Description |
|-------|---------|-------------|
| `cursor-api-key` | — | Cursor API key (required) |
| `mode` | `plan` | `plan` or `write` |
| `ui` | `false` | Single-page HTML + TOC (implies write) |
| `audience` | `both` | `developers`, `end-users`, or `both` |
| `output-dir` | `.docvault` | Output folder |
| `exclude` | `''` | Comma-separated paths to skip |
| `working-directory` | workspace | Subdirectory to analyze |

## Output

| Path | Description |
|------|-------------|
| `.docvault/AUDIT.md` | Inventory & gaps |
| `.docvault/ARCHITECTURE.md` | Design + diagrams |
| `.docvault/INTERFACES.md` | APIs, routes, env |
| `.docvault/GUIDES.md` | Quick start, deploy |
| `.docvault/ui/index.html` | Single-page UI (`ui: true`) |
| `.docvault/DOC_REPORT.md` | Summary |

## Install DocVault App

[DocVault GitHub App](https://github.com/apps/docvault) — PR comments and Marketplace listing.

## License

MIT
