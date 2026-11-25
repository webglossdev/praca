# SPDX-License-Identifier: AGPL-3.0-or-later
"""Coletores adicionais do Legislativo: votações, cota/CEAPS e eventos."""

from __future__ import annotations

import csv
import io
from datetime import UTC, date, datetime
from decimal import Decimal, InvalidOperation
from typing import Any

from praca_pipeline.convencoes import slugificar
from praca_pipeline.http import ClienteFonte
from praca_pipeline.modelos.dominio import (
    Despesa,
    Proveniencia,
    Votacao,
    Voto,
)

CAMARA_BASE = "https://dadosabertos.camara.leg.br"
SENADO_BASE = "https://legis.senado.leg.br"

_MAPA_VOTO = {
    "sim": "sim",
    "não": "nao",
    "nao": "nao",
    "abstenção": "abstencao",
    "abstencao": "abstencao",
    "obstrução": "obstrucao",
    "obstrucao": "obstrucao",
    "licença": "licenca",
    "licenca": "licenca",
}


def _normalizar_voto(valor: Any) -> str:
    if not isinstance(valor, str):
        return "ausente"
    return _MAPA_VOTO.get(valor.strip().casefold(), "ausente")


def _decimal_br(valor: Any) -> Decimal:
    if isinstance(valor, Decimal):
        return valor
    if isinstance(valor, (int, float)):
        return Decimal(str(valor))
    if not isinstance(valor, str):
        raise ValueError("valor decimal inválido")
    texto = valor.strip()
    if "," in texto:
        texto = texto.replace(".", "").replace(",", ".")
    try:
        return Decimal(texto)
    except InvalidOperation as exc:
        raise ValueError(f"não foi possível converter '{valor}' para Decimal") from exc


def coletar_votacoes_camara(
    cliente: ClienteFonte,
    *,
    data_inicio: date,
    data_fim: date,
) -> list[Votacao]:
    """Coleta votações da Câmara respeitando janela máxima de 90 dias."""

    if data_fim < data_inicio:
        raise ValueError("data_fim não pode ser anterior a data_inicio")
    if (data_fim - data_inicio).days > 90:
        raise ValueError("janela de votações da Câmara não pode exceder 90 dias")

    endpoint = f"{CAMARA_BASE}/api/v2/votacoes"
    payload = cliente.get_json(
        endpoint,
        params={
            "dataInicio": data_inicio.isoformat(),
            "dataFim": data_fim.isoformat(),
            "ordem": "DESC",
            "ordenarPor": "dataHoraRegistro",
            "itens": "100",
        },
        fresh_for=3600,
    )
    if not isinstance(payload, dict) or not isinstance(payload.get("dados"), list):
        raise ValueError("resposta de votações da Câmara deve conter 'dados'")

    resultado: list[Votacao] = []
    for item in payload["dados"]:
        if not isinstance(item, dict) or "id" not in item:
            raise ValueError("registro de votação da Câmara inválido")
        votacao_id = str(item["id"])
        bruto_votos = item.get("votos")
        if not isinstance(bruto_votos, list):
            detalhe = cliente.get_json(f"{endpoint}/{votacao_id}/votos", fresh_for=3600)
            bruto_votos = detalhe.get("dados", []) if isinstance(detalhe, dict) else []

        votos: list[Voto] = []
        for bruto in bruto_votos:
            if not isinstance(bruto, dict):
                continue
            dep = bruto.get("deputado_") or {}
            nome = str(dep.get("nome") or bruto.get("nome") or "Parlamentar").strip()
            uf = str(dep.get("siglaUf") or bruto.get("uf") or "").strip().upper() or None
            partido = str(dep.get("siglaPartido") or bruto.get("partido") or "").strip() or None
            slug = slugificar(nome, uf)
            escolha = _normalizar_voto(bruto.get("tipoVoto") or bruto.get("voto"))
            votos.append(
                Voto(
                    pid=f"pid_{slug}",
                    escolha=escolha,
                    nome=nome,
                    partido=partido,
                    uf=uf,
                )
            )

        data_bruta = str(
            item.get("data") or item.get("dataHoraRegistro") or data_inicio.isoformat()
        )
        aprovacao = item.get("aprovacao")
        resultado_str = (
            "Aprovada" if aprovacao == 1 else "Rejeitada" if aprovacao == 0 else "Registrada"
        )
        if isinstance(item.get("descricao"), str) and item["descricao"].strip():
            resultado_str = str(item.get("resultado") or resultado_str)
        proposicao_ref = str(
            item.get("proposicaoId") or item.get("idProposicao") or votacao_id
        )
        resultado.append(
            Votacao(
                id=votacao_id,
                proposicao_id=proposicao_ref,
                data=date.fromisoformat(data_bruta[:10]),
                resultado=resultado_str,
                votos=votos,
                casa="camara",
                proposicao_label=item.get("siglaOrgao"),
                titulo=item.get("descricao"),
                url=item.get("uri") or endpoint,
            )
        )
    return resultado


def coletar_cota_camara(
    cliente: ClienteFonte,
    *,
    id_camara: int,
    pid: str,
    ano: int,
    coletado_em: datetime | None = None,
) -> list[Despesa]:
    """Coleta despesas da cota parlamentar (CEAP) de um deputado na Câmara."""

    momento = coletado_em or datetime.now(UTC)
    endpoint = f"{CAMARA_BASE}/api/v2/deputados/{id_camara}/despesas"
    payload = cliente.get_json(
        endpoint,
        params={"ano": str(ano), "itens": "100", "ordem": "ASC"},
        fresh_for=12 * 3600,
    )
    if not isinstance(payload, dict) or not isinstance(payload.get("dados"), list):
        raise ValueError("resposta de despesas da Câmara deve conter 'dados'")

    despesas: list[Despesa] = []
    for item in payload["dados"]:
        if not isinstance(item, dict):
            continue
        valor_bruto = item.get("valorLiquido")
        if valor_bruto is None:
            valor_bruto = item.get("valorDocumento")
        if valor_bruto is None:
            continue
        valor = _decimal_br(valor_bruto)
        if valor < 0:
            continue
        mes = int(item.get("mes") or 1)
        ano_item = int(item.get("ano") or ano)
        competencia = date(ano_item, max(1, min(12, mes)), 1)
        categoria = str(item.get("tipoDespesa") or "Cota parlamentar").strip()
        despesas.append(
            Despesa(
                pid=pid,
                categoria=categoria,
                valor=valor,
                competencia=competencia,
                fonte=Proveniencia(
                    valor=valor,
                    fonte_id="camara",
                    url=endpoint,
                    coletado_em=momento,
                    licenca="dados públicos; termos da fonte",
                ),
            )
        )
    return despesas


def coletar_eventos_camara(
    cliente: ClienteFonte,
    *,
    data_inicio: date,
    data_fim: date,
) -> list[dict[str, Any]]:
    """Coleta eventos de pauta e reuniões da Câmara para agenda e presença."""

    endpoint = f"{CAMARA_BASE}/api/v2/eventos"
    payload = cliente.get_json(
        endpoint,
        params={
            "dataInicio": data_inicio.isoformat(),
            "dataFim": data_fim.isoformat(),
            "itens": "100",
            "ordem": "ASC",
        },
        fresh_for=1800,
    )
    if not isinstance(payload, dict) or not isinstance(payload.get("dados"), list):
        raise ValueError("resposta de eventos da Câmara deve conter 'dados'")

    eventos: list[dict[str, Any]] = []
    for item in payload["dados"]:
        if not isinstance(item, dict) or "id" not in item:
            continue
        orgaos = item.get("orgaos") or []
        orgao_sigla = (
            str(orgaos[0].get("sigla"))
            if isinstance(orgaos, list) and orgaos and isinstance(orgaos[0], dict)
            else "Plenário/Comissões"
        )
        titulo_evento = str(
            item.get("descricaoTipo") or item.get("descricao") or "Evento"
        ).strip()
        eventos.append(
            {
                "id": str(item["id"]),
                "titulo": titulo_evento,
                "orgao": orgao_sigla,
                "inicio": str(item.get("dataHoraInicio") or data_inicio.isoformat()),
                "situacao": str(item.get("situacao") or "Programado").strip(),
            }
        )
    return eventos


def coletar_votacoes_senado(
    cliente: ClienteFonte,
    *,
    data_inicio: date,
    data_fim: date,
) -> list[Votacao]:
    """Coleta votações no endpoint vigente do Senado Federal."""

    endpoint = f"{SENADO_BASE}/dadosabertos/votacao.json"
    payload = cliente.get_json(
        endpoint,
        params={
            "dataInicio": data_inicio.isoformat(),
            "dataFim": data_fim.isoformat(),
        },
        fresh_for=3600,
    )
    if isinstance(payload, dict):
        itens = payload.get("votacoes") or payload.get("dados") or []
    elif isinstance(payload, list):
        itens = payload
    else:
        raise ValueError("resposta de votações do Senado inválida")

    votacoes: list[Votacao] = []
    for item in itens:
        if not isinstance(item, dict):
            continue
        codigo = str(item.get("codigoSessaoVotacao") or item.get("id") or "")
        if not codigo:
            continue
        bruto_votos = item.get("votos") or []
        votos: list[Voto] = []
        for v in bruto_votos:
            if not isinstance(v, dict):
                continue
            nome = str(v.get("nomeParlamentar") or v.get("nome") or "").strip()
            if not nome:
                continue
            uf = str(v.get("siglaUF") or v.get("uf") or "").strip().upper() or None
            partido = str(v.get("siglaPartido") or v.get("partido") or "").strip() or None
            votos.append(
                Voto(
                    pid=f"pid_{slugificar(nome, uf)}",
                    escolha=_normalizar_voto(v.get("siglaVoto") or v.get("voto")),
                    nome=nome,
                    partido=partido,
                    uf=uf,
                )
            )

        data_str = str(item.get("dataSessao") or data_inicio.isoformat())[:10]
        votacoes.append(
            Votacao(
                id=f"senado-{codigo}",
                proposicao_id=str(item.get("codigoMateria") or codigo),
                data=date.fromisoformat(data_str),
                resultado=str(item.get("resultado") or "Registrada").strip(),
                votos=votos,
                casa="senado",
                proposicao_label=item.get("identificacao"),
                titulo=item.get("descricaoVotacao"),
                url=f"{SENADO_BASE}/dadosabertos/votacao.json",
            )
        )
    return votacoes


def parsear_ceaps_senado_csv(
    conteudo_bytes: bytes,
    *,
    coletado_em: datetime,
) -> list[Despesa]:
    """Lê CSV oficial da CEAPS (Latin-1) ignorando linha de metadados antes do cabeçalho."""

    texto = conteudo_bytes.decode("latin-1")
    linhas = [linha for linha in texto.splitlines() if linha.strip()]
    inicio_cabecalho = next(
        (i for i, linha in enumerate(linhas) if "SENADOR" in linha.upper() and ";" in linha),
        None,
    )
    if inicio_cabecalho is None:
        raise ValueError("cabeçalho CEAPS do Senado não encontrado no CSV")

    leitor = csv.DictReader(io.StringIO("\n".join(linhas[inicio_cabecalho:])), delimiter=";")
    despesas: list[Despesa] = []
    url_ceaps = "https://www12.senado.leg.br/transparencia/sen/ceaps"
    for row in leitor:
        senador = (row.get("SENADOR") or "").strip()
        if not senador:
            continue
        uf = (row.get("UF") or "").strip().upper() or None
        valor_raw = row.get("VALOR_REEMBOLSADO") or row.get("VALOR") or "0"
        valor = _decimal_br(valor_raw)
        if valor < 0:
            continue
        ano = int(row.get("ANO") or coletado_em.year)
        mes = int(row.get("MES") or 1)
        categoria = (row.get("TIPO_DESPESA") or "CEAPS").strip()
        despesas.append(
            Despesa(
                pid=f"pid_{slugificar(senador, uf)}",
                categoria=categoria,
                valor=valor,
                competencia=date(ano, max(1, min(12, mes)), 1),
                fonte=Proveniencia(
                    valor=valor,
                    fonte_id="senado",
                    url=url_ceaps,
                    coletado_em=coletado_em,
                    licenca="dados públicos; termos da fonte",
                ),
            )
        )
    return despesas
