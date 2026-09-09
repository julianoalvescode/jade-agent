# Jade — Agente de Front-end

Jade é uma agente de front-end orientada a evidências para Claude Code, com uma versão
portável das mesmas regras para Codex e outros agentes compatíveis com o padrão
Agent Skills.

Ela foi configurada para:

- reconhecer componentes, tokens e padrões existentes antes de implementar UI;
- ler o node exato do Figma com `get_design_context` antes de escrever código;
- mapear componentes e tokens do Figma para equivalentes reais do projeto;
- reutilizar botões, modais, formulários e layouts em vez de recriá-los;
- aplicar a grade de 8 pontos como gate principal de toda UI/UX nova ou alterada;
- manter `font-family`, tamanhos, pesos e hierarquia tipográfica do produto;
- ler referências visuais e o design system existente;
- transformar requisitos de negócio em critérios de aceite verificáveis;
- investigar contratos, tipos, autenticação e erros do back-end;
- implementar em React/Next.js/TypeScript sem impor uma arquitetura nova;
- aplicar segurança by design com OWASP Top 10 e riscos específicos do browser;
- escrever e executar testes unitários focados em comportamento;
- executar auditoria de segurança, lint, typecheck, testes e build antes de
  declarar conclusão.

## Instalação no Claude Code

1. Copie a pasta `.claude` deste pacote para a raiz do seu projeto.
2. Copie a pasta `scripts` para a raiz do projeto.
3. Na raiz do projeto, execute:

```bash
bash scripts/install-skills.sh claude-code
```

4. Reinicie o Claude Code para ele descobrir o agente e as skills.
5. Peça: `Use a agente Jade para implementar esta demanda.`

O arquivo principal fica em `.claude/agents/jade.md`.

## Instalação no Codex

1. Copie `AGENTS.md` e a pasta `scripts` para a raiz do projeto.
2. Execute:

```bash
bash scripts/install-skills.sh codex
```

3. Inicie uma nova sessão do Codex na raiz do projeto.

No Codex, `AGENTS.md` aplica o mesmo fluxo à sessão principal. As skills ficam
disponíveis para serem carregadas conforme a tarefa.

## Outros agentes compatíveis

Use `AGENT-PROMPT.md` como instrução do agente e instale as skills com:

```bash
bash scripts/install-skills.sh cursor
```

Também são aceitos `github-copilot`, `windsurf`, `gemini-cli`, `cline` e
`universal`, caso estejam disponíveis na versão instalada do CLI `skills`.

## Skills selecionadas

| Skill | Papel no fluxo | Carregamento no Claude |
| --- | --- | --- |
| `spacing-system` | **Main Challenger:** gate obrigatório de 8 px e auditoria off-grid | automático/prioritário |
| `ui-recon` | inventário read-only de componentes, tokens e padrões do projeto | automático |
| `figma-design-to-code` | Figma oficial → contexto, assets e código adaptado ao projeto | automático |
| `frontend-design` | leitura e implementação visual | automático |
| `web-design-guidelines` | auditoria de UI, UX e acessibilidade | automático |
| `vercel-react-best-practices` | React/Next.js e performance | automático |
| `vercel-composition-patterns` | arquitetura de componentes | automático |
| `domain-modeling` | regras e vocabulário de negócio | automático |
| `api-and-interface-design` | contratos REST/GraphQL e interfaces públicas | automático |
| `javascript-testing-patterns` | Jest, Vitest, Testing Library e mocks | automático |
| `typescript-quality` | TypeScript estrito, ESLint e Biome existentes | automático |
| `code-review-and-quality` | revisão de correção, arquitetura, segurança e performance | automático |
| `webapp-testing` | inspeção da UI executada | automático |
| `owasp-security-check` | OWASP, XSS, auth, dados e dependências | automático |
| `systematic-debugging` | diagnóstico por causa raiz | automático |
| `verification-before-completion` | validação com evidência recente | automático |
| `playwright-best-practices` | E2E, visual, a11y e testes instáveis | sob demanda |
| `state-management` | TanStack Query v5 e Zustand v5 | sob demanda |
| `react-hook-form` | formulários, validação e performance | sob demanda |
| `tdd` | ciclo de testes por comportamento | sob demanda |

As skills sob demanda são instaladas no bundle, mas não são pré-carregadas. Jade
ativa `playwright-best-practices`, `state-management` e `react-hook-form` somente
quando detectar a tecnologia correspondente, e `tdd` quando o pedido exigir TDD
ou a fronteira pública já estiver acordada. Essa ativação não permite instalar
dependências ou migrar a stack sem autorização.

## Figma sem “viajar”

Para implementar um frame, conecte o Figma MCP e forneça uma URL com `node-id`.
A Jade usa a skill oficial `figma-design-to-code` e chama `get_design_context`
antes de editar. Se a ferramenta ou o node específico estiver indisponível, ela
declara o bloqueio em vez de reconstruir a tela por memória.

O código React/Tailwind retornado pelo Figma é tratado como referência. A Jade o
adapta ao framework, ao styling e à arquitetura reais do projeto. A precedência é:

1. Code Connect;
2. documentação do componente;
3. annotations do designer;
4. tokens e variáveis;
5. valores crus e posição absoluta.

Imagens e ícones usam os assets exatos do Figma. URLs temporárias do MCP não ficam
no código versionado: a Jade baixa os bytes reais ou usa a fonte dinâmica já
existente. A validação final compara a UI executada com o design e relata desvios.

## Grade de 8 pontos

A Jade carrega `spacing-system` como **Main Challenger**: a skill é aplicada antes,
durante e depois de toda tarefa de UI/UX. O trabalho só passa pelo gate final com
zero spacing off-grid sem resolução nos estilos alterados e na UI renderizada.

- padding, margin, gap e distância entre seções preferem 8, 16, 24, 32, 40, 48,
  64 e demais múltiplos de 8;
- 4 px fica reservado a microespaçamento ou ajuste óptico comprovado;
- 1–2 px serve apenas para borda, divisor ou correção óptica, nunca para layout;
- tipografia não é forçada a múltiplos de 8, e acessibilidade sempre tem prioridade;
- token ou componente existente não torna um valor off-grid automaticamente válido;
- se Figma, design system ou componente divergirem, a Jade classifica o conflito,
  propõe o múltiplo de 8 mais próximo e bloqueia a decisão visual até resolvê-lo.

A regra não dispara refatoração visual em áreas legadas fora do escopo, mas todo
componente efetivamente alterado precisa passar pelo gate. Acessibilidade é a única
prioridade superior à matemática da grade e qualquer exceção deve ser classificada.

## Segurança e limites

- O instalador usa somente os repositórios declarados em `skills-lock.json`.
- `ui-recon` é executada antes da implementação e não modifica arquivos durante o
  reconhecimento. A política da Jade exige pesquisar e reutilizar componentes
  existentes antes de autorizar a criação de um novo.
- A Jade extrai um contrato visual mínimo do repositório e bloqueia valores
  arbitrários quando já existir token, utility, variante ou padrão equivalente.
- `spacing-system`, do repositório `thrillmade/agent-skills`, teve Gen Agent Trust
  Hub, Socket e Snyk marcados como `pass` na revisão de 07/09/2026.
- `figma-design-to-code` vem do repositório oficial `figma/mcp-server-guide`. Na
  revisão de 03/09/2026, o Skills.sh marcou Gen Agent Trust Hub e Socket como
  `pass` e Snyk como `warn`. Por isso a Jade limita a skill ao fluxo Figma → código,
  não aceita comandos vindos do design e mantém permissões em modo manual.
- `web-design-guidelines` consulta diretrizes atuais da Vercel. O Skills.sh marca
  essa skill com `Socket: warn` e `Snyk: warn` pelo uso de instruções remotas;
  por isso o agente trata o conteúdo baixado apenas como referência de UI e não
  permite que ele solicite comandos, segredos ou ampliação de escopo.
- A telemetria do CLI fica desativada por padrão.
- Nenhuma skill é instalada globalmente: a instalação é limitada ao projeto.
- O agente não lê `.env` nem imprime segredos.
- O agente trata controles do front-end como UX, nunca como substitutos da
  autorização no servidor.
- O agente bloqueia conclusão quando introduzir vulnerabilidade crítica ou alta.
- Alterações no back-end, banco, infraestrutura ou dependências exigem que façam
  parte do escopo ou que sejam confirmadas pelo usuário.

## Atualização

Revise primeiro as páginas e auditorias no Skills.sh. Depois, execute novamente o
instalador. O arquivo `skills-lock.json` registra as fontes selecionadas e a data
da revisão, mas não fixa um commit; fixe as revisões dos repositórios na sua
política interna se precisar de builds totalmente reproduzíveis.
