# ARQUITETURA DE AUTONOMIA: Operação Zero-Touch e Resiliência

> **Objetivo:** O site deve operar, coletar, cruzar dados, normalizar notícias, detectar transmissões ao vivo, compilar perfis e publicar atualizações de forma **100% autônoma**.
> **Regra de Ouro:** A intervenção humana só deve ocorrer em três casos estritos:
> 1. Adição de novas funcionalidades ou alterações visuais/design;
> 2. Correção de bugs de código ou adaptação a mudanças drásticas de APIs oficiais;
> 3. Moderação jurídica excepcional acionada via canal estruturado de contestação (`/corrigir`).

---

## 1. O Modelo Mental: Mecanismo de Precisão e Radar Cívico

Para que um sistema funcione sem supervisão diária, ele não pode ser um script frágil. Ele precisa operar como um **observatório automatizado** baseado em cinco princípios:

1. **Idempotência Estrita:** Executar a rotina 1 vez ou 100 vezes seguidas produz exatamente o mesmo resultado estável.
2. **Imutabilidade e Snapshot Fallback (Stale-While-Offline):** Se uma fonte pública cair, mudar contrato ou der erro, o sistema **nunca** apaga o dado anterior nem quebra o site; ele congela o último snapshot válido e estampa a data de atualização com alerta de integridade.
3. **Desacoplamento em Três Níveis:**
   - **Nível 1: Ingestão & Cache Bruto (Cron agendado no GitHub Actions)**
   - **Nível 2: Normalização & Validação de Schemas (Pydantic / DuckDB)**
   - **Nível 3: Compilação Estática & Borda (Astro SSG + Cloudflare Pages + Worker)**
4. **Auto-Cura e Circuit Breakers:** Falhas temporárias (HTTP 429, 502, 503) são absorvidas por *retry* com *exponential backoff* e *jitter*.
5. **Rastreabilidade e Telemetria Pública (`/status`):** O próprio sistema audita a si mesmo e expõe para o usuário o estado de saúde de cada robô de coleta.

```
┌────────────────────────────────────────────────────────────────────────┐
│                   PIPELINE DE OPERAÇÃO AUTÔNOMA                        │
└────────────────────────────────────────────────────────────────────────┘

 [ Fontes Oficiais & Feeds ]
  Câmara · Senado · TSE · CGU · DOU · RSS Oficiais/Imprensa · YouTube Live
                           │
                           ▼ (Agendamentos diferenciados)
 ┌──────────────────────────────────────────────────────────────────────┐
 │ NÍVEL 1: ROBÔS DE COLETA (GitHub Actions / Cloudflare Cron)           │
 │  • Polite Client (HTTP ETag, If-Modified-Since, 2 req/s)             │
 │  • Cache bruto em disco efêmero (evita re-download desnecessário)    │
 │  • Circuit Breaker (3 falhas seguidas = aborta coleta daquela fonte) │
 └──────────────────────────────────┬───────────────────────────────────┘
                                    │
                                    ▼
 ┌──────────────────────────────────────────────────────────────────────┐
 │ NÍVEL 2: MOTOR DE NORMALIZAÇÃO & AUDITORIA (Python + DuckDB)         │
 │  • Resolução de Entidades (Chave Composta: slug + UF + cargo)        │
 │  • Auto-Linking de Nomes (Regra Contextual com pontuação mínima 0.95)│
 │  • Validação Estrita de Contrato (Pydantic Models)                  │
 │  • DIFF Guard: se variação > 20% dos perfis, trava e alerta         │
 └──────────────────────────────────┬───────────────────────────────────┘
                                    │
                                    ▼
 ┌──────────────────────────────────────────────────────────────────────┐
 │ NÍVEL 3: PUBLICAÇÃO & BORDA (Git + Cloudflare Pages)                 │
 │  • Commita apenas JSONs finais compactos no repo (data/publico/)     │
 │  • Build do Astro gera páginas HTML estáticas ultra-rápidas          │
 │  • Cloudflare Worker gerencia o "Ao Vivo" em tempo real (cache 30s)  │
 └──────────────────────────────────────────────────────────────────────┘
```

---

## 2. As Complicações Reais e Como o Sistema as Resolve Sozinho

Abaixo estão todas as armadilhas que costumam exigir intervenção humana em projetos de dados públicos, e a solução arquitetural automatizada para cada uma.

### Complicação 1: APIs Oficiais Fora do Ar, Lentas ou Instáveis
* **Cenário:** O portal da Câmara fica instável no fim de semana, a API do Senado devolve 500, ou o DivulgaCand do TSE atinge limite de taxa.
* **Comportamento Autônomo:**
  - **Uso de Headers de Cache HTTP:** O coletor sempre envia `If-None-Match` (ETag) e `If-Modified-Since`. Se o dado não mudou, o servidor devolve `304 Not Modified` e nada é reprocessado.
  - **Circuit Breaker:** Se uma fonte retornar erro 5xx por mais de 3 tentativas, o coletor encerra a tarefa daquela fonte específica sem abortar as demais.
  - **Preservação de Snapshot:** O pipeline usa os dados da última execução bem-sucedida. O perfil continua no ar normalmente, apenas com a régua de fonte indicando: `FONTE · Câmara · coletado em 03/10/2026 (coleta automática pausada temporariamente)`.

### Complicação 2: Mudanças de Schema e Contrato nas APIs
* **Cenário:** A Câmara renomeia um campo de `siglaPartido` para `partidoSigla`, ou um endpoint é descontinuado (como ocorreu no Senado em 01/02/2026).
* **Comportamento Autônomo:**
  - **Validação com Pydantic v2:** Antes de gerar qualquer JSON público, o coletor valida a resposta contra o Schema.
  - **Diff Guard (Guarda de Discrepância):** Se um script gerar subitamente um JSON com campos nulos em mais de 10% dos políticos, ou se a contagem total de parlamentares cair de 513 para 0, o pipeline **rejeita o build**, aborta o commit e abre automaticamente uma **Issue no GitHub** com o log detalhado do erro.
  - O site em produção permanece 100% funcional servindo a versão anterior estável até você abrir a issue e ajustar a query.

### Complicação 3: Risco Jurídico e Notícias Caluniosas (Processos e Suspeitas)
* **Cenário:** Um robô raspa uma notícia acusando um político de um crime. Meses depois o inquérito é arquivado, ou a notícia original tratava de um homônimo não-parlamentar. O político notifica o site por calúnia/difamação.
* **Comportamento Autônomo:**
  - **Quarentena Hermética:** O módulo de "Processos e Investigações" **não roda por scraping genérico de notícias sem curadoria**. Ele só aceita entradas a partir de fontes primárias consolidadas (acórdãos do TCU, sanções da CGU, processos do TSE) ou arquivos YAML de casos verificados.
  - **Regra de Imputação Editorial Externa:** Toda menção de suspeita em notícias utiliza obrigatoriamente a sintaxe: `Segundo [Nome do Veículo], em [Data]: "[Título original]"` acompanhado do botão `Acessar matéria original ↗`. Isso estabelece perante a jurisprudência que o site é agregador/índice com atribuição, e não autor da imputação.
  - **Auto-Retratação:** Ao ler feeds RSS, o sistema monitora palavras-chave de desfecho (`arquivado`, `absolvido`, `rejeitada a denúncia`, `extinta a punibilidade`) ligadas a processos anteriores e gera alerta de atualização prioritária.
  - **Canal de Contestação Automatizado (`/corrigir`):** Qualquer cidadão ou assessoria pode enviar um formulário estruturado apontando erro com link comprobatório oficial. O sistema gera automaticamente uma branch de auditoria e avisa você via notificação.

### Complicação 4: Hiperlinks Errados por Homônimos (Auto-Linking em Notícias)
* **Cenário:** Uma notícia diz: *"O empresário Eduardo Pereira foi preso hoje em SP"*. O robô reconhece "Eduardo Pereira" e coloca um link para o perfil de um deputado federal homônimo de outro estado.
* **Comportamento Autônomo (Triangulação de Contexto Obrigatória):**
  - O algoritmo de vinculação exige uma **Pontuação de Confiança Mínima (Confidence Score >= 0.95)**:
    1. **Casamento de Nome:** Nome parlamentar oficial ou apelido registrado no TSE (ex: "Arthur Lira", "Gleisi Hoffmann").
    2. **Validador de Contexto no Parágrafo:** Para nomes comuns (ex: "Marcelo Santos", "Carlos Alberto"), o robô **só cria o link** se no mesmo parágrafo houver ao menos um token político de validação:
       `["deputad*", "senad*", "parlamentar", "ministr*", "líder", "bancada", "PL", "PT", "PP", "Congresso", "Câmara", "Senado", "STF", "Plenário"]`.
    3. Se o nome casar mas faltar o token de contexto, o texto **não recebe hyperlink** e é enviado silenciosamente para o log de auditoria. Falso negativo é infinitamente melhor que falso positivo.

### Complicação 5: Bloqueio de IP, Rate Limit e CAPTCHAs
* **Cenário:** O TSE ou o Portal da Transparência bloqueia o IP do runner do GitHub Actions por excesso de requisições.
* **Comportamento Autônomo:**
  - **Prioridade a CSVs Oficiais em Lote:** O pipeline não faz 640 requisições individuais ao TSE. Ele baixa **uma única vez** o arquivo CSV consolidado anual de candidaturas/bens, processa na memória com `DuckDB` em 3 segundos, e extrai todos os 640 políticos.
  - **Limitação de Ritmo no Cliente (Token Bucket):** Máximo de 2 requisições por segundo para a API da Câmara e Senado, com `User-Agent` honesto e identificado (`PracaBot/1.0 (+https://seu-dominio.com.br/bot)`), o que previne banimentos por heurística de tráfego malicioso.
  - **Espelhamento de Dados:** Dados imutáveis (histórico eleitoral 2014-2024, patrimônio declarado) são processados uma única vez e armazenados como artefatos Parquet fixos; o cron diário só busca os dados do dia corrente.

### Complicação 6: Transições Eleitorais e Dança de Cadeiras (Fevereiro de 2027)
* **Cenário:** Em 01/01 e 01/02/2027 tomam posse novos governadores e parlamentares; dezenas de suplentes assumem e deputados viram ministros.
* **Comportamento Autônomo:**
  - O modelo de dados trabalha com uma **Máquina de Estados de Mandato**:
    - `ativo`: parlamentar em exercício.
    - `eleito_aguardando_posse`: eleito no pleito de 2026 antes da data oficial de posse.
    - `licenciado`: assumiu ministério ou secretaria estadual (o perfil aponta para o cargo do executivo).
    - `suplente_em_exercicio`: indica quem está cobrindo a cadeira e a quem pertence o mandato titular.
    - `encerrado`: mandato passado arquivado na aba carreira.
  - A virada de status ocorre **automaticamente baseada no relógio do sistema (data ISO)** combinada com o endpoint diário de ocupantes de cargo da Câmara e Senado. Nenhum layout precisa ser redesenhado.

### Complicação 7: Detecção de "Ao Vivo" sem Intervenção Humana
* **Cenário:** As transmissões da TV Câmara, TV Senado e STF começam e terminam em horários imprevisíveis.
* **Comportamento Autônomo:**
  - Um microsserviço leve no **Cloudflare Worker** roda a cada 60 segundos na borda.
  - Ele consulta a YouTube Data API (ou endpoint público de streaming das emissoras legislativas) buscando eventos com status `liveBroadcastContent: "live"`.
  - Cache curto de 30 a 60 segundos com `stale-while-revalidate`.
  - Se houver sessão ativa, a Praça 2D acende o marcador pulsante vermelho `AO VIVO` e conecta o player `youtube-nocookie`.
  - Quando a sessão encerra, o marcador apaga imediatamente e a página exibe a gravação da íntegra ou a pauta do dia seguinte, sem nenhuma ação manual.

---

## 3. Matriz de Automação e Agendamentos (Cron Matrix)

Para não sobrecarregar recursos nem gerar custos de computação, as tarefas são divididas por frequência biológica do dado:

| Rotina | Frequência | Mecanismo | O que faz | Volume / Tempo |
| :--- | :--- | :--- | :--- | :--- |
| **Radar Ao Vivo** | A cada 60 seg | Cloudflare Worker | Checa se há transmissão ao vivo no Congresso/STF e atualiza estado. | ~50 ms (Borda) |
| **Radar de Notícias** | A cada 20 min | GitHub Actions (Fast Cron) | Lê feeds RSS oficiais e de imprensa, aplica desambiguação de nomes e atualiza `noticias.json`. | ~15 seg |
| **Radar Legislativo** | 2x ao dia (13h e 21h) | GitHub Actions | Coleta pautas, presenças e votações nominais do dia na Câmara e Senado. | ~45 seg |
| **Radar Executivo & Diário** | 1x ao dia (06h) | GitHub Actions | Lê atos de nomeação e exoneração no Diário Oficial da União (DOU). | ~30 seg |
| **Auditoria e Recompilação** | 1x ao dia (madrugada) | GitHub Actions | Executa o build estático completo do Astro, roda testes de schema e atualiza os índices de busca do Pagefind. | ~2 min |
| **Censo Eleitoral & Finanças** | Semanal / Mensal | GitHub Actions (Lote) | Baixa atualizações do TSE, emendas parlamentares na CGU e cota parlamentar. | ~3 min |

---

## 4. O Sistema Imunológico: Testes e Guardiões Automáticos

Para garantir que você só receba notificações quando for estritamente indispensável, o pipeline possui quatro travas automáticas:

1. **Schema Guardian:** Toda carga passa por modelos estritos Pydantic v2. Se faltar um campo obrigatório, o dado é rejeitado antes de entrar no repositório.
2. **Anomaly & Diff Guard:**
   ```python
   # Regra incorporada no compilador de saída:
   if abs(novo_total_politicos - 640) > 15:
       abortar_publicacao(f"Alerta: Coleta retornou {novo_total_politicos} políticos. Esperado ~640. Abortando deploy.")
   ```
3. **Dead-Link Hunter:** Robô semanal testa links de fontes e matérias. Links quebrados são marcados com aviso `[Link arquivado via Wayback Machine]` sem quebrar a interface.
4. **Alerta Limpo via GitHub Issues:** Quando um circuit breaker estoura 3 vezes, o próprio robô cria uma Issue etiquetada `bug:fonte-quebrada` contendo o payload do erro e o endpoint exato. Nenhuma caixa de e-mail é lotada com spam.

---

## 5. Como Implementar Isso sem Custos de Servidor (100% Free-Tier)

Toda essa infraestrutura autônoma roda inteiramente dentro dos limites gratuitos de serviços modernos de alto nível:

* **GitHub Actions:** 2.000 minutos/mês gratuitos para repositórios públicos (nossos crons somam menos de 300 min/mês).
* **Cloudflare Pages:** Hospedagem estática com largura de banda ilimitada, proteção DDoS e certificado SSL automatizado.
* **Cloudflare Workers:** 100.000 requisições diárias gratuitas (o cache de 30s na borda absorve 99% das chamadas do "ao vivo").
* **DuckDB + Parquet:** Processamento de dados colunar na memória do runner, sem necessidade de banco de dados SQL ou servidor PostgreSQL dedicado.
