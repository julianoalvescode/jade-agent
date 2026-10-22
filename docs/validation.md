# Validação da entrega 2.2.0

Data: 22/10/2026.

| Verificação | Estado | Evidência |
| --- | --- | --- |
| Manifesto, nomes e caminhos | PASS | `python3 scripts/validate.py` |
| Paridade das instruções portáveis | PASS | `scripts/sync-instructions.py --check`, executado pelo validador |
| Sintaxe do wrapper shell | PASS | `bash -n scripts/install-skills.sh` |
| Testes do instalador, Figma e contrato | PASS | 31 testes (11 base + 9 `jade-figma-to-code` + 1 acionamento pleno + 10 `jade-backend-contract`): registro local, frontmatter, descoberta core-only, ausência de regressão, roteamento, composição, lazy activation, descoberta de stacks, back-end indisponível e SHA fixado de `contract-first` |
| Skill `jade-figma-to-code` | PASS | Instala em `--core-only`; coordena `figma-design-to-code`/`ui-recon`/`spacing-system`/`frontend-quality-gate`; < 500 linhas |
| Skill `jade-backend-contract` | PASS | Opcional/lazy; compõe `contract-first` (SHA `90606c83`) + `backend-contracts.md`; 93 linhas (< 500); roteada em `jade-frontend`/`jade-workflow`/`jade-figma-to-code` |
| Roteamento automático | PASS | Figma → `jade-figma-to-code`; API/endpoint/DTO → `jade-backend-contract` (lazy); tarefa visual não ativa a de contrato |
| Figma MCP no exemplo | PASS | Servidor `figma` em `.mcp.example.json`; comando `claude mcp add` em `docs/connectors.md` |
| Instalação completa | PASS | 27 skills (21 comunitárias + 6 próprias) instaladas em diretório temporário usando os commits fixados; `contract-first` e `jade-backend-contract` presentes |
| Reinstalação completa | PASS | Conteúdo das skills equivalente após duas instalações |
| Busca direta por revisão | PASS | Fetch por SHA, checkout e identidade de `ui-recon` confirmados sem usar o cache |
| Cenário sintético de entrega | PASS | Leitura independente das skills identificou conflito 84/96 meses, mock, ambiente desconhecido, head posterior aos testes e CI pendente; recomendou NOT READY e preservou comentário existente |
| Claude e conectores reais do time | NOT RUN | Autenticação e runtime do usuário indisponíveis neste ambiente |
| Outros clientes além do Claude/Codex | NOT RUN | Mapeamentos de diretórios fornecidos; carregamento pelo cliente não exercitado |

O cenário sintético foi avaliado por outro agente neste ambiente; não equivale a uma execução no Claude Code ou nas contas do time. Os testes de instalação não comprovam a qualidade de todas as instruções comunitárias nem o funcionamento dos conectores. O workflow de CI foi incluído, mas sua execução no GitHub depende da publicação do pacote no repositório.
