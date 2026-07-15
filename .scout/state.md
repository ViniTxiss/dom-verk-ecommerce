# Registro de Execuções do Scout

## 2026-06-30 — Integração do Painel Administrativo no Site
Status: concluído
Motivo/resultado: Redirecionamento de administradores pós-login para o painel administrativo e exibição de links de atalho na navbar e menu mobile condicionalmente para usuários staff.
Arquivos tocados:
- [apps/accounts/views.py](file:///c:/Users/vini/Desktop/projetos/E-COMMERCE/apps/accounts/views.py)
- [templates/partials/navbar.html](file:///c:/Users/vini/Desktop/projetos/E-COMMERCE/templates/partials/navbar.html)

## 2026-06-30 — Simulação de Pagamento (PIX, Cartão e Boleto)
Status: concluído
Motivo/resultado: Criado o simulador de pagamento interativo na tela de confirmação de pedido com rotas e views de simulação para PIX, Cartão e Boleto, atualizando o status do pedido para 'paid' (Pago) após aprovação simulada.
Arquivos tocados:
- [apps/orders/views.py](file:///c:/Users/vini/Desktop/projetos/E-COMMERCE/apps/orders/views.py)
- [apps/orders/urls.py](file:///c:/Users/vini/Desktop/projetos/E-COMMERCE/apps/orders/urls.py)
- [apps/orders/templatetags/order_filters.py](file:///c:/Users/vini/Desktop/projetos/E-COMMERCE/apps/orders/templatetags/order_filters.py)
- [templates/orders/confirmation.html](file:///c:/Users/vini/Desktop/projetos/E-COMMERCE/templates/orders/confirmation.html)
- [apps/orders/tests.py](file:///c:/Users/vini/Desktop/projetos/E-COMMERCE/apps/orders/tests.py)


## 2026-07-02 — Alterar nomenclatura de "Flash Deals" para "Oferta Relâmpago"
Status: concluído
Motivo/resultado: Tradução do termo nos arquivos de template da loja (navegação, hero, rodapé, barra de anúncio e painel administrativo).
Arquivos tocados:
- [templates/dashboard/product_form.html](file:///c:/Users/vini/Desktop/projetos/E-COMMERCE/templates/dashboard/product_form.html)
- [templates/dashboard/products.html](file:///c:/Users/vini/Desktop/projetos/E-COMMERCE/templates/dashboard/products.html)
- [templates/home/index.html](file:///c:/Users/vini/Desktop/projetos/E-COMMERCE/templates/home/index.html)
- [templates/partials/announce_bar.html](file:///c:/Users/vini/Desktop/projetos/E-COMMERCE/templates/partials/announce_bar.html)
- [templates/partials/footer.html](file:///c:/Users/vini/Desktop/projetos/E-COMMERCE/templates/partials/footer.html)
- [templates/partials/navbar.html](file:///c:/Users/vini/Desktop/projetos/E-COMMERCE/templates/partials/navbar.html)


## 2026-07-02 — Integração de Produtos FIOTECH
Status: concluído
Motivo/resultado: Substituição do catálogo mock pelos produtos FIOTECH conforme plano aprovado, gerando novas imagens por IA, adicionando cores no modelo (Rosa, Café, Capuccino) com migração e corrigindo colisões de SKUs no ProductVariant.
Arquivos tocados:
- [apps/products/models.py](file:///c:/Users/vini/Desktop/projetos/E-COMMERCE/apps/products/models.py)
- [apps/products/management/commands/seed.py](file:///c:/Users/vini/Desktop/projetos/E-COMMERCE/apps/products/management/commands/seed.py)
- [scripts/seed_data.py](file:///c:/Users/vini/Desktop/projetos/E-COMMERCE/scripts/seed_data.py)
- [contexto.md](file:///c:/Users/vini/Desktop/projetos/E-COMMERCE/contexto.md)


## 2026-07-02 — Vídeo de Background no Hero
Status: concluído
Motivo/resultado: Substituição da imagem estática do hero por um player de vídeo em autoplay, loop e mute, carregando a mídia Black_t-shirt_with_print_202607022204.mp4.
Arquivos tocados:
- [templates/home/index.html](file:///c:/Users/vini/Desktop/projetos/E-COMMERCE/templates/home/index.html)
- [static/css/main.css](file:///c:/Users/vini/Desktop/projetos/E-COMMERCE/static/css/main.css)


## 2026-07-12 — Otimização de Imagens (Lazy-Loading & SEO)
Status: concluído
Motivo/resultado: Adicionado o atributo loading="lazy" em todas as tags de imagens dos templates do catálogo, home e checkout.
Arquivos tocados:
- [templates/partials/product_card.html](file:///c:/Users/vini/Desktop/projetos/E-COMMERCE/templates/partials/product_card.html)
- [templates/home/index.html](file:///c:/Users/vini/Desktop/projetos/E-COMMERCE/templates/home/index.html)
- [templates/orders/checkout.html](file:///c:/Users/vini/Desktop/projetos/E-COMMERCE/templates/orders/checkout.html)

## 2026-07-12 — Autocompletar CEP Dinâmico no Checkout (ViaCEP)
Status: concluído
Motivo/resultado: Implementada integração com a API ViaCEP no formulário de checkout via JavaScript assíncrono (fetch). Ao preencher 8 dígitos no campo de CEP, os campos de rua, bairro, cidade e UF são preenchidos automaticamente.
Arquivos tocados:
- [templates/orders/checkout.html](file:///c:/Users/vini/Desktop/projetos/E-COMMERCE/templates/orders/checkout.html)

## 2026-07-12 — Sistema de Cupons de Desconto
Status: concluído
Motivo/resultado: Criado modelo Coupon com migração, views AJAX de aplicar/remover cupom, suporte a cupons em porcentagem e valor fixo, integração com o checkout e registro no Django Admin.
Arquivos tocados:
- [apps/orders/models.py](file:///c:/Users/vini/Desktop/projetos/E-COMMERCE/apps/orders/models.py)
- [apps/orders/admin.py](file:///c:/Users/vini/Desktop/projetos/E-COMMERCE/apps/orders/admin.py)
- [apps/orders/migrations/0002_coupon_order_coupon.py](file:///c:/Users/vini/Desktop/projetos/E-COMMERCE/apps/orders/migrations/0002_coupon_order_coupon.py)
- [apps/cart/cart.py](file:///c:/Users/vini/Desktop/projetos/E-COMMERCE/apps/cart/cart.py)
- [apps/cart/views.py](file:///c:/Users/vini/Desktop/projetos/E-COMMERCE/apps/cart/views.py)
- [apps/cart/urls.py](file:///c:/Users/vini/Desktop/projetos/E-COMMERCE/apps/cart/urls.py)
- [apps/orders/views.py](file:///c:/Users/vini/Desktop/projetos/E-COMMERCE/apps/orders/views.py)
- [templates/orders/checkout.html](file:///c:/Users/vini/Desktop/projetos/E-COMMERCE/templates/orders/checkout.html)
- [apps/orders/tests.py](file:///c:/Users/vini/Desktop/projetos/E-COMMERCE/apps/orders/tests.py)
- [apps/products/management/commands/seed.py](file:///c:/Users/vini/Desktop/projetos/E-COMMERCE/apps/products/management/commands/seed.py)

## 2026-07-13 — Security — Auditoria Completa OWASP + Hardening
Status: concluído
Motivo/resultado: 9 vulnerabilidades encontradas (2 críticas, 2 altas, 3 médias, 2 baixas). 6 corrigidas nesta sessão. Severidade máxima: Crítico → Corrigido.
Correções aplicadas:
  - [C1] simulate_payment sem autenticação → verificação _can_access_order() + session tracking
  - [C2] order_confirmation expunha dados de terceiros → mesma proteção _can_access_order()
  - [A1] Headers de segurança HTTP ausentes → bloco de settings adicionado em core/settings.py
  - [A2] logout via GET (CSRF logout) → @require_POST + formulários POST nos 3 templates
  - [M1] Upload de imagem sem validação MIME → _validate_image() em create/edit do dashboard
  - [M2] Open Redirect após login → url_has_allowed_host_and_scheme() em accounts/views.py
Pendentes (aguardam decisão CEO):
  - [M3] CPF em texto puro (LGPD) → requer lib django-encrypted-model-fields + migration
  - [B1] Sem rate limiting no login → requer lib django-axes
  - [B2] Processo: não usar dados reais em dev local
Arquivos tocados:
  - apps/orders/views.py
  - apps/accounts/views.py
  - apps/dashboard/views.py
  - core/settings.py
  - templates/partials/navbar.html
  - templates/accounts/profile.html
  - templates/dashboard/base_dashboard.html

## 2026-07-13 — Security — M3 CPF Criptografado (LGPD) + B1 Rate Limiting Login
Status: concluído
Motivo/resultado: CPF agora armazenado com AES via EncryptedCharField (django-encrypted-model-fields). Rate limiting ativo via django-axes — 5 tentativas falhas → bloqueio de 1h por IP+usuário. Todas as migrações aplicadas com sucesso.
Arquivos tocados:
  - apps/accounts/models.py (EncryptedCharField no CPF)
  - apps/accounts/migrations/0002_cpf_encrypted.py (nova migration)
  - core/settings.py (FIELD_ENCRYPTION_KEY, AXES_*, AUTHENTICATION_BACKENDS)

## 2026-07-13 — Bugfix — Correção de Erro 500 no Checkout (Decimal vs Float)
Status: concluído
Motivo/resultado: Identificado e corrigido TypeError 500 no fluxo de checkout (/pedidos/checkout/). O cálculo de frete (19.90 como float) e desconto PIX causava colisão de tipos com Decimal ao somar com subtotal. Ajustado para cálculo estrito em Decimal (Decimal('19.90') e Decimal('0.10')).
Arquivos tocados:


## 2026-07-13 — Scout — Painel Administrativo de Cupons (P1)
Status: concluído
Motivo/resultado: Implementado sistema de gerenciamento de cupons no Dashboard em /dashboard/cupons/. Suporte a criação, edição, busca por código, toggle de ativado/desativado instantâneo via POST e dashboard de estatísticas (total, ativos, usos). 48/48 testes automatizados passando.
Arquivos tocados:
  - apps/dashboard/forms.py (novo CouponForm)
  - apps/dashboard/views.py (views dashboard_coupons, create, edit, toggle)
  - apps/dashboard/urls.py (novas rotas)
  - templates/dashboard/base_dashboard.html (link na sidebar e icon)
  - templates/dashboard/coupons.html (novo template de listagem e estatísticas)

## 2026-07-13 — Scout — Feedback Amigável de Bloqueio por Tentativas (Rate Limit Login)
Status: concluído
Motivo/resultado: Criado o template premium dark mode `templates/accounts/lockout.html` para exibição em caso de lockout por rate limit (5 tentativas falhas de login). Configurado handler de exceção `AxesBackendPermissionDenied`/`PermissionDenied` no `login_view` e `AXES_LOCKOUT_TEMPLATE` no `settings.py`. Suíte de 52/52 testes passando 100% verde.
Arquivos tocados:
  - templates/accounts/lockout.html (novo template de bloqueio de segurança)
  - apps/accounts/views.py (tratamento de exceção de lockout no login_view)
  - core/settings.py (AXES_LOCKOUT_TEMPLATE)
  - apps/accounts/tests.py (suíte de testes unitários de accounts)


