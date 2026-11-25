# Planejamento: recursos e APIs

Projeto: site/webapp de perfis de agentes políticos + app de notícias sobre política brasileira.
Documento criado em 04/10/2026 (dia do 1º turno das eleições gerais de 2026). Licença do projeto: AGPL 3.0.

Legenda de situação: **Confirmado** (li a fonte ou a documentação), **A confirmar** (existe pelo que sei, falta verificar), **Lacuna** (sem fonte clara ainda).

---

## 1. Escopo inicial

- Parlamentares (513 deputados e 81 senadores), governadores (27), ministros do STF (11) e os demais do Poder Executivo federal (presidente, vice, ministros de Estado).
- Ficam para depois: servidores de órgãos públicos (PGR, TCU etc.). BB, Caixa, Correios e similares não entram.
- Hoje, toda a Câmara e 2/3 do Senado estão em disputa. O 2º turno (presidente e governadores) é em 25/10 e os governadores tomam posse em 6/01/2027. O modelo de dados precisa guardar **histórico de mandatos** e distinguir "mandato atual" de "eleito, ainda não iniciado".
- Com mais de 640 perfis, a geração tem que ser feita por **pipeline a partir das fontes**; só biografia e tópicos relevantes exigem escrita manual.

## 2. Princípios

1. Todo dado exibido leva **fonte, data de coleta e link**.
2. Ideologia/posição só como **autodeclaração (com data e fonte)** ou **histórico de votos**, mais a posição do partido. Nunca opinião do site.
3. "Suspeitas" e "ligações" aparecem sempre com aviso de que vieram de uma notícia, com título original, veículo, data e link, e com o **desfecho atualizado** quando houver (arquivamento, absolvição, retratação).
4. Notícias: só título, veículo, data e link (mais trecho curto). Sem copiar matéria.
5. Código aberto (AGPL 3.0). Dados compilados com licença própria, a decidir.
6. *(Proposto)* Coletar das **fontes oficiais direto**; wrappers (mcp-brasil, BrasilAPI) servem de referência.

## 3. Catálogos e projetos de referência

| Recurso | O que é | Papel no projeto | Observações |
|---|---|---|---|
| **brazil-visible** (github.com/nferdica/brazil-visible) | Catálogo documentado de 92 fontes em 22 categorias (MIT) | Lista mestra de fontes e receitas de cruzamento | Não é API. Não tem categoria de Legislativo. Cópia hospedada em brazil-visible.webglossdev.tech. |
| **mcp-brasil** (github.com/Mcp-Brasil/mcp-brasil) | Servidor MCP em Python com ~70 fontes já implementadas (MIT) | Referência de implementação, sobretudo Câmara, Senado, TSE, DataJud, TCU | Feito para agentes de IA, não para site. Usar o código como referência, ou como servidor HTTP para dados recorrentes. |
| **br-acc** (World-Open-Graph/br-acc, AGPL 3.0) | Grafo (Neo4j) com ETL de ~45 bases públicas | Registro de fontes (`docs/source_registry_br_v1.csv`), validadores de ETL, documentos de LGPD/ética | Modo público bloqueia busca por pessoa. Pesado demais como base. **Usar só o repositório original.** |
| **BrasilAPI** (brasilapi.com.br) | API de utilidades (CEP, CNPJ, IBGE, bancos, feriados...) | CNPJ de empresas doadoras e IBGE (estados/municípios) | Termos proíbem varredura em massa: só consulta sob demanda, com cache. |
| **politicapp** (gmferraz/politicapp) | App open source que agrega Câmara, Senado e TSE | Lista de armadilhas reais das APIs (seção 7) | Só li o README. |
| **DivulgaCandContas** (API do TSE) | API da consulta de candidaturas, com planos de governo | Planos de governo e dados de candidatura | Sem documentação oficial; docs da comunidade em `augusto-herrmann/divulgacandcontas-doc`. Sem CORS e com limite de ritmo. Preferir os CSVs. |
| **Base dos Dados**, **Brasil.IO** | Dados públicos já tratados em massa | Candidatas a atalho de qualidade | Só vi trechos. Avaliar antes de usar. |

**Atenção:** existem cópias falsas de repositórios conhecidos (vi um fork do mcp-brasil com download de .zip "para Windows", padrão de malware). Usar apenas os repositórios oficiais ou o PyPI.

## 4. Mapa: seção do perfil → fonte

URLs citadas de memória devem ser validadas na documentação oficial antes de uso.

| Seção do perfil | Fonte primária | Acesso | Chave | Situação | Observações |
|---|---|---|---|---|---|
| Identidade, partido, cargo (deputados) | API Dados Abertos da Câmara (`dadosabertos.camara.leg.br/api/v2`) | REST | Não | Confirmado | `mcp-brasil: camara` |
| Identidade, partido, cargo (senadores) | Dados Abertos do Senado (`legis.senado.leg.br/dadosabertos`) | REST | Não | Confirmado | `mcp-brasil: senado`. Endpoint legado de votações desativado em 01/02/2026 (politicapp). |
| Governadores e Executivo federal (lista e cargos) | TSE (eleitos), gov.br, SIORG | CSV / consulta | A definir | **A confirmar** | Falta pesquisar fonte estruturada para ministros de Estado. |
| STF (composição) | Portal do STF | Site | Não | A confirmar | |
| Foto | Câmara/Senado (URL da foto), TSE, Wikimedia Commons | REST / arquivo | Não | A confirmar | Verificar licença de uso de cada fonte. |
| Biografia | DHBB (CPDOC/FGV), páginas oficiais, Wikipédia (CC BY-SA) | Páginas | Não | A confirmar | Texto do DHBB não pode ser copiado sem confirmar licença: usar link + resumo próprio com fonte. |
| Mandatos (início/fim) e eleições | TSE candidaturas e resultados | CSV | Não | Confirmado | `mcp-brasil: tse_candidatos` (2014-2024) |
| Votos que elegeram | TSE resultados / votação por município e zona | CSV (~1,6 GB) | Não | Confirmado | `mcp-brasil: tse_votacao`. Processar uma vez e guardar JSON. |
| Pesquisas de intenção de voto | PesqEle (TSE) | Consulta pública | Não | Confirmado | Registro obrigatório só em ano eleitoral: seção vazia na maior parte do tempo. |
| Aprovação/desaprovação | Institutos privados (ex.: Datafolha, Quaest, AtlasIntel) | Publicações | — | **Lacuna** | Sem fonte oficial. Exibir só com citação e link; verificar termos. |
| Dinheiro de campanha | TSE prestação de contas; FEFC (por partido) | CSV | Não | Confirmado | `mcp-brasil: tse`, `tse_fefc` |
| Empresas doadoras e sócios | Receita Federal (Estabelecimentos, QSA) em CSV; BrasilAPI (CNPJ) sob demanda | CSV / REST | Não | Confirmado | CPF dos sócios costuma vir mascarado: a confirmar. |
| Patrimônio declarado | TSE bens | CSV | Não | Confirmado | `mcp-brasil: tse_bens` |
| Plano de governo (e versão curta) | DivulgaCandContas (TSE) | API | Não | Confirmado (plano) / **A confirmar** (versão curta) | |
| Coligação/federação atual e passada | TSE candidaturas | CSV | Não | A confirmar (campo) | |
| Histórico de filiação partidária | TSE filiados | CSV | Não | Confirmado | Útil para mostrar mudanças de partido. |
| Projetos de autoria, relatorias, aprovações | Câmara e Senado (proposições) | REST | Não | Confirmado | |
| Presença e faltas | Câmara e Senado | REST | Não | **A confirmar** | politicapp avisa que a Câmara não expõe presença de forma direta. |
| Votações (como votou) | Câmara e Senado (votações nominais) | REST | Não | Confirmado | Câmara `/votacoes` aceita no máximo 3 meses por consulta. |
| Emendas parlamentares | Portal da Transparência (CGU), TransfereGov | REST | Sim (gratuita) | Confirmado | `mcp-brasil: transparencia`, `transferegov` |
| Despesas do mandato (cota parlamentar) | Câmara (cota), Senado (CEAPS) | REST / CSV | Não | Confirmado | CEAPS vem em Latin-1. |
| Sanções a empresas ligadas | CGU: CEIS, CNEP, CEPIM | REST | Sim | Confirmado | |
| Ideologia do político | Autodeclaração (com data/fonte) + histórico de votos | Calculado | — | Critério a definir | Metodologia aberta e documentada. |
| Ideologia do partido | Classificação acadêmica citável | Publicações | — | **Lacuna** | Procurar classificação publicada e citável. |
| Processos e investigações | Notícias com atribuição + fontes oficiais pontuais (STF, STJ, TCU, CGU, TSE) | Variado | Variado | Parcial | Ver seção 6. |
| Atos oficiais | DOU; Querido Diário (municipal) | REST | Não | Confirmado | `mcp-brasil: diario_oficial`. Diários oficiais estaduais não cobertos pelo brazil-visible. |
| Notícias | RSS de veículos e fontes oficiais | RSS | Não | A confirmar | Ver seção 5. |
| Tópicos relevantes | Votações nominais + declarações citadas + curadoria | Misto | — | Critério a definir | "Polêmico" precisa de critério objetivo (ex.: votação apertada ou lista fixa de temas). |

## 5. Módulo de notícias e "ao vivo"

| Item | Fonte | Situação |
|---|---|---|
| Pauta da Câmara e do Senado | APIs de agenda/eventos da Câmara e do Senado | A confirmar (endpoints) |
| Transmissão ao vivo | TV Câmara, TV Senado, TV Justiça (provavelmente YouTube) | A confirmar (como detectar "ao vivo") |
| Praça dos Três Poderes em 2D | SVG próprio com 3 marcadores (Executivo, Legislativo, Judiciário) | Visual simples; o difícil é a fonte do "agora" |
| Notícias oficiais | Agência Câmara, Agência Senado, Agência Brasil, notícias do STF | A confirmar (feeds RSS) |
| Notícias de imprensa | RSS de veículos; Google News RSS ou GDELT | A confirmar (termos de uso) |
| Nome vira link para o perfil | Dicionário de nomes e apelidos das ~640 pessoas do escopo | Viável; atenção a ambiguidade ("Davi" etc.) |

## 6. Processos judiciais: por que não há API limpa

- **DataJud (CNJ):** a API pública traz capas e movimentações, mas protege processos sigilosos e **dados das partes**. Não permite buscar processos pelo nome do político.
- **STF:** o portal tem busca por nome da parte, mas é busca em site, não API. Verificar os termos antes de automatizar. O Corte Aberta oferece CSVs estatísticos (desde 2000, com filtro por partes), mas agregados.
- **BNMP 3.0 (CNJ):** dados de medidas penais e prisões. Dado extremamente sensível; só com status oficial, fonte e revisão jurídica.
- **Outras:** CGU (sanções), TCU (acórdãos), TSE (processos eleitorais) cobrem casos pontuais.
- **Consequência:** a seção depende de notícias atribuídas + fontes oficiais por caso, sempre com status processual atualizado.

## 7. Armadilhas técnicas conhecidas (politicapp)

- Câmara `/votacoes`: intervalo máximo de 3 meses por consulta.
- Só 1.168 das 6.475 votações de 2026 são de plenário.
- Endpoint legado de votações do Senado desativado em 01/02/2026; `totalVotos` pode vir nulo.
- CEAPS (Senado) em Latin-1, com linha de metadados antes do cabeçalho.
- Câmara tem limite de requisições no endpoint de votos.
- Cada base usa um ID diferente e o CPF vem mascarado no TSE: é preciso uma regra de cruzamento (nome, UF, partido, ano) com cuidado com homônimos.

## 8. Cuidados legais e editoriais

- Revisão jurídica antes de publicar as seções de processos, suspeitas e ligações.
- LGPD: dados públicos tratados com finalidade clara; ver os documentos de privacidade do br-acc como modelo.
- Canal de contestação/correção e lista de veículos aceitos.
- Verificar os termos de uso de cada fonte (coleta automatizada, uso de imagens, republicação).
- Neutralidade: critérios de ideologia e de "tópicos relevantes" públicos e documentados.

## 9. Recursos a reunir

- [ ] Chaves gratuitas: Portal da Transparência e DataJud (Meta só se for usar anúncios eleitorais)
- [ ] Clonar os repositórios oficiais: mcp-brasil, brazil-visible, br-acc
- [ ] Baixar CSVs do TSE: candidaturas, bens, votação, prestação de contas, filiados, resultados
- [ ] Baixar CSVs da Receita (Estabelecimentos, QSA)
- [ ] Ler `docs/apis` completo do brazil-visible e as 14 categorias ainda não abertas
- [ ] Lista de pessoas do escopo com apelidos/variações de nome
- [ ] Lista de veículos de imprensa aceitos (e seus feeds RSS)
- [ ] Levantar termos de uso das fontes
- [ ] Hospedagem estática e domínio

## 10. Decisões e pendências

**Decidido:** AGPL 3.0; escopo inicial da seção 1; aviso de origem em suspeitas e ligações; manter o arquivo `PROGRESSO.md` (seção 11).

**Proposto, aguardando confirmação:** pipeline com JSON estático; coletar das fontes oficiais direto, usando wrappers só como referência.

**Pendente:** método de ideologia do político e do partido; fonte de aprovação/desaprovação; licença de fotos e biografias; detecção de "ao vivo"; fontes para ministros do Executivo e STF; stack do front-end; licença da base de dados compilada.

---

## 11. Registro de progresso (`PROGRESSO.md`)

Como o Claude não está integrado à IDE, o contexto do projeto chega até ele por este arquivo. Ele deve existir na raiz do repositório desde o primeiro commit e ser atualizado **ao fim de cada sessão de trabalho**, por você ou pelo agente de IA da IDE.

**Regras**

1. Para pedir ajuda, cole o arquivo inteiro. Se estiver grande, cole as seções 1 a 4 e as últimas entradas da seção 5.
2. A seção 1 (estado atual) é **reescrita** a cada sessão e fica curta, para o contexto caber de relance.
3. As seções 2 (decisões) e 5 (registro) são **só de acréscimo**: nunca apagar, só marcar como substituída.
4. Cada entrada do registro responde: o que foi feito, onde (arquivos e pastas), como (comando ou abordagem), por quê, como foi verificado, problemas encontrados e pendências geradas.
5. Registrar também o que **deu errado ou foi descartado**, e por quê. Isso evita repetir o mesmo caminho.
6. Pedir ao agente da IDE, no arquivo de instruções dele (por exemplo `AGENTS.md`), que atualize o `PROGRESSO.md` antes de encerrar qualquer tarefa.

Um modelo já preenchido com o estado atual acompanha este documento (`PROGRESSO.md`).
