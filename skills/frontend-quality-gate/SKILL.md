---
name: frontend-quality-gate
description: Verificar requisitos e prontidão de alterações front-end com evidências de código, contrato, UI, testes e CI. Usar para revisão, preparação de PR, regressão e conclusão de tarefas da Jade.
---

# Quality gate de front-end

Escolher revisão (leitura), execução (mudanças autorizadas) ou preparação/publicação de PR conforme o pedido. Ler ticket e documentos disponíveis, diff e instruções do repo. Não assumir acesso a sistemas externos.

## Estados

- `PASS`: executado ou inspecionado com evidência concreta correspondente ao critério.
- `FAIL`: verificação executada e requisito violado.
- `BLOCKED`: acesso, ambiente, dados ou decisão impede verificação necessária.
- `NOT RUN`: verificação relevante não executada; explicar motivo e risco.
- `N/A`: mudança não afeta a verificação; justificar.

Nunca inferir PASS de ausência de erro. Build não substitui teste funcional. Mock não comprova integração real. Evidência de outro commit não comprova o diff atual.

## Verificações por impacto

| Área | Evidência adequada |
| --- | --- |
| Requisito | Critério ligado ao comportamento, arquivo e teste/inspeção |
| Contrato | Schema/código e SHA; payload, erro, auth e ambiente |
| UI | Componentes/tokens, grade, estados, responsividade e comparação renderizada |
| Acessibilidade | Teclado, foco, semântica, labels e contraste pertinentes |
| Testes e código | Comandos reais, saída/exit code e casos afetados |
| Segurança | Fluxo de dados e controles nas fronteiras alteradas |
| Performance | Evidência proporcional ao caminho alterado; sem métricas inventadas |
| CI e entrega | Execução no commit correto, checks/reviews exigidos, conflitos e estado real |
| Documentação | Decisão ou comportamento alterado refletido quando autorizado |

Começar por inspeção e testes focados; ampliar conforme risco e gates reais do repo. Não alterar dependências/lockfiles/configuração só para obter verde. Distinguir falha introduzida, preexistente demonstrada e origem desconhecida.

Após editar código ou receber novo commit, reexecutar verificações afetadas. Para UI, não apresentar inspeção estática como validação em navegador.

## Resultado

Usar `READY` somente quando critérios/gates necessários estiverem satisfeitos; `READY WITH CAVEATS` para limitações residuais não bloqueantes explicadas; `NOT READY` quando critério/gate necessário falhar ou estiver bloqueado/não validado. Verificação opcional não executada não bloqueia automaticamente uma mudança de baixo risco.

Entregar achados por severidade, localização, impacto e correção, seguidos de matriz `critério → implementação → evidência → estado`. Informar comandos, limitações, QA restante e ações externas realizadas/propostas. Não confundir readiness técnico com autorização de merge ou publicação.
