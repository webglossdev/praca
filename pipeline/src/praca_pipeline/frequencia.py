# SPDX-License-Identifier: AGPL-3.0-or-later
"""Política de frequência de coleta por fonte."""

from enum import StrEnum


class Frequencia(StrEnum):
    HORARIA = "horaria"
    DIARIA = "diaria"
    SEMANAL = "semanal"
    EVENTO = "evento"


INTERVALOS_SEGUNDOS = {
    Frequencia.HORARIA: 60 * 60,
    Frequencia.DIARIA: 24 * 60 * 60,
    Frequencia.SEMANAL: 7 * 24 * 60 * 60,
    Frequencia.EVENTO: None,
}


def intervalo_da_frequencia(frequencia: Frequencia) -> int | None:
    return INTERVALOS_SEGUNDOS[frequencia]
