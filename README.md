# Jade — pacote final 2.0.0

Agente para Claude Code com fluxo de front-end integrado a Jira, Confluence, GitHub, Figma e repositórios back-end. Inclui quatro skills próprias e instalador para as 20 skills comunitárias, com fontes fixadas por commit.

## Instalar no seu projeto

Requisitos: Python 3.10 ou superior e Git. A instalação completa precisa de rede para baixar os commits do manifesto. Node/npm não são necessários para instalar a Jade; projetos consumidores continuam usando seus próprios requisitos.

Extraia este pacote e execute, apontando para a pasta do projeto em que usará a Jade:

```bash
bash /caminho/jade-agent/scripts/install-skills.sh claude-code --project /caminho/meu-projeto
```

Para atualizar uma instalação existente, após revisar os arquivos que serão substituídos:

```bash
bash /caminho/jade-agent/scripts/install-skills.sh claude-code --project /caminho/meu-projeto --replace
```

Arquivos diferentes são preservados por padrão: o instalador informa o conflito antes de escrever. `--replace` cria backups em `.jade/backups/`. O instalador não altera `CLAUDE.md`, `AGENTS.md`, `.mcp.json` ou os arquivos de configuração pessoal existentes. A recuperação automática cobre falhas normais de escrita; um encerramento abrupto do sistema pode exigir restauração a partir do backup.

Para instalar somente as quatro skills próprias sem rede:

```bash
bash /caminho/jade-agent/scripts/install-skills.sh claude-code --project /caminho/meu-projeto --core-only
```

O modo `--core-only` contém o fluxo completo e as regras próprias de engenharia; as 20 skills comunitárias complementares não são instaladas. Não se deve alegar que uma skill ausente foi executada.

## Configurar e usar

1. Na pasta do projeto, copie `jade.project.example.json` para `jade.project.json` e informe os repos, documentos e ambientes conhecidos. O preenchimento não é obrigatório quando essas informações já estão no pedido ou nas instruções do projeto.
2. Reutilize os conectores autenticados de Jira/Confluence, GitHub e Figma. Consulte [docs/connectors.md](docs/connectors.md) para a configuração inicial. O exemplo de MCP não contém credenciais e não é ativado automaticamente.
3. Abra uma nova sessão do Claude no projeto e peça:

> Use a agente Jade para implementar o ticket PROJ-123. Leia os documentos vinculados, confira o contrato no repositório back-end e valide os critérios de aceite. Prepare o PR com as evidências.

Para autorizar também a publicação, inclua as ações desejadas no pedido, por exemplo: “Crie o PR e publique no ticket um comentário com o link e os resultados”. Merge, transições de Jira e documentação seguem o escopo autorizado e as políticas reais do time.

## O que foi incorporado

| Recurso | Implementação |
| --- | --- |
| Coordenação da Jade | `skills/jade-workflow/SKILL.md` |
| Jira, Confluence e GitHub | `skills/jade-delivery/SKILL.md` e referências |
| Contrato e ambiente back-end | Referência `backend-contracts.md` |
| UI, Figma, 8pt e engenharia | `skills/jade-frontend/SKILL.md` e referência completa |
| Evidências e prontidão | `skills/frontend-quality-gate/SKILL.md` |
| Instalação reproduzível | `scripts/install.py` + `skills-lock.json` |
| Instruções portáveis | Geradas pelo núcleo, verificadas no CI |
| Validação do pacote | `scripts/validate.py`, `tests/` e GitHub Actions |

Apenas `jade-workflow` é pré-carregada no agente. As demais skills são carregadas conforme a tarefa. UI mantém sua grade de 8 pontos, reutilização de componentes e validação visual. Contratos são verificados no código e distinguidos da disponibilidade no ambiente.

Cada entrega relaciona critério, implementação, evidência e estado: `PASS`, `FAIL`, `BLOCKED`, `NOT RUN` ou `N/A`. A Jade distingue código implementado, validação, PR aberto, merge e deploy. Em retomadas, verifica registros existentes antes de escrever para evitar duplicação.

## Codex e outros clientes

```bash
bash /caminho/jade-agent/scripts/install-skills.sh codex --project /caminho/meu-projeto
```

O modo Codex instala as skills em `.agents/skills` e grava `JADE.md`. Peça ao cliente para ler `JADE.md`; ele não é ativado automaticamente como `AGENTS.md`. As regras existentes do projeto são preservadas. `AGENTS.md` e `AGENT-PROMPT.md` no pacote são versões portáveis geradas, que podem ser incorporadas deliberadamente ao fluxo do time.

O instalador também aceita `cursor`, `github-copilot`, `windsurf`, `gemini-cli`, `cline` e `universal`. Esses modos copiam skills para as pastas correspondentes e criam `JADE.md`; descubra/ative as instruções conforme o cliente. Não foram executados nesses aplicativos nesta entrega.

## Manutenção e verificação

A fonte canônica das regras comuns é `skills/jade-workflow/SKILL.md`. Após alterá-la:

```bash
python3 scripts/sync-instructions.py
python3 scripts/validate.py
python3 -m unittest discover -s tests -v
```

Os comandos não precisam de rede. O CI executa essas verificações e oferece um smoke test completo opcional em `workflow_dispatch`.

O instalador consome somente o manifesto, busca o SHA exato e confere o nome da skill. Não executa scripts das skills durante a instalação e não usa `skills@latest`. Ao atualizar dependências, revisar a nova fonte, alterar seu SHA/caminho no manifesto e repetir a instalação completa em projeto temporário. Fixar o commit garante rastreabilidade, não substitui revisão de segurança.

[docs/validation.md](docs/validation.md) registra os testes realizados. A instalação foi exercitada; o uso em uma sessão Claude com as suas contas precisa da autenticação local. [docs/evaluation-scenarios.md](docs/evaluation-scenarios.md) contém cenários para essa verificação.

## Conteúdo e proveniência

As skills próprias e as regras de engenharia evoluem a configuração original de `julianoalvescode/jade-agent`, base `5f9af5a777be07db7f316ca60512d8f38ff33b6d`. As skills de terceiros são baixadas dos repositórios e commits identificados no manifesto, mantendo seus arquivos; o pacote não as redistribui como conteúdo próprio.
