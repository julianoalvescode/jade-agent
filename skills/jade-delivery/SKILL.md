---
name: jade-delivery
description: Conduzir tarefas de front-end ligadas a Jira, Confluence, GitHub e repositórios back-end. Usar para reunir requisitos, verificar contratos entre repos, preparar PR, acompanhar CI ou atualizar registros autorizados sem duplicação.
---

# Entrega integrada

## 1. Estabelecer acesso e escopo

Descobrir as ferramentas realmente expostas. Não presumir nomes, schemas, autenticação ou conexão por existir um arquivo de configuração. Preferir conectores/MCP autenticados; para GitHub, usar `gh` autenticado se disponível. Usar Git local para inspecionar os repos autorizados. Registrar bloqueio apenas nas etapas dependentes e avançar no trabalho independente.

Identificar se o pedido é revisão, execução, preparação de PR ou publicação/merge. Reutilizar autorizações explícitas da sessão; não interpretar uma leitura de ticket como autorização para mudar status ou enviar mensagens.

## 2. Montar contexto mínimo

- Jira: ler descrição, critérios, comentários relevantes, QA, dependências e links; confirmar qual ticket é o alvo.
- Confluence: ler páginas vinculadas e pesquisar pelo domínio apenas quando necessário; registrar versão/data, fonte e trecho relevante.
- Front-end: mapear fluxo, componentes, client, testes e convenções de PR.
- Back-end: seguir [backend-contracts.md](references/backend-contracts.md).
- GitHub: localizar PRs relacionados, base/head, reviews e checks pertinentes.

Usar [delivery-record.md](references/delivery-record.md) como estrutura compacta. Registrar fontes verificáveis e divergências. Resolver diferenças por decisão explícita de produto/engenharia, sem assumir que o documento mais recente ou o código sempre vence. Fazer uma pergunta objetiva apenas quando a divergência bloquear uma escolha material.

## 3. Implementar e validar

Relacionar cada critério ao fluxo afetado, à implementação e à evidência. Manter dependência de API separada de mock autorizado. Carregar `jade-frontend` e `frontend-quality-gate` conforme o escopo. Nunca marcar um critério funcional como aprovado apenas porque lint ou build passou.

## 4. Preparar ou publicar

Seguir [external-updates.md](references/external-updates.md) para branch, PR, Jira e Confluence. Antes de escrita autorizada, reler o registro e verificar se o resultado já existe. Se houver timeout, consultar o estado antes de repetir a operação.

Preparar o conteúdo e as evidências antes de solicitar qualquer autorização realmente ausente. Não exigir confirmação duplicada. Atualizar apenas a parte afetada e preservar contribuições alheias.

## 5. Retomar e concluir

Reconsultar branch/head do PR, status do ticket, versão da página e execução de CI relacionada. Invalidar evidências afetadas por novos commits ou mudanças de requisito. Não confundir `implementado`, `validado`, `PR aberto`, `mergeado` e `publicado`; confirmar cada estado na sua fonte.

Se solicitado checkpoint local, guardar somente fontes, decisões, refs e próximas ações, sem payloads sensíveis; revalidar dados mutáveis ao retomar. Entregar ações realizadas, propostas e bloqueadas em categorias distintas.
