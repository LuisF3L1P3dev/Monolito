# Projeto Monólito - Delivery

Este projeto é a **Versão 1 (Monólito)** de um sistema de pedidos de restaurante, desenvolvido para estudo comparativo de arquiteturas (Monólito, Monólito Modular e Microsserviços). Foi construído utilizando Python e Django.

## Como iniciar o projeto

Para rodar o projeto localmente, siga os passos abaixo:

1. **Ative o ambiente virtual (se aplicável):**
   ```bash
   venv\Scripts\activate
   ```

2. **Instale as dependências (caso exista um `requirements.txt`):**
   ```bash
   pip install -r requirements.txt
   ```
   *(Caso não tenha, as dependências básicas são `django`)*

3. **Aplique as migrações no banco de dados:**
   ```bash
   python manage.py migrate
   ```

4. **Crie um superusuário para acessar o painel de administração:**
   ```bash
   python manage.py createsuperuser
   ```
   *O terminal pedirá para você inserir um usuário (username), email (opcional) e senha (password).*

5. **Inicie o servidor de desenvolvimento:**
   ```bash
   python manage.py runserver
   ```

6. **Acesse o Django Admin:**
   Abra o navegador e acesse `http://127.0.0.1:8000/admin/`. Faça o login com o superusuário criado no passo 4.

## Como testar o fluxo (Pedido -> Pagamento -> Cozinha)

A regra de negócio central define que um pedido só deve ser enviado para a cozinha após a confirmação do pagamento. Você pode testar esse fluxo completo diretamente pelo Django Admin utilizando uma ação customizada:

1. Vá em **Cardápio > Itens de Cardápio** e crie alguns itens (ex: Hambúrguer, Refrigerante) informando o nome e o preço.
2. Vá em **Pedidos > Pedidos**.
3. Crie um novo pedido escolhendo o status "Pendente" e, na mesma tela, adicione os itens a esse pedido utilizando a seção de Itens do Pedido. Salve o pedido. (O total será calculado automaticamente).
4. Na listagem de pedidos, **marque o quadradinho (checkbox)** do pedido que você acabou de criar (ele deve estar como PENDENTE).
5. No menu suspenso **"Ação"** (fica logo acima da lista de pedidos), selecione: **"Processar Pagamento (Simular fluxo completo)"**.
6. Clique no botão **"Ir"**.
7. A página vai "carregar" por cerca de 5 segundos. Isso simula a latência (demora) real de uma API de pagamento.
8. Ao terminar, você verá:
   * Uma mensagem de sucesso verde no topo da tela do Admin.
   * O status do pedido na lista mudará automaticamente para **Enviado à Cozinha**.
   * Se você for em **Pagamento > Transações**, verá que uma transação aprovada foi criada para aquele pedido com o valor exato.
   * Se você for em **Notificação > Logs Notificação**, verá o log registrado avisando a cozinha para preparar o pedido.
