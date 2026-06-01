# Sistema de Pedidos - Monólito Modular

Esta é a **Versão 2 (Monólito Modular)** do sistema de pedidos, com fronteiras explícitas entre módulos, uso de DTOs(para comunicação entre modulos) e serviços para comunicação entre modulos(interfaces padronizadas).

## Como Rodar

1. **Configurar Ambiente:**
   ```bash
   python3 -m venv venv
   source venv/bin/activate  # Linux/Mac
   # venv\Scripts\activate   # Windows
   pip install -r requirements.txt
   ```

2. **Preparar Banco de Dados:**
   ```bash
   # Remova o db.sqlite3 antigo se houver conflito de esquema
   python manage.py makemigrations
   python manage.py migrate
   ```

3. **Executar Servidor:**
   ```bash
   python manage.py runserver
   ```

## Como Testar a Modularidade

### 1. Script de Teste Automatizado (Recomendado)
Criei um script que realiza um teste comparativo completo. Ele executa dois fluxos seguidos (Cardápio -> Pedido -> Pagamento -> Notificação), o primeiro utilizando o **Pagamento Padrão** (com delay) e o segundo utilizando o **Pagamento Rápido** (instantâneo), provando que os módulos se comunicam apenas por interfaces:
```bash
python test_modular_logic.py
```

### 2. Teste via Django Admin
1. Acesse `http://127.0.0.1:8000/admin/`.
2. Crie itens no **Cardápio**.
3. Crie um **Pedido** (insira o ID do item do cardápio manualmente, pois agora são módulos isolados).
4. Na lista de pedidos, selecione o pedido e use a ação: **"Processar Pagamento (Via Services Modular)"**.
5. Observe o delay de 5s (Pagamento Padrão) e a notificação automática enviada à cozinha.

### 3. O Experimento de Troca 
Para validar o baixo acoplamento:
1. Abra `pagamento/views.py`.
2. Troque a linha `pagamento_service = PagamentoPadraoService()` por `pagamento_service = PagamentoRapidoService()`.
3. Repita o teste. O delay de 5s desaparecerá, mas o sistema continuará funcionando perfeitamente. Nenhuma linha de código em `pedidos` ou `notificacao` precisou ser alterada.

---

# Documentação Técnica da Transição

Este documento descreve as alterações realizadas para transformar a aplicação em um Monólito Modular, seguindo os requisitos de fronteiras explícitas, interfaces públicas e desacoplamento de dados.

## 1. O que foi alterado
- **Criação de DTOs (`dto.py`):** Introduzidas classes de dados em cada módulo para transferir informações sem expor instâncias de models do Django.
- **Camada de Serviço (`services.py`):** Implementação de interfaces públicas para todos os módulos (`CardapioService`, `PedidoService`, `PagamentoService`, `NotificacaoService`).
- **Interfaces Abstratas:** Criação de `PagamentoInterface` para permitir múltiplas implementações.
- **Isolamento de Banco:** Remoção de `ForeignKey` entre apps. 
    - `pagamento.Transacao` agora usa `pedido_id` (Integer) em vez de uma chave estrangeira direta.
    - `pedidos.ItemPedido` agora usa `item_cardapio_id` (Integer) em vez de apontar para `cardapio.ItemCardapio`.
    - Isso garante que se o banco de um módulo for movido para outro servidor, o código continuará funcionando via chamadas de Service.

## 2. Por que e como foi alterado
- **Por que:** No monólito original, os módulos acessavam as tabelas uns dos outros diretamente (`ForeignKey` de `pagamento` para `pedidos`). Isso criava um "emaranhado" (spaghetti) que impedia mudanças isoladas e violava o princípio de "Schemas Separados".
- **Como:** 
    1. Criamos os DTOs para padronizar a comunicação.
    2. Envolvemos a lógica de cada app em um Service.
    3. Substituímos importações de models externos por chamadas aos Services.
    4. Refatoramos os Models para usar IDs lógicos em vez de chaves estrangeiras físicas entre módulos.

## 3. Impacto no Desenvolvimento
- **Facilidade de Testes:** É possível testar o módulo de `pedidos` mockando apenas o `CardapioService`, sem precisar de dados reais no banco de cardápio.
- **Manutenibilidade:** Mudanças internas em `pagamento` (como trocar o provedor de pagamento) não exigem nenhuma alteração em `pedidos`.
- **Consistência de Dados e Evolução:** 
    - Adicionamos `preco_unitario` em `ItemPedido`. 
    - Isso é fundamental em sistemas modulares/distribuídos: o módulo de Pedidos deve "congelar" o preço no ato da compra. Se o preço no `Cardápio` mudar amanhã, o histórico do pedido não é alterado, mantendo a integridade financeira sem precisar consultar o módulo de cardápio para cálculos históricos.

## 4. Esforço do Experimento
O experimento de trocar a implementação de pagamento (`Padrao` para `Rapido`) exigiu a alteração de apenas **1 linha de código** em um único arquivo do módulo de pagamento. Isso demonstra o sucesso do desacoplamento por interfaces, onde o comportamento do sistema mudou drasticamente sem afetar nenhum outro domínio de negócio.

## 5. Análise de Microsserviços
Quais módulos poderiam virar serviços independentes amanhã?
- **Todos.** Com a refatoração atual, `cardapio`, `pagamento` e `notificacao` já possuem fronteiras de dados claras.

O que falta para isso?
1. **Infraestrutura de Rede:** Substituir as chamadas de método em `services.py` por chamadas HTTP (REST) ou gRPC.
2. **Mensageria:** Implementar um Broker (como RabbitMQ ou Kafka) para que a `notificacao` reaja a eventos de "PagamentoConfirmado" em vez de ser chamada sincronicamente.
