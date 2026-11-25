# SPDX-License-Identifier: AGPL-3.0-or-later
import json
from pathlib import Path

from praca_pipeline.modelos import Pessoa


def test_as_cinco_fixtures_sao_validas() -> None:
    caminho = Path(__file__).parents[2] / "data/publico/fixtures/pessoas.json"
    pessoas = [
        Pessoa.model_validate(item)
        for item in json.loads(caminho.read_text(encoding="utf-8"))
    ]
    assert len(pessoas) == 5
    assert len({p.pid for p in pessoas}) == 5
