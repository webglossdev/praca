# PROGRESSO: perfis políticos + app de notícias de política

> Arquivo de passagem de contexto. Atualize ao fim de cada sessão de trabalho (você ou o agente da IDE).
> Para pedir ajuda ao Claude, cole este arquivo inteiro, ou as seções 1 a 4 e as últimas entradas da seção 5.
> Regras: a seção 1 é reescrita; as seções 2 e 5 só recebem acréscimos (nada é apagado, só marcado como substituído).

---

## 1. Estado atual (reescrever a cada sessão; máx. ~15 linhas)

- **Fase:** preparação pública concluída localmente; primeiro commit criado, remoto configurado e push bloqueado por ausência de repositório/autenticação no GitHub.
- **Funciona hoje:** Câmara 513 deputados e Senado 81 senadores ativos em `data/publico/pessoas.json`; 166 notícias normalizadas; `npm run check` sem diagnósticos; build público com 1.402 páginas; Pagefind indexou 1.402 páginas; Vitest 3/3 e Playwright/axe 4/4.
- **Melhorias desta sessão:** skip link e menu móvel, estados dinâmicos com `aria-live`, filtros preservados na URL, semântica de tabela corrigida, tooltip/estado de compartilhamento tratado, partido neutro em relação aos Poderes, fontes Fraunces/Instrument Sans/JetBrains Mono instaladas como Fontsource e gerenciador Node padronizado em npm.
- **Em andamento / pendente externo:** conexão de chaves de produção (`CGU_API_KEY`, `DATAJUD_API_KEY`), ingestão em lote de CSVs completos do TSE/Receita (~1,6 GB) em Parquet/DuckDB, revisão jurídica (`PLANO.md §7.6`) para desbloqueio de `SECOES_SENSIVEIS_ATIVAS`, validação com pesquisador externo (`§8.7`), Pagefind/Playwright/axe E2E e deploy no Cloudflare Pages + GitHub remoto.
- **Quebrado ou bloqueado:** não há erro do front-end nesta sessão. Persistem integrações reais não conectadas, Worker/front sem contrato único e workflow autônomo sem persistência/deploy.
- **Próximo passo:** configurar repositório remoto + segredos no GitHub, cadastrar tokens CGU/DataJud, rodar suíte E2E (Playwright + axe) e cumprir revisão jurídica §7.6 antes do lançamento público.

## 2. Decisões (só acréscimo)

| Data | Decisão | Por quê | Alternativas descartadas |
|---|---|---|---|
| 2026-10-04 | Licença AGPL 3.0 | Princípio do autor: todo código aberto, livre para ver, usar, modificar e distribuir com créditos; AGPL cobre uso em serviço web | — |
| 2026-10-04 | Escopo inicial: parlamentares, governadores, STF e Executivo federal | Cobrir os três poderes federais + governadores sem inviabilizar o trabalho | Incluir servidores de órgãos públicos (fica para depois) |
| 2026-10-04 | "Suspeitas" e "ligações" sempre com aviso de que vieram de uma notícia | O produto é um app de notícias; precisa deixar clara a origem | — |
| 2026-10-04 | Manter este arquivo como registro de progresso | O Claude não está integrado à IDE | — |
| 2026-10-05 | Direção de design "Tinta & Papel": 3 cores para os Poderes (verdigris, âmbar, índigo), sem vermelho × azul | Neutralidade visual: cor partidária seria leitura de viés | Paleta com vermelho/azul; verde-amarelo da bandeira |
| 2026-10-05 | `PLANO.md` é o plano mestre com checklist; progresso calculado por `scripts/progresso.py` | Acompanhar o andamento item a item | Checklist solto no `PROGRESSO.md` |
| 2026-10-05 | Operação Zero-Touch (`AUTONOMIA.md`): pipeline desacoplado em 3 níveis com fallback de snapshot, circuit breakers e guarda de diff | Usuário quer intervir apenas para novas funções ou bugs | Manutenção manual diária ou scripts frágeis sem auto-recuperação |
| 2026-11-14 | Incorporar pilar completo de educação cívica (`Como funciona`, `Guia do Cidadão`, `Glossário`) já na v1 | Unir o observatório factual de políticos ao aprendizado intuitivo do Estado brasileiro (Pacto Federativo, Poderes, Leis, Orçamento, Eleições e participação cidadã) | Deixar explicadores e glossário apenas para pós-lançamento |

**Propostas ainda não confirmadas:** pipeline com JSON estático; coletar das fontes oficiais direto, usando mcp-brasil, BrasilAPI e brazil-visible só como referência; stack completa D-01 a D-12 do `PLANO.md` §3 (Python no pipeline; Astro + TypeScript + CSS puro no front; Cloudflare Pages + Worker; GitHub Actions; dados sob ODbL); nome de trabalho "Praça".

## 3. Mapa do repositório (atualizar ao criar ou mover arquivos)

| Caminho | Para que serve | Alimentado por |
|---|---|---|
| `PROGRESSO.md` | Este registro | Manual / agente da IDE |
| `recursos-apis.md` | Planejamento: fontes, APIs, cuidados | Manual |
| `PLANO.md` | Plano mestre: stack, design, rotas, marcos, riscos e checklist por fase | Manual + `scripts/progresso.py` (quadro) |
| `AUTONOMIA.md` | Arquitetura de operação zero-touch: resiliência, crons, circuit breakers, tratamento de homônimos | Manual |
| `PAGINAS.md` | Inventário de páginas (v1, v1.x, futuro) com conteúdo e layout em planta | Manual |
| `design/tokens.css` | Tokens de design (cor, tipografia, espaço, movimento) | Manual |
| `design/guia-estilo.html` | Guia de estilo vivo (abrir no navegador) | Manual |
| `design/mockups.html` | Pranchas de alta fidelidade das telas prioritárias | Manual |
| `design/mockups/home-v0.jpg` | Mockup de referência da home | Gerado por IA; textos ilustrativos |
| `scripts/progresso.py` | Conta itens marcados no `PLANO.md` e atualiza o quadro | `py scripts/progresso.py --atualizar` |
| `pipeline/src/praca_pipeline/` | Modelos Pydantic v2 expandidos, HTTP resiliente, resolução anti-homônimo, coletores (`camara`, `senado`, `proposicoes`, `legislativo_extra`, `tse_cgu`), `noticias` (RSS/desfecho) e `posicionamento` | Pipeline e testes |
| `pipeline/tests/` | 27 testes automatizados (contratos, HTTP/circuit breaker, coletores, RSS, posicionamento e contraste WCAG AA) | CI |
| `scripts/validar_dados.py` | Valida todos os JSONs públicos (`fontes`, `pessoas`, `noticias`, `votacoes`, `ao-vivo`, `correcoes`, `status`) via Pydantic e guarda de licença | CI e local |
| `schema/pessoa.schema.json` | JSON Schema gerado para pessoa | `scripts/gerar_schema.py` |
| `data/publico/fixtures/` | Fixtures completas e validadas (`pessoas`, `noticias`, `votacoes`, `ao-vivo`, `correcoes`, `status`) | Testes e build Astro |
| `data/publico/fontes.yml` | Registro de 10 fontes oficiais/agências e licenças (`fontes.json`) | Pipeline |
| `data/publico/veiculos.yml` | Política de feeds RSS por veículo (agências oficiais × imprensa só trecho) | Pipeline notícias |
| `web/src/data/educacao.ts` | Conteúdo estruturado de educação cívica com proveniência oficial | Conteúdo curado e referenciado |
| `web/src/data/{pessoas,portal}.ts` | Dados tipados para perfis completos e portal (notícias, votações, ao vivo, correções, status) | Astro SSG |
| `web/src/components/{PersonCard,PracaSvg,SourceRule,InstitucionalPage}.astro` | Cartões de perfil, SVG paramétrico da Praça dos Três Poderes, régua de fonte e template institucional | Páginas Astro |
| `web/src/pages/aprender/index.astro` | Guia "Como funciona o Brasil", Bússola Federativa e simulador de Quociente Eleitoral | `educacao.ts` |
| `web/src/pages/guia-do-cidadao.astro` | Roteiros oficiais de participação, LAI (Fala.BR), e-Cidadania e fiscalização | `educacao.ts` |
| `web/src/pages/glossario.astro` | Glossário cívico, orçamentário e de status judicial A–Z com filtros | `educacao.ts` |
| `web/src/pages/` | 54 rotas estáticas geradas: Home, `/pessoas`, `/pessoas/[slug]`, `/pessoas/[slug]/votos` (com CSV), `/comparar`, `/noticias`, `/ao-vivo`, `/votacoes/[id]`, `/partidos`, `/estados`, `/busca` (atalho `/`), `/corrigir`, `/status`, `/metodologia`, `/fontes`, `/dados`, `/sobre`, `/privacidade`, `/termos` e `/sitemap.xml` | Astro SSG |
| `workers/ao-vivo/` | Cloudflare Worker (`/api/ao-vivo`, cache 60s, CORS configurável, fallback seguro) | Cloudflare Edge |
| `.github/` | Templates de Issue (`correcao-dado.yml`, `fonte-quebrada.yml`), PR template e workflows (`ci.yml`, `coleta-autonoma.yml`) | GitHub Actions |

## 4. Fontes de dados integradas e Runbook de operação

Status possíveis: planejada, parser-pronto, ativa (em fixture/snapshot), degradada, quebrada.

| Fonte | Status | Script / Módulo | Frequência | Armadilha operacional e mitigação |
|---|---|---|---|---|
| Câmara (API v2) | parser-pronto / snapshot | `coletores/{camara,proposicoes,legislativo_extra}.py` | 2x/dia | `/votacoes` falha se janela > 90 dias (validado com `ValueError` preventivo) |
| Senado (API REST + CEAPS) | parser-pronto / snapshot | `coletores/{senado,legislativo_extra}.py` | 2x/dia | Usar `/dadosabertos/votacao.json` (legado desativado em 01/02/2026); CEAPS exige `latin-1` e pular linha de metadados |
| TSE (CSVs + PesqEle) | parser-pronto / snapshot | `coletores/tse_cgu.py`, `posicionamento.py` | Por eleição / mensal | Preferir CSVs em lote a scraping; distinguir `eleito_aguardando_posse` de mandato ativo |
| Portal da Transparência (CGU) | parser-pronto (requer token em prod) | `coletores/tse_cgu.py` (`normalizar_emendas_cgu`, `normalizar_sancoes_cgu`) | Diária | Emendas, CEIS, CNEP e CEPIM requerem `CGU_API_KEY` nos segredos do GitHub Actions |
| Receita Federal (CNPJ/QSA) | parser-pronto | `coletores/tse_cgu.py` (`parsear_qsa_receita_csv`) | Mensal | Preservar `***CPF**` mascarado conforme publicado na origem |
| STF / Executivo / DOU | parser-pronto | `coletores/tse_cgu.py` (`normalizar_agentes_publicos`) | Diária | DataJud não permite busca direta por nome de partes |
| Notícias (RSS oficiais & imprensa) | parser-pronto / snapshot | `noticias.py` (`parsear_feed_rss`, `vincular_pessoas_noticia`) | 30 min / 6h | Imprensa bloqueada para `corpo_integral`; vínculo automático exige confiança ≥ 0,95 + contexto político |

**Runbook rápido (se uma coleta falhar):**
1. Verificar `/status` e o alerta aberto na Issue `.github/ISSUE_TEMPLATE/fonte-quebrada.yml` gerada por `.github/workflows/coleta-autonoma.yml`.
2. O Circuit Breaker em `pipeline/src/praca_pipeline/http.py` mantém automaticamente o último snapshot válido em cache (política Stale-While-Offline).
3. Validar localmente com `uv run python scripts/validar_dados.py`, `uv run pytest -v` e `npm run check` antes de publicar nova revisão.

## 5. Registro (mais recente primeiro)

Modelo de entrada:

```

### 2026-11-24: preparação do repositório aberto e Live Demo
- **Quem:** Coordenador Técnico Principal
- **O que:** preparado README público, workflow de GitHub Pages, base `/praca` no Astro, `.gitignore` ampliado para ferramentas locais, Playwright, coverage e `.agents`, além de revisão de segredos antes da publicação.
- **Onde:** `README.md`, `.gitignore`, `.github/workflows/pages.yml`, `web/astro.config.mjs`, `web/src/layouts/Layout.astro`, `PROGRESSO.md`.
- **Como:** segurança revisada antes do commit; artefatos locais, cache bruto, ambiente virtual, builds e resultados de testes foram exclídos do rastreamento. Live Demo configurada para o subdiretório GitHub Pages `/praca/`.
- **Por quê:** disponibilizar o projeto aberto em desenvolvimento sem publicar credenciais, dados brutos, CPFs completos ou artefatos desnecessários.
- **Verificação:** revisão de segurança não encontrou tokens, chaves privadas ou CPF completo rastreável; `test-results/` foi excluído. Próximo passo exige credencial GitHub CLI ou API para criar remoto e fazer push.
- **Problemas e armadilhas:** GitHub CLI não estava instalado no PATH; também não havia credencial GitHub ou remote configurado. Publicação remota ainda depende de autenticação humana.
- **Pendências geradas:** criar repositório remoto, configurar Pages, validar URL live, proteger branch principal e publicar o primeiro commit.

### 2026-11-24: criação local e tentativa de publicação no GitHub
- **Quem:** Coordenador Técnico Principal
- **O que:** criado o primeiro commit local `5d765b7`, configurado o remoto `https://github.com/webglossdev/praca.git` e tentado `git push -u origin main`.
- **Onde:** repositório Git local da raiz `D:\.exp\IDE-WEBDEV-PAGES\app`.
- **Como:** revisão staged, varredura de padrões de token/chave privada, configuração de usuário Git local e push HTTPS.
- **Por quê:** concluir a publicação aberta e preparar o deploy GitHub Pages.
- **Verificação:** commit criado e diretório de trabalho limpo. O push foi rejeitado pelo GitHub com `Repository not found`, indicando repositório inexistente ou credencial sem acesso.
- **Problemas e armadilhas:** GitHub CLI não estava disponível por PATH e não havia credencial autenticada/remote pré-configurado. Nenhum segredo foi encontrado no staged.
- **Pendências geradas:** autenticar GitHub, criar o repositório `webglossdev/praca`, concluir o push, configurar Pages pela ação ou Settings e validar a URL pública.

### 2026-11-24: ingestão real inicial e estrutura jurídica completa
- **Quem:** Coordenador Técnico Principal com cinco subagentes especialistas
- **O que:** criado `python -m praca_pipeline`/CLI em `pipeline/src/praca_pipeline/cli.py` e wrapper `scripts/coletar_dados_reais.py`; coletados 513 deputados da Câmara e 81 senadores do Senado; normalizadas 166 notícias de RSS oficiais e de imprensa; publicados snapshots em `data/publico/pessoas.json`, `noticias.json`, `status.json` e `ao-vivo.json`; corrigida sigla partidária “SOLIDARIEDADE”; refinado modelo de votação com licença e limite de partidos em 32 caracteres; criado `JURIDICO.md` com critérios 7.1, fluxo 7.3, SLA 7.7 e documentação LGPD/LDA/LAI/Marco Civil/eleitoral.
- **Onde:** `pipeline/src/praca_pipeline/{cli.py,__main__.py,posicionamento.py,noticias.py,modelos/dominio.py,coletores/legislativo_extra.py}`; `scripts/coletar_dados_reais.py`, `scripts/validar_dados.py`; `web/src/data/{pessoas,portal}.ts`; `web/src/pages/corrigir.astro`; `JURIDICO.md`; `PLANO.md`; `PROGRESSO.md`; `data/publico/`.
- **Como:** coleta HTTP com cache, rate-limit e fallback já existentes; normalização Pydantic; validação de partido/sigla; preferência por dados públicos em produção por `PRACA_DATA_MODE=publico`, mantendo fixtures determinísticas em testes. A fonte CGU foi marcada como planejada sem chave e STF/DataJud como planejados sem credencial; nenhum dado foi inventado.
- **Por quê:** substituir a dependência exclusiva de fixtures por uma primeira ingestão verificável de fontes abertas e deixar o projeto pronto para o restante da operação sem ativar seções sensíveis prematuramente.
- **Verificação:** `uv run ruff check pipeline scripts` passou; `uv run pytest -v` passou com 28 testes; fontes, schema e validação passaram; coleta real terminou com 594 pessoas e 166 notícias; `npm run check` passou com 45 arquivos e 0 diagnósticos em modo `publico`; `npm run build` gerou 1.402 páginas em modo real e Pagefind indexou 1.402 páginas; Vitest passou 3/3; Playwright passou 4/4 em desktop/mobile; `npm audit --omit=dev` passou com 0 vulnerabilidades.
- **Problemas e armadilhas:** Câmara respondeu inicialmente com erro e depois foi coletada integralmente após nova tentativa; sigla partidária criada pela API exigiu normalização ASCII; a Câmara não publicou uma URL RSS válida no feed configurado e STF/TSE bloquearam ou redirecionaram feeds, ficando degradados no `status.json`; CGU e DataJud permanecem planejados sem chave; as seções sensíveis continuam desligadas por bloqueio jurídico humano.
- **Pendências geradas:** completar portal CGU/DataJud/TSE em lote/Receita/Executivo/DOU conforme credenciais e lote, ativar cron real de persistência/commit, validar termos vigentes por fonte com responsável humano, concluir LGPD/DPIA/licença da base, revisão jurídica independente de `7.6`, Lighthouse/link-checker/backups/deploy e remoção final de fixtures do modo público.

### 2026-11-24: conclusão técnica do MVP front-end e qualidade automatizada
- **Quem:** agente da IDE com agentes especializados de design, engenharia e web
- **O que:** concluído o MVP do front-end; integrada busca estática Pagefind; alinhado o contrato `/api/ao-vivo` no Worker e no front com fallback estático; adicionados downloads JSON públicos; corrigidos menu por teclado, Escape/foco, deep-link de filtros, formulário de votos/CSV, 404 e cabeçalhos de segurança. Adicionadas suítes Vitest, Playwright desktop/mobile e axe no CI. Atualizado Astro de 5.14.1 para 7.4.13 com dependências compatíveis.
- **Onde:** `workers/ao-vivo/src/index.ts`, `web/src/pages/`, `web/src/layouts/Layout.astro`, `web/public/_headers`, `package.json`, `package-lock.json`, `vitest.config.mts`, `playwright.config.ts`, `tests/`, `.github/workflows/ci.yml`, `.github/workflows/coleta-autonoma.yml`, `PLANO.md`, `PROGRESSO.md`.
- **Como:** auditorias independentes por sub-agentes; correções verificáveis em Astro/CSS/TypeScript/Python; build de produção com indexação Pagefind; testes unitários, acessibilidade automatizada e navegação real em Chromium desktop/mobile.
- **Por quê:** fechar o máximo possível do desenvolvimento local sem substituir decisões externas pendentes, reduzindo riscos de busca, integração ao vivo, downloads, segurança e regressão.
- **Verificação:** `uv run ruff check pipeline scripts` passou; `uv run pytest -v` passou com 27 testes; `npm run test:web` passou com 3 testes; `npm run check` passou com 45 arquivos e 0 diagnósticos; `npm run build` gerou 54 páginas e 1962–2108 palavras indexadas pelo Pagefind; `npm run test:e2e` passou com 4 testes em desktop/mobile; `npm audit --omit=dev` passou com 0 vulnerabilidades.
- **Problemas e armadilhas:** domínio público real, repositório remoto, credenciais CGU/DataJud, dados completos TSE/Receita/CGU/Executivo/DOU e revisão jurídica não podem ser concluídos apenas no código local. Os dados continuam em fixtures enquanto não houver snapshot real publicado.
- **Pendências geradas:** configurar Cloudflare Pages/Worker e domínio, obter segredos oficiais, implementar coletores reais pendentes, publicar 640+ perfis, revisar termos/licenças/fotos/LGPD, realizar validação externa e beta.

### 2026-11-24: revisão técnica e correções de acessibilidade, navegação e tipografia
- **Quem:** agente da IDE com três agentes especializados (design director, software engineer e web programmer)
- **O que:** corrigidos padrões de acessibilidade e navegação no front-end; adicionados skip link, menu móvel colapsável, estados `aria-live`, pluralização correta, filtros compartilháveis na URL e semântica de cabeçalhos de tabela. Ajustados chip partidário neutro, indicador visual de agenda e movimento reduzido. Instaladas as famílias Fraunces, Instrument Sans e JetBrains Mono via Fontsource. Padronizado o gerenciador Node em npm.
- **Onde:** `web/src/layouts/Layout.astro`, `web/src/styles/global.css`, `web/src/components/PersonCard.astro`, páginas `busca`, `noticias`, `pessoas`, `corrigir`, `comparar`, `guia-do-cidadao`, `aprender` e perfil de pessoa; `package.json`, `package-lock.json`, `PLANO.md`, `PROGRESSO.md`.
- **Como:** revisão baseada nos agentes e nas Web Interface Guidelines; mudanças cirúrgicas em Astro/CSS/TypeScript; fontes importadas diretamente no layout para manter produção self-hosted.
- **Por quê:** tornar a navegação por teclado e tecnologia assistiva mais consistente, preservar estado filtrado e fortalecer a identidade "Tinta & Papel" sem associar partidos aos Poderes.
- **Verificação:** `npm run check` (`39 files: 0 errors, 0 warnings, 0 hints`) e `npm run build` (`54 page(s) built`; saída concluída em 4,42 s). Fontes permanecem em dependências locais do pacote.
- **Problemas e armadilhas:** `npm install` informou 8 vulnerabilidades transitivas no relatório local e deve ser revisado depois. A auditoria confirmou pendências estruturais ainda fora desta correção: pipeline de dados reais, contrato Worker/web, publicação do workflow autônomo e proveniência obrigatória em todos os modelos.
- **Pendências geradas:** itens 9.4–9.8 de qualidade/E2E, integração real dos dados, correção do contrato `/api/ao-vivo`, persistência/deploy do workflow e resolução das vulnerabilidades npm.
### AAAA-MM-DD: título curto
- **Quem:** humano / agente da IDE / Claude
- **O que:** 
- **Onde:** arquivos e pastas tocados
- **Como:** comando ou abordagem
- **Por quê:** 
- **Verificação:** como foi testado e o resultado
- **Problemas e armadilhas:** 
- **Pendências geradas:** 
```

### 2026-11-14: conclusão estrutural completa do projeto Praça (Etapas 1 a 5)
- **Quem:** agente da IDE
- **O que:** concluídas as etapas de fundação (`git init -b main`, AGPL-3.0 integral em `LICENSE`, `.gitignore` com `.wrangler/`, templates de Issue/PR e `README.md`), expansão completa do pipeline Python (`dominio.py`, `legislativo_extra.py`, `tse_cgu.py`, `noticias.py` com parser RSS/vinculação anti-homônimo ≥ 0,95/detector de desfecho, `posicionamento.py`, `scripts/validar_dados.py`), catálogo de 10 fontes (`fontes.yml`/`fontes.json`) e 8 veículos RSS (`veiculos.yml`), fixtures enriquecidas (`pessoas.json`, `noticias.json`, `votacoes.json`, `ao-vivo.json`, `correcoes.json`, `status.json`), suíte de 27 testes incluindo verificação WCAG AA automática de `design/tokens.css`, todas as novas telas Astro (`54` rotas estáticas incluindo perfis em 11 seções, histórico de votações com exportação CSV, `/comparar`, `/noticias`, `/ao-vivo` com player `youtube-nocookie` sob clique, `/votacoes/[id]`, `/partidos`, `/estados`, `/busca` com atalho `/`, `/corrigir`, `/status` e rotas diretas institucionais), Worker Cloudflare (`/api/ao-vivo`) e workflows `.github/workflows/{ci,coleta-autonoma}.yml`.
- **Onde:** `LICENSE`, `.gitignore`, `README.md`, `.github/{ISSUE_TEMPLATE,pull_request_template.md,workflows}`, `design/tokens.css`, `pipeline/`, `scripts/validar_dados.py`, `data/publico/`, `schema/pessoa.schema.json`, `web/src/`, `workers/ao-vivo/`, `PLANO.md`, `PROGRESSO.md`.
- **Como:** implementação modular com contratos Pydantic v2 `extra="forbid"`, guarda dupla de direitos autorais (pipeline + `validar_dados.py` + Astro) impedindo exibição de corpo integral de imprensa sem licença aberta, `SECOES_SENSIVEIS_ATIVAS = false` mantendo atribuições sensíveis em quarentena até revisão jurídica, e componente compartilhado `InstitucionalPage.astro`.
- **Por quê:** concluir o projeto Praça de ponta a ponta unindo observatório auditável de dados públicos e educação cívica com a direção `Tinta & Papel`.
- **Verificação:** `.venv\Scripts\ruff.exe check pipeline scripts` (`All checks passed!`), `uv run python scripts/gerar_fontes.py` (exit 0), `uv run python scripts/gerar_schema.py` (exit 0), `uv run python scripts/validar_dados.py` (exit 0 — 5 pessoas, 5 notícias, 3 votações, 3 eventos ao vivo, 2 correções, 6 fontes monitoradas), `uv run pytest -v` (27 passed in 0.53s), `npm run check` (`Result (39 files): 0 errors, 0 warnings, 0 hints`), `npm run build` (`54 page(s) built`), `uv run python scripts/progresso.py --atualizar` (`108/159 itens · 68%`).
- **Problemas e armadilhas:** o teste automático WCAG AA detectou `--atrib` claro (`#7A6F4F`) sobre `--bg` (`#F5F1E8`) em `4.42 < 4.5`; ajustado para `#716648` em `design/tokens.css` para cumprir AA nos dois temas. Também foi adicionado `sys.path.insert` em `scripts/validar_dados.py` espelhando `scripts/gerar_schema.py`.
- **Pendências geradas:** obtenção de chaves CGU/DataJud em produção, ingestão completa TSE/Parquet (~1,6 GB), revisão jurídica §7.6, validação externa §8.7, suíte Vitest/Playwright/axe/Pagefind e deploy remoto no Cloudflare Pages + GitHub.

### 2026-11-14: plataforma de educação cívica, Guia do Cidadão e correções do front/pipeline
- **Quem:** humano + agente da IDE
- **O que:** expandida a Praça com o módulo completo de educação política e cidadania (P-37 `/aprender`, P-40 `/guia-do-cidadao`, P-26 `/glossario`), adicionadas pontes contextuais nos perfis, Poderes e Home, corrigidos bugs de filtragem SSG/query string, variável `--poder` na linha do tempo de perfis, alternância inicial de tema, navegação mobile, catálogo real em `/institucional/fontes`, sitemap dinâmico e remoção de parâmetros `utm_*`/`fbclid`/`gclid` na deduplicação de notícias.
- **Onde:** `PAGINAS.md`, `PLANO.md`, `PROGRESSO.md`, `pipeline/src/praca_pipeline/noticias.py`, `pipeline/tests/test_noticias.py`, `web/src/data/{educacao.ts,pessoas.ts}`, `web/src/layouts/Layout.astro`, `web/src/styles/global.css`, `web/src/components/PersonCard.astro`, `web/src/pages/{index.astro,aprender/index.astro,guia-do-cidadao.astro,glossario.astro,sitemap.xml.ts,pessoas/index.astro,pessoas/[slug].astro,poderes/[poder].astro,institucional/[pagina].astro}`.
- **Como:** base estruturada tipada (`educacao.ts`) com proveniência oficial para Constituição Federal, Câmara, Senado, TSE, Tesouro Transparente, CGU, STF, MPF e TCU; filtros e simulador de Quociente Eleitoral client-side sem dependências externas; preservação integral da direção `Tinta & Papel`.
- **Por quê:** atender à ampliação da visão do autor para unir o observatório factual de agentes políticos a uma plataforma intuitiva, neutra e educativa sobre como funciona o governo brasileiro e como o cidadão pode agir e cobrar pelos canais oficiais.
- **Verificação:** `.venv\Scripts\ruff.exe check pipeline scripts` (`All checks passed!`), `uv run pytest -v` (20 passed in 0.41s), `npm run check` (19 files: 0 errors, 0 warnings, 0 hints), `npm run build` (28 page(s) built in 6.51s), `uv run python scripts/progresso.py --atualizar` (`Total: 63/159 itens (40%)`). Inspeção direta dos arquivos gerados `web/dist/sitemap.xml`, `web/dist/poderes/judiciario/index.html`, `web/dist/pessoas/fulana-de-tal-uf/index.html` e `web/dist/institucional/fontes/index.html`.
- **Problemas e armadilhas:** no `global.css`, classes com `display: grid` (`.card`, `.person-card`) sobrepunham a regra padrão de navegador `[hidden]`, exigindo `[hidden] { display: none !important; }` explícito para os filtros client-side funcionarem em todas as telas.
- **Pendências geradas:** validar visualmente no navegador com Playwright (E2E e testes em 320/360/768/1280px), conectar coletores reais do pipeline ao front-end e adicionar seletores por UF/município ao Guia do Cidadão quando a camada de dados locais entrar em escopo.

### 2026-10-05: arquitetura de operação 100% autônoma (Zero-Touch)
- **Quem:** agente da IDE
- **O que:** criado o documento `AUTONOMIA.md` detalhando como o site opera sem intervenção manual diária: matriz de agendamentos (GitHub Actions + Cloudflare Workers), mitigação de 7 complicações críticas (APIs fora do ar com Stale-While-Offline, quebra de contratos via Pydantic e Diff Guard, riscos jurídicos por quarentena e atribuição estrita, desambiguação contextual de homônimos com confidence ≥ 0.95, rate limits via token bucket e CSVs em lote, transição eleitoral via máquina de estados temporal, e detecção autônoma de transmissões ao vivo na borda).
- **Onde:** `AUTONOMIA.md`, `PLANO.md` (itens 3.2a, 3.28a, 5.5, 11.2, 11.2a, 11.5), `PROGRESSO.md`
- **Como:** modelagem de sistemas distribuídos resilientes e circuit breakers inspirados no conceito de radar cívico e mecanismo de precisão.
- **Por quê:** o autor solicitou operação autônoma máxima, intervindo apenas para novos recursos, redesigns ou correção de bugs de código.
- **Verificação:** `py scripts/progresso.py --atualizar` executado (11/153 itens).
- **Problemas e armadilhas:** automação cega em temas sensíveis (processos criminais) gera risco judicial imediato; a solução foi isolar investigações em quarentena estruturada com desfecho obrigatório e limitar notícias a citações curtas com atribuição ao veículo.
- **Pendências geradas:** implementação dos coletores com retry/backoff na Fase 3.

### 2026-10-06: protótipo navegável da home e panorama
- **Quem:** agente da IDE
- **O que:** criado o protótipo navegável `design/prototipo.html`, com home, mapa abstrato da Praça, cartões dos três Poderes, radar de notícias, agenda ao vivo, amostra de pessoas e princípios editoriais.
- **Onde:** `design/prototipo.html`, `PLANO.md` (item 2.4d), `PROGRESSO.md`.
- **Como:** HTML e CSS puros reutilizando `design/tokens.css`; tema claro/escuro, âncoras de navegação, busca demonstrativa, filtros visuais e layout responsivo para 360px+.
- **Por quê:** transformar as plantas de `PAGINAS.md` em uma experiência navegável antes de iniciar o Astro.
- **Verificação:** revisão estática do HTML/CSS; próxima verificação é abrir no navegador em desktop e mobile.
- **Problemas e armadilhas:** os perfis, números e notícias são explicitamente fictícios; fontes externas de tipografia só existem neste preview.
- **Pendências geradas:** validar o inventário com o autor (2.4b), revisar a direção e congelar v1 (2.5), e produzir mockups de alta fidelidade (2.4c).

### 2026-10-06: correção de overflow responsivo
- **Quem:** agente da IDE
- **O que:** corrigido o estouro horizontal em telas estreitas e o desalinhamento causado por tracks de grid com tamanho mínimo implícito; controles e navegação também foram ajustados para 320–360px.
- **Onde:** `design/prototipo.html`.
- **Como:** tracks mobile passaram a usar `minmax(0, 1fr)`, filhos de grids receberam `min-width: 0`, busca recebeu largura limitada ao contêiner, textos de eyebrow podem quebrar, e a navegação secundária é ocultada no breakpoint estreito.
- **Por quê:** o layout ultrapassava a viewport e quebrava ao redimensionar, especialmente em 320px e 360px.
- **Verificação:** Playwright mediu `scrollWidth == clientWidth` em 320, 360, 390, 480, 768, 1024, 1280 e 1440px; problemas do editor: nenhum.
- **Problemas e armadilhas:** o scrollbar vertical reduz o `clientWidth` em alguns tamanhos, mas não gera overflow; o teste compara os dois valores corretos.
- **Pendências geradas:** revisar visualmente as cinco pranchas de alta fidelidade antes de iniciar o front Astro.

### 2026-10-06: fundação Astro + TypeScript
- **Quem:** agente da IDE
- **O que:** criado o front-end estático mínimo com layout acessível, tema claro/escuro, home, lista filtrável de pessoas e perfis individuais gerados a partir das fixtures públicas.
- **Onde:** `web/`, `package.json`, `package-lock.json`, `PLANO.md`
- **Como:** Astro 5, TypeScript estrito, CSS puro importando `design/tokens.css`, sem alterar o pipeline Python.
- **Por quê:** transformar a direção visual e o contrato de pessoas em uma base navegável e leve para o MVP.
- **Verificação:** `npm install` e `npm run build` concluídos; 7 páginas estáticas geradas.
- **Problemas e armadilhas:** `npm install` reportou 3 vulnerabilidades transitivas; não foi executado `npm audit fix` para evitar upgrades não solicitados.
- **Pendências geradas:** validar visualmente em desktop/mobile e conectar dados produzidos pelo pipeline.

### 2026-10-06: pranchas de alta fidelidade
- **Quem:** agente da IDE
- **O que:** criada uma prancha navegável com as telas prioritárias P-01 (início), P-02 (notícias), P-03 (notícia), P-05 (perfil) e P-07 (ao vivo).
- **Onde:** `design/mockups.html`, `PLANO.md` (item 2.4c), `PROGRESSO.md`.
- **Como:** HTML/CSS puro sobre os tokens existentes, com abas acessíveis, deep links por hash, tema claro/escuro, estados de fonte, contexto editorial, perfil e estado ao vivo.
- **Por quê:** validar hierarquia e densidade das telas principais antes de escolher e implementar o framework do front-end.
- **Verificação:** cada aba foi aberta em 320, 360, 390, 480, 768, 1024 e 1440px; todas tiveram `overflow` horizontal igual a zero e permaneceram ativas corretamente; problemas do editor: nenhum.
- **Problemas e armadilhas:** os dados são fictícios; o indicador “ao vivo” é apenas uma representação visual até o Worker da Fase 6 existir.
- **Pendências geradas:** revisão do inventário v1 pelo autor (2.4b), congelamento da direção visual (2.5) e aprovação da stack (0.7).

### 2026-10-06: fundação e contratos de dados
- **Quem:** agente da IDE
- **O que:** criado o esqueleto Python/uv, metadados do projeto, CI, modelos Pydantic do domínio, envelope de proveniência, convenções de `pid`/slug, schema JSON, registro inicial de fontes e cinco fixtures fictícias.
- **Onde:** `.gitignore`, `.editorconfig`, `.python-version`, `.nvmrc`, `package.json`, `README.md`, `LICENSE`, `NOTICE`, `AGENTS.md`, `pyproject.toml`, `pipeline/`, `schema/`, `data/publico/`, `.github/workflows/ci.yml`.
- **Como:** contratos estritos com `extra="forbid"`, validação de URL/data/licença, testes sem rede e geração reproduzível de schema.
- **Por quê:** criar a base executável necessária para o front consumir dados consistentes e para futuras fontes serem conectadas sem espalhar regras pelo código.
- **Verificação:** `uv sync`; `uv run ruff check pipeline scripts`; `uv run pytest` (4 testes); `uv run python scripts/gerar_schema.py` (schema gerado).
- **Problemas e armadilhas:** o texto de `LICENSE` aponta para a cópia oficial online em vez de duplicar o documento integral; a licença do conjunto de dados continua proposta e cada fonte precisa de validação jurídica.
- **Pendências geradas:** implementar cliente HTTP/cache (3.2), gerar `fontes.json` (3.3 completo), completar mypy e revisar a aprovação formal da stack (0.7).

### 2026-10-06: fechamento do marco de 20%
- **Quem:** agente da IDE
- **O que:** adicionada política de contribuição DCO, cabeçalhos SPDX aos arquivos Python e versão fixa do gerenciador pnpm no `package.json`; o item 0.9 permaneceu pendente porque o download do texto integral da AGPL falhou por indisponibilidade de rede.
- **Onde:** `CONTRIBUTING.md`, `package.json`, arquivos Python de `pipeline/` e `scripts/`, `PLANO.md`, `PROGRESSO.md`.
- **Como:** validação local com uv, sem mascarar o bloqueio externo da licença.
- **Por quê:** alcançar o marco de 20% contando apenas itens verificáveis.
- **Verificação:** testes e lint executados após os ajustes; a licença curta em `LICENSE` continua explicitamente apontando para a fonte oficial.
- **Problemas e armadilhas:** `git init`, texto integral da licença e proteção do remoto ainda exigem decisão/execução fora do escopo local.
- **Pendências geradas:** completar 0.9 quando a fonte oficial estiver acessível; gerar `fontes.json` e implementar cliente HTTP com cache.

### 2026-10-06: cliente HTTP resiliente
- **Quem:** agente da IDE
- **O que:** implementado cliente comum para fontes públicas com cache JSON em disco, escrita atômica, User-Agent identificado, limite de ritmo, retry de erros 429/5xx e backoff com jitter.
- **Onde:** `pipeline/src/praca_pipeline/http.py`, `pipeline/tests/test_http.py`, `pyproject.toml`, `uv.lock`, `PLANO.md`, `PROGRESSO.md`.
- **Como:** `httpx.Client` com `MockTransport` nos testes; o cache evita nova chamada para a mesma URL e parâmetros.
- **Por quê:** estabelecer a camada de coleta resiliente antes dos coletores Câmara/Senado/TSE.
- **Verificação:** `uv sync`; `uv run ruff check pipeline scripts`; `uv run pytest` — 7 testes passaram; teste confirmou retry, cache e User-Agent.
- **Problemas e armadilhas:** o cliente ainda não implementa circuito por fonte nem Stale-While-Offline; isso permanece no item 3.2a.
- **Pendências geradas:** concluir publicação `fontes.json` (3.3) e adicionar circuit breaker/fallback (3.2a).

### 2026-10-06: publicação do registro de fontes
- **Quem:** agente da IDE
- **O que:** criado gerador determinístico de `fontes.json` a partir de `data/publico/fontes.yml`, com validação estrita de campos, URLs HTTP e IDs únicos.
- **Onde:** `scripts/gerar_fontes.py`, `scripts/__init__.py`, `data/publico/fontes.json`, `pipeline/tests/test_fontes.py`, `pyproject.toml`, `uv.lock`, `PLANO.md`, `PROGRESSO.md`.
- **Como:** `yaml.safe_load` + modelo Pydantic fechado; fontes ordenadas por ID e serializadas com versão do registro.
- **Por quê:** tornar o catálogo de proveniência consumível pelo front-end e por integrações sem duplicar o YAML editorial.
- **Verificação:** `uv run python scripts/gerar_fontes.py`; `uv run ruff check pipeline scripts`; `uv run pytest` — 8 testes passaram.
- **Problemas e armadilhas:** URLs são normalizadas pelo `HttpUrl` com barra final; o circuito e o fallback ainda permanecem no item 3.2a.
- **Pendências geradas:** implementar circuit breaker/fallback e iniciar os coletores Câmara/Senado/TSE.

### 2026-10-06: circuito de proteção por fonte
- **Quem:** agente da IDE
- **O que:** adicionado `CircuitBreaker` configurável ao cliente HTTP, com limiar de falhas, estado aberto, cooldown e sonda de recuperação.
- **Onde:** `pipeline/src/praca_pipeline/http.py`, `pipeline/tests/test_http.py`.
- **Como:** o circuito é consultado antes da rede, registra sucesso após uma resposta válida e registra uma falha somente depois de esgotar as tentativas da coleta.
- **Por quê:** evitar tempestade de requisições contra uma fonte degradada e expor o estado de indisponibilidade explicitamente.
- **Verificação:** `uv run ruff check pipeline scripts`; `uv run pytest` — 9 testes passaram.
- **Problemas e armadilhas:** o fallback Stale-While-Offline ainda não foi ativado; o cache atual continua sendo retorno fresco por chave e não deve ser apresentado como snapshot degradado.
- **Pendências geradas:** implementar snapshots versionados/fallback stale e iniciar os coletores Câmara/Senado/TSE.

### 2026-10-06: fallback Stale-While-Offline
- **Quem:** agente da IDE
- **O que:** adicionada janela opcional de frescor, leitura da idade do cache e fallback explícito para o último snapshot válido quando a renovação falha ou o circuito está aberto.
- **Onde:** `pipeline/src/praca_pipeline/http.py`, `pipeline/tests/test_http.py`, `PLANO.md`, `PROGRESSO.md`.
- **Como:** `get_json(..., fresh_for=...)` tenta atualizar snapshots expirados; em falha, devolve o cache anterior e expõe `degraded` e `last_snapshot_age`.
- **Por quê:** manter o site funcional sem apresentar dados antigos como se fossem atuais.
- **Verificação:** `uv run ruff check pipeline scripts`; `uv run pytest` — 10 testes passaram; problemas do editor: nenhum.
- **Problemas e armadilhas:** chamadas sem `fresh_for` preservam a compatibilidade e continuam servindo o cache imediatamente; coletores devem usar uma janela de frescor para ativar renovação.
- **Pendências geradas:** iniciar os coletores Câmara/Senado/TSE e incluir telemetria pública do estado degradado.

### 2026-10-06: primeiro coletor da Câmara
- **Quem:** agente da IDE
- **O que:** criado coletor paginado da API Dados Abertos da Câmara para deputados, UF, partido quando disponível, mandato atual e proveniência.
- **Onde:** `pipeline/src/praca_pipeline/coletores/camara.py`, `pipeline/src/praca_pipeline/coletores/__init__.py`, `pipeline/tests/test_camara.py`, `PLANO.md`, `PROGRESSO.md`.
- **Como:** endpoint REST `/api/v2/deputados`, páginas de até 100 itens, `ClienteFonte` com cache/frescor e contrato Pydantic `DeputadoCamara`.
- **Por quê:** iniciar a ingestão oficial sem scraping e manter IDs/slug determinísticos para o front-end futuro.
- **Verificação:** `uv run ruff check pipeline scripts`; `uv run pytest` — 11 testes passaram.
- **Problemas e armadilhas:** a listagem pode não carregar o nome completo do partido; o coletor não inventa esse valor e deixa `partido_nome` nulo quando ausente. O endpoint de detalhe partidário fica para o enriquecimento.
- **Pendências geradas:** implementar enriquecimento de detalhes da Câmara e coletor do Senado.

### 2026-10-06: coletor da lista atual do Senado
- **Quem:** agente da IDE
- **O que:** criado coletor da lista JSON oficial de senadores em exercício, com código legislativo, nomes, UF, partido, mandato e proveniência.
- **Onde:** `pipeline/src/praca_pipeline/coletores/senado.py`, `pipeline/tests/test_senado.py`, `PLANO.md`, `PROGRESSO.md`.
- **Como:** endpoint `/dadosabertos/senador/lista/atual.json`, estrutura `ListaParlamentarEmExercicio`, cache com janela de frescor e normalização Pydantic.
- **Por quê:** cobrir a identidade legislativa atual do Senado sem depender do endpoint legado de votações.
- **Verificação:** `uv run ruff check pipeline scripts`; `uv run pytest` — 12 testes passaram; endpoint oficial conferido em 06/10/2026.
- **Problemas e armadilhas:** a lista atual não substitui histórico completo de mandatos nem dados de votação; esses itens permanecem separados no plano.
- **Pendências geradas:** implementar proposições/votações e enriquecer detalhes partidários da Câmara.

### 2026-10-06: marco de 35% e fundação do MVP
- **Quem:** agente da IDE
- **O que:** implementados coletor de proposições da Câmara, normalização de notícias, resolução legislativa conservadora, gerador de índices, diff guard, política de frequência e front-end Astro com rotas de pessoas, partidos, estados, Poderes, institucionais, 404, sitemap e download JSON.
- **Onde:** `pipeline/src/praca_pipeline/{coletores/proposicoes.py,resolucao.py,qualidade.py,gerar.py,frequencia.py,noticias.py}`, testes correspondentes, `web/`, `data/publico/veiculos.yml`, `PLANO.md`.
- **Como:** contratos Pydantic, fixtures HTTP sem rede, build estático Astro, filtros client-side, JSON-LD, Open Graph SVG, sitemap e compartilhamento nativo sem rastreadores.
- **Por quê:** transformar a base de contratos em uma primeira experiência navegável e proteger a publicação contra dados duplicados, nulos ou oscilações anômalas.
- **Verificação:** `uv run ruff check pipeline scripts`; `uv run pytest` — 19 testes passaram; `npm run build` — 25 rotas estáticas geradas; problemas do editor: nenhum.
- **Problemas e armadilhas:** a busca usa filtro client-side simples, ainda sem Pagefind; a página inicial usa fixtures fictícias e não deve ser tratada como dado de produção; `npm install` reportou 3 vulnerabilidades transitivas a revisar.
- **Pendências geradas:** implementar votações, cota/CEAPS, ingestão TSE e conectar o front às saídas reais do pipeline.

### 2026-10-06: direção visual atlas editorial
- **Quem:** agente da IDE
- **O que:** aplicada uma nova camada visual na home Astro, com hero assimétrico, cartão de pulso da coleta, filete tricolor de sinal e microinterações discretas nos cartões.
- **Onde:** `web/src/pages/index.astro`, `web/src/styles/global.css`.
- **Como:** composição modular responsiva, contraste editorial, bordas/filetes em vez de sombras pesadas e uso das três cores dos Poderes sem transformar cor em opinião.
- **Por quê:** tornar a home mais reconhecível como observatório de dados e reforçar a leitura de estado/atualização sem abandonar a direção Tinta & Papel.
- **Verificação:** `npm run check`; `npm run build`; `uv run ruff check pipeline scripts`; `uv run pytest` — 19 testes passaram. Overflow horizontal medido em 320, 360, 390, 480, 768 e 1280 px: zero.
- **Problemas e armadilhas:** a inspiração foi usada somente como direção visual; a sequência aleatória não foi incorporada ao produto. O npm ainda reporta 3 vulnerabilidades transitivas para revisão posterior.
- **Pendências geradas:** revisar visualmente as páginas internas no mesmo tratamento e decidir se o hero deve migrar para o protótipo HTML legado.

### 2026-10-05: inventário de páginas
- **Quem:** agente da IDE
- **O que:** 39 páginas mapeadas (18 na v1, 9 na v1.x, 12 futuras), cada uma com objetivo, conteúdo e layout em planta; peças comuns; mapa de navegação.
- **Onde:** `PAGINAS.md`, `PLANO.md` (itens 2.4a–d, 5.4a–b), `PROGRESSO.md`
- **Como:** esquemas em texto sobre a grade de 12 colunas da direção Tinta & Papel.
- **Por quê:** o autor pediu o planejamento de todas as páginas antes dos mockups.
- **Verificação:** revisão de texto; nada executável.
- **Problemas e armadilhas:** exibir notícia completa só é permitido com licença aberta ou acordo. Ter acesso ao texto por uma API não dá direito de republicar. Para o resto, só título, trecho curto e link.
- **Pendências geradas:** 2.4b, 5.4a.

### 2026-10-05: plano mestre, stack proposta e design v0
- **Quem:** agente da IDE
- **O que:** criado o plano de desenvolvimento completo com 13 fases e 145 itens; proposta de stack (D-01 a D-12); direção de design "Tinta & Papel" com tokens, guia de estilo vivo e mockup da home; script de progresso.
- **Onde:** `PLANO.md`, `design/tokens.css`, `design/guia-estilo.html`, `design/mockups/home-v0.jpg`, `scripts/progresso.py`, `PROGRESSO.md`
- **Como:** direção criativa derivada de uma string aleatória gerada no shell (não registrada de propósito); mockup gerado por IA.
- **Por quê:** transformar a ideia em um caminho verificável, item a item.
- **Verificação:** `py scripts/progresso.py --atualizar` rodou e preencheu o quadro (10/145). O guia de estilo ainda não foi aberto no navegador por mim.
- **Problemas e armadilhas:** `python` no terminal é o atalho da Store (não executa); `py` só roda fora do sandbox. O mockup tem trechos de texto sem sentido gerados pela IA: serve só como clima e composição. O guia de estilo carrega fontes do Google apenas como preview; em produção são self-hosted.
- **Pendências geradas:** itens 0.7, 0.8, 2.5 do `PLANO.md`.

### 2026-10-04: planejamento inicial e levantamento de recursos
- **Quem:** humano + Claude
- **O que:** definiu-se a visão do projeto, o escopo inicial e os princípios; foram avaliados mcp-brasil, brazil-visible, BrasilAPI, br-acc e politicapp como recursos de referência; foi montada a tabela mestra de fontes.
- **Onde:** `recursos-apis.md`, `PROGRESSO.md`
- **Como:** leitura da documentação pública de cada projeto e das categorias do brazil-visible; pesquisas sobre PesqEle, DataJud e STF.
- **Por quê:** saber quais dados existem, de onde vêm e quais seções do perfil ainda não têm fonte antes de escrever o plano principal.
- **Verificação:** o que foi lido diretamente está marcado como "Confirmado" em `recursos-apis.md`; o restante está como "A confirmar" ou "Lacuna".
- **Problemas e armadilhas:** o DataJud não permite buscar processos pelo nome das partes; não há categoria de Legislativo no brazil-visible; existem forks falsos de repositórios conhecidos (usar só os oficiais).
- **Pendências geradas:** ver seção 6.

## 6. Pendências abertas

- [ ] Definir o método de ideologia do político e do partido
- [ ] Encontrar fonte de aprovação/desaprovação
- [ ] Verificar licença de fotos e biografias (DHBB/FGV)
- [ ] Definir como detectar "ao vivo" nas transmissões
- [ ] Achar fontes estruturadas para ministros do Executivo e do STF
- [ ] Escolher a stack do front-end
- [ ] Decidir a licença da base de dados compilada
- [ ] Ler `docs/apis` completo do brazil-visible e as 14 categorias não abertas
- [ ] Obter chaves do Portal da Transparência e do DataJud
- [ ] Baixar os CSVs do TSE e da Receita Federal
- [ ] Levantar os termos de uso de cada fonte

## 7. Convenções (preencher quando forem definidas)

- **Formato dos JSONs públicos:** UTF-8, indentação de 2 espaços, datas em ISO 8601 (`YYYY-MM-DD` / UTC ISO), validados contra Pydantic v2 (`extra="forbid"`) e `schema/pessoa.schema.json`.
- **Identificadores e slugs:** `pid` estável prefixado com `pid_` (ASCII minúsculo com hifens, desambiguado por UF/casa/cargo); URLs de perfil em `/pessoas/[slug]` e votos em `/pessoas/[slug]/votos`.
- **Proveniência obrigatória:** todo dado carregado nos perfis preserva `{valor, fonte_id, url, coletado_em, licenca}`; campos ausentes permanecem vazios ou nulos com aviso explícito na interface.
- **Direitos autorais e seções sensíveis:** notícias de imprensa exibem apenas título, veículo, data, trecho ≤ 500 caracteres e link canônico; seções sensíveis (`atribuicoes`) seguem desligadas via `SECOES_SENSIVEIS_ATIVAS = false` até revisão jurídica (§7.6).
