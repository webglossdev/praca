# SPDX-License-Identifier: AGPL-3.0-or-later
from datetime import UTC, datetime

import httpx
from praca_pipeline.coletores.camara import ENDPOINT, coletar_deputados
from praca_pipeline.http import ClienteFonte, DiskCache


def test_coletor_da_camara_normaliza_e_pagina(tmp_path) -> None:
    chamadas: list[tuple[str, int]] = []

    def handler(request: httpx.Request) -> httpx.Response:
        pagina = int(request.url.params["pagina"])
        chamadas.append((str(request.url), pagina))
        dados = (
            [
                {
                    "id": 42,
                    "nome": "Deputada Exemplo",
                    "siglaUf": "sp",
                    "siglaPartido": "ABC",
                    "nomePartido": "Partido Exemplo",
                }
            ]
            if pagina == 1
            else []
        )
        return httpx.Response(200, json={"dados": dados}, request=request)

    cliente = ClienteFonte(
        DiskCache(tmp_path),
        client=httpx.Client(transport=httpx.MockTransport(handler)),
        rate=100,
    )
    deputados = coletar_deputados(
        cliente,
        coletado_em=datetime(2026, 10, 6, tzinfo=UTC),
        itens_por_pagina=1,
    )

    assert [pagina for _, pagina in chamadas] == [1, 2]
    assert all(url.startswith(ENDPOINT) for url, _ in chamadas)
    assert deputados[0].id_camara == 42
    assert deputados[0].slug == "deputada-exemplo-sp"
    assert deputados[0].partido_nome == "Partido Exemplo"
    assert str(deputados[0].fonte.url).startswith("https://")
