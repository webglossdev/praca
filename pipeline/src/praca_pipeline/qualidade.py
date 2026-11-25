# SPDX-License-Identifier: AGPL-3.0-or-later
"""Guardas de qualidade e relatório de completude dos dados públicos."""

from dataclasses import dataclass
from typing import Any


@dataclass(frozen=True, slots=True)
class RelatorioQualidade:
    total: int
    validos: int
    nulos: int
    duplicados: int
    campos_vazios: dict[str, int]

    @property
    def taxa_valida(self) -> float:
        return self.validos / self.total if self.total else 1.0


def auditar_registros(registros: list[dict[str, Any]], *, chave: str) -> RelatorioQualidade:
    ids = [registro.get(chave) for registro in registros]
    ids_validos = [item for item in ids if item is not None]
    duplicados = len(ids_validos) - len(set(ids_validos))
    nulos = sum(not item.get(chave) for item in registros)
    campos: dict[str, int] = {}
    for registro in registros:
        for campo, valor in registro.items():
            if valor is None or valor == "":
                campos[campo] = campos.get(campo, 0) + 1
    return RelatorioQualidade(
        total=len(registros),
        validos=len(registros) - nulos,
        nulos=nulos,
        duplicados=duplicados,
        campos_vazios=campos,
    )


def validar_diff(
    atual: RelatorioQualidade,
    anterior: RelatorioQualidade,
    *,
    limite_nulos: int = 15,
) -> None:
    if atual.nulos > limite_nulos:
        raise ValueError(f"diff guard: {atual.nulos} registros sem chave")
    if anterior.total and atual.total < anterior.total * 0.8:
        raise ValueError("diff guard: queda superior a 20% no total de registros")
    if atual.duplicados:
        raise ValueError("diff guard: registros duplicados")
