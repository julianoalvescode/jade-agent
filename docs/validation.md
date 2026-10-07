# Validação da entrega 2.0.0

Data: 07/10/2026.

| Verificação | Estado | Evidência |
| --- | --- | --- |
| Manifesto, nomes e caminhos | PASS | `python3 scripts/validate.py` |
| Paridade das instruções portáveis | PASS | `scripts/sync-instructions.py --check`, executado pelo validador |
| Sintaxe do wrapper shell | PASS | `bash -n scripts/install-skills.sh` |
| Testes do instalador | PASS | 11 testes: conflito, backup, rollback, idempotência, falha externa, symlink, versão mutável, nomes duplicados, destino Codex e argumento inválido |
| Fontes externas | PASS | 14 repositórios obtidos, SHA confirmado e caminhos das 20 skills resolvidos |
| Instalação completa | PASS | 24 skills instaladas em diretório temporário usando checkouts dos commits fixados |
| Reinstalação completa | PASS | Conteúdo das skills equivalente após duas instalações |
| Busca direta por revisão | PASS | Fetch por SHA, checkout e identidade de `ui-recon` confirmados sem usar o cache |
| Cenário sintético de entrega | PASS | Leitura independente das skills identificou conflito 84/96 meses, mock, ambiente desconhecido, head posterior aos testes e CI pendente; recomendou NOT READY e preservou comentário existente |
| Claude e conectores reais do time | NOT RUN | Autenticação e runtime do usuário indisponíveis neste ambiente |
| Outros clientes além do Claude/Codex | NOT RUN | Mapeamentos de diretórios fornecidos; carregamento pelo cliente não exercitado |

O cenário sintético foi avaliado por outro agente neste ambiente; não equivale a uma execução no Claude Code ou nas contas do time. Os testes de instalação não comprovam a qualidade de todas as instruções comunitárias nem o funcionamento dos conectores. O workflow de CI foi incluído, mas sua execução no GitHub depende da publicação do pacote no repositório.
