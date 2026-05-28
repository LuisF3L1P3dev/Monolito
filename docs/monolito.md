# Especificação Técnica: Versão 1 — Monólito (Python & Django CBV)

Este documento centraliza as diretrizes, requisitos e o escopo de implementação para a **Versão 1 — Monólito** do sistema. A arquitetura escolhida reflete uma aplicação unificada, onde todo o domínio de negócio reside em uma única base de código, executa em um único processo e compartilha o mesmo banco de dados.

As tecnologias definidas para esta implementação são **Python** e **Django**, utilizando obrigatoriamente **Class-Based Views (CBVs)** para a estrutura das rotas e controladores.

---

## 1. Diretrizes de Arquitetura e Estrutura

### Premissas do Monólito:
* **Processo Único:** Tudo roda em uma única aplicação, escutando em uma única porta lógica (ex: `8000`).
* **Deploy Único:** O sistema inteiro é empacotado e distribuído em bloco.
* **Banco de Dados Unificado:** Um único banco de dados relacional (ex: SQLite para desenvolvimento) contendo todas as tabelas, sem separação física ou lógica de schemas nesta fase.
* **Acoplamento Natural:** Os módulos de negócio (`pedidos`, `cardapio`, `pagamento`, `notificacao`) podem residir em pastas ou apps Django separados, mas as fronteiras rígidas não devem ser forçadas. Chamadas diretas de funções, imports diretos entre apps e relacionamentos via ORM (Foreign Keys) entre tabelas de domínios diferentes são permitidos e esperados para simular o comportamento de um monólito tradicional.
* **Comunicação:** A interação entre as capacidades do sistema ocorre via chamadas diretas de métodos/funções na memória (comunicação em processo/síncrona).

---

## 2. Domínio do Sistema e Mapeamento em Django

O projeto deve ser estruturado utilizando os conceitos nativos do Django (Apps). Sugere-se a criação de um projeto Django (ex: `delivery_project`) e apps separados para organização do código, mantendo o acoplamento direto:

### A. Pedidos (`apps.pedidos`)
* **Responsabilidades:** Criar novos pedidos, listar o histórico e permitir o cancelamento.
* **Modelos Sugeridos:** `Pedido` (com campos como `id`, `data_criacao`, `status` [Pendente, Pago, Cancelado], `total`).
* **Estrutura CBV:** * `PedidoCreateView(CreateView)` ou `APIView`/`View` customizada para a criação.
  * `PedidoListView(ListView)` para listagem.
  * `PedidoCancelView(UpdateView)` ou `View` para alteração de status.

### B. Cardápio (`apps.cardapio`)
* **Responsabilidades:** CRUD completo de itens do cardápio, definição de preços e controle de disponibilidade.
* **Modelos Sugeridos:** `ItemCardapio` (com campos `nome`, `descricao`, `preco`, `disponivel`).
* **Estrutura CBV:** Implementação padrão de views baseadas em classe para as operações de Create, Read, Update e Delete (`ItemCreateView`, `ItemListView`, `ItemUpdateView`, `ItemDeleteView`).

### C. Pagamento (`apps.pagamento`)
* **Responsabilidades:** Processar o pagamento de forma simulada (*mock*) e expor consulta de status do processamento.
* **Modelos/Estruturas:** Pode conter uma tabela `Transacao` ou gerenciar o estado diretamente no fluxo do pedido.
* **Estrutura CBV:** `ProcessarPagamentoView(View)` que recebe o ID do pedido, executa a lógica e atualiza o estado.

### D. Notificação (`apps.notificacao`)
* **Responsabilidades:** Notificar a cozinha assim que um pedido tiver o pagamento confirmado.
* **Lógica no Monólito:** Uma função ou método simples dentro deste módulo que é chamado diretamente pelo módulo de pagamento após o sucesso da transação. Pode apenas registrar um log detalhado ou simular o envio da ordem para a tela da cozinha.

> **Regra de Negócio Crítica:** Um pedido só muda seu status para "Enviado à Cozinha" após a confirmação de pagamento com sucesso. O fluxo obrigatório na memória deve ser: **Criar Pedido** $\rightarrow$ **Chamar Módulo de Pagamento** $\rightarrow$ **Se Pago com Sucesso, Chamar Módulo de Notificação**.

---

## 3. Checklist de Verificação da IA

Abaixo estão os critérios exatos que a Inteligência Artificial utilizará para validar a sua entrega técnica:

- [ ] **[CHECK-01] Única aplicação rodando em uma única porta:** O projeto deve ser iniciado via um único comando (ex: `python manage.py runserver`) unificado.
- [ ] **[CHECK-02] Banco de dados único:** Uma única string de conexão/configuração no `settings.py` que gerencia todas as tabelas em conjunto, permitindo chaves estrangeiras diretas do ORM entre `Pedido` e `ItemCardapio`.
- [ ] **[CHECK-03] Fluxo completo funcional:** O endpoint ou fluxo deve demonstrar a cadeia contínua: *Criar Pedido* $\rightarrow$ *Pagar* $\rightarrow$ *Notificar Cozinha* sem interrupções e de forma síncrona.
- [ ] **[CHECK-04] Endpoint de Health Check:** Implementação de uma view baseada em classe `HealthCheckView(View)` mapeada para a rota `GET /health`, retornando um JSON básico contendo o status da aplicação (ex: `{"status": "UP"}`).
- [ ] **[CHECK-05] Uso de Django Class-Based Views (CBV):** Todas as rotas principais devem ser controladas por classes que herdam das views nativas do Django, estruturando o comportamento via métodos HTTP (`get`, `post`, etc.).
- [ ] **[CHECK-06] Ausência de Front-end/Interface Visual:** O foco deve ser estritamente nos endpoints e lógica de negócio. Respostas em JSON ou retornos estruturados via terminal/logs são perfeitamente aceitáveis.

---

## 4. Experimento Obrigatório e Simulação

Você deve testar o impacto do acoplamento direto do monólito realizando o seguinte experimento:

1. **Injeção de Latência:** No módulo de pagamento (`apps.pagamento`), adicione uma linha de bloqueio explícito usando `time.sleep(5)` dentro do método de processamento da sua Class-Based View.
2. **Execução do Teste:** Realize uma requisição de pagamento e, simultaneamente, tente acessar o endpoint de listagem do cardápio (`GET /cardapio/`) ou o endpoint de *Health Check* (`GET /health`).
3. **Observação do Comportamento:** Note como a lentidão em um único componente impacta a thread/processo inteiro do servidor, deixando os outros recursos do sistema temporariamente indisponíveis ou lentos.

---

## 5. Entregáveis de Documentação

No arquivo de documentação final ou na seção de resultados do seu repositório, responda formalmente à seguinte questão arquitetural baseada na sua experiência com este código:

* **Questão:** *O que precisaria mudar na infraestrutura ou na arquitetura da aplicação se o módulo de **Cardápio** passasse a receber subitamente 10 vezes mais acessos e requisições de leitura do que o resto de todo o sistema? Como escalar o cardápio sem desperdiçar recursos escalando o pagamento e os pedidos juntos?*