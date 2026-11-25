# SPDX-License-Identifier: AGPL-3.0-or-later
"""Coletor da lista atual de senadores do Senado Federal."""

from datetime import UTC, date, datetime
from typing import Any

from pydantic import Field

from praca_pipeline.convencoes import slugificar
from praca_pipeline.http import ClienteFonte
from praca_pipeline.modelos.dominio import (
    Contrato,
    Mandato,
    Poder,
    Proveniencia,
    StatusMandato,
)

BASE_URL = "https://legis.senado.leg.br"
ENDPOINT = f"{BASE_URL}/dadosabertos/senador/lista/atual.json"


class SenadorSenado(Contrato):
    """Registro normalizado da lista de senadores em exercício."""

    id_senado: int = Field(ge=1)
    nome: str = Field(min_length=1)
    nome_completo: str | None = None
    slug: str = Field(pattern=r"^[a-z0-9]+(?:-[a-z0-9]+)+$")
    uf: str = Field(min_length=2, max_length=2)
    partido_sigla: str | None = None
    mandato: Mandato
    fonte: Proveniencia[str]


def _primeiro_exercicio(mandato: dict[str, Any]) -> date:
    exercicios = mandato.get("Exercicios", {}).get("Exercicio", [])
    if isinstance(exercicios, dict):
        exercicios = [exercicios]
    if not exercicios or not isinstance(exercicios[0], dict):
        return date(2023, 2, 1)
    inicio = exercicios[0].get("DataInicio")
    if not isinstance(inicio, str):
        return date(2023, 2, 1)
    return date.fromisoformat(inicio)


def _normalizar(item: dict[str, Any], coletado_em: datetime) -> SenadorSenado:
    identificacao = item.get("IdentificacaoParlamentar")
    mandato = item.get("Mandato")
    if not isinstance(identificacao, dict) or not isinstance(mandato, dict):
        raise ValueError("registro do Senado sem identificação ou mandato")
    try:
        codigo = int(identificacao["CodigoParlamentar"])
        nome = str(identificacao["NomeParlamentar"]).strip()
        uf = str(identificacao["UfParlamentar"]).strip().upper()
    except (KeyError, TypeError, ValueError) as exc:
        raise ValueError("registro do Senado sem código, nome ou UF válidos") from exc
    if not nome or len(uf) != 2:
        raise ValueError("registro do Senado sem nome ou UF válidos")

    nome_completo = identificacao.get("NomeCompletoParlamentar")
    return SenadorSenado(
        id_senado=codigo,
        nome=nome,
        nome_completo=nome_completo.strip() if isinstance(nome_completo, str) else None,
        slug=slugificar(nome, uf),
        uf=uf,
        partido_sigla=identificacao.get("SiglaPartidoParlamentar"),
        mandato=Mandato(
            poder=Poder.LEGISLATIVO,
            cargo="Senador",
            uf=uf,
            inicio=_primeiro_exercicio(mandato),
            status=StatusMandato.ATIVO,
        ),
        fonte=Proveniencia(
            valor="Senador listado pela API do Senado",
            fonte_id="senado",
            url=BASE_URL,
            coletado_em=coletado_em,
            licenca="dados públicos; termos da fonte",
        ),
    )


def coletar_senadores(
    cliente: ClienteFonte,
    *,
    coletado_em: datetime | None = None,
) -> list[SenadorSenado]:
    """Coleta a lista atual de senadores em exercício."""

    momento = coletado_em or datetime.now(UTC)
    payload = cliente.get_json(ENDPOINT, fresh_for=24 * 60 * 60)
    try:
        itens = payload["ListaParlamentarEmExercicio"]["Parlamentares"]["Parlamentar"]
    except (KeyError, TypeError) as exc:
        raise ValueError("resposta do Senado sem a lista de parlamentares") from exc
    if isinstance(itens, dict):
        itens = [itens]
    if not isinstance(itens, list):
        raise ValueError("lista de parlamentares do Senado inválida")
    return [_normalizar(item, momento) for item in itens]
