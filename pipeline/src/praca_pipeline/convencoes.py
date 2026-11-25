# SPDX-License-Identifier: AGPL-3.0-or-later
"""Convenções estáveis para IDs, slugs e arquivos públicos."""

import re
import unicodedata


def slugificar(nome: str, uf: str | None = None) -> str:
    normalizado = unicodedata.normalize("NFKD", nome).encode("ascii", "ignore").decode()
    slug = re.sub(r"[^a-z0-9]+", "-", normalizado.lower()).strip("-")
    return f"{slug}-{uf.lower()}" if uf else slug


def pid_para_slug(pid: str) -> str:
    if not pid.startswith("pid_"):
        raise ValueError("pid deve começar com 'pid_'")
    return pid.removeprefix("pid_")
