# SPDX-License-Identifier: AGPL-3.0-or-later
"""Coletores e parsers em lote para TSE, Receita/QSA, CGU, Executivo, STF e DOU."""

from __future__ import annotations

import csv
import io
from datetime import date, datetime
from decimal import Decimal
from typing import Any

from praca_pipeline.convencoes import slugificar
from praca_pipeline.modelos.dominio import (
    Bem,
    Doacao,
    Emenda,
    Filiacao,
    Mandato,
    Partido,
    Pessoa,
    Poder,
    Proveniencia,
    SancaoEmpresa,
    StatusMandato,
)

TSE_PORTAL = "https://dadosabertos.tse.jus.br"
CGU_PORTAL = "https://portaldatransparencia.gov.br"


def _dec(raw: Any) -> Decimal:
    texto = str(raw or "0").strip()
    if "," in texto:
        texto = texto.replace(".", "").replace(",", ".")
    return Decimal(texto)


def _data_br_ou_iso(raw: str | None, fallback: date) -> date:
    if not raw or not raw.strip():
        return fallback
    texto = raw.strip()[:10]
    if "/" in texto:
        dia, mes, ano = texto.split("/")
        return date(int(ano), int(mes), int(dia))
    return date.fromisoformat(texto)


def _status_tse(situacao: str, posse_iniciada: bool) -> StatusMandato:
    s = situacao.strip().upper()
    if "ELEITO" in s:
        return StatusMandato.ATIVO if posse_iniciada else StatusMandato.ELEITO_AGUARDANDO_POSSE
    if "SUPLENTE" in s:
        return StatusMandato.ENCERRADO
    return StatusMandato.ENCERRADO


def _abrir_csv(linhas: str) -> csv.DictReader[str]:
    amostra = linhas.splitlines()[0] if linhas.strip() else ";"
    delimitador = ";" if amostra.count(";") >= amostra.count(",") else ","
    return csv.DictReader(io.StringIO(linhas.strip()), delimiter=delimitador)


def parsear_candidaturas_tse_csv(
    linhas: str,
    *,
    coletado_em: datetime,
    posse_iniciada: bool = False,
) -> list[Pessoa]:
    """Converte linhas CSV do TSE em perfis normalizados com distinção de posse."""

    pessoas: list[Pessoa] = []
    for row in _abrir_csv(linhas):
        nome = (row.get("NM_CANDIDATO") or "").strip()
        if not nome:
            continue
        nome_urna = (row.get("NM_URNA_CANDIDATO") or nome).strip()
        cargo = (row.get("DS_CARGO") or "Cargo eletivo").strip().title()
        uf_raw = (row.get("SG_UF") or "").strip().upper()
        uf = uf_raw if len(uf_raw) == 2 and uf_raw != "BR" else None
        sigla_partido = (row.get("SG_PARTIDO") or "").strip().upper()
        nome_partido = (row.get("NM_PARTIDO") or sigla_partido).strip()
        numero_raw = (row.get("NR_PARTIDO") or "").strip()
        ano_eleicao = int(row.get("ANO_ELEICAO") or row.get("NR_ANO_ELEICAO") or 2026)
        inicio_mandato = date(ano_eleicao + 1, 1, 1)
        if "DEPUTAD" in cargo.upper() or "SENADOR" in cargo.upper():
            inicio_mandato = date(ano_eleicao + 1, 2, 1)

        slug = slugificar(nome_urna, uf)
        if "-" not in slug:
            slug = f"{slug}-br"
        partido = (
            Partido(
                sigla=sigla_partido,
                nome=nome_partido,
                numero=int(numero_raw) if numero_raw.isdigit() else None,
            )
            if len(sigla_partido) >= 2
            else None
        )
        pessoas.append(
            Pessoa(
                pid=f"pid_{slug}",
                nome=nome.title(),
                nome_publico=nome_urna.title(),
                slug=slug,
                mandatos=[
                    Mandato(
                        poder=Poder.EXECUTIVO
                        if any(k in cargo.upper() for k in ("PRESIDENTE", "GOVERNADOR", "PREFEIT"))
                        else Poder.LEGISLATIVO,
                        cargo=cargo,
                        uf=uf,
                        inicio=inicio_mandato,
                        status=_status_tse(row.get("DS_SIT_TOT_TURNO") or "", posse_iniciada),
                    )
                ],
                partido=partido,
                apelidos=[nome_urna.title()] if nome_urna.title() != nome.title() else [],
                fontes=[
                    Proveniencia(
                        valor="Tribunal Superior Eleitoral",
                        fonte_id="tse",
                        url=TSE_PORTAL,
                        coletado_em=coletado_em,
                        licenca="dados públicos; termos da fonte",
                    )
                ],
            )
        )
    return pessoas


def parsear_bens_tse_csv(linhas: str, *, coletado_em: datetime) -> list[Bem]:
    """Lê bens declarados do CSV oficial do TSE."""

    bens: list[Bem] = []
    for row in _abrir_csv(linhas):
        slug_cand = slugificar(row.get("NM_URNA_CANDIDATO", ""), row.get("SG_UF"))
        pid = (row.get("PID") or f"pid_{slug_cand}").strip()
        valor = _dec(row.get("VR_BEM_CANDIDATO"))
        ano = int(row.get("ANO_ELEICAO") or 2026)
        bens.append(
            Bem(
                pid=pid,
                descricao=(row.get("DS_BEM_CANDIDATO") or "Bem declarado").strip(),
                valor=valor,
                ano_eleitoral=ano,
                fonte=Proveniencia(
                    valor=valor,
                    fonte_id="tse",
                    url=TSE_PORTAL,
                    coletado_em=coletado_em,
                    licenca="dados públicos; termos da fonte",
                ),
            )
        )
    return bens


def parsear_doacoes_tse_csv(linhas: str, *, coletado_em: datetime) -> list[Doacao]:
    """Lê receitas/doações de campanha e FEFC do CSV do TSE."""

    doacoes: list[Doacao] = []
    for row in _abrir_csv(linhas):
        slug_cand = slugificar(row.get("NM_CANDIDATO", ""), row.get("SG_UF"))
        pid = (row.get("PID") or f"pid_{slug_cand}").strip()
        valor = _dec(row.get("VR_RECEITA"))
        if valor <= 0:
            continue
        ano = int(row.get("ANO_ELEICAO") or 2026)
        doador = (
            row.get("NM_DOADOR") or row.get("DS_ORIGEM_RECEITA") or "Não identificado"
        ).strip()
        doacoes.append(
            Doacao(
                candidato_pid=pid,
                doador=doador,
                valor=valor,
                ano_eleitoral=ano,
                fonte=Proveniencia(
                    valor=valor,
                    fonte_id="tse",
                    url=TSE_PORTAL,
                    coletado_em=coletado_em,
                    licenca="dados públicos; termos da fonte",
                ),
            )
        )
    return doacoes


def parsear_filiacoes_tse_csv(linhas: str, *, coletado_em: datetime) -> list[Filiacao]:
    """Lê histórico de filiações partidárias."""

    filiacoes: list[Filiacao] = []
    for row in _abrir_csv(linhas):
        slug_eleitor = slugificar(row.get("NM_ELEITOR", ""), row.get("SG_UF"))
        pid = (row.get("PID") or f"pid_{slug_eleitor}").strip()
        sigla = (row.get("SG_PARTIDO") or "").strip().upper()
        if not sigla:
            continue
        inicio = _data_br_ou_iso(row.get("DT_FILIACAO"), date(2020, 1, 1))
        fim_raw = row.get("DT_DESFILIACAO")
        fim = _data_br_ou_iso(fim_raw, date(2020, 1, 1)) if fim_raw and fim_raw.strip() else None
        filiacoes.append(
            Filiacao(
                pid=pid,
                partido_sigla=sigla,
                inicio=inicio,
                fim=fim,
                fonte=Proveniencia(
                    valor=f"Filiação ao {sigla}",
                    fonte_id="tse",
                    url=TSE_PORTAL,
                    coletado_em=coletado_em,
                    licenca="dados públicos; termos da fonte",
                ),
            )
        )
    return filiacoes


def parsear_qsa_receita_csv(linhas: str) -> dict[str, list[dict[str, str]]]:
    """Indexa sócios por CNPJ preservando CPF mascarado conforme publicado pela Receita."""

    indice: dict[str, list[dict[str, str]]] = {}
    for row in _abrir_csv(linhas):
        cnpj_bruto = row.get("CNPJ_BASICO") or row.get("CNPJ") or ""
        cnpj = "".join(ch for ch in cnpj_bruto if ch.isdigit())
        nome_socio = (row.get("NOME_SOCIO") or "").strip()
        if not cnpj or not nome_socio:
            continue
        indice.setdefault(cnpj, []).append(
            {
                "nome": nome_socio,
                "cpf_cnpj_mascarado": (row.get("CPF_CNPJ_SOCIO") or "não informado").strip(),
                "qualificacao": (row.get("QUALIFICACAO_SOCIO") or "Sócio").strip(),
            }
        )
    return indice


def normalizar_emendas_cgu(
    itens: list[dict[str, Any]],
    *,
    coletado_em: datetime,
) -> list[Emenda]:
    """Normaliza emendas parlamentares do Portal da Transparência (CGU)."""

    emendas: list[Emenda] = []
    for item in itens:
        pid = str(item.get("pid") or "").strip()
        if not pid:
            continue
        valor = _dec(item.get("valorEmpenhado") or item.get("valor") or 0)
        favorecido = str(
            item.get("localidadeDoGasto") or item.get("favorecido") or "Nacional"
        ).strip()
        emendas.append(
            Emenda(
                parlamentar_pid=pid,
                favorecido=favorecido,
                valor_empenhado=valor,
                ano=int(item.get("ano") or coletado_em.year),
                fonte=Proveniencia(
                    valor=valor,
                    fonte_id="cgu-transparencia",
                    url=CGU_PORTAL,
                    coletado_em=coletado_em,
                    licenca="dados públicos; termos da fonte",
                ),
            )
        )
    return emendas


def normalizar_sancoes_cgu(
    itens: list[dict[str, Any]],
    *,
    coletado_em: datetime,
) -> list[SancaoEmpresa]:
    """Normaliza registros oficiais CEIS, CNEP e CEPIM da CGU."""

    sancoes: list[SancaoEmpresa] = []
    for item in itens:
        cnpj = str(item.get("cnpj") or "").strip()
        razao = str(item.get("razaoSocial") or item.get("razao_social") or "").strip()
        if not cnpj or not razao:
            continue
        cadastro = str(item.get("cadastro") or "CEIS").strip().upper()
        motivo = str(
            item.get("motivo") or item.get("fundamentacaoLegal") or "Sanção administrativa"
        ).strip()
        sancoes.append(
            SancaoEmpresa(
                cnpj=cnpj,
                razao_social=razao,
                cadastro=cadastro,
                motivo=motivo,
                data_inicio=_data_br_ou_iso(item.get("dataInicioSancao"), coletado_em.date()),
                data_fim=(
                    _data_br_ou_iso(item.get("dataFimSancao"), coletado_em.date())
                    if item.get("dataFimSancao")
                    else None
                ),
                fonte=Proveniencia(
                    valor=f"Registro {cadastro}",
                    fonte_id="cgu-transparencia",
                    url=CGU_PORTAL,
                    coletado_em=coletado_em,
                    licenca="dados públicos; termos da fonte",
                ),
            )
        )
    return sancoes


def normalizar_agentes_publicos(
    itens: list[dict[str, Any]],
    *,
    poder: Poder,
    fonte_id: str,
    url: str,
    coletado_em: datetime,
) -> list[Pessoa]:
    """Normaliza ministros do Executivo, ministros do STF, governadores e atos de posse/DOU."""

    pessoas: list[Pessoa] = []
    for item in itens:
        nome = str(item.get("nome") or "").strip()
        cargo = str(item.get("cargo") or "").strip()
        if not nome or not cargo:
            continue
        uf_raw = str(item.get("uf") or "").strip().upper()
        uf = uf_raw if len(uf_raw) == 2 else None
        slug = slugificar(nome, uf or ("stf" if poder == Poder.JUDICIARIO else "br"))
        inicio = _data_br_ou_iso(item.get("inicio"), coletado_em.date())
        pessoas.append(
            Pessoa(
                pid=f"pid_{slug}",
                nome=nome,
                nome_publico=str(item.get("nome_publico") or nome).strip(),
                slug=slug,
                mandatos=[
                    Mandato(
                        poder=poder,
                        cargo=cargo,
                        uf=uf,
                        inicio=inicio,
                        status=StatusMandato(item.get("status") or StatusMandato.ATIVO),
                    )
                ],
                fontes=[
                    Proveniencia(
                        valor=str(item.get("fonte_valor") or cargo),
                        fonte_id=fonte_id,
                        url=url,
                        coletado_em=coletado_em,
                        licenca="dados públicos; termos da fonte",
                    )
                ],
            )
        )
    return pessoas
