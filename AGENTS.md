# Instruções para agentes

## Ao finalizar qualquer tarefa

1. Leia `PROGRESSO.md` antes de editar.
2. Atualize a seção 1 de `PROGRESSO.md` e acrescente uma entrada na seção 5.
3. Marque no `PLANO.md` somente itens verificados.
4. Rode a menor validação relevante e registre o resultado.

## Regras do projeto

- Todo dado público precisa de fonte, URL, data de coleta e licença.
- Não inferir ideologia: usar apenas autodeclaração datada, histórico de votos ou metodologia publicada.
- Notícias de terceiros exibem título, veículo, data, trecho curto e link; não copiar matéria sem licença.
- Seções sensíveis ficam desligadas até revisão jurídica.
- Preserve a direção visual `Tinta & Papel` e o comportamento responsivo.

## Convenções

- Python: `ruff`, `pytest`, modelos em `pipeline/src/praca_pipeline/modelos`.
- IDs públicos são estáveis; slugs são minúsculos, ASCII e desambiguados por UF/cargo/ano.
- JSON público usa UTF-8, indentação de dois espaços e datas ISO 8601.
