---
name: jade-frontend
description: Implementar e revisar front-end React, Next.js e TypeScript preservando componentes, contratos, segurança e testes. Usar para alterações de código, UI, Figma, formulários, estado e diagnóstico no fluxo da Jade.
---

# Engenharia front-end

Ler [engineering.md](references/engineering.md) por seção conforme o impacto. Essa referência preserva as regras originais da Jade. Não aplicar a rotina visual quando não houver UI afetada.

## Roteamento

| Impacto | Seções da referência | Skills comunitárias complementares, se instaladas |
| --- | --- | --- |
| Qualquer implementação | Entender repo, negócio, fatias, implementar, validar e revisar | domain-modeling, typescript-quality, code-review-and-quality, verification-before-completion |
| UI | Reconhecer UI, reuse-first, contrato visual e grade de 8 pontos | ui-recon, spacing-system, frontend-design, web-design-guidelines |
| Figma | Fluxo Figma → código, assets e comparação renderizada | figma-design-to-code |
| React/Next | Implementação, SSR/RSC e performance | vercel-react-best-practices, vercel-composition-patterns |
| API | Analisar back-end e limites de dados | api-and-interface-design |
| Testes | Testar comportamento e validar projeto | javascript-testing-patterns, webapp-testing |
| Segurança | Revisão proporcional ao risco; completa em auth, dados ou fronteiras críticas | owasp-security-check |
| Bug | Diagnóstico e regressão | systematic-debugging |
| E2E | Somente quando ferramenta existente ou escopo justificar | playwright-best-practices |
| Estado/formulário | Somente com bibliotecas existentes | state-management (TanStack Query v5/Zustand v5), react-hook-form |
| TDD | Somente pedido explícito ou fronteira acordada | tdd |

Carregar apenas as skills pertinentes. As instruções próprias da referência continuam válidas na instalação `--core-only`; se uma skill complementar não estiver instalada, informar essa ausência quando relevante sem alegar sua execução.

## Regras centrais

- Investigar e compor componentes existentes. Preservar tokens, fontes e APIs públicas.
- UI exige grade de 8 pontos; 4 px somente microespaçamento justificado, 1–2 px borda/divisor/correção óptica. Acessibilidade tem prioridade. Conflito com Figma/token deve ser identificado e resolvido no menor escopo, sem refatoração ampla.
- Ler design context do node antes de implementar Figma. Descobrir o schema real da ferramenta; usar `skillNames` somente se aceito pelo schema exposto. Não enviar parâmetros presumidos. Sem contexto necessário, bloquear somente a implementação visual dependente.
- Não inventar contratos; comparar código back-end e disponibilidade no ambiente com `jade-delivery`.
- Testar comportamento no runner existente e executar verificações proporcionais ao risco. Não criar teste de baixo valor apenas para marcar checklist, nem instalar ferramentas sem escopo.
- Revisar segurança nas fronteiras alteradas. Autorização real pertence ao servidor. Não expor segredos nem ampliar testes ativos a produção sem autorização.
- Corrigir falhas introduzidas e apresentar evidências pelo `frontend-quality-gate`.
