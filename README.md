<div align="center">

# 🪷 Jade

**Uma agente de front-end para Claude Code — um agente, várias skills.**

Implementa e revisa React, Next.js e TypeScript com contexto real de
Jira, Confluence, GitHub, Figma e contratos de back-end — e entrega
evidências critério a critério.

<sub>Versão 2.1.0 · Claude Code · Codex · Cursor · Copilot · Windsurf · Gemini CLI · Cline</sub>

</div>

---

## Por que Jade

Jade **não é um gerador de telas**. É uma engenheira de front-end sênior que
investiga antes de editar, reutiliza o que o projeto já tem, respeita a stack
existente e nunca declara pronto sem evidência. Um único agente
(`jade`) carrega apenas o núcleo `jade-workflow` e **descobre as demais skills
sob demanda**, conforme o impacto da tarefa — sem subagentes, sem contexto
desperdiçado.

> [!NOTE]
> **Um agente, várias skills.** A arquitetura é deliberada: só `jade-workflow` é
> pré-carregada. UI, Figma, entrega, testes e segurança entram como skills
> separadas apenas quando a tarefa as exige.

## Skills próprias

| Skill | Papel |
| --- | --- |
| **`jade-workflow`** | Núcleo operacional: início, roteamento e entrega com evidências. É a única pré-carregada. |
| **`jade-frontend`** | Engenharia de front-end: reconhecimento de UI, reuso, grade de 8 pontos e implementação. |
| **`jade-figma-to-code`** | 🆕 Coordena Figma → código com leitura seletiva, reuso de componentes e economia de tokens. |
| **`jade-delivery`** | Jira, Confluence, GitHub e contratos entre repos, sem duplicar registros. |
| **`frontend-quality-gate`** | Prontidão por evidências: `PASS`/`FAIL`/`BLOCKED`/`NOT RUN`/`N/A`. |

Mais **20 skills comunitárias** (fixadas por commit em `skills-lock.json`)
complementam as regras próprias: `ui-recon`, `spacing-system`,
`figma-design-to-code`, `react-hook-form`, `state-management`,
`owasp-security-check`, `systematic-debugging`, entre outras.

## 🎨 Figma → código (`jade-figma-to-code`)

Acionada automaticamente quando o pedido traz um frame, node ou URL do Figma
(«implemente esta tela», «converta este node em React», «ajuste a UI ao
design»). Coordena o fluxo sem reescrever as skills oficiais:

```
A. Discovery       → identificar o node exato (exige node-id)
B. Project Mapping → ui-recon: mapear componente/token existente
C. Extraction      → figma-design-to-code: get_design_context (1 chamada)
D. Implementation  → código de produção na stack real + grade 8pt
E. Validation      → lint/types/testes direcionados + comparação visual
F. Delivery        → resumo com evidências e pendências reais
```

### Economia de tokens em três níveis

| Nível | Lê | Para quando |
| --- | --- | --- |
| **1 — mínimo** | stack, convenções e candidatos por **busca de símbolo/nome/import** + 1 chamada ao node | basta para mapear |
| **2 — específico** | só os arquivos da feature e do node (trechos, não arquivos inteiros) | a implementação está coberta |
| **3 — expandido** | dependências extras (subnodes, contrato de API) **só com necessidade comprovada** | — |

Regras firmes: nunca carregar o arquivo Figma inteiro, uma chamada MCP por node
(reaproveitando o contexto), nunca reler arquivo sem alteração, saídas curtas.
**Nunca** sacrificar correção, segurança ou fidelidade visual por tokens.

### Stack agnóstica

Jade **detecta** o framework, TS/JS, biblioteca de UI, design system, estilização
(Tailwind, CSS Modules, Styled Components, shadcn…), estado, testes e lint — e o
**padrão existente do projeto vence as preferências do agente**. Se já existe um
`Button`, `Input` ou `Modal`, reutiliza antes de criar.

## Instalar no seu projeto

Requisitos: **Python 3.10+** e **Git**. A instalação completa precisa de rede
para baixar os commits do manifesto; Node/npm não são necessários para instalar
a Jade.

```bash
# instalação completa (núcleo + 20 skills comunitárias)
bash /caminho/jade-agent/scripts/install-skills.sh claude-code --project /caminho/meu-projeto

# somente as cinco skills próprias, sem rede
bash /caminho/jade-agent/scripts/install-skills.sh claude-code --project /caminho/meu-projeto --core-only

# atualizar preservando arquivos divergentes (backup em .jade/backups/)
bash /caminho/jade-agent/scripts/install-skills.sh claude-code --project /caminho/meu-projeto --replace
```

O instalador **não** altera `CLAUDE.md`, `AGENTS.md`, `.mcp.json` ou configuração
pessoal: conflitos são informados antes de escrever. Também aceita `codex`,
`cursor`, `github-copilot`, `windsurf`, `gemini-cli`, `cline` e `universal` —
esses modos instalam em `.agents/skills` (ou equivalente) e gravam `JADE.md`.

## Configurar e usar

1. Copie `jade.project.example.json` para `jade.project.json` e preencha os repos,
   documentos e ambientes conhecidos (campos vazios = desconhecido, não contrato).
2. Reutilize os conectores autenticados — Jira/Confluence, GitHub e **Figma**. Veja
   [docs/connectors.md](docs/connectors.md). O exemplo de MCP não traz credenciais.
3. Abra uma sessão do Claude no projeto e peça.

**Exemplo — ticket completo:**

> Use a agente Jade para implementar o ticket PROJ-123. Leia os documentos
> vinculados, confira o contrato no back-end e valide os critérios. Prepare o PR
> com as evidências.

**Exemplo — Figma → código:**

> Jade, implemente esta tela do Figma:
> `https://www.figma.com/design/<fileKey>/Tela?node-id=12-345`.
> Reutilize os componentes do projeto e mantenha a grade de 8 pontos.

> [!IMPORTANT]
> **Figma MCP.** Se `get_design_context` não estiver exposto/autenticado, a Jade
> registra `BLOCKED` na etapa visual e **não recria a tela de memória**. Conecte o
> servidor `figma` (`claude mcp add --transport http figma https://mcp.figma.com/mcp`)
> e conclua o OAuth em `/mcp`. A entrada também consta em `.mcp.example.json`.

## Entrega com evidências

Cada tarefa relaciona **critério → implementação → evidência → estado**, usando
`PASS`, `FAIL`, `BLOCKED`, `NOT RUN` ou `N/A`. A Jade distingue código
implementado, validação, PR aberto, merge e deploy — e, ao retomar, verifica o
estado remoto antes de escrever, evitando duplicação.

## Manutenção e verificação

A fonte canônica das regras comuns é `skills/jade-workflow/SKILL.md`. Após
alterá-la:

```bash
python3 scripts/sync-instructions.py            # regenera AGENTS.md, AGENT-PROMPT.md e jade.md
python3 scripts/validate.py                      # manifesto, skills, referências, preload e paridade
python3 -m unittest discover -s tests -v         # 20 testes do instalador e da skill Figma
```

Nenhum comando precisa de rede. O CI executa essas verificações
([.github/workflows/validate-agent.yml](.github/workflows/validate-agent.yml)) e
oferece um smoke test completo em `workflow_dispatch`. O instalador consome apenas
o manifesto, busca o SHA exato, confere o nome da skill e **não executa scripts de
terceiros** durante a instalação. Ver [docs/validation.md](docs/validation.md) e
[docs/evaluation-scenarios.md](docs/evaluation-scenarios.md).

## Proveniência

As skills próprias e as regras de engenharia evoluem a configuração original de
`julianoalvescode/jade-agent` (base `5f9af5a777be07db7f316ca60512d8f38ff33b6d`).
As skills de terceiros são baixadas dos repositórios e commits do manifesto,
mantendo seus arquivos; o pacote não as redistribui como conteúdo próprio. Fixar
o commit garante rastreabilidade, não substitui revisão de segurança.
