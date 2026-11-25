# PLANO: desenvolvimento completo do site

> Plano mestre do projeto (título de trabalho: **Praça**, de "Praça dos Três Poderes").
> Marque `[x]` ao concluir cada passo. O quadro de progresso abaixo é atualizado por `python scripts/progresso.py --atualizar`.
> Relação com os outros arquivos: `recursos-apis.md` (fontes e cuidados), `AUTONOMIA.md` (arquitetura zero-touch, resiliência e circuit breakers), `PROGRESSO.md` (diário de sessões e decisões), `PAGINAS.md` (inventário e layout das páginas), `design/` (tokens, guia de estilo, mockups).

<!-- PROGRESSO:INICIO -->
### Quadro de progresso

**Total: 114/159 itens (72%)** `██████████████████████░░░░░░░░`

| Fase | Itens | % | Progresso |
|---|---|---|---|
| 0 · Fundação e decisões | 11/14 | 79% | `█████████░░░` |
| 1 · Modelo de dados e convenções | 10/10 | 100% | `████████████` |
| 2 · Design, UX e conteúdo | 12/18 | 67% | `████████░░░░` |
| 3 · Pipeline de dados (Python) | 26/32 | 81% | `██████████░░` |
| 4 · Front-end MVP (Astro + TypeScript) | 17/17 | 100% | `████████████` |
| 5 · Notícias | 7/10 | 70% | `████████░░░░` |
| 6 · Ao vivo e Praça dos Três Poderes | 5/6 | 83% | `██████████░░` |
| 7 · Seções sensíveis (processos, suspeitas, ligações) | 4/8 | 50% | `██████░░░░░░` |
| 8 · Posicionamento, votos e índices | 5/8 | 62% | `████████░░░░` |
| 9 · Qualidade | 3/8 | 38% | `████░░░░░░░░` |
| 10 · Legal, privacidade e ética | 4/9 | 44% | `█████░░░░░░░` |
| 11 · Deploy e operação | 4/8 | 50% | `██████░░░░░░` |
| 12 · Lançamento e pós-lançamento | 0/5 | 0% | `░░░░░░░░░░░░` |
| 13 · Educação cívica e Guia do Cidadão | 6/6 | 100% | `████████████` |
<!-- PROGRESSO:FIM -->

---

## 1. Produto em uma página

**O que é:** plataforma aberta de política e governo brasileiro que combina perfis de agentes públicos (parlamentares, governadores, STF, Executivo federal), módulo de notícias e painel "ao vivo" com um centro completo e interativo de educação cívica (*Como funciona o Brasil*, *Guia do Cidadão* e *Glossário*).

**Para quem:** cidadão comum que quer entender de forma intuitiva *quem faz o quê no país, como nascem as leis, para onde vai o orçamento e como agir/cobrar pelos canais oficiais*, além de saber *quem é quem, o que votou e o que a imprensa apurou*; jornalistas e pesquisadores que querem dados abertos e citáveis.

**Promessas ao leitor (não negociáveis):**
1. Todo dado traz **fonte, data de coleta e link**.
2. O site **não opina**: ideologia = autodeclaração datada ou histórico de votos.
3. Suspeitas e ligações só aparecem **como atribuição à imprensa**, com desfecho atualizado.
4. Sem rastreadores. Sem cookies de publicidade. Código e metodologia abertos (AGPL-3.0).

**Fora do escopo da v1:** servidores de órgãos (PGR, TCU etc.), assembleias estaduais e câmaras municipais, contas de usuário, comentários, aplicativo nativo.

## 2. Marcos e prazos (propostos)

| Marco | Entrega | Referência de data |
|---|---|---|
| M0 | Fundação: repo, stack aprovada, design v0 | até 18/10/2026 |
| M1 | Pipeline Câmara + Senado + TSE gerando JSON validado | até 08/11/2026 |
| M2 | Front MVP: home, lista, perfil, busca (parlamentares atuais) | até 29/11/2026 |
| M3 | Notícias + ao vivo | até 13/12/2026 |
| M4 | Beta fechado, revisão jurídica, qualidade | até 20/12/2026 |
| M5 | **Lançamento público (seções sensíveis ainda desligadas)** | antes da posse de 01/01/2027 |
| M6 | Virada de mandatos: governadores (06/01/2027), Congresso (01/02/2027) | jan–fev/2027 |
| M7 | Seções sensíveis (processos, suspeitas, ligações) após revisão jurídica | quando liberado |

Datas eleitorais: 2º turno em **25/10/2026**. O modelo de dados distingue "mandato atual" de "eleito, ainda não iniciado".

## 3. Decisões técnicas propostas (confirmar na tarefa 0.7)

| ID | Decisão | Por quê | Alternativa |
|---|---|---|---|
| D-01 | Site **estático** (SSG) gerado a partir de JSON | 640+ perfis, leitura pesada, custo ~zero, rápido, seguro | SSR com banco (mais caro e frágil) |
| D-02 | Pipeline de dados em **Python 3.12+** | Ecossistema de dados; `mcp-brasil` já é Python (referência) | Node/TypeScript no pipeline |
| D-03 | Front-end em **Astro + TypeScript** com **CSS puro** (tokens) | Zero JS por padrão, páginas por rota geradas dos JSON, ilhas só onde precisa | Next.js (mais pesado), Eleventy |
| D-04 | Busca no cliente com **Pagefind** | Índice estático, sem servidor, funciona offline | MiniSearch/Fuse |
| D-05 | Dados volumosos (votos, TSE) em **Parquet/DuckDB** no pipeline; só JSON enxuto vai ao site | CSV do TSE passa de 1,6 GB | SQLite |
| D-06 | **Cloudflare Pages** + **Worker** pequeno só para "ao vivo" | Banda ilimitada, cache de borda, CORS controlado | GitHub Pages (sem Worker) |
| D-07 | **GitHub Actions** agenda coleta → valida → build → deploy | Tudo versionado e auditável | Servidor próprio |
| D-08 | Licença dos dados compilados: **ODbL 1.0** (ou CC BY-SA 4.0) | Alinha com "livre, com crédito, e continua livre" | CC BY 4.0, CC0 |
| D-09 | Fontes **self-hosted**, sem Google Fonts/CDN em produção | Privacidade (LGPD) e velocidade | Google Fonts |
| D-10 | Vídeo ao vivo via `youtube-nocookie`, **só após clique** | Nenhum rastreio sem consentimento | Embed direto |
| D-11 | Analytics: nenhum, ou **Umami/Plausible** self-hosted, sem cookies | Respeito ao leitor | GA4 |
| D-12 | Gerenciadores: **uv** (Python), **pnpm** (Node) | Reprodutível e rápido | pip/npm |

## 4. Stack e linguagens

| Camada | Tecnologia |
|---|---|
| Pipeline | Python 3.12+, `httpx`, `polars` ou `pandas`, `duckdb`, `pydantic` v2, `selectolax`/`lxml`, `feedparser`, `pytest`, `ruff`, `mypy` |
| Contratos | JSON Schema (gerado dos modelos Pydantic), validado no CI e no build |
| Front-end | Astro 5, TypeScript estrito, CSS puro + `design/tokens.css`, Pagefind, SVG próprio (gráficos e Praça), Biome (lint/format) |
| Ao vivo | Cloudflare Worker (TypeScript), cache de 30–60 s |
| Testes | `pytest`, Vitest, Playwright (E2E), axe-core (acessibilidade), Lighthouse CI |
| Automação | GitHub Actions, Dependabot, secret scanning |
| Docs | Markdown neste repositório |

### Estrutura de pastas alvo

```
/
├─ AGENTS.md              instruções ao agente da IDE
├─ PLANO.md  PROGRESSO.md  recursos-apis.md
├─ LICENSE  NOTICE  README.md
├─ design/                tokens.css, guia-estilo.html, mockups/
├─ schema/                JSON Schemas (gerados)
├─ pipeline/              Python (coletores, resolução de entidades, gerador)
│  ├─ src/praca_pipeline/{fontes,modelos,resolucao,gerar}/
│  └─ tests/
├─ data/
│  ├─ bruto/              (ignorado pelo git) CSVs/respostas originais
│  └─ publico/            JSON final: pessoas/, partidos/, noticias/, indices/
├─ web/                   Astro (src/pages, src/components, src/styles)
├─ workers/ao-vivo/       Cloudflare Worker
├─ scripts/               utilitários (progresso.py etc.)
└─ .github/workflows/
```

## 5. Direção de design (v0)

> Arquivos: [`design/tokens.css`](design/tokens.css) · [`design/guia-estilo.html`](design/guia-estilo.html) (abrir no navegador) · [`design/mockups/home-v0.jpg`](design/mockups/home-v0.jpg).
> **Inventário completo de páginas, conteúdo e layout: [`PAGINAS.md`](PAGINAS.md)** (substitui o mapa de rotas resumido abaixo).
> O mockup é referência de clima e composição. Os textos dele são ilustrativos.

**Conceito: "Tinta & Papel".** Sóbria como um jornal, precisa como um cartório. Um site de política precisa parecer **confiável e neutro**, não gritante nem partidário.

- **Cor.** Papel quente (`#F5F1E8`) e tinta azul-noite (`#14161F`). Três cores de identidade para os Poderes: **verdigris** (Legislativo), **âmbar** (Executivo), **índigo** (Judiciário). **Evitamos vermelho × azul** de propósito: leria como posição partidária. Um único tom quente-saturado, o **vermelhão de sinal**, reservado a "ao vivo" e alertas. Tom **fumê** exclusivo para atribuições de imprensa, para nunca parecerem dado oficial.
- **Assinatura visual.** Barra fina de 3 segmentos (verdigris/âmbar/índigo) no topo do site; **régua de fonte** em todo dado (mono, pequena: `FONTE · Câmara · coletado em … ↗`).
- **Tipografia.** *Fraunces* (serifa editorial variável) em títulos; *Instrument Sans* no texto e na interface; *JetBrains Mono* em dados, datas e fontes. Escala modular 1,25, fluida; medida de leitura 66ch.
- **Layout.** Grade de 12 colunas, contêiner de 76rem, mobile-first (testar a 360px). Filete (1px) em vez de sombra; raios pequenos; muito branco. Movimento discreto: elevação de cartões, pulso do "ao vivo", respeito a `prefers-reduced-motion`.
- **Tema.** Claro e escuro desde o início (`light-dark()`), com contraste AA validado par a par.
- **Acessibilidade.** Cor nunca é o único sinal (sempre rótulo + ícone); foco visível; HTML semântico; navegação por teclado; atalho `/` para busca.
- **Neutralidade visual.** Partidos aparecem como sigla em chip neutro, sem cor partidária. Gráficos usam a paleta dos Poderes ou tons de tinta.

### Mapa do site (rotas)

| Rota | Conteúdo |
|---|---|
| `/` | Hero, Praça dos Três Poderes em SVG, contadores, últimas notícias, "ao vivo agora", busca |
| `/pessoas` | Lista com filtros (poder, cargo, UF, partido, situação do mandato) |
| `/pessoas/[slug]` | Perfil (ver abaixo) |
| `/aprender` | Guia interativo "Como funciona o Brasil" (Pacto Federativo, Poderes, Leis, Orçamento, Eleições) |
| `/guia-do-cidadao` | Ferramentas oficiais de participação, cobrança, LAI e fiscalização |
| `/glossario` | Glossário cívico, orçamentário e jurídico (A–Z e por tema) |
| `/partidos/[sigla]` | Bancada, histórico de fusões, orientação de voto, finanças (FEFC) |
| `/estados/[uf]` | Bancada, governador, eleitos |
| `/poderes/[executivo\|legislativo\|judiciario]` | Visão por Poder |
| `/noticias` | Agregador com filtros por Poder, tema e pessoa |
| `/ao-vivo` | Transmissões e pauta do dia |
| `/busca` | Resultado de busca (Pagefind) |
| `/metodologia` | Fórmulas, critérios, limitações |
| `/fontes` | Registro público de fontes, licenças e frequência |
| `/dados` | Downloads JSON/CSV + licença |
| `/corrigir` | Canal de contestação e log público de correções |
| `/sobre`, `/privacidade`, `/termos` | Institucional e legal |

### Perfil de pessoa (ordem das seções)

1. **Cabeçalho:** foto (se licença permitir), nome, cargo, partido, UF, situação do mandato (atual / eleito, não iniciado / encerrado).
2. **Resumo em 5 números** (presença, projetos, votos alinhados, gasto de cota, patrimônio) com régua de fonte.
3. **Biografia curta** (texto próprio, com link às fontes).
4. **Carreira:** linha do tempo de mandatos e filiações.
5. **Atuação:** proposições, relatorias, votações nominais, presença, emendas, cota parlamentar.
6. **Dinheiro:** campanha (doadores, empresas e sócios), patrimônio declarado, sanções a empresas ligadas.
7. **Posicionamento:** autodeclaração datada + resumo de votos (metodologia aberta).
8. **Plano de governo** (quando houver) e **pesquisas** (em ano eleitoral).
9. **Na imprensa:** notícias recentes (só título, veículo, data, link).
10. **Processos, suspeitas e ligações:** *desligado até revisão jurídica*; sempre com aviso de origem e desfecho.
11. **Corrigir este perfil** e histórico de alterações.

---

## 6. Checklist por fase

Convenção: `[x]` feito · `[ ]` pendente. IDs estáveis (não renumerar; novos itens ganham sufixo, ex.: 3.5a).
**Definição de pronto de um item:** funciona, tem teste ou verificação descrita, está documentado e foi registrado em `PROGRESSO.md`.

## FASE 0 · Fundação e decisões

- [x] **0.1** Visão, escopo inicial e princípios (`recursos-apis.md` §1–2)
- [x] **0.2** Licença do código: AGPL-3.0 (decidida)
- [x] **0.3** Levantamento inicial de fontes e projetos de referência
- [x] **0.4** Registro de progresso (`PROGRESSO.md`)
- [x] **0.5** Direção criativa, tokens de design e guia de estilo v0 (`design/`)
- [x] **0.6** Este plano de desenvolvimento
- [ ] **0.7** Aprovar stack (D-01 a D-12) e atualizar `PROGRESSO.md` §2
- [ ] **0.8** Escolher nome definitivo; checar domínio (registro.br) e marca (INPI)
- [x] **0.9** `git init`, `.gitignore`, `.editorconfig`, `README.md`, texto integral da AGPL-3.0 em `LICENSE`
- [x] **0.10** Direitos autorais: cabeçalho `SPDX-License-Identifier: AGPL-3.0-or-later` nos arquivos, `NOTICE` com créditos a terceiros, política de contribuição (DCO ou CLA)
- [x] **0.11** `AGENTS.md`: regras para o agente da IDE (atualizar `PROGRESSO.md` ao fim da sessão, convenções, regra "todo dado tem fonte")
- [x] **0.12** Versões fixadas para Node LTS (`.nvmrc`/`package.json`), npm, Python 3.12+ (`.python-version`) e ambiente uv
- [ ] **0.13** Repositório remoto, proteção da branch principal, templates de issue/PR (inclui "correção de dado")
- [x] **0.14** CI mínima: lint + testes em cada PR

## FASE 1 · Modelo de dados e convenções

- [x] **1.1** Chave de cruzamento e regras de homônimos; ID interno estável por pessoa (`pid`)
- [x] **1.2** Regra de slug (`nome-politico-uf`, desambiguação por cargo/ano)
- [x] **1.3** Modelos Pydantic + JSON Schema: Pessoa, Mandato, Partido, Filiação, Proposição, Votação, Voto, Despesa, Doação, Bem, Emenda, Notícia, Atribuição, Fonte
- [x] **1.4** Envelope de dado com proveniência: `{valor, fonte_id, url, coletado_em, licença}`
- [x] **1.5** Modelo de mandatos: atual / eleito-não-iniciado / encerrado; suplência; licença; troca de partido
- [x] **1.6** Convenções de arquivos e pastas (preencher `PROGRESSO.md` §7)
- [x] **1.7** Dicionário de nomes e apelidos (nome vira link para o perfil; tratar ambiguidade tipo "Davi")
- [x] **1.8** Tabela de partidos: sigla, nome, número, federação, fusões e renomeações
- [x] **1.9** Validação dos JSON contra o schema (CI e build)
- [x] **1.10** Fixtures: 5 pessoas fictícias completas para o front trabalhar sem o pipeline

## FASE 2 · Design, UX e conteúdo

- [x] **2.1** Direção criativa e paleta
- [x] **2.2** Tokens CSS (`design/tokens.css`)
- [x] **2.3** Guia de estilo vivo (`design/guia-estilo.html`)
- [x] **2.4** Mockup da home (`design/mockups/home-v0.jpg`)
- [x] **2.4a** Inventário de páginas com conteúdo e layout em planta (`PAGINAS.md`)
- [ ] **2.4b** Validar o inventário com o autor (o que entra na v1)
- [x] **2.4c** Mockups de alta fidelidade de P-01, P-02, P-03, P-05 e P-07
- [x] **2.4d** Protótipo navegável em HTML com dados fictícios
- [ ] **2.5** Revisar a direção com você (cores, nome, tom) e congelar v1
- [ ] **2.6** Wireframes: perfil (desktop e mobile), lista, partido, estado, notícias, ao vivo, busca, metodologia
- [x] **2.7** Fontes self-hosted via fontsource (Fraunces, Instrument Sans, JetBrains Mono), subset latino
- [ ] **2.8** Inventário e especificação de componentes (card de poder, perfil, régua de fonte, atribuição, chip, linha do tempo, tabela de votos, gráfico, selo de status)
- [ ] **2.9** Ícones em SVG (conjunto de licença permissiva, ex.: Lucide/ISC)
- [x] **2.10** Ilustração SVG da Praça dos Três Poderes (3 marcadores, estados "ao vivo")
- [x] **2.11** Contraste WCAG AA verificado par a par, claro e escuro
- [x] **2.12** Breakpoints e testes a 360px, 768px, 1280px
- [x] **2.13** Redação: voz do site, glossário, microcopy dos avisos ("Segundo a imprensa…", "Sem dado")
- [ ] **2.14** Teste de usabilidade rápido com 5 pessoas no protótipo

## FASE 3 · Pipeline de dados (Python)

**Infra**
- [x] **3.1** Esqueleto: `pyproject.toml`, uv, ruff, pytest
- [x] **3.2** Cliente HTTP comum: cache em disco, retry com backoff, limite de ritmo, User-Agent identificado
- [x] **3.2a** Circuit breaker e fallback resiliente (Stale-While-Offline): preserva último snapshot válido se a fonte falhar
- [x] **3.3** Registro de fontes em YAML (id, URL, termos, licença, frequência) → publica `fontes.json`
- [x] **3.4** Testes de contratos e fixtures gravadas (sem rede no CI)

**Câmara**
- [x] **3.5** Deputados, mandatos e partidos
- [x] **3.6** Proposições (autoria e relatoria)
- [x] **3.7** Votações nominais e votos (janelas de ≤ 3 meses; respeitar limite de requisições)
- [x] **3.8** Cota parlamentar
- [x] **3.9** Presença e eventos (confirmar endpoint)

**Senado**
- [x] **3.10** Senadores e mandatos
- [x] **3.11** Votações (endpoint novo) e proposições
- [x] **3.12** CEAPS (Latin-1, linha de metadados antes do cabeçalho)

**TSE**
- [ ] **3.13** Candidaturas 2014–2026 (CSV → Parquet/DuckDB)
- [x] **3.14** Bens declarados
- [ ] **3.15** Votação (votos que elegeram)
- [x] **3.16** Prestação de contas (doações) e FEFC
- [x] **3.17** Filiação partidária
- [x] **3.18** Resultados 2026 (eleitos, 2º turno); distinguir eleito × diplomado × empossado
- [ ] **3.19** Planos de governo (DivulgaCandContas ou CSV)

**Demais fontes**
- [x] **3.20** Receita Federal: CNPJ/QSA dos doadores (CSV + consulta sob demanda com cache)
- [ ] **3.21** Portal da Transparência: emendas (obter chave)
- [x] **3.22** CGU: CEIS, CNEP, CEPIM
- [ ] **3.23** Executivo federal: pesquisar fonte estruturada (SIORG/gov.br) e coletar
- [x] **3.24** STF: composição (fonte e coleta)
- [x] **3.25** Governadores: eleitos (TSE) e atuais
- [ ] **3.26** Atos oficiais (DOU; Querido Diário opcional)

**Integração**
- [x] **3.27** Resolução de entidades (IDs Câmara × Senado × TSE) com testes de homônimos
- [x] **3.28** Gerador de perfis: um JSON por pessoa (+ arquivos de votos separados, carregados sob demanda) e índices (lista, busca, partidos, estados)
- [x] **3.28a** Anomaly & Diff Guard: trava o build e gera alerta se houver oscilação anômala (>15 perfis nulos ou corrompidos)
- [x] **3.29** Relatório de qualidade: campos vazios, divergências entre fontes, fontes quebradas
- [x] **3.30** Frequência por fonte (diária, semanal, por evento eleitoral)

## FASE 4 · Front-end MVP (Astro + TypeScript)

- [x] **4.1** Esqueleto: Astro, TS estrito, Biome, Vitest, importação dos tokens
- [x] **4.2** Layout base: barra tripartite, cabeçalho, rodapé, tema claro/escuro persistente
- [x] **4.3** Home (hero, contadores, notícias, bloco "ao vivo")
- [x] **4.4** Lista de pessoas com filtros (sem recarregar a página)
- [x] **4.5** Busca (Pagefind) com atalho `/`
- [x] **4.6** Perfil: cabeçalho, identidade e resumo em números
- [x] **4.7** Perfil: carreira (linha do tempo)
- [x] **4.8** Perfil: atuação (proposições, votações, presença, emendas, cota)
- [x] **4.9** Perfil: dinheiro (campanha, doadores, patrimônio, sanções)
- [x] **4.10** Perfil: biografia, plano de governo, pesquisas
- [x] **4.11** Componente "régua de fonte" aplicado a todo dado
- [x] **4.12** Páginas de partido, estado e Poderes
- [x] **4.13** Institucionais: metodologia, fontes, dados, sobre, privacidade, termos
- [x] **4.14** SEO: título/descrição por página, Open Graph com imagem gerada, sitemap, JSON-LD `Person`, canonical
- [x] **4.15** 404 e estados vazios ("sem dado disponível", nunca campo em branco)
- [x] **4.16** Downloads de dados abertos (JSON/CSV)
- [x] **4.17** Compartilhamento sem rastreadores

## FASE 5 · Notícias

- [x] **5.1** Lista de veículos aceitos, critérios de inclusão e feeds RSS
- [ ] **5.2** Coletor das fontes oficiais (Agência Câmara, Agência Senado, Agência Brasil, STF)
- [ ] **5.3** Coletor de imprensa (RSS; avaliar Google News/GDELT e termos de uso)
- [x] **5.4** Normalização: título, veículo, data, link, trecho curto; remoção de duplicatas
- [x] **5.4a** Verificar licença de cada fonte para leitura completa no site (Agência Brasil, Agência Câmara, Agência Senado, STF); o resto fica só com trecho e link
- [x] **5.5** Vinculação contextual nome → perfil (Confidence Score ≥ 0.95 com exigência de tokens de contexto no parágrafo para homônimos)
- [x] **5.6** Página `/noticias` com filtros
- [x] **5.7** Bloco de notícias no perfil
- [x] **5.8** Política de atualização e remoção (retratação, link quebrado)
- [ ] **5.9** Rotina de atualização a cada ~30 min

## FASE 6 · Ao vivo e Praça dos Três Poderes

- [x] **6.1** Pauta do dia: eventos da Câmara e do Senado (confirmar endpoints)
- [ ] **6.2** Detecção de transmissão ao vivo (TV Câmara, TV Senado, TV Justiça/STF)
- [x] **6.3** Cloudflare Worker `/api/ao-vivo` (cache curto, CORS restrito)
- [x] **6.4** Praça em SVG com marcadores por Poder e estado "ao vivo"
- [x] **6.5** Página `/ao-vivo` com player `youtube-nocookie` carregado após clique
- [x] **6.6** Fallback quando a fonte falha (mensagem honesta, sem dado inventado)

## FASE 7 · Seções sensíveis (processos, suspeitas, ligações)

> Bloqueadas por feature flag até a conclusão de **7.6**.

- [x] **7.1** Critérios editoriais: o que entra, o que nunca entra (ex.: vida privada, acusações sem fonte)
- [x] **7.2** Modelo `Atribuição`: título original, veículo, data, link, desfecho, histórico de status
- [ ] **7.3** Fluxo de curadoria: um arquivo YAML por caso, revisão por duas pessoas
- [ ] **7.4** Fontes oficiais pontuais (STF, STJ, TCU, CGU, TSE)
- [x] **7.5** Interface: rótulo "Segundo a imprensa", selo de status, desfecho em destaque
- [ ] **7.6** **Revisão jurídica** (bloqueante)
- [x] **7.7** Processo de contestação com prazo de resposta público
- [ ] **7.8** Piloto com poucos casos bem documentados

## FASE 8 · Posicionamento, votos e índices

- [x] **8.1** Método de ideologia do político (autodeclaração + votos)
- [ ] **8.2** Ideologia do partido (classificação acadêmica citável)
- [ ] **8.3** Aprovação/desaprovação: fonte e termos de uso
- [x] **8.4** Índices: alinhamento ao partido e ao governo, orientação de bancada
- [x] **8.5** "Tópicos relevantes" com critério objetivo (ex.: votação apertada, lista fixa de temas)
- [x] **8.6** Página de metodologia com fórmulas e link para o código
- [ ] **8.7** Validação por pesquisador externo
- [x] **8.8** Pesquisas (PesqEle) como seção sazonal

## FASE 9 · Qualidade

- [x] **9.1** Testes unitários e de integração do pipeline
- [x] **9.2** Testes de componentes (Vitest)
- [x] **9.3** E2E (Playwright): busca, filtro, perfil, tema
- [ ] **9.4** Acessibilidade: axe no CI + teste manual com leitor de tela
- [ ] **9.5** Desempenho: LCP < 2 s em 4G, JS da home ≤ 60 kB, Lighthouse CI
- [ ] **9.6** Verificador de links quebrados
- [ ] **9.7** Build completo em < 5 min com ~700 perfis
- [ ] **9.8** Segurança: CSP, `npm/pip audit`, Dependabot, varredura de segredos

## FASE 10 · Legal, privacidade e ética

- [ ] **10.1** Levantar termos de uso de cada fonte (coleta automatizada, imagens, republicação)
- [ ] **10.2** Decidir licença da base compilada (D-08)
- [ ] **10.3** Licença de fotos e biografias (Câmara, Senado, Wikimedia, DHBB/FGV)
- [ ] **10.4** LGPD: base legal, avaliação de impacto, política de privacidade
- [x] **10.5** Política editorial pública (critérios, correções, conflito de interesse)
- [ ] **10.6** Legislação eleitoral: regras de neutralidade em período eleitoral
- [x] **10.7** Página `/corrigir` e log público de correções
- [x] **10.8** Aviso de independência (sem vínculo com governo, partido ou campanha)
- [x] **10.9** Atribuição de terceiros em `NOTICE` e rodapé

## FASE 11 · Deploy e operação

- [ ] **11.1** Hospedagem (Cloudflare Pages) e domínio, HTTPS, cabeçalhos de segurança
- [x] **11.2** Cron Matrix no GitHub Actions: rotinas independentes (notícias 20 min, legislativo 2x/dia, censo semanal)
- [x] **11.2a** Worker autônomo na borda (Cloudflare) para detecção de "Ao Vivo" a cada 60s com cache inteligente
- [ ] **11.3** Onde guardar os dados processados (branch `data`, release ou R2)
- [ ] **11.4** Preview por PR
- [x] **11.5** Alerta automático de fonte quebrada via GitHub Issues geradas pelo bot após 3 falhas de circuit breaker
- [ ] **11.6** Backups
- [x] **11.7** Runbook em `PROGRESSO.md` §4

## FASE 12 · Lançamento e pós-lançamento

- [ ] **12.1** Beta fechado com jornalistas e pesquisadores
- [ ] **12.2** Revisão final de conteúdo e jurídica
- [ ] **12.3** Lançamento público (seções sensíveis desligadas)
- [ ] **12.4** Rotina de virada de mandatos (06/01/2027 e 01/02/2027)
- [ ] **12.5** Roadmap v2 (órgãos, assembleias, municípios, API pública)

## FASE 13 · Educação cívica e Guia do Cidadão

- [x] **13.1** Arquitetura pedagógica e base estruturada (`web/src/data/educacao.ts`) com proveniência oficial (CF/88, Câmara, Senado, TSE, Tesouro, CGU, CNJ)
- [x] **13.2** Bússola Federativa interativa ("Quem faz o quê": Município × Estado × União + resolvedor de problemas cotidianos) em `/aprender`
- [x] **13.3** Explicadores interativos: Ciclo de uma Lei (PL/PEC/MP), Três Poderes, Orçamento Público (PPA/LDO/LOA, Emendas, FPM) e Eleições (Simulador de Quociente Eleitoral e Urna/BU)
- [x] **13.4** Página `/guia-do-cidadao`: passo a passo prático de participação e fiscalização (e-Cidadania, Fala.BR/LAI, Ouvidorias, Ação Popular, TVs públicas)
- [x] **13.5** Página `/glossario`: dicionário A–Z filtrável de termos políticos, orçamentários e status judiciais (Réu, 1ª/2ª instância, Trânsito em julgado, Prescrição, Liminar)
- [x] **13.6** Pontes contextuais de aprendizado integradas aos perfis (`/pessoas/[slug]`), páginas de Poderes (`/poderes/[poder]`) e Home (`/`)

---

## 7. Riscos

| Risco | Impacto | Mitigação |
|---|---|---|
| Processo judicial por conteúdo sensível | Alto | Seções sensíveis atrás de flag; revisão jurídica; só atribuição + desfecho; canal de contestação |
| API oficial muda ou cai | Médio | Cache, versão dos dados, alerta de fonte quebrada, dados com data de coleta |
| Homônimos ligando dados à pessoa errada | Alto | Chave composta, testes de homônimos, revisão manual de casos duvidosos, link "corrigir" |
| Acusação de viés político | Alto | Metodologia aberta, sem cor partidária, sem opinião, política editorial pública |
| Limites de taxa/termos de uso | Médio | Coleta com ritmo controlado, cache; dados em lote (CSV) preferidos |
| Escopo grande (640+ perfis) | Médio | Pipeline automatizado; só biografia é manual; MVP só com parlamentares atuais |
| Direitos de imagem e texto | Médio | Só fontes com licença clara; biografia própria com link |
| Esgotar tempo antes de 01/01/2027 | Médio | Cortar escopo do M5: lançar sem ao vivo se preciso |

## 8. Como trabalhar com este plano

1. Escolha o próximo item pendente da fase atual (ou peça: "faça a 0.9").
2. Execute, verifique, marque `[x]`.
3. Rode `python scripts/progresso.py --atualizar` para atualizar o quadro.
4. Registre a sessão em `PROGRESSO.md` (§1 estado, §5 registro).
