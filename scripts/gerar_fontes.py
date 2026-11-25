# SPDX-License-Identifier: AGPL-3.0-or-later
"""Converte o registro editorial de fontes em JSON público determinístico."""

import json
from pathlib import Path

import yaml
from pydantic import BaseModel, ConfigDict, HttpUrl


class RegistroFonte(BaseModel):
    model_config = ConfigDict(extra="forbid")

    id: str
    nome: str
    url: HttpUrl
    licenca: str
    frequencia: str


ROOT = Path(__file__).resolve().parent.parent
ORIGEM = ROOT / "data" / "publico" / "fontes.yml"
DESTINO = ROOT / "data" / "publico" / "fontes.json"


def carregar() -> list[RegistroFonte]:
    dados = yaml.safe_load(ORIGEM.read_text(encoding="utf-8"))
    if not isinstance(dados, list):
        raise ValueError("fontes.yml deve conter uma lista")
    fontes = [RegistroFonte.model_validate(item) for item in dados]
    ids = [fonte.id for fonte in fontes]
    if len(ids) != len(set(ids)):
        raise ValueError("IDs de fontes devem ser únicos")
    return sorted(fontes, key=lambda fonte: fonte.id)


def main() -> None:
    DESTINO.write_text(
        json.dumps(
            {"versao": 1, "fontes": [fonte.model_dump(mode="json") for fonte in carregar()]},
            ensure_ascii=False,
            indent=2,
        )
        + "\n",
        encoding="utf-8",
    )


if __name__ == "__main__":
    main()
