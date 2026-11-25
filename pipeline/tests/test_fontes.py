# SPDX-License-Identifier: AGPL-3.0-or-later
import json
from pathlib import Path

from scripts.gerar_fontes import carregar


def test_registro_de_fontes_existe_e_tem_fontes_principais() -> None:
    registro = Path(__file__).parents[2] / "data/publico/fontes.yml"
    conteudo = registro.read_text(encoding="utf-8")
    assert "id: camara" in conteudo
    assert "id: tse" in conteudo
    assert "licenca:" in conteudo


def test_registro_gera_ids_unicos_e_json_publicavel() -> None:
    fontes = carregar()
    ids = [fonte.id for fonte in fontes]
    assert len(ids) == len(set(ids))
    assert len(ids) >= 10
    assert {"camara", "senado", "tse", "cgu-transparencia", "stf"} <= set(ids)
    serializado = json.loads(json.dumps([fonte.model_dump(mode="json") for fonte in fontes]))
    assert serializado[0]["url"].startswith("https://")
