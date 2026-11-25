# SPDX-License-Identifier: AGPL-3.0-or-later
"""Cálculos objetivos de alinhamento em votações e tópicos relevantes (Fase 8)."""

from __future__ import annotations

from datetime import UTC, date, datetime
from typing import Any

from praca_pipeline.modelos.dominio import (
    PesquisaEleitoral,
    Proveniencia,
    Votacao,
    VotoNominal,
)


def calcular_indice_alinhamento(
    votos: list[VotoNominal],
    *,
    alvo: str = "partido",
    n_minimo: int = 10,
) -> float | None:
    """Calcula percentual de votos nominais coincidentes com orientação de partido ou governo."""

    if n_minimo < 1:
        raise ValueError("n_minimo deve ser maior que zero")
    if alvo not in {"partido", "governo"}:
        raise ValueError("alvo deve ser 'partido' ou 'governo'")

    comparaveis = 0
    coincidentes = 0
    for voto in votos:
        escolha = voto.escolha
        if escolha not in {"sim", "nao"}:
            continue
        orientacao = voto.orientacao_partido if alvo == "partido" else voto.orientacao_governo
        if not orientacao:
            continue
        norm = orientacao.strip().casefold()
        norm_orient = "sim" if norm == "sim" else "nao" if norm in {"não", "nao"} else None
        if norm_orient is None:
            continue
        comparaveis += 1
        if escolha == norm_orient:
            coincidentes += 1

    if comparaveis < n_minimo:
        return None
    return round(100.0 * coincidentes / comparaveis, 1)


def filtrar_votacoes_relevantes(
    votacoes: list[Votacao],
    *,
    margem_maxima: float = 0.20,
    n_minimo: int = 10,
    cobertura_minima: float = 0.50,
) -> list[Votacao]:
    """Critério objetivo para votações em destaque: placar nominal apertado dentro da margem."""

    if n_minimo < 1:
        raise ValueError("n_minimo deve ser maior que zero")
    if not 0 <= cobertura_minima <= 1.0:
        raise ValueError("cobertura_minima deve estar entre 0 e 1")
    if not 0 < margem_maxima <= 1.0:
        raise ValueError("margem_maxima deve estar entre 0 e 1")

    selecionadas: list[Votacao] = []
    for votacao in votacoes:
        sim = sum(1 for v in votacao.votos if v.escolha == "sim")
        nao = sum(1 for v in votacao.votos if v.escolha == "nao")
        total = sim + nao
        if total < n_minimo:
            continue
        if len(votacao.votos) and total / len(votacao.votos) < cobertura_minima:
            continue
        diferenca_relativa = abs(sim - nao) / total
        if diferenca_relativa <= margem_maxima:
            selecionadas.append(votacao)
    return selecionadas


def validar_pesquisa_eleitoral(
    dados: dict[str, Any],
    *,
    coletado_em: datetime | None = None,
) -> PesquisaEleitoral:
    """Valida e registra pesquisa eleitoral com número de registro no TSE e margem de erro."""

    momento = coletado_em or datetime.now(UTC)
    registro = str(dados["registro_tse"]).strip()
    instituto = str(dados["instituto"]).strip()
    return PesquisaEleitoral(
        registro_tse=registro,
        instituto=instituto,
        cargo=str(dados["cargo"]).strip(),
        data_divulgacao=date.fromisoformat(str(dados["data_divulgacao"])[:10]),
        margem_erro_pp=float(dados["margem_erro_pp"]),
        confianca_pct=float(dados.get("confianca_pct") or 95.0),
        percentual_candidato=float(dados["percentual_candidato"]),
        fonte=Proveniencia(
            valor=f"{instituto} ({registro})",
            fonte_id="tse",
            url=str(dados.get("url") or "https://www.tse.jus.br/eleicoes/pesquisas-eleitorais"),
            coletado_em=momento,
            licenca="dados públicos; registro oficial TSE",
        ),
    )
