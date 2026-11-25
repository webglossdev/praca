# SPDX-License-Identifier: AGPL-3.0-or-later
"""Geração de JSON enxuto de perfis e índices de navegação."""

import json
from pathlib import Path
from typing import Any


def gerar_indices(pessoas: list[dict[str, Any]], destino: Path) -> None:
    destino.mkdir(parents=True, exist_ok=True)
    ordenadas = sorted(pessoas, key=lambda pessoa: pessoa.get("nome_publico", ""))
    (destino / "pessoas.json").write_text(
        json.dumps(ordenadas, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    indice = [
        {
            "pid": pessoa["pid"],
            "slug": pessoa["slug"],
            "nome": pessoa["nome_publico"],
        }
        for pessoa in ordenadas
    ]
    (destino / "indice-pessoas.json").write_text(
        json.dumps(indice, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
