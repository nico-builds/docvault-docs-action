#!/usr/bin/env python3
"""GitHub Action entrypoint for DocVault documentation generator."""

from __future__ import annotations

import os
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from cursor_sdk import Agent, CursorAgentError, LocalAgentOptions

from _doc_prompts import DocScope, phases_for_scope
from _shared import require_api_key


def _truthy(value: str) -> bool:
    return value.strip().lower() in {"1", "true", "yes", "on"}


def parse_scope_from_env() -> tuple[DocScope, str]:
    mode = os.environ.get("DOCS_MODE", "plan").strip().lower()
    write = mode == "write"
    ui = _truthy(os.environ.get("DOCS_UI", "false"))
    if ui:
        write = True

    audience = os.environ.get("DOCS_AUDIENCE", "both").strip()
    if audience not in {"developers", "end-users", "both"}:
        audience = "both"

    output_dir = os.environ.get("DOCS_OUTPUT_DIR", ".docvault").strip() or ".docvault"

    default_excludes = [
        "node_modules",
        ".git",
        ".venv",
        "venv",
        "__pycache__",
        "dist",
        "build",
        ".docvault",
    ]
    extra = os.environ.get("DOCS_EXCLUDE", "").strip()
    excludes = default_excludes + [p.strip() for p in extra.split(",") if p.strip()]
    excludes = list(dict.fromkeys(excludes))

    workspace = os.environ.get("DOCS_WORKING_DIRECTORY", "").strip()
    if not workspace:
        workspace = os.environ.get("GITHUB_WORKSPACE", os.getcwd())
    cwd = str(Path(workspace).expanduser().resolve())
    if not Path(cwd).is_dir():
        print(f"::error::Working directory does not exist: {cwd}", file=sys.stderr)
        sys.exit(1)

    scope = DocScope(
        write=write,
        ui=ui,
        output_dir=output_dir,
        audience=audience,
        excludes=excludes,
    )
    return scope, cwd


def stream_assistant(run) -> None:
    for message in run.messages():
        if message.type != "assistant":
            continue
        for block in message.message.content:
            if block.type == "text":
                print(block.text, end="", flush=True)
    print()


def run_phase(agent, label: str, prompt: str) -> None:
    print(f"\n{'=' * 60}\nPhase: {label}\n{'=' * 60}\n", file=sys.stderr)
    run = agent.send(prompt)
    print(f"run_id={run.id}", file=sys.stderr)
    stream_assistant(run)
    result = run.wait()
    if result.status == "error":
        print(f"::error::Phase '{label}' failed: {result.id}", file=sys.stderr)
        sys.exit(2)


def main() -> None:
    api_key = require_api_key()
    scope, cwd = parse_scope_from_env()

    mode_label = "WRITE" if scope.write else "PLAN"
    ui = " + UI" if scope.ui else ""
    print(f"::notice::DocVault [{mode_label}{ui}] → {cwd}")

    template_path = Path(__file__).resolve().parent / "templates" / "docvault-page.template.html"
    template_hint = ""
    if scope.ui and template_path.is_file():
        template_hint = (
            f"\nHTML template reference: `{template_path}` — use TOC + scroll-spy pattern "
            f"in `{scope.output_dir}/ui/index.html`."
        )

    phases = phases_for_scope(scope)

    try:
        with Agent.create(
            model="composer-2.5",
            api_key=api_key,
            local=LocalAgentOptions(cwd=cwd, setting_sources=[]),
        ) as agent:
            print(f"agent_id={agent.agent_id}", file=sys.stderr)

            opener = (
                "You are starting a multi-phase documentation audit in CI. "
                f"Repository root: `{cwd}`. Output: `{scope.output_dir}/`. "
                f"Audience: {scope.audience}.{template_hint}"
            )
            run_phase(agent, "Initialize", opener)

            for label, prompt in phases:
                run_phase(agent, label, prompt)

            if scope.ui and scope.write:
                print(
                    f"::notice::UI docs at {scope.output_dir}/ui/index.html",
                    file=sys.stderr,
                )
            print(f"::notice::DocVault finished. agent_id={agent.agent_id}")
    except CursorAgentError as err:
        print(f"::error::Startup failed: {err.message}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
