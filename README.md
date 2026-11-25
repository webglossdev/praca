# Praça

[![CI](https://github.com/webglossdev/praca/actions/workflows/ci.yml/badge.svg)](https://github.com/webglossdev/praca/actions/workflows/ci.yml)
[![Deploy](https://github.com/webglossdev/praca/actions/workflows/pages.yml/badge.svg)](https://github.com/webglossdev/praca/actions/workflows/pages.yml)
[![License: AGPL-3.0](https://img.shields.io/badge/License-AGPL--3.0-blue.svg)](LICENSE)

Praça é um observatório aberto de política e governo brasileiro. O projeto reúne perfis públicos, mandatos, votações, despesas, notícias com atribuição e educação cívica em uma interface estática rápida e citável.

Live demo: https://webglossdev.github.io/praca/

## Principios

- Todo dado publicado traz fonte, URL, data de coleta e licença.
- Nenhuma ideologia é atribuída por inferência. Só usamos autodeclaração datada, histórico de votos ou metodologia acadêmica publicada.
- Notícias de imprensa exibem título, veículo, data, trecho curto e link. Texto integral só aparece com licença aberta confirmada.
- Seções sensíveis continuam desligadas até revisão jurídica humana.
- Dados públicos são compilados sem cookies de publicidade ou rastreadores.

## O que ja esta implementado

- 594 perfis reais obtidos da API da Câmara (513 deputados) e do Senado (81 senadores).
- Snapshot público em `data/publico/`, separado das fixtures usadas em testes offline.
- Coleta controlada com cache, limite de ritmo, retry, Circuit Breaker e fallback stale.
- Notícias normalizadas de feeds oficiais e de imprensa sem republicação integral indevida.
- Home, perfis, filtros, comparação, votações, estados, partidos, Poderes, Ao Vivo, educação cívica e Guia do Cidadão.
- Página Pagefind com índice estático gerado no build.
- Tema claro/escuro, navegação por teclado, estados `aria-live`, CSS responsivo e direção visual “Tinta & Papel”.
- Testes Vitest, Playwright desktop/mobile e axe.

## Estado dos dados

Os dados em `data/publico/pessoas.json` e `data/publico/noticias.json` são snapshots. Atualizações públicas são feitas pelo pipeline e podem ser degradadas sem remover o último snapshot válido.

Sem credencial configurada:

- `CGU_API_KEY`: CGU marcado como planejado.
- `DATAJUD_API_KEY`: STF/DataJud marcado como planejado.
- TSE/Receita em lote: execução separada quando os CSVs estiverem disponíveis.

Não altere `SECOES_SENSIVEIS_ATIVAS` sem concluir `JURIDICO.md` e obter revisão jurídica humana.

## Executar localmente

Requisitos: Node.js 22+, Python 3.12+, `uv`.

```bash
uv sync
npm ci
npm run dev
```

Build com dados públicos:

```bash
PRACA_DATA_MODE=publico npm run build
```

No Windows PowerShell:

```powershell
$env:PRACA_DATA_MODE="publico"
npm run build
```

Build em modo fixtures para testes offline:

```bash
PRACA_DATA_MODE=fixtures npm run build
```

## Pipeline de dados

Executar coleta pública controlada:

```bash
uv run python scripts/coletar_dados_reais.py --data-mode publico
```

Gerar e validar artefatos:

```bash
uv run python scripts/gerar_fontes.py
uv run python scripts/gerar_schema.py
uv run python scripts/validar_dados.py
```

Ver documentação completa da arquitetura em `AUTONOMIA.md`.

## Testes

```bash
uv run ruff check pipeline scripts
uv run pytest -v
npm run check
npm run test:web
npx playwright install chromium
npm run test:e2e
npm audit --omit=dev
```

## Estrutura

```text
pipeline/          contratos e coletores Python
scripts/           coleta, validação e geração
data/publico/      snapshots públicos e fixtures
schema/            JSON Schema gerado
web/src/           aplicação Astro
web/public/        arquivos estáticos
workers/ao-vivo/   worker de transmissão ao vivo
.github/workflows/ CI e GitHub Pages
```

## Licença e responsabilidade

- Código: [AGPL-3.0-or-later](LICENSE).
- Direitos de terceiros: consulte [NOTICE](NOTICE) e [JURIDICO.md](JURIDICO.md).
- Correções e contestação: use o canal público do projeto.
- A licença final da base compilada ainda deve ser revista contra os termos de todas as fontes.

## Contribuir

Leia [CONTRIBUTING.md](CONTRIBUTING.md) e [AGENTS.md](AGENTS.md). Contribuições devem manter proveniência, neutralidade, JSON UTF-8 indentado em dois espaços e datas ISO 8601 no pipeline.
