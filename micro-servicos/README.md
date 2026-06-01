# Versão 3 — Microsserviços

Sistema de pedidos de lanchonete implementado como microsserviços independentes.

## Arquitetura

```
Cliente
  │
  ├── POST /api/pedidos/<id>/pagar/
  │         │
  │   servico-pedidos :8001
  │   (retry + timeout)
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

| Serviço              | Porta | Banco              | Função                              |
|----------------------|-------|--------------------|-------------------------------------|
| servico-cardapio     | 8002  | cardapio_db        | CRUD de itens do cardápio           |
| servico-pedidos      | 8001  | pedidos_db         | Criar, listar, pagar, cancelar      |
| servico-pagamento    | 8003  | pagamento_db       | Processar pagamento (mock)          |
| servico-notificacao  | 8004  | notificacao_db     | API de logs + worker da fila        |
| rabbitmq             | 5672  | —                  | Fila assíncrona de notificações     |

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
POST   /api/cardapio/           {"nome": "X-Burger", "preco": "18.50", "disponivel": true}
GET    /api/cardapio/<id>/
PUT    /api/cardapio/<id>/
DELETE /api/cardapio/<id>/
```

### Pedidos (porta 8001)
```
GET    /health
GET    /api/pedidos/
POST   /api/pedidos/            {"itens": [{"item_cardapio_id": 1, "quantidade": 2}], "observacao": "sem cebola"}
GET    /api/pedidos/<id>/
POST   /api/pedidos/<id>/pagar/
POST   /api/pedidos/<id>/cancelar/
DELETE /api/pedidos/<id>/
```

### Pagamento (porta 8003)
```
GET    /health
POST   /api/pagamentos/processar/           {"pedido_id": 1, "valor": "18.50"}
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

## Estratégias de resiliência implementadas

### 1. Timeout explícito (pedidos → pagamento)
`servico-pedidos/pedidos/services.py` usa `timeout=10s` em todas as chamadas HTTP.

### 2. Retry com backoff exponencial (pedidos → pagamento)
Até 3 tentativas com espera de 1s, 2s, 4s entre tentativas antes de desistir.

### 3. Fire-and-forget na fila (pagamento → notificação)
Se o RabbitMQ estiver indisponível, `servico-pagamento` loga o aviso mas **não falha o pagamento**. A transação é aprovada normalmente.

### 4. Reconexão automática do worker
O `notificacao-worker` reconecta ao RabbitMQ automaticamente após falhas de conexão.

### 5. Mensagens persistentes + ACK manual
A fila é `durable=True` e as mensagens têm `delivery_mode=2` (persistentes). O worker só dá ACK após salvar no banco, evitando perda de mensagens.

## Experimento obrigatório: derrubar o serviço de notificação

```bash
# Derruba o worker de notificação
docker compose stop notificacao-worker

# Faz um pedido normalmente
curl -X POST http://localhost:8001/api/pedidos/ \
  -d '{"itens": [{"item_cardapio_id": 1, "quantidade": 1}]}'

curl -X POST http://localhost:8001/api/pedidos/2/pagar/
```

**Resultado esperado:** O pagamento é aprovado com sucesso (HTTP 200). A mensagem fica retida na fila RabbitMQ. Quando o worker voltar (`docker compose start notificacao-worker`), ele consumirá as mensagens pendentes automaticamente.

**Conclusão:** O pagamento NÃO falha junto com o serviço de notificação. O desacoplamento via fila garante que cada serviço pode falhar independentemente.

## Documentação: rollback apenas do serviço de pagamento

Como cada serviço tem seu próprio container e banco de dados isolado, o rollback é cirúrgico:

```bash
# 1. Subir versão anterior do serviço de pagamento
docker compose up -d --no-deps --build servico-pagamento

# Ou para uma versão específica de imagem:
# docker compose stop servico-pagamento
# docker compose rm servico-pagamento
# Edite docker-compose.yml para apontar para a imagem/tag anterior
# docker compose up -d servico-pagamento
```

**O que NÃO é afetado:**
- `servico-pedidos` continua funcionando (cadastro, listagem, cancelamento)
- `servico-cardapio` continua funcionando (CRUD de itens)
- `servico-notificacao` e worker continuam consumindo a fila
- Banco de dados de pedidos, cardápio e notificações intactos

**O que para de funcionar:**
- Apenas o endpoint `POST /api/pedidos/<id>/pagar/` falha (timeout → retorna 502)
- Pedidos que já foram pagos permanecem com status PAGO

Isso é impossível no monólito e complexo no monólito modular: requer redeployar o app inteiro.
