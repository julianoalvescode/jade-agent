# Contratos entre repositórios

Consultar `jade.project.json`, instruções do projeto e links da tarefa para localizar o back-end. Se o caminho/repositório estiver ausente, pesquisar somente no escopo autorizado; pedir o identificador quando não houver correspondência inequívoca.

1. Registrar URL/caminho do repo, branch e commit efetivamente consultado. Não trocar branches ou alterar o checkout do usuário para investigar; preferir leitura via Git ou checkout isolado autorizado.
2. Localizar OpenAPI/GraphQL/schema, rotas, DTOs, controllers, autorização e testes relevantes. Conferir se contrato publicado e implementação divergem.
3. Mapear método/path, autenticação, permissões, entrada, saída, nulabilidade, enum, erro, data/moeda/timezone, paginação, filtros, cache, retry e cancelamento conforme a mudança.
4. Identificar client, hook, query ou server action do front-end. Reutilizar geração de tipos existente; não introduzir casts ou dados fictícios para esconder incompatibilidade.
5. Distinguir existência no código de disponibilidade em ambiente. Consultar evidência de deploy/versão e testes no ambiente permitido. Endpoint respondendo não prova sozinho que o commit esperado foi implantado.
6. Quando a versão implantada for desconhecida, registrar `versão implantada não confirmada`. Não declarar integração real aprovada sem verificação correspondente.
7. API ausente ou incompatível: indicar critério afetado, contrato necessário, dependência e ticket/PR quando conhecido. Não inventar responsável. Implementar mock ou fallback somente se fizer parte do escopo/requisito; identificá-lo como tal.

| API | Contrato/commit | Ambiente/versão | Verificação | Dependência |
| --- | --- | --- | --- | --- |
| Preencher com fonte real | Arquivo ou schema e SHA | Confirmado ou desconhecido | Evidência e estado | Ticket/PR conhecido ou não identificado |

Revalidar informação mutável a cada retomada. Testes ativos somente em ambiente local ou explicitamente autorizado, sem efeitos de negócio indesejados.
