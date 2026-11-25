# SPDX-License-Identifier: AGPL-3.0-or-later
from datetime import UTC, datetime

import httpx
from praca_pipeline.coletores.senado import ENDPOINT, coletar_senadores
from praca_pipeline.http import ClienteFonte, DiskCache


def test_coletor_do_senado_normaliza_lista_atual(tmp_path) -> None:
    payload = {
        "ListaParlamentarEmExercicio": {
            "Parlamentares": {
                "Parlamentar": [
                    {
                        "IdentificacaoParlamentar": {
                            "CodigoParlamentar": "1234",
                            "NomeParlamentar": "Senadora Exemplo",
                            "NomeCompletoParlamentar": "Senadora Exemplo da Silva",
                            "SiglaPartidoParlamentar": "ABC",
                            "UfParlamentar": "RJ",
                        },
                        "Mandato": {
                            "Exercicios": {
                                "Exercicio": [{"DataInicio": "2023-02-01"}]
                            }
                        },
                    }
                ]
            }
        }
    }

    def handler(request: httpx.Request) -> httpx.Response:
        assert str(request.url) == ENDPOINT
        return httpx.Response(200, json=payload, request=request)

    cliente = ClienteFonte(
        DiskCache(tmp_path),
        client=httpx.Client(transport=httpx.MockTransport(handler)),
        rate=100,
    )
    senadores = coletar_senadores(
        cliente,
        coletado_em=datetime(2026, 10, 6, tzinfo=UTC),
    )

    assert len(senadores) == 1
    assert senadores[0].id_senado == 1234
    assert senadores[0].slug == "senadora-exemplo-rj"
    assert senadores[0].mandato.inicio.isoformat() == "2023-02-01"
    assert senadores[0].partido_sigla == "ABC"
