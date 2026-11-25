# SPDX-License-Identifier: AGPL-3.0-or-later
"""Validação automática de contraste WCAG AA dos tokens Tinta & Papel."""

from __future__ import annotations

import re
from pathlib import Path


def _canal_linear(canal_255: int) -> float:
    c = canal_255 / 255.0
    return c / 12.92 if c <= 0.03928 else ((c + 0.055) / 1.055) ** 2.4


def _luminancia(hex_cor: str) -> float:
    limpa = hex_cor.lstrip("#")
    r, g, b = int(limpa[0:2], 16), int(limpa[2:4], 16), int(limpa[4:6], 16)
    return 0.2126 * _canal_linear(r) + 0.7152 * _canal_linear(g) + 0.0722 * _canal_linear(b)


def _contraste(cor_a: str, cor_b: str) -> float:
    la, lb = _luminancia(cor_a), _luminancia(cor_b)
    maior, menor = max(la, lb), min(la, lb)
    return (maior + 0.05) / (menor + 0.05)


def _extrair_tokens() -> dict[str, tuple[str, str]]:
    raiz = Path(__file__).resolve().parents[2]
    css = (raiz / "design" / "tokens.css").read_text(encoding="utf-8")
    padrao = re.compile(
        r"(--[a-z0-9-]+)\s*:\s*light-dark\((#[0-9A-Fa-f]{6}),\s*(#[0-9A-Fa-f]{6})\)"
    )
    return {m.group(1): (m.group(2), m.group(3)) for m in padrao.finditer(css)}


def test_tokens_texto_atingem_wcag_aa() -> None:
    tokens = _extrair_tokens()
    fundos = ("--bg", "--surface")
    textos = (
        "--text",
        "--text-soft",
        "--text-muted",
        "--leg-text",
        "--exe-text",
        "--jud-text",
        "--signal-text",
        "--atrib",
    )

    falhas: list[str] = []
    for fundo in fundos:
        bg_light, bg_dark = tokens[fundo]
        for texto in textos:
            fg_light, fg_dark = tokens[texto]
            r_light = _contraste(fg_light, bg_light)
            r_dark = _contraste(fg_dark, bg_dark)
            if r_light < 4.5:
                falhas.append(f"{texto} sobre {fundo} (light): {r_light:.2f} < 4.5")
            if r_dark < 4.5:
                falhas.append(f"{texto} sobre {fundo} (dark): {r_dark:.2f} < 4.5")

    assert not falhas, "Falhas de contraste WCAG AA:\n" + "\n".join(falhas)
