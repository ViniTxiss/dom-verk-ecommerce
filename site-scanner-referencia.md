# 🔍 Site Scanner — Referências de Design para Lojas de Camisetas
> Documento de análise estrutural para uso como contexto em prompts de geração de UI/frontend
> Gerado por análise de: `web_fetch` + `web_search` estrutural
> Sites analisados: True Classic Tees (BR) · Chico Rei (produto) · Carnan

---

## Como usar este documento

Cole este arquivo inteiro como contexto no início do seu prompt de geração de UI.
Diga ao modelo: _"Use as referências abaixo para guiar as decisões de design."_
Escolha o perfil que mais se alinha à sua marca, ou misture elementos dos três.

---

## 📊 Comparativo Rápido dos Três Perfis

| Dimensão | True Classic | Chico Rei | Carnan |
|---|---|---|---|
| **Arquétipo** | Performance + Conversão | Cultura + Comunidade | Lifestyle + Moda |
| **Tom de voz** | Direto, masculino, orientado a resultado | Bem-humorado, irreverente, cultural | Editorial, sofisticado, silencioso |
| **Modelo de negócio** | Bundle / multi-pack | Estampa única / coleção de artistas | Drops sazonais / lookbook |
| **Urgência** | Alta (Flash Deals, timer, desconto) | Baixa-média (ofertas pontuais) | Baixa (escassez implícita) |
| **Prova social** | Estrelas, % de satisfação, UGC | Comunidade, GPTW, selos éticos | Lookbook, editorial |
| **Público-alvo** | Homem 25–45, prático, quer fit | Criativo, engajado culturalmente | Consumidor de moda, 20–35 |
| **Paleta percebida** | Preto, branco, vermelho de CTA | Branco, preto, estampas coloridas | Off-white, preto, tons neutros |
| **Tipografia** | Sans-serif bold, impacto imediato | Sans-serif clean, legível | Serif fina + sans clean |
| **Hero** | Banner com desconto + produto em destaque | Produto + copy cultural | Vídeo ou foto editorial fullscreen |
| **Nav** | Megamenu por categoria de produto | Horizontal simples por gênero/tipo | Megamenu fotográfico |

---

## 1. TRUE CLASSIC TEES
**URL:** `https://www.trueclassictees.com/en-br`
**Perfil:** E-commerce de conversão agressiva — DTC americano adaptado para Brasil

### 1.1 Estrutura de Página (ordem das seções)
```
[Announce Bar] → desconto com código + urgência temporal
[Nav Principal] → logo centralizado + megamenu + busca + conta + cart
[Hero Banner] → imagem fullscreen + CTA duplo (Shop All / Shop Clearance)
[Category Grid] → ícones de categoria (Short Sleeves, Long Sleeves, etc.)
[Flash Deals] → timer regressivo + produtos em oferta relâmpago
[Variety Packs] → destaque para packs (maior ticket médio)
[Social Proof] → reviews com estrelas, % de satisfação
[Brand Promise] → "Butter soft", "Slim fit", "87% feel more buff"
[Footer] → links utilitários + formas de pagamento
```

### 1.2 Announce Bar
- **Posição:** topo fixo, acima do nav
- **Conteúdo:** `[emoji] Texto de oferta [código] [emoji] Flash Deals [link CTA]`
- **Padrão de copy:** sempre dois elementos — desconto + urgência
- **Exemplo real:** `"Summer Sale! Save 20%"` + `"⚡ Flash Deals Ending Soon [Claim Now]"`
- **Background:** preto (`#000`) / texto branco / CTA em sublinhado ou destaque colorido

### 1.3 Navegação
- **Estrutura:** Logo (esquerda) + Links principais (centro) + Ações (direita)
- **Links principais:** Men | Women | Flash Deals ⚡️ | Top Rated | We Made Too Much | Our Story
- **Megamenu por gênero:** subdivide em Short Sleeves / Long Sleeves / Bottoms / Outerwear / Activewear / Dress Shirts / Boxers & More / Tall
- **Padrão de nomenclatura:** categorias em inglês mesmo no Brasil — sinaliza posicionamento premium internacional
- **Ações no nav:** Busca | Conta | Cart com contador numérico
- **Observação UX:** "Flash Deals ⚡️" com emoji no nav — cria hierarquia visual de urgência dentro da própria navegação

### 1.4 Copy / Tom de Voz
- **Estilo:** Benefit-led, direto, sem rodeios
- **Fórmula hero:** `[Problema] → [Solução com número]`
- **Exemplos reais extraídos:**
  - _"We didn't just make another T-shirt... we created the T-shirt."_
  - _"A Fit That Makes 87% Of Guys Feel More Buff"_
  - _"So Soft, You'll Never Take It Off"_
  - _"Built To Last — And Outlast"_
  - _"Problem: Baggy, unflattering fit. Solution: Fits that sharpen your look"_
- **Padrão:** sempre métricas (87%, 81%, 100 days), sempre benefício concreto
- **Garantia:** _"Perfect Fit, Made to Last Guarantee — 100 days, replace for free, no questions asked"_

### 1.5 Produto
- **Widget "Find My Fit":** altura + peso + tipo de caimento desejado → recomendação automática
- **Pack Builder:** cliente monta packs e economiza — aumenta ticket médio
- **Flash Deals:** timer regressivo visível na categoria e no nav
- **Imagens:** lifestyle com modelo masculino jovem/médio, fundo limpo ou ambiente casual
- **Sizing copy:** _"Between sizes? Size up for relaxed, down for fitted."_

### 1.6 Paleta e Tipografia (inferida)
```
Background: #FFFFFF / #000000
CTA primário: preto sólido ou vermelho (urgência)
CTA secundário: outline preto
Texto body: sans-serif system / Inter
Heading: bold pesado, todas-maiúsculas ou sentence case
Accent de urgência: vermelho ou amarelo (Flash Deals)
```

### 1.7 Social Proof Pattern
- Estrelas (4.8/5.0 ou similar) em destaque no hero ou logo abaixo
- Número total de reviews (ex: "50,000+ reviews")
- % de satisfação com copy específico ("87% feel more buff", "81% feel more confident")
- UGC de influenciadores mas sem criar canal próprio no YouTube (oportunidade identificada)

### 1.8 Footer
- Links agrupados: Help / Company / Follow Us
- Store locator (lojas físicas)
- Formas de pagamento em ícones
- App download badges

---

## 2. CHICO REI
**URL:** `https://chicorei.com/camiseta/camiseta-picos-do-brasil-19765.html`
**Perfil:** Marketplace cultural brasileiro — estampas com propósito, artistas independentes

### 2.1 Identidade de Marca (resumo executivo)
- Fundada 2008, Juiz de Fora/MG — R$ 35M de faturamento em 2025
- +3.000 criações inéditas, +500k peças/ano
- Parcerias com ícones da cultura brasileira (Milton Nascimento, etc.)
- Selos: GPTW, PETA Approved Vegan, Better Cotton Initiative (BCI), Pacto Global ONU
- Nova plataforma "Uma Penca" — qualquer pessoa cria e vende estampas usando estrutura Chico Rei

### 2.2 Estrutura de Página de Produto (PDP)
```
[Nav] → logo + categorias horizontais (Novidades | Feminino | Masculino | Infantil | Acessórios | Casa | Collabs | Ofertas)
[Breadcrumb] → Home > Categoria > Produto
[Galeria de Produto] → imagem principal + thumbs (múltiplos ângulos)
[Info do Produto]:
  - Nome + Artista (ex: "Camiseta Picos do Brasil - Nicolle Bello")
  - Preço + parcelamento (4x s/juros)
  - Seletor de cor de malha
  - Seletor de tamanho (PP, P, M, G, GG, 2GG, 3GG, 4GG)
  - Botão "Comprar" + "Adicionar à sacola"
  - Copy da estampa (texto cultural/criativo sobre o design)
[Selos de Qualidade] → PETA, BCI, GPTW inline
[Produtos Relacionados] → "Você também pode gostar"
[Seção Impacto] → 4 pilares (Impacto Social / Produtos Sustentáveis / Criação / Impacto Ambiental)
[Footer] → 3 colunas (Ajuda / Sobre / Empresa) + redes sociais + métodos de pagamento + selos legais
```

### 2.3 Copy de Produto (padrão Chico Rei)
- **Fórmula:** Copy poético/literário sobre o conceito da estampa, não sobre o produto em si
- **Exemplo real:** _"A camiseta Picos do Brasil estampa uns lugares altos que mesmo nos deixando pequenos, faz a gente crescer. Vai entender, né?"_
- **Tom:** coloquial mineiro, bem-humorado, cúmplice com o comprador
- **Nunca fala de:** tecido, caimento, durabilidade no primeiro parágrafo — fala de ideia
- **Regra de ouro:** a estampa tem uma história, o produto é o veículo

### 2.4 Tamanhos e Inclusão
- **Range:** PP ao 4GG (muito maior que concorrentes)
- **Copy de tamanho:** orientado a ajudar, sem julgamento de corpo
- **Modelagens:** unissex por padrão em muitos produtos

### 2.5 Proposta de Valor — 4 Pilares do Footer
```
1. IMPACTO SOCIAL
   "Geramos relações de trabalho justas e inclusivas, fazendo a conexão entre 
   o time, a comunidade e os nossos clientes. Desde 2021, certificados GPTW."

2. PRODUTOS SUSTENTÁVEIS E VEGANOS
   "Matéria-prima certificada Better Cotton Initiative e PETA Approved Vegan."

3. CRIAR É A NOSSA ALMA
   "+3.000 criações inéditas + royalties para artistas independentes."

4. IMPACTO AMBIENTAL REDUZIDO
   "Zero Plástico em todos os pedidos + compensação ambiental."
```

### 2.6 Navegação
- **Estrutura:** simples, horizontal, sem megamenu fotográfico
- **Categorias:** Novidades | Feminino | Masculino | Infantil | Acessórios | Casa | Collabs | Ofertas
- **Destaque:** "Collabs" — sinaliza que parcerias com artistas são feature, não exceção
- **Mobile-first:** barra de busca proeminente

### 2.7 Métodos de Pagamento (relevante para mercado BR)
- Mastercard, Visa, Elo, Amex, Hipercard, **PIX**
- PIX como método destacado — alinhado com realidade brasileira
- Parcelamento 4x sem juros em destaque

### 2.8 Paleta e Tipografia (inferida)
```
Background: #FFFFFF puro
Texto: #000000 / #333333
Accent: cor variável por estampa (marca é a estampa, não a cor da loja)
CTA: preto ou cor primária da marca
Tags/Selos: pequenos, discretos, em rodapé ou próximos ao produto
Nav: preto sobre branco, letras em lowercase ou capitalize
```

### 2.9 Redes Sociais (presença multicanal)
Instagram · Twitter/X · Facebook · TikTok · Pinterest · YouTube · **Spotify** · Prosa (blog)
- Spotify e Prosa diferenciam: marca com curadoria cultural, não só fashion

---

## 3. CARNAN
**URL:** `https://www.carnan.com.br`
**Perfil:** Lifestyle premium brasileiro — inspiração em viagens, drops sazonais, editorial

### 3.1 Estrutura de Página
```
[Announce Bar] → desconto código + PIX
[Nav] → logo centro + links + cart
[Hero] → vídeo fullscreen autoplay (sem som) → link para lançamentos
[Split Man / Woman] → duas imagens fullscreen lado a lado
[Products Grid] → grid de produtos sem molduras
[Footer] → 4 colunas + links sociais
```
_(Análise detalhada feita no scan anterior — ver VANE como implementação)_

### 3.2 Padrões Únicos da Carnan
- **Vídeo hero** sem CTA visível — confiar no produto em si puxar atenção
- **Megamenu fotográfico** — hover abre painel com imagens de categoria
- **Nomenclatura bilíngue:** "Tops/Partes de cima", "Bottoms/Parte de baixo" — sinaliza aspiração internacional
- **Announce bar duplo:** desconto na primeira compra + PIX = dois motivadores simultâneos
- **WhatsApp** como canal de suporte primário
- **Store locator** (lojas físicas em markets/shoppings)

---

## 🧰 Prompt Template para Geração de UI

Use o bloco abaixo como base. Substitua os `[VARIÁVEIS]` conforme seu projeto.

```
Você é um designer de produto especialista em e-commerce de moda.

OBJETIVO: Criar uma [landing page / página de produto / homepage] para uma loja de camisetas brasileira.

MARCA:
- Nome: [NOME]
- Arquétipo: [escolha: Conversão (True Classic) / Cultural (Chico Rei) / Lifestyle (Carnan)]
- Público: [ex: homens 20-35, urban, renda B/C]
- Tom de voz: [ex: direto e confiante / bem-humorado e cultural / editorial e silencioso]

REFERÊNCIAS COMBINADAS:
- Estrutura de seções: baseada em [True Classic / Chico Rei / Carnan]
- Copy pattern: use o padrão [benefit-led numérico (TC) / poético-cultural (CR) / editorial mínimo (Carnan)]
- Paleta: [descreva sua paleta ou diga "derive das referências"]
- Urgência: [Alta com timer / Média com edição limitada / Baixa com escassez implícita]

SEÇÕES OBRIGATÓRIAS:
1. Announce Bar: [código de desconto] + [PIX ou frete grátis]
2. Nav: [megamenu fotográfico (Carnan) / megamenu por categoria (TC) / horizontal simples (CR)]
3. Hero: [banner com desconto (TC) / vídeo editorial (Carnan) / produto cultural (CR)]
4. [Seção específica do arquétipo — ver abaixo]
5. Grid de produtos: 4 colunas, hover com add-to-cart
6. Proposta de valor: 3-4 pilares (ícone + título + texto curto)
7. Email capture: campo minimalista
8. Footer: 3-4 colunas + métodos de pagamento BR (incluir PIX) + redes sociais

SEÇÃO ESPECÍFICA POR ARQUÉTIPO:
- True Classic: "Find My Fit" widget + Flash Deals com timer + Pack Builder CTA
- Chico Rei: Seção de artista/collab + selos éticos + copy cultural do produto
- Carnan: Split Man/Woman fullscreen + ticker animado + lookbook editorial

COPY DE PRODUTO (escolha o padrão):
- True Classic: "[Problema]. [Solução com métrica]. [Garantia em X dias]."
- Chico Rei: "[Metáfora poética sobre o conceito da estampa]. [Convite coloquial]."
- Carnan: "[Título da coleção]. [Uma frase. Ponto.] [Temporada e ano]."

TECH STACK: HTML + CSS + JS vanilla (sem frameworks)
TIPOGRAFIA: [Space Grotesk bold (TC/BLOCK) / Inter + Cormorant (Carnan/VANE) / system-sans (CR)]
IMAGENS: use Unsplash como placeholder — fashion, modelo wearing tshirt, lookbook

RESTRIÇÕES DE DESIGN:
- Sem cara de IA: proibido cream + terracota + serif + número 01/02/03
- Sem gradientes decorativos
- Sem ícones de emoji no corpo do texto
- Bordas finas (0.5px) ou sem bordas
- Espaçamento generoso — respira antes de decorar
- Um elemento de assinatura único (o que torna inesquecível)

OUTPUT ESPERADO: HTML completo, auto-contido, pronto para abrir no browser.
```

---

## 📋 Checklist de Qualidade — Use antes de entregar qualquer UI

### Conversão (True Classic mindset)
- [ ] Announce bar com oferta clara e código
- [ ] Timer ou indicador de urgência (se produto limitado)
- [ ] CTA primário visível acima da dobra sem scroll
- [ ] Prova social próxima ao CTA (estrelas ou número)
- [ ] Garantia mencionada explicitamente
- [ ] PIX como método de pagamento destacado

### Identidade (Chico Rei mindset)
- [ ] Copy do produto conta uma história, não lista especificações
- [ ] Selos de qualidade/ética visíveis mas discretos
- [ ] Range de tamanho inclusivo (até 4GG se possível)
- [ ] Artista ou origem da estampa creditado
- [ ] Tom de voz consistente do nav ao footer

### Estética (Carnan mindset)
- [ ] Hero respira — não sobrecarregado com texto
- [ ] Tipografia tem caráter (não é Arial/Roboto default)
- [ ] Um único elemento de cor ou acento (não três)
- [ ] Hover states em todos os elementos clicáveis
- [ ] Imagens com qualidade editorial, não foto de catálogo
- [ ] Footer limpo e funcional, não amontoado

### Técnico
- [ ] Sticky nav sem salto de layout
- [ ] Imagens com fallback (onerror) para quando Unsplash não carrega
- [ ] Ticker animado com loop infinito sem piscar
- [ ] Mobile responsivo (min-width 320px)
- [ ] Sem `console.error` em produção
- [ ] Acessibilidade básica: alt em imagens, labels em inputs

---

## 🔄 Matriz de Combinação — Escolha seus ingredientes

| Elemento | Opção A (TC) | Opção B (CR) | Opção C (Carnan) |
|---|---|---|---|
| Hero | Banner + desconto + CTA duplo | Produto + copy cultural | Vídeo/foto fullscreen editorial |
| Urgência | Timer + Flash Deals | Edição limitada (unidades) | Drops semanais implícitos |
| Copy principal | Benefício numérico | Poesia coloquial | Uma frase. Ponto. |
| Prova social | Stars + % satisfação | Comunidade + selos éticos | Lookbook + editorial |
| Produto grid | 4-6 colunas compactas | Grid com copy de estampa | 3-4 colunas com hover editorial |
| Nav megamenu | Por categoria de produto | Simples por tipo/gênero | Fotográfico com imagens |
| Footer depth | Alto (muitos links) | Médio + proposta ética | Baixo (essencial) |
| CTA cor | Preto/vermelho bold | Cor da marca variável | Preto outline ou fundo |

---

## 📌 Observações de Mercado Brasil

**PIX é obrigatório:** os três sites mencionam. Não é opcional — é expectativa do consumidor BR.

**Parcelamento:** destaque "4x sem juros" ou "até 10x" — parte do processo decisório.

**Frete grátis:** threshold visível no announce bar (R$200, R$300 etc.).

**WhatsApp como suporte:** Carnan e Chico Rei usam. True Classic usa e-mail/telefone (modelo americano).

**Tamanhos:** Chico Rei vai até 4GG — diferencial de inclusão. TC faz linha "Tall". Oportunidade para marcas emergentes.

**Artistas/Collabs:** Chico Rei construiu metade do faturamento com collabs culturais. Modelo replicável para marcas nicho.

---

_Documento gerado por: web_fetch + web_search estrutural em junho/2025_
_Para regenerar/atualizar: refaça fetch dos URLs base e atualize as seções marcadas como [DATA-SENSÍVEL]_
