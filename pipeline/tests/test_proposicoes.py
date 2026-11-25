# SPDX-License-Identifier: AGPL-3.0-or-later
from datetime import date

import httpx
from praca_pipeline.coletores.proposicoes import ENDPOINT, coletar_proposicoes
from praca_pipeline.http import ClienteFonte, DiskCache


def test_coletor_de_proposicoes_da_camara(tmp_path) -> None:
    def handler(request: httpx.Request) -> httpx.Response:
        assert str(request.url).startswith(ENDPOINT)
        assert request.url.params["dataApresentacaoInicio"] == "2026-01-01"
        return httpx.Response(
            200,
            json={
                "dados": [
                    {
                        "id": 123,
                        "siglaTipo": "PL",
                        "numero": 42,
                        "ano": 2026,
                        "ementa": "Ementa de teste",
                        "uri": "https://dadosabertos.camara.leg.br/api/v2/proposicoes/123",
                    }
                ]
            },
            request=request,
        )

    cliente = ClienteFonte(
        DiskCache(tmp_path),
        client=httpx.Client(transport=httpx.MockTransport(handler)),
        rate=100,
    )
    resultado = coletar_proposicoes(cliente, desde=date(2026, 1, 1))

    assert resultado[0].id == "123"
    assert resultado[0].casa == "camara"
    assert resultado[0].tipo == "PL"
