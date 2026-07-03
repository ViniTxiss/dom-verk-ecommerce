# 📝 Registro de Contexto & IA Handoff — DOM VERK

> [!NOTE]
> **Olá, Assistente de IA!** Este arquivo foi criado para servir como um ponto de persistência de contexto e handoff entre sessões. Leia este documento com atenção para entender exatamente onde o projeto parou, a arquitetura de decisões e quais são as próximas tarefas prioritárias, economizando seus tokens de contexto e tempo de pesquisa.

---

## 🚦 Status Atual do Desenvolvimento

- **Branch Ativa:** `master`
- **Ambiente:** Local (`DEBUG=True`, banco SQLite local `db.sqlite3`).
- **Estado Geral:** MVP (Mínimo Produto Viável) estruturado e funcional. 
  - Catálogo de produtos, filtros e variantes funcionando.
  - Adição/remoção/atualização assíncrona do carrinho via sessões (sem necessidade de login) funcionando.
  - Fluxo de Checkout básico (coleta de endereço e criação de pedido) operando.
  - Painel de administração (Dashboard) customizado com controle de pedidos e CRUD de produtos ativo.

---

## 🔑 Decisões de Arquitetura & Padrões Importantes

Para evitar reescrever ou quebrar padrões estabelecidos no código, siga estas regras:

1. **Modelo de Usuário Customizado:** 
   - O projeto utiliza `apps.accounts.models.CustomUser` como `AUTH_USER_MODEL` (configurado em `core/settings.py`). Ele possui campos adicionais como `phone`, `cpf`, `birth_date` e o endereço padrão (`address_street`, `address_number`, etc.).
2. **Carrinho em Sessão (Session-Based Cart):**
   - Implementado na classe `Cart` em `apps/cart/cart.py`.
   - Injetado nos templates globais através do context processor `apps.cart.context_processors.cart_context` em `core/settings.py` (expõe a variável `cart` em qualquer template).
   - O frontend interage com o carrinho enviando requisições AJAX POST que retornam JSON. O arquivo JS responsável é [cart.js](file:///c:/Users/vini/Desktop/projetos/E-COMMERCE/static/js/cart.js).
3. **Variantes de Produtos (Estoque):**
   - O estoque não é gerenciado diretamente no modelo `Product`, mas sim no `ProductVariant` (`apps/products/models.py`), que associa um produto a uma combinação única de `color` (Preto, Branco, etc.) e `size` (PP a 4GG). 
   - Lembre-se disso ao atualizar o carrinho ou verificar disponibilidade de estoque!
4. **Estilização e Animações:**
   - **Estilo:** Baseado em Vanilla CSS moderno com tema escuro (Dark Mode premium). Os arquivos principais ficam em `static/css/main.css` e `static/css/components/pages.css`. Evite frameworks como Tailwind, a menos que explicitamente solicitado.
   - **Animações:** Utiliza **GSAP** e **AOS (Animate On Scroll)** importados no rodapé do [base.html](file:///c:/Users/vini/Desktop/projetos/E-COMMERCE/templates/base.html).

---

## 🔄 Histórico Recente de Alterações

- **Correção de Scroll:** Resolvido o bloqueio de rolagem da página inicial (`home/index.html`).
- **Páginas Institucionais:** Templates e rotas para Privacidade, Termos de Uso, Trocas, Sobre Nós e Guia de Tamanhos.
- **Links placeholders:** Substituídos todos os `href="#"` do cabeçalho e rodapé por rotas reais.
- **Seed Data (script):** [seed_data.py](file:///c:/Users/vini/Desktop/projetos/E-COMMERCE/scripts/seed_data.py) — apenas para uso local.
- **Management Command `seed`:** Criado `apps/products/management/commands/seed.py` — roda com `python manage.py seed`. **Este é o comando a rodar no Railway para popular o PostgreSQL de produção.** Idempotente.
- **Footer social links:** Corrigidos os 3 `href="#"` de Instagram, TikTok e WhatsApp com URLs reais (perfis domverk). ⚠️ O número do WhatsApp em `footer.html` (linha 50) está como `5511999999999` — substitua pelo número real.
- **Integração do Painel Admin:** Configurado o redirecionamento automático de usuários administradores (`is_staff`) diretamente para o painel após o login no site (`/conta/entrar/`). Adicionados atalhos condicionais de acesso ao painel (ícone de grade no desktop e link no menu mobile) visíveis apenas para perfis administradores.
- **Simulação de Pagamento (PIX, Cartão e Boleto):** Implementado o simulador de pagamento diretamente na tela de confirmação de pedidos (`confirmation.html`). Criada a view `simulate_payment` em `apps/orders/views.py` que altera o status do pedido de 'pending' para 'paid' após o clique no botão de simulação correspondente ao método escolhido (geração de QR Code dinâmico para PIX, dados fictícios para Cartão ou boleto bancário simulado).
- **Tradução de Termos:** Alteração de "Flash Deals" para "Oferta Relâmpago" na navegação desktop/mobile, cabeçalho, rodapé, barra de anúncio e painel de administração de produtos.
- **Integração de Produtos FIOTECH:** Substituição total do catálogo antigo por 5 novos produtos da FIOTECH (Camiseta Dryfit, Conjunto Top/Legging, Short Fitness, Top Nadador e Camiseta Oversized). Foram geradas imagens premium via IA para cada produto, criadas novas categorias (Fitness, Feminino, Conjuntos), adicionadas cores (Rosa, Café, Capuccino) com migração de banco e correção de colisão de SKUs.
- **Vídeo de Background no Hero:** Substituição da imagem de fundo estática no hero da página inicial por um loop de vídeo em tela cheia (`Black_t-shirt_with_print_202607022204.mp4`), estilizado para preenchimento cover responsivo.

---

## 🎯 Próximas Mudanças (Backlog Priorizado para a IA)

Caso os créditos da IA anterior tenham acabado, a IA atual deve começar pela **Prioridade 1** ou pela instrução explícita do usuário:

### 🟩 Prioridade 1: Otimização de Imagens (Lazy-Loading & SEO)
*   **O que fazer:** Adicionar o atributo `loading="lazy"` nas tags de imagens do catálogo (Home e Loja) e otimizar assets.
*   **Onde alterar:** `templates/home/index.html` e `templates/products/list.html`.
*   **Foco técnico:** Evitar que imagens pesadas travem o carregamento inicial da página.

### 🟨 Prioridade 2: Autocompletar CEP Dinâmico no Checkout (ViaCEP)
*   **O que fazer:** Integrar o formulário de checkout com a API ViaCEP via JavaScript assíncrono (AJAX). Ao preencher o CEP com 8 dígitos, os campos de Rua, Bairro, Cidade e Estado devem ser preenchidos automaticamente.
*   **Onde alterar:** `templates/orders/checkout.html` (ou script correspondente) e lógica de form.
*   **Foco técnico:** UX (Experiência do Usuário) fluida e sem recarregamento de página.

### 🟥 Prioridade 3: Sistema de Cupons de Desconto
*   **O que fazer:** Criar modelo `Coupon` (código, porcentagem/valor fixo, validade e ativo). Integrar aplicação de cupons no carrinho e na sessão de checkout com atualização dinâmica do total.

---

## 🛠️ Comandos de Terminal Úteis

- **Iniciar Servidor:** `python manage.py runserver`
- **Fazer Migrações:** `python manage.py makemigrations` e `python manage.py migrate`
- **Popular Banco:** `python scripts/seed_data.py`
- **Criar Superusuário (Admin):** `python manage.py createsuperuser`
- **Instalar Dependências:** `pip install -r requirements.txt`

---

## 📂 Mapa Rápido de Lógica do Projeto

- 🛒 **Carrinho (Backend):** [cart.py](file:///c:/Users/vini/Desktop/projetos/E-COMMERCE/apps/cart/cart.py)
- 🛒 **Carrinho (Frontend JS):** [cart.js](file:///c:/Users/vini/Desktop/projetos/E-COMMERCE/static/js/cart.js)
- 📦 **Checkout e Pedidos:** [models.py](file:///c:/Users/vini/Desktop/projetos/E-COMMERCE/apps/orders/models.py) & [forms.py](file:///c:/Users/vini/Desktop/projetos/E-COMMERCE/apps/orders/forms.py)
- 👕 **Produtos e Filtros:** [models.py](file:///c:/Users/vini/Desktop/projetos/E-COMMERCE/apps/products/models.py) & [views.py](file:///c:/Users/vini/Desktop/projetos/E-COMMERCE/apps/products/views.py)
- 👤 **CustomUser (Contas):** [models.py](file:///c:/Users/vini/Desktop/projetos/E-COMMERCE/apps/accounts/models.py)
