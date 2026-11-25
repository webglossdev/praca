# SPDX-License-Identifier: AGPL-3.0-or-later
"""Resolução conservadora de entidades entre fontes legislativas."""

from dataclasses import dataclass

from praca_pipeline.coletores.camara import DeputadoCamara
from praca_pipeline.coletores.senado import SenadorSenado


@dataclass(frozen=True, slots=True)
class Correspondencia:
    pid: str
    fonte_id: str
    fonte_codigo: int
    confianca: float


def resolver_legislativos(
    deputados: list[DeputadoCamara],
    senadores: list[SenadorSenado],
) -> list[Correspondencia]:
    """Gera IDs estáveis; não une homônimos entre casas sem chave compartilhada."""

    correspondencias = [
        Correspondencia(f"pid_{item.slug}", "camara", item.id_camara, 1.0)
        for item in deputados
    ]
    correspondencias.extend(
        Correspondencia(f"pid_{item.slug}", "senado", item.id_senado, 1.0)
        for item in senadores
    )
    return correspondencias
