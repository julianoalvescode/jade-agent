# Regras de engenharia back-end da Jade

## Navegação

- 1: repositório; 2: domínio; 3: API; 4: dados; 5: escalabilidade.
- 6: segurança; 7: performance; 8: operação; 9–11: testes, validação e revisão.

Ler apenas as seções afetadas. Skills externas são complementares quando
instaladas; sem elas, seguir estas regras e declarar verificações não feitas.

## 1. Entender o repositório

- Ler `AGENTS.md`, `CLAUDE.md`, `README`, ADRs e documentação de arquitetura.
- Identificar linguagem, framework, build (`pom.xml`, `build.gradle`,
  `package.json`, `pyproject.toml`, `go.mod`), versão de runtime e lockfile.
- Mapear camadas reais: controller/resolver → service/use case → repository →
  modelo; onde ficam validação, mapeamento de DTO, tratamento de erro e auth.
- Localizar migrações, seeds, configuração por ambiente, testes semelhantes e
  pipeline de CI.
- Ler só nomes de variáveis e arquivos de exemplo. Nunca abrir `.env`,
  credenciais, chaves ou dumps de banco.

## 2. Modelar o domínio

- Registrar ator, objetivo, regra de negócio, invariantes e critérios de aceite.
- Decidir onde cada invariante é garantida: banco (constraint), domínio ou serviço.
- Listar efeitos colaterais: escrita, evento, e-mail, chamada externa, auditoria.
- Usar o vocabulário do domínio já presente no código.

## 3. Projetar a API

- Seguir o estilo existente (REST, GraphQL, RPC), nomes, envelopes de resposta e
  formato de erro (preferir RFC 9457 `application/problem+json` se já adotado).
- Métodos e status corretos: 200/201/204, 400 validação, 401 sem autenticação,
  403 sem permissão, 404, 409 conflito, 422 regra de negócio, 429 limite.
- Listas sempre paginadas (cursor para volume alto), com filtro e ordenação
  validados por allowlist e limite máximo de página.
- Compatibilidade: adicionar campo opcional é seguro; remover, renomear ou mudar
  tipo é breaking change e exige versão nova ou período de convivência.
- Atualizar OpenAPI/GraphQL schema, tipos gerados e o consumidor front-end no
  mesmo escopo. Usar `contract-first` e `api-and-interface-design` quando houver.
- Não expor entidade de banco direto: mapear para DTO com só os campos necessários.

## 4. Dados, migrações e transações

- Modelar com constraints (NOT NULL, UNIQUE, FK, CHECK) para proteger invariantes.
- Criar índice para filtros, joins e ordenações novos; conferir o plano
  (`EXPLAIN`) em consultas de lista ou relatório.
- Migrações versionadas, pequenas e reversíveis.
  Seguir expand → migrate → contract: a versão anterior da aplicação deve
  continuar funcionando.
- Em tabela grande, evitar lock longo: criar índice de forma concorrente quando o
  banco suportar e fazer backfill em lotes.
- Transação curta, só em volta da escrita que precisa ser atômica. Nada de
  chamada HTTP externa dentro de transação.
- Tratar concorrência: lock otimista (versão) ou restrição única em vez de
  "ler e depois gravar" sem proteção.
- Datas em UTC, dinheiro em decimal/inteiro de centavos, enums validados.
- Nunca rodar migração, seed ou script de dados em ambiente compartilhado sem
  autorização explícita e backup.

## 5. Escalabilidade

- Serviço sem estado em memória local entre requisições; sessão e cache em
  armazenamento compartilhado quando houver mais de uma instância.
- Operações repetíveis idempotentes (chave de idempotência em POST de pagamento,
  pedido ou integração; consumidores de fila tolerantes a entrega duplicada).
- Trabalho lento ou não crítico vai para fila/job assíncrono com retry, backoff,
  limite de tentativas e dead-letter.
- Cache só com dono, chave, TTL e regra de invalidação claros. Não cachear dado
  por usuário em cache compartilhado sem a identidade na chave.
- Limitar tudo que cresce: tamanho de payload, página, upload, lote, conexões e
  fan-out. Aplicar rate limit nas rotas públicas ou caras.
- Chamadas externas com timeout explícito, retry só em erro transitório e
  circuit breaker quando o projeto já tiver o padrão.
- Pensar em 10× o volume atual: o algoritmo ou a consulta continua aceitável?

## 6. Segurança (OWASP API Security Top 10:2023 e Top 10:2025)

Revisão proporcional ao risco em toda mudança; completa em auth, pagamento, PII,
upload, multi-tenant, admin ou integração externa. Usar `owasp-security-check`.

- **Autorização por objeto (BOLA/IDOR):** todo acesso a recurso confere se o
  usuário/tenant pode vê-lo ou alterá-lo, no servidor, a cada requisição.
- **Autorização por função:** rotas admin e ações privilegiadas com checagem
  explícita; negar por padrão.
- **Mass assignment / exposição excessiva:** DTO de entrada com allowlist de
  campos; DTO de saída sem campos internos ou sensíveis.
- **Autenticação:** usar o mecanismo existente; validar assinatura, emissor,
  audiência e expiração de tokens; senhas com hash forte (bcrypt/argon2).
- **Injeção:** consultas parametrizadas/ORM; nunca concatenar SQL, shell, LDAP ou
  caminhos com entrada do usuário. Validar tipo, tamanho e formato na fronteira.
- **SSRF:** URLs fornecidas pelo usuário só com allowlist de destino; bloquear
  rede interna e metadados de nuvem.
- **Upload:** validar tipo real, tamanho e nome; armazenar fora da raiz pública.
- **Segredos:** em variáveis de ambiente ou cofre; nunca no código, log, teste ou
  resposta. Não registrar token, senha, cookie ou documento pessoal.
- **Erros:** resposta genérica ao cliente, detalhe só no log interno.
- **CORS e headers:** origens explícitas, sem `*` com credenciais.
- **Dependências:** auditoria read-only do gerenciador; não atualizar nem rodar
  `audit fix` sem escopo.

Classificar achados como crítico, alto, médio ou baixo com evidência, categoria,
impacto e correção. Achado crítico ou alto introduzido pela mudança bloqueia a
conclusão. Testes ativos só em ambiente local ou autorizado.

## 7. Performance

- Medir antes e depois no caminho alterado (teste de carga leve, `EXPLAIN`,
  profiler ou métrica existente). Não inventar números.
- Eliminar N+1: carregar relações em lote ou com join; contar queries no teste
  quando o projeto permitir.
- Selecionar só as colunas necessárias; paginar no banco, nunca em memória.
- Evitar trabalho síncrono pesado no request; mover para job quando passar do
  orçamento de latência acordado.
- Pool de conexões e timeouts coerentes com a carga; não abrir conexão por item.
- Compressão e cache HTTP (`ETag`, `Cache-Control`) quando o recurso permitir.

## 8. Operação e observabilidade

- Logs estruturados com correlação (request id/trace id) e nível adequado.
- Métricas e traces no padrão existente para rotas e jobs novos.
- Health/readiness checks não devem depender de serviço externo opcional.
- Feature flag ou rollout gradual para mudança arriscada, quando o projeto usar.
- Plano de rollback claro para código e migração.

## 9. Testar comportamento

- Unitário para regra de negócio e casos de borda.
- Integração na fronteira real (controller + banco de teste/Testcontainers, ou o
  padrão do projeto) para rota, transação e migração.
- Testes de segurança nos limites alterados: sem token, token de outro usuário
  (BOLA), payload inválido, campo extra (mass assignment), limite excedido.
- Teste de contrato quando o projeto tiver (OpenAPI, Pact, schema snapshot).
- Mock só na fronteira externa (rede de terceiros, relógio, fila).
- Para regressão, reproduzir a falha com teste antes de corrigir.

## 10. Validar o projeto

Rodar, quando existirem: testes focados, suíte, lint/format check, typecheck ou
compilação, build e auditoria read-only de dependências. Ler saída e exit code.
Corrigir falhas causadas pela mudança. Separar falha introduzida, preexistente
comprovada e bloqueio de ambiente.

## 11. Revisar antes da entrega

Usar `code-review-and-quality` nos arquivos alterados: correção, legibilidade,
arquitetura, segurança, escalabilidade e performance. Corrigir achados causados
pela mudança e repetir as verificações afetadas, sem refactor amplo.

# Limites

- Não executar comandos destrutivos, `DROP`/`TRUNCATE`, force push ou reset hard.
- Não alterar infraestrutura, IAM, permissões, banco compartilhado ou deploy sem
  pedido explícito.
- Não desativar testes, lint, validação ou checagem de auth para obter verde.
- Não atualizar dependências ou lockfiles incidentalmente.
