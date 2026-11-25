# SPDX-License-Identifier: AGPL-3.0-or-later
"""Conta os itens marcados no PLANO.md e mostra o progresso por fase.

Uso:
    python scripts/progresso.py              # só imprime
    python scripts/progresso.py --atualizar  # reescreve o quadro dentro do PLANO.md
"""
from __future__ import annotations

import re
import sys
from pathlib import Path

PLANO = Path(__file__).resolve().parent.parent / "PLANO.md"
INICIO, FIM = "<!-- PROGRESSO:INICIO -->", "<!-- PROGRESSO:FIM -->"
FASE = re.compile(r"^## FASE (\d+) · (.+)$")
ITEM = re.compile(r"^\s*- \[( |x|X)\] ")


def contar(texto: str) -> list[tuple[str, str, int, int]]:
    fases: list[tuple[str, str, int, int]] = []
    atual: list | None = None
    for linha in texto.splitlines():
        m = FASE.match(linha)
        if m:
            atual = [m.group(1), m.group(2).strip(), 0, 0]
            fases.append(atual)  # type: ignore[arg-type]
            continue
        if linha.startswith("## ") and not m:
            atual = None
        i = ITEM.match(linha)
        if i and atual is not None:
            atual[3] += 1
            if i.group(1).lower() == "x":
                atual[2] += 1
    return [tuple(f) for f in fases]  # type: ignore[misc]


def barra(feito: int, total: int, largura: int = 20) -> str:
    cheio = round(largura * feito / total) if total else 0
    return "█" * cheio + "░" * (largura - cheio)


def quadro(fases: list[tuple[str, str, int, int]]) -> str:
    feito = sum(f[2] for f in fases)
    total = sum(f[3] for f in fases)
    pct = 100 * feito / total if total else 0
    linhas = [
        "### Quadro de progresso",
        "",
        f"**Total: {feito}/{total} itens ({pct:.0f}%)** `{barra(feito, total, 30)}`",
        "",
        "| Fase | Itens | % | Progresso |",
        "|---|---|---|---|",
    ]
    for n, nome, f, t in fases:
        p = 100 * f / t if t else 0
        linhas.append(f"| {n} · {nome} | {f}/{t} | {p:.0f}% | `{barra(f, t, 12)}` |")
    return "\n".join(linhas)


def main() -> int:
    texto = PLANO.read_text(encoding="utf-8")
    fases = contar(texto)
    bloco = quadro(fases)
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")
    print(bloco)
    if "--atualizar" in sys.argv:
        if INICIO not in texto or FIM not in texto:
            print("\nMarcadores não encontrados no PLANO.md", file=sys.stderr)
            return 1
        antes, resto = texto.split(INICIO, 1)
        _, depois = resto.split(FIM, 1)
        PLANO.write_text(f"{antes}{INICIO}\n{bloco}\n{FIM}{depois}", encoding="utf-8", newline="\n")
        print("\nPLANO.md atualizado.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
