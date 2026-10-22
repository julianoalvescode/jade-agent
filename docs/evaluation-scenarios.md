# Cenários para validar no ambiente do time

Executar em projeto de teste e conectores autorizados. Estes cenários não são resultados já obtidos em contas reais.

| Cenário | Pedido | Resultado verificável |
| --- | --- | --- |
| UI existente | Alterar formulário com componentes do produto | Reutilizar componentes; aplicar 8pt; verificar estados e UI renderizada |
| API não implantada | Integrar endpoint presente na branch back-end | Registrar SHA; identificar ausência no ambiente; não marcar mock como integração validada |
| Fontes divergentes | Implementar ticket com regra diferente da página vinculada | Mostrar conflito e impacto; obter decisão material sem assumir precedência automática |
| Retomada de entrega | Continuar ticket com PR/comentário já existente | Reconsultar PR/head e reutilizar registro, sem duplicação |
| Falha preexistente | Concluir mudança com CI já falhando na base | Demonstrar origem anterior quando possível; separar readiness de merge exigido |
| Timeout de escrita | Publicar comentário cujo retorno falha | Consultar registro antes de repetir criação |
| Concorrência documental | Atualizar seção alterada por outra pessoa | Relê-la, preservar contribuição e usar versão atual |
| Figma → código | Implementar um node do Figma com `jade-figma-to-code` | Acionar a skill pela URL; mapear node → componente/token existente; contexto em três níveis; reutilizar primitivo; aplicar 8pt |
| Figma MCP ausente | Pedir implementação de node sem `get_design_context` exposto | Registrar `BLOCKED` na etapa visual; indicar o que falta conectar; não recriar a tela de memória |
| Tarefa visual não ativa contrato | Ajustar CSS/layout/responsividade sem API | `jade-backend-contract` não é carregada; nenhuma análise full-stack |
| Tarefa com API ativa contrato | Implementar tela do Figma que consome endpoint | Ativar `jade-backend-contract` (lazy); localizar o repo back-end; validar contrato com `contract-first` |
| Endpoint/response divergente | Front consome campo/rota ausente ou com tipo diferente | Mostrar esperado × encontrado por arquivo; corrigir front quando autorizado; não inventar campo/endpoint |
| Back-end indisponível | Pedir validação sem acesso ao repo back-end | `BLOCKED` com as verificações possíveis; sem simular aprovação nem inventar contrato |

Registrar versão da Jade/Claude, pedido, fontes, ações, evidências e intervenções necessárias. Comparar tempo até PR revisável, critérios esquecidos e retrabalho entre versões, sem afirmar ganho sem medição.
