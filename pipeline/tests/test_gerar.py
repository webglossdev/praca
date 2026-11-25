# SPDX-License-Identifier: AGPL-3.0-or-later
import json

from praca_pipeline.gerar import gerar_indices


def test_gerador_cria_lista_e_indice_ordenados(tmp_path) -> None:
    gerar_indices(
        [
            {"pid": "pid_b", "slug": "b-pid", "nome_publico": "Zeta"},
            {"pid": "pid_a", "slug": "a-pid", "nome_publico": "Alfa"},
        ],
        tmp_path,
    )
    assert json.loads((tmp_path / "pessoas.json").read_text()) [0]["pid"] == "pid_a"
    assert len(json.loads((tmp_path / "indice-pessoas.json").read_text())) == 2
