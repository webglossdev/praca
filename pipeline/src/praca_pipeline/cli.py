# SPDX-License-Identifier: AGPL-3.0-or-later
"""CLI de coleta pública controlada do projeto Praça."""

from __future__ import annotations

import argparse
import json
import os
import re
import unicodedata
from datetime import UTC, datetime
from pathlib import Path

import yaml

from praca_pipeline.coletores.camara import coletar_deputados
from praca_pipeline.coletores.senado import coletar_senadores
from praca_pipeline.http import ClienteFonte, DiskCache
from praca_pipeline.modelos.dominio import (
    Partido,
    Pessoa,
    StatusColetor,
)
from praca_pipeline.noticias import parsear_feed_rss, remover_duplicatas

ROOT = Path(__file__).resolve().parents[3]
PUBLICO = ROOT / "data" / "publico"
BRUTO = ROOT / "data" / "bruto"


def _json_dump(path: Path, value: object) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        json.dumps(value, ensure_ascii=False, indent=2, default=str) + "\n",
        encoding="utf-8",
    )


def _status(
    fonte_id: str,
    nome: str,
    status: str,
    observado_em: datetime,
    *,
    observacao: str,
    circuit_breaker: str = "fechado",
) -> dict[str, object]:
    return StatusColetor(
        fonte_id=fonte_id,
        nome=nome,
        status=status,
        ultima_coleta=observado_em,
        latencia_ms=None,
        circuit_breaker=circuit_breaker,
        observacao=observacao,
    ).model_dump(mode="json")


def _partido(sigla: str | None, nome: str | None) -> Partido | None:
    if not sigla:
        return None
    sigla_ascii = (
        unicodedata.normalize("NFKD", sigla)
        .encode("ascii", "ignore")
        .decode()
        .upper()
    )
    sigla_normalizada = re.sub(r"[^A-Z0-9]", "", sigla_ascii)
    if not 2 <= len(sigla_normalizada) <= 32:
        return None
    nome_limpo = nome or sigla_normalizada
    if not nome_limpo.strip() or "/" in nome_limpo:
        nome_limpo = sigla_normalizada
    return Partido(sigla=sigla_normalizada, nome=nome_limpo.strip())


def _coletar_pessoas(
    cliente: ClienteFonte,
    observado_em: datetime,
) -> tuple[list[Pessoa], list[dict[str, object]]]:
    pessoas: list[Pessoa] = []
    statuses: list[dict[str, object]] = []

    try:
        deputados = coletar_deputados(cliente)
        for deputado in deputados:
            pessoas.append(
                Pessoa(
                    pid=f"pid_{deputado.slug}",
                    nome=deputado.nome,
                    nome_publico=deputado.nome,
                    slug=deputado.slug,
                    mandatos=[deputado.mandato],
                    partido=_partido(deputado.partido_sigla, deputado.partido_nome),
                    fontes=[deputado.fonte],
                )
            )
        statuses.append(
            _status(
                "camara",
                "Dados Abertos da Câmara",
                "ativa",
                observado_em,
                observacao=f"{len(deputados)} deputados coletados.",
            )
        )
    except Exception as exc:
        statuses.append(
            _status(
                "camara",
                "Dados Abertos da Câmara",
                "degradada",
                observado_em,
                observacao=(
                    f"Coleta indisponível: {exc}. "
                    "Último snapshot foi preservado quando disponível."
                ),
                circuit_breaker="aberto",
            )
        )

    try:
        senadores = coletar_senadores(cliente)
        for senador in senadores:
            pessoas.append(
                Pessoa(
                    pid=f"pid_{senador.slug}",
                    nome=senador.nome_completo or senador.nome,
                    nome_publico=senador.nome,
                    slug=senador.slug,
                    mandatos=[senador.mandato],
                    partido=_partido(senador.partido_sigla, senador.partido_sigla),
                    fontes=[senador.fonte],
                )
            )
        statuses.append(
            _status(
                "senado",
                "Dados Abertos do Senado",
                "ativa",
                observado_em,
                observacao=f"{len(senadores)} senadores coletados.",
            )
        )
    except Exception as exc:
        statuses.append(
            _status(
                "senado",
                "Dados Abertos do Senado",
                "degradada",
                observado_em,
                observacao=(
                    f"Coleta indisponível: {exc}. "
                    "Último snapshot foi preservado quando disponível."
                ),
                circuit_breaker="aberto",
            )
        )

    if not os.getenv("CGU_API_KEY"):
        statuses.append(
            _status(
                "cgu-transparencia",
                "Portal da Transparência (CGU)",
                "planejada",
                observado_em,
                observacao=(
                    "CGU_API_KEY não configurada. "
                    "Emendas e bases privadas não foram inventadas."
                ),
            )
        )

    if not os.getenv("DATAJUD_API_KEY"):
        statuses.append(
            _status(
                "stf",
                "STF / DataJud",
                "planejada",
                observado_em,
                observacao="DATAJUD_API_KEY não configurada. Composição pública não foi estimada.",
            )
        )

    deduplicadas: dict[str, Pessoa] = {pessoa.pid: pessoa for pessoa in pessoas}
    return list(deduplicadas.values()), statuses


def _coletar_noticias(
    cliente: ClienteFonte,
    observado_em: datetime,
) -> tuple[
    list[dict[str, object]],
    list[dict[str, object]],
    list[dict[str, object]],
]:
    veiculos_path = PUBLICO / "veiculos.yml"
    if not veiculos_path.exists():
        return [], [], []

    with veiculos_path.open("r", encoding="utf-8") as arquivo:
        veiculos = yaml.safe_load(arquivo) or []
    if not isinstance(veiculos, list):
        raise ValueError("veiculos.yml deve ser uma lista")

    noticias = []
    statuses = []
    pessoas_status = []

    for veiculo in veiculos:
        if not isinstance(veiculo, dict):
            continue
        fonte_id = str(veiculo["id"])
        nome = str(veiculo["nome"])
        feed = str(veiculo["feed"])
        try:
            resposta = cliente.client.get(feed, headers=cliente.headers)
            resposta.raise_for_status()
            itens = parsear_feed_rss(
                resposta.text,
                veiculo=nome,
                tipo_fonte=str(veiculo["tipo"]),
                licenca_aberta=veiculo.get("licenca_aberta"),
            )
            noticias.extend(itens)
            statuses.append(
                _status(
                    fonte_id,
                    nome,
                    "ativa",
                    observado_em,
                    observacao=f"{len(itens)} notícias normalizadas.",
                )
            )
        except Exception as exc:
            statuses.append(
                _status(
                    fonte_id,
                    nome,
                    "degradada",
                    observado_em,
                    observacao=f"Feed indisponível: {exc}",
                    circuit_breaker="aberto",
                )
            )

    normalizadas = [item.model_dump(mode="json") for item in remover_duplicatas(noticias)]
    return normalizadas, statuses, pessoas_status


def executar(*, data_mode: str = "publico") -> int:
    observado_em = datetime.now(UTC)
    cache = DiskCache(BRUTO / "cache")
    cliente = ClienteFonte(cache, rate=1.5)

    pessoas, status_pessoas = _coletar_pessoas(cliente, observado_em)
    noticias, status_noticias, _ = _coletar_noticias(cliente, observado_em)
    cliente.close()

    if len(pessoas) < 10:
        raise RuntimeError(
            f"Diff Guard: coleta produziu apenas {len(pessoas)} pessoas; publicação interrompida."
        )

    pessoas_json = [pessoa.model_dump(mode="json") for pessoa in pessoas]
    _json_dump(PUBLICO / "pessoas.json", pessoas_json)
    _json_dump(PUBLICO / "noticias.json", noticias)

    ao_vivo = {
        "emSessao": False,
        "atualizadoEm": observado_em.isoformat(),
        "eventos": [],
    }
    _json_dump(PUBLICO / "ao-vivo.json", ao_vivo)
    _json_dump(PUBLICO / "status.json", status_pessoas + status_noticias)

    print(
        f"Coleta concluída: {len(pessoas)} pessoas, {len(noticias)} notícias "
        f"em {observado_em.isoformat()}."
    )
    return 0


def main() -> int:
    parser = argparse.ArgumentParser(description="Coletor público controlado da Praça")
    parser.add_argument("--data-mode", choices=("publico", "fixtures"), default="publico")
    args = parser.parse_args()
    return executar(data_mode=args.data_mode)


if __name__ == "__main__":
    raise SystemExit(main())
