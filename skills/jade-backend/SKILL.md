---
name: jade-backend
description: Implementar e revisar back-end (APIs REST/GraphQL, serviços, dados, filas e jobs) com foco em qualidade, escalabilidade, segurança e performance. Usar quando a tarefa incluir no escopo endpoint, controller, service, repositório, migração, schema, job, fila, cache ou integração servidor a servidor. NÃO usar só para consumir API no front-end; nesse caso usar jade-backend-contract.
---

# Engenharia back-end

Ler [engineering.md](references/engineering.md) por seção conforme o impacto. Detectar a stack real (Java/Spring Boot, Node com Express/NestJS/Fastify, Python, Go, .NET etc.), seus padrões de camadas, ORM, migrações, testes e lint. **O padrão existente do projeto vence a preferência da agente.**

## Quando usar

- O pedido inclui alterar ou criar código de servidor, banco, fila, job ou integração.
- A tarefa full-stack exige mudar os dois lados de um contrato.

Se o back-end não estiver no escopo autorizado, não alterar: usar `jade-backend-contract` para verificar o contrato e registrar a dependência.

## Roteamento

| Impacto | Seções da referência | Skills comunitárias complementares, se instaladas |
| --- | --- | --- |
| Qualquer mudança | 1 repositório, 2 domínio, 9 testes, 10 validação, 11 revisão | domain-modeling, code-review-and-quality, verification-before-completion |
| API/contrato | 3 design de API e compatibilidade | api-and-interface-design, contract-first |
| Dados | 4 modelagem, migração e transações | — |
| Escalabilidade | 5 concorrência, idempotência, filas e cache | — |
| Segurança | 6 OWASP API Top 10 e segredos | owasp-security-check |
| Performance | 7 medição, consultas e orçamento | — |
| Operação | 8 observabilidade e resiliência | — |
| Bug | Diagnóstico com causa raiz provada | systematic-debugging |
| TDD | Somente pedido explícito ou fronteira acordada | tdd |

Carregar só as skills pertinentes. Sem a skill complementar instalada, seguir a referência própria e informar a ausência quando relevante.

## Regras centrais

- Contrato primeiro: mudar API pública somente com compatibilidade retroativa ou versão nova acordada. Atualizar OpenAPI/schema e tipos do front no mesmo escopo.
- Validar toda entrada na fronteira, autorizar no servidor por recurso (anti-IDOR/BOLA) e nunca confiar em dado do cliente.
- Consultas parametrizadas, sem N+1, com índice e paginação em listas. Medir antes de otimizar.
- Migração reversível, compatível com a versão anterior em execução e nunca aplicada em ambiente compartilhado sem autorização.
- Operações repetíveis devem ser idempotentes; chamadas externas com timeout, retry com backoff e limite.
- Logs estruturados sem segredo nem PII; erros sem stack trace para o cliente.
- Não alterar infraestrutura, permissões, banco compartilhado ou deploy sem pedido explícito.
- Testar comportamento (unitário + integração na fronteira real) e apresentar evidências pelo `frontend-quality-gate`.
