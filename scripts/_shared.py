"""Shared helpers for DocVault GitHub Action."""

from __future__ import annotations

import os
import sys


def require_api_key() -> str:
    key = os.environ.get("CURSOR_API_KEY", "").strip()
    if not key:
        print(
            "::error::CURSOR_API_KEY is required. Add your Cursor API key as a secret.",
            file=sys.stderr,
        )
        sys.exit(1)
    return key
