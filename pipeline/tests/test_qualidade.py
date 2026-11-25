# SPDX-License-Identifier: AGPL-3.0-or-later
import pytest
from praca_pipeline.qualidade import auditar_registros, validar_diff


def test_relatorio_detecta_nulos_duplicados_e_campos_vazios() -> None:
    relatorio = auditar_registros(
        [{"id": "a", "nome": "A"}, {"id": "a", "nome": ""}, {"id": None, "nome": "C"}],
        chave="id",
    )
    assert relatorio.total == 3
    assert relatorio.nulos == 1
    assert relatorio.duplicados == 1
    assert relatorio.campos_vazios["nome"] == 1


def test_diff_guard_interrompe_queda_anomala() -> None:
    anterior = auditar_registros([{"id": str(i)} for i in range(10)], chave="id")
    atual = auditar_registros([{"id": "1"}], chave="id")
    with pytest.raises(ValueError, match="20%"):
        validar_diff(atual, anterior)
