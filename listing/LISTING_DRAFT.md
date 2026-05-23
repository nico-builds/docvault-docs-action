# GitHub Marketplace listing — DocVault Action

| Field | Value |
|-------|-------|
| **Action name** | `DocVault Documentation Generator` |
| **Repository** | `nico-builds/docvault-docs-action` |
| **Primary category** | Documentation |
| **Secondary category** | Continuous integration |
| **Tagline** | Full-project docs with optional single-page UI |

## Short description

> DocVault audits your entire codebase or app and generates comprehensive documentation with the Cursor SDK. Optional single-page HTML UI with clickable table of contents.

## Release notes — v1.0.0

```markdown
## DocVault v1.0.0

- Multi-phase documentation audit and generation
- Modes: plan (safe) and write
- Optional single-page HTML UI with clickable TOC
- Output in .docvault/

uses: nico-builds/docvault-docs-action@v1
with:
  cursor-api-key: ${{ secrets.CURSOR_API_KEY }}
  mode: write
  ui: 'true'
```

## Pricing

Free Action listing. Users provide `CURSOR_API_KEY`.
