# SPDX-License-Identifier: AGPL-3.0-or-later
"""Coletor mínimo dos deputados da API Dados Abertos da Câmara."""

from datetime import UTC, date, datetime
from typing import Any

from pydantic import Field

from praca_pipeline.convencoes import slugificar
from praca_pipeline.http import ClienteFonte
from praca_pipeline.modelos.dominio import Contrato, Mandato, Poder, Proveniencia, StatusMandato

BASE_URL = "https://dadosabertos.camara.leg.br"
ENDPOINT = f"{BASE_URL}/api/v2/deputados"


class DeputadoCamara(Contrato):
    """Registro normalizado da listagem de deputados da Câmara."""

    id_camara: int = Field(ge=1)
    nome: str = Field(min_length=1)
    slug: str = Field(pattern=r"^[a-z0-9]+(?:-[a-z0-9]+)+$")
    uf: str = Field(min_length=2, max_length=2)
    partido_sigla: str | None = None
    partido_nome: str | None = None
    mandato: Mandato
    fonte: Proveniencia[str]


def _texto(item: dict[str, Any], chave: str) -> str | None:
    valor = item.get(chave)
    return valor.strip() if isinstance(valor, str) and valor.strip() else None


def _normalizar(item: dict[str, Any], coletado_em: datetime) -> DeputadoCamara:
    try:
        id_camara = int(item["id"])
        nome = str(item["nome"]).strip()
        uf = str(item["siglaUf"]).strip().upper()
    except (KeyError, TypeError, ValueError) as exc:
        raise ValueError("registro da Câmara sem id, nome ou siglaUf válidos") from exc
    if not nome or len(uf) != 2:
        raise ValueError("registro da Câmara sem nome ou UF válidos")

    return DeputadoCamara(
        id_camara=id_camara,
        nome=nome,
        slug=slugificar(nome, uf),
        uf=uf,
        partido_sigla=_texto(item, "siglaPartido"),
        partido_nome=_texto(item, "nomePartido"),
        mandato=Mandato(
            poder=Poder.LEGISLATIVO,
            cargo="Deputado federal",
            uf=uf,
            inicio=date(2023, 2, 1),
            status=StatusMandato.ATIVO,
        ),
        fonte=Proveniencia(
            valor="Deputado listado pela API da Câmara",
            fonte_id="camara",
            url=BASE_URL,
            coletado_em=coletado_em,
            licenca="dados públicos; termos da fonte",
        ),
    )


def coletar_deputados(
    cliente: ClienteFonte,
    *,
    coletado_em: datetime | None = None,
    itens_por_pagina: int = 100,
) -> list[DeputadoCamara]:
    """Coleta todas as páginas da listagem atual de deputados."""

    if not 1 <= itens_por_pagina <= 100:
        raise ValueError("itens_por_pagina deve estar entre 1 e 100")
    momento = coletado_em or datetime.now(UTC)
    resultado: list[DeputadoCamara] = []
    pagina = 1
    while True:
        payload = cliente.get_json(
            ENDPOINT,
            params={
                "pagina": str(pagina),
                "itens": str(itens_por_pagina),
                "ordem": "ASC",
                "ordenarPor": "nome",
            },
            fresh_for=24 * 60 * 60,
        )
        if not isinstance(payload, dict) or not isinstance(payload.get("dados"), list):
            raise ValueError("resposta da Câmara deve conter a lista 'dados'")
        dados = payload["dados"]
        resultado.extend(_normalizar(item, momento) for item in dados)
        if len(dados) < itens_por_pagina:
            return resultado
        pagina += 1
