# SPDX-License-Identifier: AGPL-3.0-or-later
from datetime import UTC, datetime

from praca_pipeline.coletores.camara import DeputadoCamara
from praca_pipeline.coletores.senado import SenadorSenado
from praca_pipeline.modelos.dominio import Mandato, Poder, Proveniencia, StatusMandato
from praca_pipeline.resolucao import resolver_legislativos


def _fonte() -> Proveniencia[str]:
    return Proveniencia(
        valor="teste",
        fonte_id="camara",
        url="https://example.test",
        coletado_em=datetime(2026, 1, 1, tzinfo=UTC),
        licenca="dados públicos",
    )


def test_resolucao_preserva_casa_e_nao_une_homonimos() -> None:
    mandato = Mandato(
        poder=Poder.LEGISLATIVO,
        cargo="Deputado federal",
        uf="SP",
        inicio="2023-02-01",
        status=StatusMandato.ATIVO,
    )
    deputado = DeputadoCamara(
        id_camara=1,
        nome="Nome Igual",
        slug="nome-igual-sp",
        uf="SP",
        mandato=mandato,
        fonte=_fonte(),
    )
    senador = SenadorSenado(
        id_senado=2,
        nome="Nome Igual",
        slug="nome-igual-sp",
        uf="SP",
        mandato=mandato.model_copy(update={"cargo": "Senador"}),
        fonte=_fonte(),
    )
    resultado = resolver_legislativos([deputado], [senador])
    assert [(item.fonte_id, item.fonte_codigo) for item in resultado] == [
        ("camara", 1),
        ("senado", 2),
    ]
