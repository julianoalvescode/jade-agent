# Conectar as ferramentas

A Jade usa ferramentas já autenticadas no cliente. O pacote não inclui credenciais e não conecta contas automaticamente. Reutilizar os conectores existentes evita configurações duplicadas.

## Jira e Confluence no Claude Code

Se Atlassian ainda não estiver configurado, adicionar o servidor oficial:

```bash
claude mcp add --transport http atlassian https://mcp.atlassian.com/v2/mcp
```

Abrir `/mcp` no Claude Code e concluir a autenticação. A disponibilidade de operações depende da conta, do site e das políticas da organização. A Jade deve verificar as ferramentas expostas e ler o ticket/página antes de alegar acesso.

## GitHub

Usar o conector/MCP já autenticado ou GitHub CLI (`gh`) autenticado. A alternativa em `.mcp.example.json` usa o servidor remoto oficial e a variável `JADE_GITHUB_PAT`; disponibilizar o segredo pelo mecanismo seguro do ambiente, nunca dentro do arquivo versionado ou de um prompt.

Se optar pelo exemplo, mesclar somente a entrada necessária na configuração existente e verificar a conexão em `/mcp`. O instalador grava `.mcp.jade.example.json` e não substitui `.mcp.json`.

## Repositório back-end e Figma

Informar o repo/caminho autorizado do back-end em `jade.project.json` ou no pedido. Se estiver fora do diretório permitido pelo cliente, conceder acesso pelo mecanismo do próprio cliente. A Jade não contorna a restrição.

Para Figma, reutilizar o MCP oficial já conectado e fornecer URL com node-id. A
ferramenta precisa expor o contexto de design necessário; os parâmetros devem
seguir o schema realmente disponível. Se o servidor ainda não estiver conectado,
adicioná-lo (a entrada `figma` também consta em `.mcp.example.json`):

```bash
claude mcp add --transport http figma https://mcp.figma.com/mcp
```

Abrir `/mcp` e concluir a autenticação OAuth. Enquanto `get_design_context` não
estiver exposto e autenticado, a `jade-figma-to-code` registra `BLOCKED` na etapa
visual e não recria a tela de memória.

## Configuração de projeto

Copiar `jade.project.example.json` para `jade.project.json` e preencher apenas os campos conhecidos. Campos vazios significam desconhecido; não são contratos ou endpoints fictícios. Não preencher tokens, cookies, senhas ou payloads de cliente.

As URLs identificam recursos; não autorizam escrita nem tornam disponível uma API ainda não implantada. Em cada tarefa, verificar commit consultado e evidência de ambiente.

## Fontes oficiais consultadas

- https://code.claude.com/docs/en/mcp
- https://code.claude.com/docs/en/sub-agents#preload-skills-into-subagents
- https://support.atlassian.com/atlassian-ai-gateway/docs/get-started-with-the-atlassian-remote-mcp-server/
