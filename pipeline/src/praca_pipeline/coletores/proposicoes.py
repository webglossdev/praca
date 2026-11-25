# SPDX-License-Identifier: AGPL-3.0-or-later
"""Coleta de proposições da Câmara a partir da API oficial."""

from datetime import date
from typing import Any

from praca_pipeline.http import ClienteFonte
from praca_pipeline.modelos.dominio import Proposicao

BASE_URL = "https://dadosabertos.camara.leg.br"
ENDPOINT = f"{BASE_URL}/api/v2/proposicoes"


def _data(value: Any) -> date:
    if not isinstance(value, str):
        raise ValueError("proposição sem data válida")
    return date.fromisoformat(value[:10])


def coletar_proposicoes(
    cliente: ClienteFonte,
    *,
    pagina: int = 1,
    itens: int = 100,
    desde: date | None = None,
) -> list[Proposicao]:
    """Coleta uma página de proposições, opcionalmente filtrada por data."""

    if pagina < 1 or not 1 <= itens <= 100:
        raise ValueError("pagina deve ser positiva e itens deve estar entre 1 e 100")
    params = {
        "pagina": str(pagina),
        "itens": str(itens),
        "ordem": "DESC",
        "ordenarPor": "id",
    }
    if desde:
        params["dataApresentacaoInicio"] = desde.isoformat()
    payload = cliente.get_json(ENDPOINT, params=params, fresh_for=6 * 60 * 60)
    if not isinstance(payload, dict) or not isinstance(payload.get("dados"), list):
        raise ValueError("resposta de proposições deve conter a lista 'dados'")

    resultado: list[Proposicao] = []
    for item in payload["dados"]:
        if not isinstance(item, dict):
            raise ValueError("item de proposição inválido")
        try:
            resultado.append(
                Proposicao(
                    id=str(item["id"]),
                    casa="camara",
                    tipo=str(item["siglaTipo"]),
                    numero=int(item["numero"]),
                    ano=int(item["ano"]),
                    ementa=str(item["ementa"]),
                    url=item["uri"],
                )
            )
        except (KeyError, TypeError, ValueError) as exc:
            raise ValueError("proposição sem campos obrigatórios") from exc
    return resultado
