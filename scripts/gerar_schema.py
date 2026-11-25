# SPDX-License-Identifier: AGPL-3.0-or-later
"""Gera o JSON Schema público dos contratos Pydantic."""

import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "pipeline" / "src"))

from praca_pipeline.modelos import Pessoa

DESTINO = Path(__file__).resolve().parent.parent / "schema" / "pessoa.schema.json"


def main() -> None:
    DESTINO.parent.mkdir(parents=True, exist_ok=True)
    schema = Pessoa.model_json_schema()
    schema["$schema"] = "https://json-schema.org/draft/2020-12/schema"
    DESTINO.write_text(json.dumps(schema, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


if __name__ == "__main__":
    main()
