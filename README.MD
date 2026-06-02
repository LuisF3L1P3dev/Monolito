# Sistema de Pedidos — Microsserviços

Sistema de pedidos de lanchonete implementado como microsserviços independentes, cada um com seu próprio processo, banco de dados e contêiner Docker.

## Arquitetura

```
Cliente
  │
  ├── POST /api/pedidos/<id>/pagar/
  │         │
  │   servico-pedidos :8001
  │   (retry + backoff exponencial)
  │         │ HTTP síncrono
  │         ▼
  │   servico-pagamento :8003
  │         │ publica na fila
  │         ▼
  │      RabbitMQ
  │         │ consome
  │         ▼
  │   notificacao-worker → salva LogNotificacao
  │
  └── GET /api/cardapio/
        servico-cardapio :8002
```

| Serviço             | Porta | Banco          | Função                          |
|---------------------|-------|----------------|---------------------------------|
| servico-cardapio    | 8002  | cardapio_db    | CRUD de itens do cardápio       |
| servico-pedidos     | 8001  | pedidos_db     | Criar, listar, pagar, cancelar  |
| servico-pagamento   | 8003  | pagamento_db   | Processar pagamento             |
| servico-notificacao | 8004  | notificacao_db | API de logs + worker da fila    |
| rabbitmq            | 5672  | —              | Fila assíncrona de notificações |

## Como rodar

```bash
cd micro-servicos
docker compose up --build
```

Aguarde todos os health checks passarem. O RabbitMQ demora ~15s para ficar pronto.

## Endpoints

### Cardápio (porta 8002)
```
GET    /health
GET    /api/cardapio/
POST   /api/cardapio/          {"nome": "X-Burger", "preco": "18.50", "disponivel": true}
GET    /api/cardapio/<id>/
PUT    /api/cardapio/<id>/
DELETE /api/cardapio/<id>/
```

### Pedidos (porta 8001)
```
GET    /health
GET    /api/pedidos/
POST   /api/pedidos/           {"itens": [{"item_cardapio_id": 1, "quantidade": 2}], "observacao": "sem cebola"}
GET    /api/pedidos/<id>/
POST   /api/pedidos/<id>/pagar/
POST   /api/pedidos/<id>/cancelar/
DELETE /api/pedidos/<id>/
```

### Pagamento (porta 8003)
```
GET    /health
POST   /api/pagamentos/processar/         {"pedido_id": 1, "valor": "18.50"}
GET    /api/pagamentos/<pedido_id>/status/
```

### Notificação (porta 8004)
```
GET    /health
GET    /api/notificacoes/
```

## Fluxo completo

```bash
# 1. Criar item no cardápio
curl -X POST http://localhost:8002/api/cardapio/ \
  -H "Content-Type: application/json" \
  -d '{"nome": "X-Burger", "descricao": "Hambúrguer artesanal", "preco": "18.50", "disponivel": true}'

# 2. Criar pedido
curl -X POST http://localhost:8001/api/pedidos/ \
  -H "Content-Type: application/json" \
  -d '{"itens": [{"item_cardapio_id": 1, "quantidade": 2}], "observacao": "sem cebola"}'

# 3. Pagar (chama pagamento via HTTP; pagamento publica na fila)
curl -X POST http://localhost:8001/api/pedidos/1/pagar/

# 4. Verificar notificações (worker consumiu a fila)
curl http://localhost:8004/api/notificacoes/
```

## Padrões de resiliência implementados

### Timeout explícito (pedidos → pagamento)
Todas as chamadas HTTP usam `timeout=10s`, evitando que uma falha no serviço de pagamento bloqueie o serviço de pedidos indefinidamente.

### Retry com backoff exponencial (pedidos → pagamento)
Até 3 tentativas com espera de 1s e 2s entre elas. Erros 4xx não são retentados (falha definitiva do cliente); erros 5xx sim (falha transiente do servidor).

### Fire-and-forget na fila (pagamento → notificação)
Se o RabbitMQ estiver indisponível, o serviço de pagamento loga o aviso mas não falha o pagamento. A transação é aprovada normalmente.

### Reconexão automática do worker
O `notificacao-worker` reconecta ao RabbitMQ automaticamente após falhas de conexão.

### Mensagens persistentes + ACK manual
A fila é `durable=True` e as mensagens têm `delivery_mode=2` (persistidas em disco). O worker só confirma o recebimento (ACK) após salvar no banco, evitando perda de mensagens em caso de crash.

## Experimento: derrubar o serviço de notificação

```bash
# Derruba o worker
docker compose stop notificacao-worker

# Faz um pedido e paga normalmente
curl -X POST http://localhost:8001/api/pedidos/ \
  -d '{"itens": [{"item_cardapio_id": 1, "quantidade": 1}]}'
curl -X POST http://localhost:8001/api/pedidos/2/pagar/
```

**Resultado esperado:** pagamento aprovado com HTTP 200. A mensagem fica retida na fila. Quando o worker voltar (`docker compose start notificacao-worker`), ele consome as mensagens pendentes automaticamente.

O pagamento não falha junto com a notificação — cada serviço falha de forma independente.

## Rollback cirúrgico de um único serviço

Como cada serviço tem seu próprio contêiner e banco isolado, o rollback não exige redeployar o sistema inteiro:

```bash
docker compose up -d --no-deps --build servico-pagamento
```

O que continua funcionando durante o rollback:
- `servico-pedidos` — cadastro, listagem, cancelamento
- `servico-cardapio` — CRUD de itens
- `servico-notificacao` e worker — consumo da fila

O que para de funcionar:
- Apenas `POST /api/pedidos/<id>/pagar/` (retorna 502 após timeout e retries)
