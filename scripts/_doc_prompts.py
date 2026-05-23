"""Prompt templates for the comprehensive documentation auditor agent."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass
class DocScope:
    write: bool
    ui: bool
    output_dir: str
    audience: str
    excludes: list[str]


def _exclude_block(excludes: list[str]) -> str:
    if not excludes:
        return ""
    lines = "\n".join(f"- `{p}`" for p in excludes)
    return f"""
## Paths to exclude from analysis
{lines}
"""


def _mode_block(scope: DocScope) -> str:
    if scope.write:
        return "**MODE: WRITE** — Create and update documentation files in the repository."
    return "**MODE: PLAN** — Analyze only; describe what you would write but do not create files yet."


def _ui_block(scope: DocScope) -> str:
    if not scope.ui:
        return "Skip single-page UI generation unless content is needed for PLAN preview."
    return f"""
## Single-page UI requirement (CRITICAL)

When `--ui` is enabled, you MUST write **`{scope.output_dir}/ui/index.html`** — one self-contained HTML file:

1. **All documentation on a single scrollable page** (no iframes, no external doc sites)
2. **Table of contents** visible at all times (sticky left sidebar on desktop, collapsible top on mobile)
3. **Every TOC entry is clickable** — uses `<a href="#section-id">` anchor links that jump to the section
4. **Every section has a matching `id`** — kebab-case matching the TOC href (e.g. `#architecture-overview`)
5. **Self-contained** — inline CSS only; no CDN required (works offline / embedded in project UI)
6. **Include:** smooth scroll behavior, active TOC highlight on scroll (IntersectionObserver or scroll spy)
7. **Accessible** — semantic HTML (`nav`, `main`, `section`, `h1`-`h3`), skip link, sufficient contrast

Reference structure is in the agent templates folder (`docvault-page.template.html`) if available in the repo;
otherwise follow the structure below in your output.

Required TOC sections (add more as needed):
- Overview
- Architecture
- Directory structure
- Setup & installation
- Configuration
- API / routes / endpoints
- Data models
- Frontend / UI (if applicable)
- Deployment
- Testing
- Troubleshooting
- Glossary
"""


def phase1_discovery(scope: DocScope) -> str:
    return f"""You are a principal technical writer and staff engineer performing a **full codebase audit for documentation**.

{_mode_block(scope)}
Audience focus: **{scope.audience}**.
Output directory: `{scope.output_dir}/`
{_exclude_block(scope.excludes)}

## Phase 1 — Discovery & inventory

Systematically explore the entire project (code, configs, infra, frontend, backend, mobile, docs, CI).

Catalog:
1. **Project type** — web app, API, monorepo, static site, CLI, library, etc.
2. **Tech stack** — languages, frameworks, databases, hosting
3. **Entry points** — main files, routes, package scripts
4. **Module map** — top-level directories and responsibility of each
5. **Existing docs** — README, docs/, inline comments worth preserving
6. **External integrations** — APIs, auth, payments, third-party services
7. **Gaps** — what is undocumented or outdated

## Output format

# Documentation Audit Report

## Project snapshot
## Stack & dependencies
## Directory inventory
| Path | Purpose | Documented? (Y/N/PARTIAL) |
## Entry points & runtime flow
## Existing documentation assessment
## Critical gaps (prioritized)

Be exhaustive. Include websites (routes/pages), apps (screens/flows), and backend services.
"""


def phase2_architecture(scope: DocScope) -> str:
    return f"""## Phase 2 — Architecture & data flow

Based on Phase 1, document how the system works.

{_mode_block(scope)}

Cover:
1. **High-level architecture** — components and boundaries
2. **Request/data flow** — user action → UI → API → DB → response (adapt to project type)
3. **Auth & security model** (if any)
4. **State management** (frontend/backend)
5. **Key design decisions** inferable from code
6. **Mermaid diagrams** — at least `flowchart TD` for main flow and `graph LR` for components

## Output format

# Architecture Documentation

## System overview
## Component diagram (mermaid)
## Main execution flows (mermaid)
## Security & authentication
## Configuration & environment
## Dependencies between modules
"""


def phase3_interfaces(scope: DocScope) -> str:
    return f"""## Phase 3 — APIs, routes, and public interfaces

{_mode_block(scope)}

Document every public interface:
- HTTP routes / REST / GraphQL
- CLI commands
- Exported functions/classes (libraries)
- Web pages / app screens (for websites and UIs)
- Webhooks & events
- Environment variables

## Output format

# Interface Reference

## API / route table
| Method / Type | Path / Command | Purpose | Auth |
## Key modules & exports
## Environment variables
| Name | Required | Description | Default |
## UI routes / screens (if applicable)
| Route / Screen | Purpose | Key components |
"""


def phase4_guides(scope: DocScope) -> str:
    return f"""## Phase 4 — Practical guides

Write actionable documentation for **{scope.audience}**.

{_mode_block(scope)}

Include:
1. **Quick start** — clone to running locally (exact commands from repo)
2. **Installation & prerequisites**
3. **Configuration** — step-by-step
4. **Common workflows** — how to accomplish main tasks
5. **Deployment** — if detectable from CI/Docker/terraform
6. **Testing** — how to run tests, coverage
7. **Troubleshooting** — common errors and fixes
8. **FAQ**

## Output format

# User & Developer Guides

## Quick start
## Installation
## Configuration walkthrough
## Common tasks
## Deployment
## Testing
## Troubleshooting & FAQ
"""


def phase5_write(scope: DocScope) -> str:
    if not scope.write:
        return ""

    files = f"""
- `{scope.output_dir}/README.md` — index linking all artifacts
- `{scope.output_dir}/AUDIT.md` — Phase 1 report
- `{scope.output_dir}/ARCHITECTURE.md` — Phase 2
- `{scope.output_dir}/INTERFACES.md` — Phase 3
- `{scope.output_dir}/GUIDES.md` — Phase 4
- `{scope.output_dir}/GLOSSARY.md` — terms and acronyms
"""
    ui_file = ""
    if scope.ui:
        ui_file = f"- `{scope.output_dir}/ui/index.html` — **single-page UI with clickable TOC** (see UI requirements)\n"

    return f"""## Phase 5 — Write documentation files

{_mode_block(scope)}
{_ui_block(scope)}

Write all markdown files to `{scope.output_dir}/`:
{files}{ui_file}

Rules:
1. Use clear headings, tables, and code blocks with language tags
2. Cross-link between files using relative markdown links
3. Replace outdated README sections only if clearly wrong — prefer linking to `{scope.output_dir}/`
4. Every code sample must match actual project commands/paths
5. Do not invent features not present in the codebase

If UI mode: the HTML file must be production-ready for embedding in a project dashboard or `/docs` route.
"""


def phase6_finalize(scope: DocScope) -> str:
    ui_note = ""
    if scope.ui and scope.write:
        ui_note = f"""
Verify `{scope.output_dir}/ui/index.html`:
- [ ] TOC links match section ids
- [ ] All sections present on one page
- [ ] Click navigation works (anchor jump)
- [ ] No broken internal links
"""

    plan_note = (
        f"Write `{scope.output_dir}/DOC_REPORT.md` with summary and file list."
        if scope.write
        else "Summarize planned documentation in your response only."
    )

    return f"""## Final phase — Verification & report

{_mode_block(scope)}

1. Re-scan for accuracy — commands, paths, version numbers
2. Ensure consistency across all `{scope.output_dir}/` files
3. {plan_note}
4. List recommended next steps (diagrams to add, APIs needing examples)
{ui_note}

End with a concise executive summary and how to open the UI page locally:
`open {scope.output_dir}/ui/index.html` (if UI mode).
"""


def phases_for_scope(scope: DocScope) -> list[tuple[str, str]]:
    out: list[tuple[str, str]] = [
        ("Discovery audit", phase1_discovery(scope)),
        ("Architecture", phase2_architecture(scope)),
        ("Interfaces", phase3_interfaces(scope)),
        ("Guides", phase4_guides(scope)),
    ]
    p5 = phase5_write(scope)
    if p5:
        out.append(("Write documentation", p5))
    out.append(("Finalize", phase6_finalize(scope)))
    return out
