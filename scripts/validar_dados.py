# SPDX-License-Identifier: AGPL-3.0-or-later
"""Valida todos os JSONs públicos publicados pelo pipeline usando os contratos Pydantic."""

from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "pipeline" / "src"))

from praca_pipeline.modelos.dominio import (  # noqa: E402
    CorrecaoPublica,
    EventoAoVivo,
    Noticia,
    Pessoa,
    StatusColetor,
    Votacao,
)
from praca_pipeline.qualidade import auditar_registros  # noqa: E402

PUBLICO = ROOT / "data" / "publico"
FIXTURES = PUBLICO / "fixtures"


def _carregar_json(caminho: Path) -> object:
    if not caminho.exists():
        raise FileNotFoundError(f"Arquivo obrigatório ausente: {caminho}")
    return json.loads(caminho.read_text(encoding="utf-8"))


def validar_tudo() -> int:
    fontes = _carregar_json(PUBLICO / "fontes.json")
    if not isinstance(fontes, dict) or not fontes.get("fontes"):
        raise ValueError("fontes.json inválido ou vazio")

    pessoas_publicas = PUBLICO / "pessoas.json"
    pessoas_raw = _carregar_json(
        pessoas_publicas if pessoas_publicas.exists() else FIXTURES / "pessoas.json"
    )
    if not isinstance(pessoas_raw, list):
        raise ValueError("pessoas.json deve ser lista")
    pessoas = [Pessoa.model_validate(item) for item in pessoas_raw]
    relatorio = auditar_registros(
        [p.model_dump(mode="json") for p in pessoas],
        chave="pid",
    )
    if relatorio.duplicados or relatorio.nulos:
        raise ValueError(
            f"Problemas em pessoas.json: duplicados={relatorio.duplicados}, nulos={relatorio.nulos}"
        )

    noticias_publicas = PUBLICO / "noticias.json"
    noticias_raw = _carregar_json(
        noticias_publicas if noticias_publicas.exists() else FIXTURES / "noticias.json"
    )
    if not isinstance(noticias_raw, list):
        raise ValueError("noticias.json deve ser lista")
    noticias = [Noticia.model_validate(item) for item in noticias_raw]
    for noticia in noticias:
        if noticia.corpo_integral and (
            noticia.tipo_fonte != "oficial" or not noticia.licenca_texto_integral
        ):
            raise ValueError(
                f"Notícia {noticia.id} contém corpo_integral sem licença aberta oficial"
            )

    votacoes_publicas = PUBLICO / "votacoes.json"
    votacoes_raw = _carregar_json(
        votacoes_publicas if votacoes_publicas.exists() else FIXTURES / "votacoes.json"
    )
    if not isinstance(votacoes_raw, list):
        raise ValueError("votacoes.json deve ser lista")
    [Votacao.model_validate(item) for item in votacoes_raw]

    ao_vivo_publico = PUBLICO / "ao-vivo.json"
    ao_vivo_raw = _carregar_json(
        ao_vivo_publico if ao_vivo_publico.exists() else FIXTURES / "ao-vivo.json"
    )
    if not isinstance(ao_vivo_raw, dict) or not isinstance(ao_vivo_raw.get("eventos"), list):
        raise ValueError("ao-vivo.json inválido")
    [EventoAoVivo.model_validate(item) for item in ao_vivo_raw["eventos"]]

    correcoes_publicas = PUBLICO / "correcoes.json"
    correcoes_raw = _carregar_json(
        correcoes_publicas if correcoes_publicas.exists() else FIXTURES / "correcoes.json"
    )
    if not isinstance(correcoes_raw, list):
        raise ValueError("correcoes.json deve ser lista")
    [CorrecaoPublica.model_validate(item) for item in correcoes_raw]

    status_publico = PUBLICO / "status.json"
    status_raw = _carregar_json(
        status_publico if status_publico.exists() else FIXTURES / "status.json"
    )
    if not isinstance(status_raw, list):
        raise ValueError("status.json deve ser lista")
    [StatusColetor.model_validate(item) for item in status_raw]

    print(
        f"Validação concluída: {len(pessoas)} pessoas, {len(noticias)} notícias, "
        f"{len(votacoes_raw)} votações, {len(ao_vivo_raw['eventos'])} eventos ao vivo, "
        f"{len(correcoes_raw)} correções, {len(status_raw)} fontes monitoradas."
    )
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(validar_tudo())
    except Exception as exc:
        print(f"ERRO DE VALIDAÇÃO: {exc}", file=sys.stderr)
        raise SystemExit(1) from exc
