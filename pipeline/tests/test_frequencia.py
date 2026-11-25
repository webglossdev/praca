# SPDX-License-Identifier: AGPL-3.0-or-later
from praca_pipeline.frequencia import Frequencia, intervalo_da_frequencia


def test_frequencias_tem_intervalos_explicitos() -> None:
    assert intervalo_da_frequencia(Frequencia.DIARIA) == 86400
    assert intervalo_da_frequencia(Frequencia.EVENTO) is None
