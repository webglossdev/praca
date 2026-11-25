# Documento jurídico operacional do Praça

> Este documento é uma especificação técnica e editorial. Não substitui parecer jurídico humano. A publicação de processos, suspeitas e ligações permanece desligada até aprovação formal.

## Status de bloqueio

`SECOES_SENSIVEIS_ATIVAS` permanece `false`.

Não ativar seções sensíveis sem:

- assinatura de responsável jurídico;
- revisão humana de fonte e desfecho;
- aprovação editorial por duas pessoas;
- teste de contestação e correção;
- registro público da revisão.

## Bases legais e objetivos

### LAI

A coleta usa dados públicos para transparência ativa, com fonte, URL, data ISO 8601 e licença.

- não criar canal próprio para pedidos que devem seguir os canais oficiais da LAI;
- distinguir dado primário, dado compilado, interpretação e atribuição jornalística;
- não inferir campo ausente;
- manter histórico de correções.

### LGPD

Dados manifestamente públicos de agentes políticos podem ser tratados para finalidade cívico-informacional clara.

- preferir atividade legítima de interesse público, base manifestamente pública, obrigação legal ou defesa de direitos;
- não usar consentimento como base padrão;
- minimizar dados, informar finalidade e retenção;
- oferecer correção, atualização e contestação;
- mascarar CPF no QSA e rejeitar números completos;
- não enviar dados sensíveis em issues públicas.

Regra técnica de CPF:

- aceitar somente o formato já mascarado pela fonte;
- remover ou mascarar sequências de 11 dígitos antes de JSON, logs, issues e exports;
- rejeitar arquivos com padrão completo de CPF;
- não tentar recuperar CPF por inferência.

### Direitos autorais

- notícias de imprensa: título, veículo, data, trecho curto e link;
- limite técnico atual: 500 caracteres;
- texto integral somente com licença aberta documentada;
- verificar a licença da Agência Brasil, Câmara, Senado, STF e TSE caso a caso;
- não declarar ODbL ou CC global sem inventário compatível;
- manter AGPL-3.0-or-later para o código e licenças separadas por dados e imagens.

### Marco Civil da Internet

- atribuir toda imputação a veículo e data;
- registrar reclamação, correção ou indisponibilidade;
- não transformar notícia em acusação factual;
- preservar desfechos e direito de resposta.

### Neutralidade eleitoral

Durante períodos eleitorais:

- não publicar opinião partidária ou ranking persuasivo;
- não segmentar ou recomendar conteúdo político;
- não receber apoio de candidato;
- não alterar metodologia a meio do ciclo;
- não inferir ideologia;
- identificar candidatos, diplomados, eleitos e empossados;
- pesquisar só com registro TSE, margem e metodologia compatíveis.

## Critérios editoriais

### Pode entrar

- ato ou processo oficial confirmado;
- desfecho oficial atualizado;
- informação diretamente ligada à atuação pública;
- atribuição claramente nominal a veículo;
- histórico factual de mandato e status.

### Não entra

- vida privada sem relevância pública;
- boato ou acusação sem fonte;
- conteúdo familiar, médico ou sexual;
- CPF completo;
- endereço privado;
- inferência de culpa;
- rótulo ideológico inferido;
- conexão empresarial não confirmada.

Regras processuais:

- distinguir denúncia, investigação, acusação formal, sentença e desfecho;
- não inferir culpa;
- dar prioridade a absolvição, arquivamento, prescrição e retratação.

## Fluxo YAML de casos

Arquivo por caso:

```text
data/publico/atribuicoes/{pid}/{caso-id}.yaml
```

Modelo mínimo:

```yaml
id: caso-2026-001
pid: pid_exemplo
titulo: "Texto factual atribuído à imprensa"
status: investigacao
desfecho: null
publicavel: false
fontes:
  - veiculo: "Nome do veículo"
    titulo_original: "Título original"
    url: "https://www.exemplo.org/materia"
    publicado_em: "2026-11-24"
    licenca_trecho: "rss-link"
    trecho: "Até 500 caracteres"
historico:
  - em: "2026-11-24"
    status: investigacao
    base: "Fonte primária"
revisores:
  - id: revisor-editorial
    resultado: pendente
  - id: revisor-juridico
    resultado: pendente
updated_at: "2026-11-24T05:33:09-03:00"
motivo: "Relevância pública objetiva"
```

Estados:

`fato_publico`, `investigacao`, `acusacao_formal`, `sentenca`, `arquivado`, `prescrito`, `absolvido`, `retratado`, `extinto`.

Fluxo:

1. curadoria do caso;
2. confirmação da fonte por segundo revisor;
3. revisão jurídica;
4. validação Pydantic/YAML;
5. publicação somente com feature flag ativada;
6. atualização automática ou humana de desfecho.

## Direito de resposta e contestação

SLA público recomendado:

- confirmação automática: até 1 hora;
- triagem humana: até 2 dias úteis;
- correção simples comprovada: até 5 dias úteis;
- contestação complexa ou sensível: até 10 dias úteis;
- resposta técnica complexa: até 15 dias úteis;
- prazo máximo sem revisão especial: 30 dias corridos.

Correções urgentes devem ser sinalizadas em até 24 horas. Suspender o conteúdo afetado quando houver risco jurídico.

## Termos e licenças por fonte

Antes de cada publicação, registrar:

- fonte;
- URL oficial;
- termos vigentes;
- licença;
- coleta permitida;
- republicação permitida;
- crédito;
- imagens;
- frequência;
- responsável pela revisão;
- data da revisão.

Os itens externos permanecem pendentes até verificação humana das versões vigentes.

## Fotos e biografias

Não publicar foto sem licença ou atribuição registrada.

Verificar separadamente Câmara, Senado, TSE, Wikimedia Commons, DHBB/FGV e arquivos institucionais.

## Licença da base compilada

Não declarar ODbL ou CC por padrão. A licença final depende de um inventário compatível de todas as fontes.

O código continua sob AGPL-3.0-or-later. Dados compilados, fotos, textos institucionais e trechos jornalísticos devem receber licenças separadas e explícitas.

## Piloto com casos sensíveis

Somente após aprovação jurídica:

- usar poucos casos já confirmados;
- exigir fonte primária;
- mostrar desfecho;
- registrar revisores;
- testar correção e rollback;
- testar leitura por celular e tecnologia assistiva;
- não publicar em exports sem revisão.
