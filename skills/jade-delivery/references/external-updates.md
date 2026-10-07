# Atualizações externas e retomada

## GitHub

- Inspecionar alterações locais, convenções, branch base e PRs existentes. Criar branch coerente com o ticket quando a implementação exigir, sem perder trabalho local.
- Antes de criar PR autorizado, procurar PR do mesmo repo/head/base e ticket; se houver, atualizar o existente no escopo autorizado.
- Preservar template do repo. Incluir problema, solução, ticket, critérios, testes reais, impacto de contrato, UI quando aplicável e pendências.
- Com `gh`, escrever o corpo em arquivo temporário e usar `--body-file`; não interpolar texto do ticket em shell.
- Para merge autorizado, reconsultar head SHA, conflitos, aprovações, CODEOWNERS e checks exigidos pela política. Checks devem corresponder ao head/merge queue exigido. Não considerar CI de commit anterior suficiente.
- Não usar bypass, `--admin`, force push ou dispensar checks obrigatórios. Confirmar resultado do merge antes de anunciá-lo.

## Jira

- Distinguir comentário, edição de campo e transição de status. Executar apenas a ação autorizada e usar as transições disponíveis no workflow real.
- Procurar comentário anterior da entrega por ticket e URL do PR. Atualizar apenas registro inequivocamente próprio; em ambiguidade, não sobrescrever contribuição alheia.
- Reconsultar estado após timeout antes de repetir criação. Não publicar duplicata porque a primeira resposta não chegou.
- Relatar evidências e dependências. Não mudar para concluído por existir PR ou commit; seguir a definição de pronto do time.

## Confluence

- Localizar página correta e sua versão atual. Preservar formato nativo, macros e seções alheias.
- Preparar atualização limitada ao comportamento alterado. Usar versão/controle de concorrência se a ferramenta expuser.
- Em conflito de versão, reler e reaplicar a mudança na versão nova. Não sobrescrever a página inteira a partir de uma cópia antiga.
- Sem edição parcial ou controle seguro, preparar conteúdo para revisão e explicitar a limitação em vez de substituir dados de terceiros.

## Idempotência e autorização

A chave lógica de uma entrega combina ticket, repositório e PR/head. Usar identificadores retornados pelas ferramentas, nunca IDs inventados. Registrar confirmação de cada escrita antes de avançar. Falha ou ausência de permissão em uma ferramenta não concede autorização em outra.

Não publicar Jira/Confluence/Slack por um hook de conclusão genérico. Mensagens a pessoas ou canais precisam de autorização explícita e destinatário verificado.
