# SPDX-License-Identifier: AGPL-3.0-or-later
"""Executa a coleta pública real e publica snapshots normalizados."""

from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "pipeline" / "src"))

from praca_pipeline.cli import main  # noqa: E402

raise SystemExit(main())
