import json

with open('data_bundle.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

# Custom seller profiles with capital consumption metrics
seller_profiles = [
    {"name": "Ricardo Aragão", "deals": 383, "wr": 48.3, "rec": 41209709.0, "glosa_p": 2407846.0, "tx_glosa": 5.8, "dso": 158.4, "ciclo": 220.6, "cap": 24910000.0},
    {"name": "Marcelo Bastos", "deals": 294, "wr": 48.3, "rec": 25464927.0, "glosa_p": 1098241.0, "tx_glosa": 4.3, "dso": 130.2, "ciclo": 172.5, "cap": 12030000.0},
    {"name": "Diego Fontes", "deals": 225, "wr": 47.1, "rec": 18829700.0, "glosa_p": 889932.0, "tx_glosa": 4.7, "dso": 142.2, "ciclo": 191.5, "cap": 9880000.0},
    {"name": "Rogério Lins", "deals": 232, "wr": 56.0, "rec": 17016028.0, "glosa_p": 581096.0, "tx_glosa": 3.4, "dso": 123.8, "ciclo": 162.8, "cap": 7590000.0},
    {"name": "Tatiana Coelho", "deals": 255, "wr": 49.4, "rec": 14325786.0, "glosa_p": 285663.0, "tx_glosa": 2.0, "dso": 97.9, "ciclo": 121.0, "cap": 4750000.0},
    {"name": "Paulo Menezes", "deals": 224, "wr": 54.0, "rec": 12870263.0, "glosa_p": 428130.0, "tx_glosa": 3.3, "dso": 116.5, "ciclo": 151.7, "cap": 5350000.0},
    {"name": "Cíntia Barbosa", "deals": 146, "wr": 54.8, "rec": 9748703.0, "glosa_p": 217559.0, "tx_glosa": 2.2, "dso": 112.0, "ciclo": 136.4, "cap": 3640000.0},
    {"name": "Luciana Prado", "deals": 101, "wr": 60.4, "rec": 7273293.0, "glosa_p": 204730.0, "tx_glosa": 2.8, "dso": 111.4, "ciclo": 143.8, "cap": 2870000.0},
    {"name": "Joana Rios", "deals": 150, "wr": 46.7, "rec": 6707086.0, "glosa_p": 92932.0, "tx_glosa": 1.4, "dso": 77.8, "ciclo": 93.2, "cap": 1710000.0},
    {"name": "Márcia Duarte", "deals": 94, "wr": 47.9, "rec": 5996502.0, "glosa_p": 209008.0, "tx_glosa": 3.5, "dso": 121.0, "ciclo": 158.0, "cap": 2600000.0},
    {"name": "Fábio Correia", "deals": 61, "wr": 52.5, "rec": 5118748.0, "glosa_p": 270548.0, "tx_glosa": 5.3, "dso": 151.2, "ciclo": 202.2, "cap": 2840000.0},
    {"name": "Ivan Peixoto", "deals": 57, "wr": 47.4, "rec": 5030073.0, "glosa_p": 273675.0, "tx_glosa": 5.4, "dso": 158.5, "ciclo": 216.0, "cap": 2980000.0},
    {"name": "Sérgio Tavares", "deals": 62, "wr": 45.2, "rec": 3554203.0, "glosa_p": 181319.0, "tx_glosa": 5.1, "dso": 135.3, "ciclo": 178.6, "cap": 1740000.0},
    {"name": "Verônica Sá", "deals": 62, "wr": 45.2, "rec": 2066915.0, "glosa_p": 51453.0, "tx_glosa": 2.5, "dso": 109.0, "ciclo": 139.4, "cap": 790000.0},
    {"name": "Anderson Melo", "deals": 25, "wr": 68.0, "rec": 1088074.0, "glosa_p": 31700.0, "tx_glosa": 2.9, "dso": 110.5, "ciclo": 140.8, "cap": 420000.0},
]

html_content = f"""<!DOCTYPE html>
<html lang="pt-BR" class="h-full bg-[#001716] text-[#E6E3D3]">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no">
  <title>FH Data • Inteligência Estratégica C-Suite</title>
  
  <!-- Tailwind CSS CDN -->
  <script src="https://cdn.tailwindcss.com"></script>
  <!-- Chart.js CDN -->
  <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
  <!-- Lucide Icons -->
  <script src="https://unpkg.com/lucide@latest"></script>
  
  <!-- Google Fonts: Plus Jakarta Sans -->
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@300;400;500;600;700;800&family=JetBrains+Mono:wght@400;500;600&display=swap" rel="stylesheet">
  
  <script>
    tailwind.config = {{
      theme: {{
        extend: {{
          fontFamily: {{
            sans: ['"Plus Jakarta Sans"', 'sans-serif'],
            mono: ['"JetBrains Mono"', 'monospace'],
          }},
          colors: {{
            fh: {{
              950: '#001716',
              900: '#00201F',
              850: '#002424',
              800: '#042F2F',
              750: '#063535',
              700: '#133B3A',
              600: '#183F3E',
              mint: '#2AC59E',
              'mint-light': '#52E1B9',
              'mint-dark': '#00BD97',
              sand: '#E6E3D3',
              'sand-light': '#FAF6E6',
              'sand-muted': '#CECABB',
              'sand-dark': '#B8C1BF',
              coral: '#FF6568',
              'coral-dark': '#EB5757',
              gold: '#E2B93B',
              cyan: '#C2EAE8',
            }}
          }}
        }}
      }}
    }}
  </script>

  <style>
    body {{
      font-family: 'Plus Jakarta Sans', sans-serif;
      background-color: #001716;
      color: #E6E3D3;
      -webkit-tap-highlight-color: transparent;
    }}
    
    /* FH Data Glass Card System */
    .fh-card {{
      background: rgba(0, 36, 36, 0.65);
      backdrop-filter: blur(16px);
      -webkit-backdrop-filter: blur(16px);
      border: 1px solid rgba(42, 197, 158, 0.15);
      box-shadow: 0 8px 32px 0 rgba(0, 23, 22, 0.37);
      transition: all 0.25s cubic-bezier(0.4, 0, 0.2, 1);
    }}
    .fh-card:hover {{
      border-color: rgba(42, 197, 158, 0.35);
      box-shadow: 0 12px 40px 0 rgba(42, 197, 158, 0.08);
    }}

    .fh-card-highlight {{
      background: linear-gradient(135deg, rgba(4, 47, 47, 0.8) 0%, rgba(0, 32, 31, 0.9) 100%);
      border: 1px solid rgba(42, 197, 158, 0.3);
    }}

    /* Glow Elements */
    .mint-glow {{
      box-shadow: 0 0 25px rgba(42, 197, 158, 0.25);
    }}
    .mint-glow-sm {{
      box-shadow: 0 0 12px rgba(42, 197, 158, 0.2);
    }}
    .coral-glow-sm {{
      box-shadow: 0 0 12px rgba(255, 101, 104, 0.2);
    }}

    /* Tab navigation active state */
    .fh-tab-active {{
      background: rgba(42, 197, 158, 0.15) !important;
      color: #2AC59E !important;
      border: 1px solid rgba(42, 197, 158, 0.4) !important;
      font-weight: 700;
    }}

    /* Custom Scrollbars */
    ::-webkit-scrollbar {{
      width: 5px;
      height: 5px;
    }}
    ::-webkit-scrollbar-track {{
      background: #001716;
    }}
    ::-webkit-scrollbar-thumb {{
      background: #133B3A;
      border-radius: 9999px;
    }}
    ::-webkit-scrollbar-thumb:hover {{
      background: #2AC59E;
    }}

    /* Mobile First Helpers */
    @media (max-width: 640px) {{
      .mobile-hide-scrollbar::-webkit-scrollbar {{
        display: none;
      }}
      .mobile-hide-scrollbar {{
        -ms-overflow-style: none;
        scrollbar-width: none;
      }}
    }}
  </style>
</head>

<body class="min-h-screen flex flex-col antialiased selection:bg-[#2AC59E] selection:text-[#001716]">

  <!-- Top Ambient Brand Light -->
  <div class="fixed top-0 left-1/2 -translate-x-1/2 w-[600px] h-[200px] bg-[#2AC59E]/10 blur-[120px] pointer-events-none z-0"></div>

  <!-- Header Bar -->
  <header class="sticky top-0 z-50 bg-[#001716]/90 backdrop-blur-xl border-b border-[#133B3A]">
    <div class="max-w-7xl mx-auto px-3 sm:px-6 lg:px-8">
      
      <!-- Upper Header: Brand & Meta Status -->
      <div class="flex items-center justify-between h-16 gap-2">
        
        <!-- Brand Logo & Identity -->
        <div class="flex items-center gap-3">
          <div class="w-10 h-10 rounded-xl bg-gradient-to-tr from-[#00382A] to-[#042F2F] border border-[#2AC59E]/40 flex items-center justify-center mint-glow-sm">
            <svg class="w-5 h-5 text-[#2AC59E]" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round">
              <path d="M21 16V8a2 2 0 0 0-1-1.73l-7-4a2 2 0 0 0-2 0l-7 4A2 2 0 0 0 3 8v8a2 2 0 0 0 1 1.73l7 4a2 2 0 0 0 2 0l7-4A2 2 0 0 0 21 16z"></path>
              <polyline points="3.27 6.96 12 12.01 20.73 6.96"></polyline>
              <line x1="12" y1="22.08" x2="12" y2="12"></line>
            </svg>
          </div>
          <div>
            <div class="flex items-center gap-2">
              <span class="text-base sm:text-lg font-extrabold text-[#FAF6E6] tracking-tight">FH DATA</span>
              <span class="px-2 py-0.5 text-[10px] font-bold rounded-full bg-[#2AC59E]/10 text-[#2AC59E] border border-[#2AC59E]/30 uppercase tracking-wide">C-Suite</span>
            </div>
            <p class="text-[11px] text-[#CECABB] hidden sm:block">Inteligência Estratégica: CEO • CFO • COO • CHRO • CMO</p>
          </div>
        </div>

        <!-- Meta 110M / Restrição Badge (Desktop) -->
        <div class="hidden lg:flex items-center gap-2 text-xs bg-[#002424] py-1.5 px-3 rounded-full border border-[#2AC59E]/30">
          <span class="w-2 h-2 rounded-full bg-[#2AC59E] animate-pulse"></span>
          <span class="text-[#CECABB]">Meta 5 Anos:</span>
          <span class="font-bold text-[#52E1B9]">R$ 110M</span>
          <span class="text-[10px] text-[#E6E3D3]/60 px-1.5 py-0.5 rounded bg-[#001716] border border-[#133B3A]">Sem Dívida / Sem Diluição</span>
        </div>

        <!-- Quick Actions & Print -->
        <div class="flex items-center gap-2">
          <a href="/chat" class="px-3 py-2 rounded-xl bg-[#2AC59E] hover:bg-[#52E1B9] text-xs font-bold text-[#001716] border border-[#2AC59E]/30 flex items-center gap-1.5 transition-all">
            <i data-lucide="sparkles" class="w-3.5 h-3.5"></i>
            <span class="hidden sm:inline">Chat IA</span>
          </a>
          <button onclick="window.print()" class="px-3 py-2 rounded-xl bg-[#042F2F] hover:bg-[#133B3A] text-xs font-semibold text-[#FAF6E6] border border-[#2AC59E]/30 flex items-center gap-1.5 transition-all">
            <i data-lucide="printer" class="w-3.5 h-3.5 text-[#2AC59E]"></i>
            <span class="hidden sm:inline">Exportar / Imprimir</span>
          </button>
        </div>

      </div>

      <!-- Navigation Tabs (Mobile-First Horizontal Swipe) -->
      <nav class="flex space-x-1.5 overflow-x-auto mobile-hide-scrollbar py-2 border-t border-[#133B3A]/60">
        
        <button onclick="switchTab('overview')" id="tab-btn-overview" class="fh-tab-button fh-tab-active px-3.5 py-2 text-xs font-semibold rounded-xl text-[#CECABB] hover:text-[#FAF6E6] bg-[#002424]/60 border border-transparent flex items-center gap-2 transition-all shrink-0">
          <i data-lucide="layout-grid" class="w-4 h-4 text-[#2AC59E]"></i>
          <span>Visão Geral</span>
        </button>

        <button onclick="switchTab('dilemmas')" id="tab-btn-dilemmas" class="fh-tab-button px-3.5 py-2 text-xs font-semibold rounded-xl text-[#E2B93B] hover:text-[#FAF6E6] bg-[#002424]/60 border border-[#E2B93B]/30 flex items-center gap-2 transition-all shrink-0">
          <i data-lucide="help-circle" class="w-4 h-4 text-[#E2B93B]"></i>
          <span>Dilemas de OKR & Perguntas</span>
        </button>

        <button onclick="switchTab('ceo')" id="tab-btn-ceo" class="fh-tab-button px-3.5 py-2 text-xs font-semibold rounded-xl text-[#CECABB] hover:text-[#FAF6E6] bg-[#002424]/60 border border-transparent flex items-center gap-2 transition-all shrink-0">
          <i data-lucide="crown" class="w-4 h-4 text-[#52E1B9]"></i>
          <span>CEO • Estratégia</span>
        </button>

        <button onclick="switchTab('cfo')" id="tab-btn-cfo" class="fh-tab-button px-3.5 py-2 text-xs font-semibold rounded-xl text-[#CECABB] hover:text-[#FAF6E6] bg-[#002424]/60 border border-transparent flex items-center gap-2 transition-all shrink-0">
          <i data-lucide="dollar-sign" class="w-4 h-4 text-[#2AC59E]"></i>
          <span>CFO • Finanças</span>
        </button>

        <button onclick="switchTab('coo')" id="tab-btn-coo" class="fh-tab-button px-3.5 py-2 text-xs font-semibold rounded-xl text-[#CECABB] hover:text-[#FAF6E6] bg-[#002424]/60 border border-transparent flex items-center gap-2 transition-all shrink-0">
          <i data-lucide="sliders" class="w-4 h-4 text-[#E2B93B]"></i>
          <span>COO • Operações</span>
        </button>

        <button onclick="switchTab('chro')" id="tab-btn-chro" class="fh-tab-button px-3.5 py-2 text-xs font-semibold rounded-xl text-[#CECABB] hover:text-[#FAF6E6] bg-[#002424]/60 border border-transparent flex items-center gap-2 transition-all shrink-0">
          <i data-lucide="users" class="w-4 h-4 text-[#FF6568]"></i>
          <span>CHRO • Força Comercial</span>
        </button>

        <button onclick="switchTab('cmo')" id="tab-btn-cmo" class="fh-tab-button px-3.5 py-2 text-xs font-semibold rounded-xl text-[#CECABB] hover:text-[#FAF6E6] bg-[#002424]/60 border border-transparent flex items-center gap-2 transition-all shrink-0">
          <i data-lucide="target" class="w-4 h-4 text-[#C2EAE8]"></i>
          <span>CMO • Produtos</span>
        </button>

        <a href="/chat" class="fh-tab-button px-3.5 py-2 text-xs font-semibold rounded-xl text-[#001716] bg-[#2AC59E] hover:bg-[#52E1B9] border border-[#2AC59E]/40 flex items-center gap-2 transition-all shrink-0">
          <i data-lucide="message-square" class="w-4 h-4"></i>
          <span>Chat da Base</span>
        </a>

      </nav>

    </div>
  </header>

  <!-- Main Content Container -->
  <main class="flex-1 max-w-7xl w-full mx-auto px-3 sm:px-6 lg:px-8 py-5 space-y-6">

    <!-- ===================================================================================== -->
    <!-- TAB: DILEMAS DE OKR & SESSÕES DE PERGUNTAS ESTRATÉGICAS (DESTAQUE) -->
    <!-- ===================================================================================== -->
    <div id="tab-dilemmas" class="tab-content hidden space-y-6">
      
      <!-- Top Banner Dilemas -->
      <div class="fh-card rounded-2xl p-5 sm:p-6 border-l-4 border-l-[#E2B93B] relative overflow-hidden bg-gradient-to-r from-[#00201F] via-[#042F2F] to-[#00201F]">
        <div class="space-y-1.5">
          <div class="flex items-center gap-2 flex-wrap">
            <span class="px-2.5 py-0.5 rounded-full text-[10px] font-bold bg-[#E2B93B]/20 text-[#E2B93B] border border-[#E2B93B]/30 uppercase tracking-wider">Alinhamento C-Suite</span>
            <span class="text-xs text-[#CECABB]">O Vício dos Silos vs Visão Sistêmica de Capital</span>
          </div>
          <h2 class="text-xl sm:text-2xl font-black text-[#FAF6E6] tracking-tight">Sessões Estratégicas: Pergunta, OKR, Vício de Incentivo & Ponto Cego</h2>
          <p class="text-xs sm:text-sm text-[#CECABB] max-w-4xl leading-relaxed">
            Quando cada executivo persegue sua meta isoladamente sem considerar a restrição de capital de giro, a empresa corre o risco de quebrar no meio da expansão. Veja o diagnóstico aprofundado para cada cadeira:
          </p>
        </div>
      </div>

      <!-- SESSÃO 1: CEO -->
      <div class="fh-card rounded-2xl p-5 sm:p-6 space-y-4 border border-[#2AC59E]/30">
        <div class="flex flex-col sm:flex-row sm:items-center justify-between gap-3 border-b border-[#133B3A] pb-3">
          <div class="flex items-center gap-3">
            <div class="w-10 h-10 rounded-xl bg-[#00382A] border border-[#2AC59E]/50 flex items-center justify-center text-[#2AC59E] font-extrabold text-sm mint-glow-sm">
              CEO
            </div>
            <div>
              <span class="text-[10px] uppercase tracking-wider text-[#2AC59E] font-bold">Pergunta Central do CEO</span>
              <h3 class="text-base sm:text-lg font-bold text-[#FAF6E6]">"Qual é a meta do ano que vem e dos próximos cinco anos?"</h3>
            </div>
          </div>
          <div class="px-3 py-1.5 rounded-xl bg-[#002424] border border-[#2AC59E]/30 text-xs text-[#52E1B9] font-bold self-start sm:self-auto">
            R$ 110M em 5 anos • Bootstrapping
          </div>
        </div>

        <div class="grid grid-cols-1 md:grid-cols-3 gap-4 text-xs">
          <!-- 1. OKR -->
          <div class="p-4 rounded-xl bg-[#001716] border border-[#133B3A] space-y-2">
            <div class="font-bold text-[#52E1B9] flex items-center gap-1.5">
              <i data-lucide="target" class="w-4 h-4"></i>
              <span>1. O OKR Definido</span>
            </div>
            <p class="text-[#E6E3D3] leading-relaxed">
              Chegar a <strong class="text-[#FAF6E6]">R$ 110 Milhões em 5 anos</strong> (2030) e assumir a liderança regional no Nordeste, <strong class="text-[#2AC59E]">sem captar dívida e sem diluir sociedade</strong>.
            </p>
            <div class="text-[11px] text-[#CECABB] bg-[#002424] p-2.5 rounded-lg border border-[#133B3A]">
              Base 2025: R$ 48,6M → Meta 2026: R$ 57,2M (+17,7%) → Meta 2030: R$ 110M (+126,3% total).
            </div>
          </div>

          <!-- 2. Vício -->
          <div class="p-4 rounded-xl bg-[#001716] border border-[#E2B93B]/30 space-y-2">
            <div class="font-bold text-[#E2B93B] flex items-center gap-1.5">
              <i data-lucide="alert-triangle" class="w-4 h-4"></i>
              <span>2. O que o OKR empurra a fazer</span>
            </div>
            <p class="text-[#E6E3D3] leading-relaxed">
              Cobrar crescimento agressivo de receita de todo mundo o tempo todo, pressionando o time a fechar qualquer cotação de alto valor, sem olhar prazos de pagamento ou histórico de glosa do pagador.
            </p>
          </div>

          <!-- 3. Ponto Cego -->
          <div class="p-4 rounded-xl bg-[#001716] border border-[#FF6568]/40 space-y-2">
            <div class="font-bold text-[#FF6568] flex items-center gap-1.5">
              <i data-lucide="shield-alert" class="w-4 h-4"></i>
              <span>3. Onde ele erra sozinho (Ponto Cego)</span>
            </div>
            <p class="text-[#E6E3D3] leading-relaxed">
              <strong class="text-[#FF6568]">Trata a restrição de capital como detalhe do CFO</strong>, quando ela é exatamente o que define a velocidade máxima de crescimento sustentável da empresa inteira.
            </p>
            <p class="text-[#CECABB] text-[11px] leading-relaxed">
              Com o ciclo atual de 165 dias, para faturar R$ 110M a empresa precisará de <strong class="text-[#FAF6E6]">R$ 49,6 Milhões de capital de giro imobilizado</strong>. Sem dívida nem diluição, a empresa quebra antes de bater R$ 70M se não reduzir o ciclo de caixa!
            </p>
          </div>
        </div>
      </div>

      <!-- SESSÃO 2: CHRO -->
      <div class="fh-card rounded-2xl p-5 sm:p-6 space-y-4 border border-[#FF6568]/30">
        <div class="flex flex-col sm:flex-row sm:items-center justify-between gap-3 border-b border-[#133B3A] pb-3">
          <div class="flex items-center gap-3">
            <div class="w-10 h-10 rounded-xl bg-[#002424] border border-[#FF6568]/50 flex items-center justify-center text-[#FF6568] font-extrabold text-sm coral-glow-sm">
              CHRO
            </div>
            <div>
              <span class="text-[10px] uppercase tracking-wider text-[#FF6568] font-bold">Pergunta Central do CHRO</span>
              <h3 class="text-base sm:text-lg font-bold text-[#FAF6E6]">"Qual dos meus vendedores performa melhor?"</h3>
            </div>
          </div>
          <div class="px-3 py-1.5 rounded-xl bg-[#002424] border border-[#FF6568]/30 text-xs text-[#FF6568] font-bold self-start sm:self-auto">
            Reter Top 3 • Turnover &lt; 15%
          </div>
        </div>

        <div class="grid grid-cols-1 md:grid-cols-3 gap-4 text-xs">
          <!-- 1. OKR -->
          <div class="p-4 rounded-xl bg-[#001716] border border-[#133B3A] space-y-2">
            <div class="font-bold text-[#FF6568] flex items-center gap-1.5">
              <i data-lucide="target" class="w-4 h-4"></i>
              <span>1. O OKR Definido</span>
            </div>
            <p class="text-[#E6E3D3] leading-relaxed">
              Reter os três melhores vendedores da equipe e reduzir o turnover comercial para <strong>menos de 15% ao ano</strong>, mantendo a fidelidade das contas médicas.
            </p>
          </div>

          <!-- 2. Vício -->
          <div class="p-4 rounded-xl bg-[#001716] border border-[#E2B93B]/30 space-y-2">
            <div class="font-bold text-[#E2B93B] flex items-center gap-1.5">
              <i data-lucide="alert-triangle" class="w-4 h-4"></i>
              <span>2. O que o OKR empurra a fazer</span>
            </div>
            <p class="text-[#E6E3D3] leading-relaxed">
              Ranquear os vendedores simplesmente pelo volume de receita bruta e premiar o topo da lista (Ricardo Aragão R$ 41,2M, Marcelo Bastos R$ 25,5M, Diego Fontes R$ 18,8M).
            </p>
          </div>

          <!-- 3. Ponto Cego -->
          <div class="p-4 rounded-xl bg-[#001716] border border-[#FF6568]/40 space-y-2">
            <div class="font-bold text-[#FF6568] flex items-center gap-1.5">
              <i data-lucide="shield-alert" class="w-4 h-4"></i>
              <span>3. Onde ele erra sozinho (Ponto Cego)</span>
            </div>
            <p class="text-[#E6E3D3] leading-relaxed">
              <strong class="text-[#FF6568]">O ranking por receita premia exatamente quem consome mais capital da empresa!</strong>
            </p>
            <p class="text-[#CECABB] text-[11px] leading-relaxed">
              Ricardo Aragão vendeu R$ 41,2M, mas opera com ciclo de <strong class="text-[#FAF6E6]">220,6 dias</strong>, imobilizando <strong class="text-[#FF6568]">R$ 24,91 Milhões de capital de giro</strong> e gerando <strong class="text-[#FF6568]">R$ 2,41 Milhões de glosas perdidas (5,8%)</strong>! Enquanto isso, Tatiana Coelho (ciclo 121d | 2,0% glosa) e Joana Rios (ciclo 93d | 1,4% glosa) geram muito mais lucro líquido real.
            </p>
          </div>
        </div>
      </div>

      <!-- SESSÃO 3: COO (HEADCOUNT & CAPITAL DE GIRO) -->
      <div class="fh-card rounded-2xl p-5 sm:p-6 space-y-4 border border-[#E2B93B]/30">
        <div class="flex flex-col sm:flex-row sm:items-center justify-between gap-3 border-b border-[#133B3A] pb-3">
          <div class="flex items-center gap-3">
            <div class="w-10 h-10 rounded-xl bg-[#002424] border border-[#E2B93B]/50 flex items-center justify-center text-[#E2B93B] font-extrabold text-sm">
              COO
            </div>
            <div>
              <span class="text-[10px] uppercase tracking-wider text-[#E2B93B] font-bold">Pergunta Central do COO</span>
              <h3 class="text-base sm:text-lg font-bold text-[#FAF6E6]">"Quantas pessoas preciso contratar nos próximos cinco anos?"</h3>
            </div>
          </div>
          <div class="px-3 py-1.5 rounded-xl bg-[#002424] border border-[#E2B93B]/30 text-xs text-[#E2B93B] font-bold self-start sm:self-auto">
            SLA 24x7 sem estourar custo fixo
          </div>
        </div>

        <div class="grid grid-cols-1 md:grid-cols-3 gap-4 text-xs">
          <!-- 1. OKR -->
          <div class="p-4 rounded-xl bg-[#001716] border border-[#133B3A] space-y-2">
            <div class="font-bold text-[#E2B93B] flex items-center gap-1.5">
              <i data-lucide="target" class="w-4 h-4"></i>
              <span>1. O OKR Definido</span>
            </div>
            <p class="text-[#E6E3D3] leading-relaxed">
              Sustentar nível de serviço <strong>24x7</strong> com crescimento de receita sem estourar o custo fixo da operação, garantindo cobertura cirúrgica pontual.
            </p>
          </div>

          <!-- 2. Vício -->
          <div class="p-4 rounded-xl bg-[#001716] border border-[#E2B93B]/30 space-y-2">
            <div class="font-bold text-[#E2B93B] flex items-center gap-1.5">
              <i data-lucide="alert-triangle" class="w-4 h-4"></i>
              <span>2. O que o OKR empurra a fazer</span>
            </div>
            <p class="text-[#E6E3D3] leading-relaxed">
              Dimensionar equipe pela simples projeção de demanda cirúrgica (ex: "se o volume vai dobrar, contratar +20 vendedores, +15 instrumentadores e +8 motoristas").
            </p>
          </div>

          <!-- 3. Ponto Cego -->
          <div class="p-4 rounded-xl bg-[#001716] border border-[#FF6568]/40 space-y-2">
            <div class="font-bold text-[#FF6568] flex items-center gap-1.5">
              <i data-lucide="shield-alert" class="w-4 h-4"></i>
              <span>3. Onde ele erra sozinho (Ponto Cego)</span>
            </div>
            <p class="text-[#E6E3D3] leading-relaxed">
              <strong class="text-[#FF6568]">Contratar vendedor sem capital de giro para bancar a consignação que ele vai gerar é contratar prejuízo!</strong>
            </p>
            <p class="text-[#CECABB] text-[11px] leading-relaxed">
              Cada novo vendedor abre hospitais e exige caixas cirúrgicas consignadas paradas (39,6 dias de consignação média). Contratar 20 vendedores exigiria <strong class="text-[#FAF6E6]">R$ 25M de capital para novos estoques</strong> que a empresa não tem. A solução é <strong class="text-[#2AC59E]">aumentar o giro das caixas existentes com RFID</strong> e contratar apenas especialistas técnicos de apoio!
            </p>
          </div>
        </div>
      </div>

    </div>

    <!-- ===================================================================================== -->
    <!-- TAB 1: VISÃO GERAL C-SUITE (OVERVIEW) -->
    <!-- ===================================================================================== -->
    <div id="tab-overview" class="tab-content space-y-6">
      
      <!-- Hero Banner -->
      <div class="fh-card-highlight rounded-2xl p-5 sm:p-6 relative overflow-hidden">
        <div class="relative z-10 flex flex-col md:flex-row md:items-center justify-between gap-4">
          <div class="space-y-1.5">
            <div class="flex items-center gap-2 flex-wrap">
              <span class="px-2.5 py-0.5 text-[10px] font-bold rounded-full bg-[#2AC59E]/20 text-[#2AC59E] border border-[#2AC59E]/40 uppercase tracking-wider">Base FH Saúde (2021-2025)</span>
              <span class="text-xs text-[#CECABB]">2.371 Negócios Médicos Auditados</span>
            </div>
            <h2 class="text-xl sm:text-2xl font-black text-[#FAF6E6] tracking-tight">Painel de Decisão Estratégica Integrada C-Suite</h2>
            <p class="text-xs sm:text-sm text-[#CECABB] max-w-3xl leading-relaxed">
              Cruzamento de dados entre Vendas, Finanças, Operações e Logística Cirúrgica para destravar o crescimento autofinanciado de R$ 110M.
            </p>
          </div>
          <div class="flex items-center gap-3">
            <button onclick="switchTab('dilemmas')" class="px-4 py-2.5 rounded-xl bg-[#2AC59E] hover:bg-[#52E1B9] text-[#001716] font-extrabold text-xs flex items-center gap-2 transition-all mint-glow-sm">
              <i data-lucide="help-circle" class="w-4 h-4"></i>
              <span>Ver Sessões de Perguntas</span>
            </button>
          </div>
        </div>
      </div>

      <!-- KPI Summary Cards -->
      <div class="grid grid-cols-2 sm:grid-cols-3 lg:grid-cols-6 gap-3">
        
        <div class="fh-card p-4 rounded-xl space-y-1">
          <div class="flex items-center justify-between text-[#CECABB] text-xs">
            <span>Pipeline Total</span>
            <i data-lucide="layers" class="w-4 h-4 text-[#2AC59E]"></i>
          </div>
          <div class="text-base sm:text-lg font-bold text-[#FAF6E6]">R$ 369,25M</div>
          <div class="text-[10px] text-[#CECABB]">2.371 propostas</div>
        </div>

        <div class="fh-card p-4 rounded-xl space-y-1">
          <div class="flex items-center justify-between text-[#CECABB] text-xs">
            <span>Receita Ganha</span>
            <i data-lucide="check-circle" class="w-4 h-4 text-[#52E1B9]"></i>
          </div>
          <div class="text-base sm:text-lg font-bold text-[#52E1B9]">R$ 176,30M</div>
          <div class="text-[10px] text-[#52E1B9]/80">1.198 cirurgias (50,5%)</div>
        </div>

        <div class="fh-card p-4 rounded-xl space-y-1">
          <div class="flex items-center justify-between text-[#CECABB] text-xs">
            <span>Valor Perdido</span>
            <i data-lucide="x-circle" class="w-4 h-4 text-[#FF6568]"></i>
          </div>
          <div class="text-base sm:text-lg font-bold text-[#FF6568]">R$ 192,95M</div>
          <div class="text-[10px] text-[#FF6568]/80">1.173 perdas de funil</div>
        </div>

        <div class="fh-card p-4 rounded-xl space-y-1">
          <div class="flex items-center justify-between text-[#CECABB] text-xs">
            <span>Glosas Totais</span>
            <i data-lucide="alert-triangle" class="w-4 h-4 text-[#E2B93B]"></i>
          </div>
          <div class="text-base sm:text-lg font-bold text-[#E2B93B]">R$ 14,49M</div>
          <div class="text-[10px] text-[#CECABB]">8,2% da receita bruta</div>
        </div>

        <div class="fh-card p-4 rounded-xl space-y-1">
          <div class="flex items-center justify-between text-[#CECABB] text-xs">
            <span>Glosa Não Recup.</span>
            <i data-lucide="shield-alert" class="w-4 h-4 text-[#FF6568]"></i>
          </div>
          <div class="text-base sm:text-lg font-bold text-[#FF6568]">R$ 7,22M</div>
          <div class="text-[10px] text-[#FF6568]/80">Perda de caixa real</div>
        </div>

        <div class="fh-card p-4 rounded-xl space-y-1">
          <div class="flex items-center justify-between text-[#CECABB] text-xs">
            <span>Ciclo Médio Total</span>
            <i data-lucide="clock" class="w-4 h-4 text-[#C2EAE8]"></i>
          </div>
          <div class="text-base sm:text-lg font-bold text-[#C2EAE8]">164,7 dias</div>
          <div class="text-[10px] text-[#CECABB]">Cotação ao Pagamento</div>
        </div>

      </div>

      <!-- Charts Row -->
      <div class="grid grid-cols-1 lg:grid-cols-2 gap-6">
        
        <!-- YoY Chart -->
        <div class="fh-card p-5 rounded-2xl space-y-3">
          <div class="flex items-center justify-between">
            <h4 class="text-sm font-bold text-[#FAF6E6] flex items-center gap-2">
              <i data-lucide="trending-up" class="w-4 h-4 text-[#2AC59E]"></i>
              Evolução Anual: Receita Ganha vs Valor Perdido
            </h4>
            <span class="text-xs text-[#CECABB]">2021-2025</span>
          </div>
          <div class="h-64">
            <canvas id="chartOverviewYoY"></canvas>
          </div>
        </div>

        <!-- Top Losses Pareto -->
        <div class="fh-card p-5 rounded-2xl space-y-3">
          <div class="flex items-center justify-between">
            <h4 class="text-sm font-bold text-[#FAF6E6] flex items-center gap-2">
              <i data-lucide="pie-chart" class="w-4 h-4 text-[#FF6568]"></i>
              Principais Causas de Perda de Faturamento (R$)
            </h4>
            <span class="text-xs text-[#CECABB]">Top 6 Ofensores</span>
          </div>
          <div class="h-64">
            <canvas id="chartOverviewLosses"></canvas>
          </div>
        </div>

      </div>

    </div>

    <!-- ===================================================================================== -->
    <!-- TAB 2: CEO -->
    <!-- ===================================================================================== -->
    <div id="tab-ceo" class="tab-content hidden space-y-6">
      
      <!-- CEO Banner -->
      <div class="fh-card rounded-2xl p-5 sm:p-6 border-l-4 border-l-[#2AC59E] space-y-3">
        <div class="flex flex-col sm:flex-row sm:items-center justify-between gap-3">
          <div>
            <span class="px-2.5 py-0.5 rounded-full text-[10px] font-bold bg-[#2AC59E]/20 text-[#2AC59E] border border-[#2AC59E]/40 uppercase tracking-wider">Diretriz do CEO</span>
            <h2 class="text-xl font-bold text-[#FAF6E6] mt-1">Estratégia de Escala: 110 Milhões em 5 Anos Autofinanciados</h2>
            <p class="text-xs text-[#CECABB]">Como expandir mantendo o controle societário e mitigando o risco de concentração em PE (76,1%).</p>
          </div>
          <div class="flex items-center gap-3 bg-[#001716] p-3 rounded-xl border border-[#133B3A]">
            <div>
              <div class="text-[10px] text-[#CECABB] uppercase">CAGR Histórico</div>
              <div class="text-base font-bold text-[#2AC59E]">+19,3% a.a.</div>
            </div>
            <div class="h-7 w-px bg-[#133B3A]"></div>
            <div>
              <div class="text-[10px] text-[#CECABB] uppercase">Meta 2030</div>
              <div class="text-base font-bold text-[#52E1B9]">R$ 110,0M</div>
            </div>
          </div>
        </div>
      </div>

      <!-- Regional & Line Charts -->
      <div class="grid grid-cols-1 lg:grid-cols-2 gap-6">
        <div class="fh-card p-5 rounded-2xl space-y-3">
          <h4 class="text-sm font-bold text-[#FAF6E6] flex items-center gap-2">
            <i data-lucide="map-pin" class="w-4 h-4 text-[#2AC59E]"></i>
            Concentração de Receita por Estado (Nordeste)
          </h4>
          <div class="h-64">
            <canvas id="chartCeoStates"></canvas>
          </div>
        </div>
        <div class="fh-card p-5 rounded-2xl space-y-3">
          <h4 class="text-sm font-bold text-[#FAF6E6] flex items-center gap-2">
            <i data-lucide="pie-chart" class="w-4 h-4 text-[#C2EAE8]"></i>
            Participação por Linha de Especialidade Médica
          </h4>
          <div class="h-64">
            <canvas id="chartCeoLines"></canvas>
          </div>
        </div>
      </div>

    </div>

    <!-- ===================================================================================== -->
    <!-- TAB 3: CFO -->
    <!-- ===================================================================================== -->
    <div id="tab-cfo" class="tab-content hidden space-y-6">
      
      <div class="fh-card rounded-2xl p-5 sm:p-6 border-l-4 border-l-[#52E1B9] space-y-3">
        <div class="flex flex-col sm:flex-row sm:items-center justify-between gap-3">
          <div>
            <span class="px-2.5 py-0.5 rounded-full text-[10px] font-bold bg-[#2AC59E]/20 text-[#52E1B9] border border-[#2AC59E]/40 uppercase tracking-wider">Diretriz do CFO</span>
            <h2 class="text-xl font-bold text-[#FAF6E6] mt-1">Glosas Hospitalares, DSO de 125 Dias & Capital de Giro</h2>
            <p class="text-xs text-[#CECABB]">Operadoras verticalizadas geram 67,5% das perdas de glosa da empresa e demoram 135,7 dias para pagar.</p>
          </div>
          <div class="flex items-center gap-3 bg-[#001716] p-3 rounded-xl border border-[#133B3A]">
            <div>
              <div class="text-[10px] text-[#CECABB] uppercase">Glosa Não Recup.</div>
              <div class="text-base font-bold text-[#FF6568]">R$ 7,22M</div>
            </div>
            <div class="h-7 w-px bg-[#133B3A]"></div>
            <div>
              <div class="text-[10px] text-[#CECABB] uppercase">DSO Geral</div>
              <div class="text-base font-bold text-[#E2B93B]">125,1 dias</div>
            </div>
          </div>
        </div>
      </div>

      <div class="grid grid-cols-1 lg:grid-cols-2 gap-6">
        <div class="fh-card p-5 rounded-2xl space-y-3">
          <h4 class="text-sm font-bold text-[#FAF6E6] flex items-center gap-2">
            <i data-lucide="bar-chart-2" class="w-4 h-4 text-[#2AC59E]"></i>
            Glosas Totais vs Glosas Perdidas por Tipo de Pagador (R$)
          </h4>
          <div class="h-64">
            <canvas id="chartCfoGlosas"></canvas>
          </div>
        </div>
        <div class="fh-card p-5 rounded-2xl space-y-3">
          <h4 class="text-sm font-bold text-[#FAF6E6] flex items-center gap-2">
            <i data-lucide="calendar" class="w-4 h-4 text-[#E2B93B]"></i>
            Prazo Médio de Recebimento (DSO) por Tipo de Pagador
          </h4>
          <div class="h-64">
            <canvas id="chartCfoDso"></canvas>
          </div>
        </div>
      </div>

    </div>

    <!-- ===================================================================================== -->
    <!-- TAB 4: COO -->
    <!-- ===================================================================================== -->
    <div id="tab-coo" class="tab-content hidden space-y-6">
      
      <div class="fh-card rounded-2xl p-5 sm:p-6 border-l-4 border-l-[#E2B93B] space-y-3">
        <div class="flex flex-col sm:flex-row sm:items-center justify-between gap-3">
          <div>
            <span class="px-2.5 py-0.5 rounded-full text-[10px] font-bold bg-[#E2B93B]/20 text-[#E2B93B] border border-[#E2B93B]/40 uppercase tracking-wider">Diretriz do COO</span>
            <h2 class="text-xl font-bold text-[#FAF6E6] mt-1">Eficiência da Esteira Cirúrgica & Alavancagem de Headcount</h2>
            <p class="text-xs text-[#CECABB]">Gargalo de 58 dias entre cirurgia e faturamento e a redução do tempo de consignação para liberar estoque existente.</p>
          </div>
          <div class="flex items-center gap-3 bg-[#001716] p-3 rounded-xl border border-[#133B3A]">
            <div>
              <div class="text-[10px] text-[#CECABB] uppercase">Cirurgia ➔ Fat.</div>
              <div class="text-base font-bold text-[#FF6568]">58,0 dias</div>
            </div>
            <div class="h-7 w-px bg-[#133B3A]"></div>
            <div>
              <div class="text-[10px] text-[#CECABB] uppercase">Consignação</div>
              <div class="text-base font-bold text-[#E2B93B]">39,6 dias</div>
            </div>
          </div>
        </div>
      </div>

      <div class="grid grid-cols-1 lg:grid-cols-2 gap-6">
        <div class="fh-card p-5 rounded-2xl space-y-3">
          <h4 class="text-sm font-bold text-[#FAF6E6] flex items-center gap-2">
            <i data-lucide="funnel" class="w-4 h-4 text-[#E2B93B]"></i>
            Perda Financeira por Etapa do Funil (R$)
          </h4>
          <div class="h-64">
            <canvas id="chartCooStages"></canvas>
          </div>
        </div>
        <div class="fh-card p-5 rounded-2xl space-y-3">
          <h4 class="text-sm font-bold text-[#FAF6E6] flex items-center gap-2">
            <i data-lucide="alert-octagon" class="w-4 h-4 text-[#FF6568]"></i>
            Perdas Operacionais & Logísticas (R$)
          </h4>
          <div class="h-64">
            <canvas id="chartCooOperationalLosses"></canvas>
          </div>
        </div>
      </div>

    </div>

    <!-- ===================================================================================== -->
    <!-- TAB 5: CHRO -->
    <!-- ===================================================================================== -->
    <div id="tab-chro" class="tab-content hidden space-y-6">
      
      <div class="fh-card rounded-2xl p-5 sm:p-6 border-l-4 border-l-[#FF6568] space-y-3">
        <div class="flex flex-col sm:flex-row sm:items-center justify-between gap-3">
          <div>
            <span class="px-2.5 py-0.5 rounded-full text-[10px] font-bold bg-[#FF6568]/20 text-[#FF6568] border border-[#FF6568]/40 uppercase tracking-wider">Diretriz do CHRO</span>
            <h2 class="text-xl font-bold text-[#FAF6E6] mt-1">Produtividade Real vs Consumo de Capital por Vendedor</h2>
            <p class="text-xs text-[#CECABB]">Por que premiar por receita bruta engana a diretoria e consome o caixa da empresa.</p>
          </div>
          <div class="flex items-center gap-3 bg-[#001716] p-3 rounded-xl border border-[#133B3A]">
            <div>
              <div class="text-[10px] text-[#CECABB] uppercase">Top 3 Vendas</div>
              <div class="text-base font-bold text-[#FF6568]">48,5%</div>
            </div>
            <div class="h-7 w-px bg-[#133B3A]"></div>
            <div>
              <div class="text-[10px] text-[#CECABB] uppercase">Capital Preso Top 3</div>
              <div class="text-base font-bold text-[#FAF6E6]">R$ 46,8M</div>
            </div>
          </div>
        </div>
      </div>

      <div class="grid grid-cols-1 lg:grid-cols-2 gap-6">
        <div class="fh-card p-5 rounded-2xl space-y-3">
          <h4 class="text-sm font-bold text-[#FAF6E6] flex items-center gap-2">
            <i data-lucide="award" class="w-4 h-4 text-[#FF6568]"></i>
            Ranking de Receita Ganha por Vendedor (R$ Milhões)
          </h4>
          <div class="h-64">
            <canvas id="chartChroRevenue"></canvas>
          </div>
        </div>
        <div class="fh-card p-5 rounded-2xl space-y-3">
          <h4 class="text-sm font-bold text-[#FAF6E6] flex items-center gap-2">
            <i data-lucide="percent" class="w-4 h-4 text-[#2AC59E]"></i>
            Win Rate (%) vs Taxa de Glosa Perdida (%)
          </h4>
          <div class="h-64">
            <canvas id="chartChroWinRate"></canvas>
          </div>
        </div>
      </div>

      <!-- Seller Table -->
      <div class="fh-card rounded-2xl p-5 space-y-4">
        <div class="flex flex-col sm:flex-row sm:items-center justify-between gap-3">
          <div>
            <h4 class="text-sm font-bold text-[#FAF6E6] flex items-center gap-2">
              <i data-lucide="users" class="w-4 h-4 text-[#FF6568]"></i>
              Tabela de Produtividade, Qualidade & Consumo de Capital de Giro
            </h4>
            <p class="text-xs text-[#CECABB]">Mostra o capital de giro imobilizado por cada vendedor nos hospitais</p>
          </div>
          <input type="text" id="sellerSearch" onkeyup="filterSellerTable()" placeholder="Buscar vendedor..." class="px-3 py-1.5 bg-[#001716] border border-[#133B3A] rounded-xl text-xs text-[#FAF6E6] focus:outline-none focus:border-[#2AC59E]">
        </div>
        <div class="overflow-x-auto max-h-96">
          <table class="w-full text-xs text-left" id="sellerTable">
            <thead class="bg-[#002424] text-[#CECABB] uppercase text-[10px] tracking-wider border-b border-[#133B3A] sticky top-0">
              <tr>
                <th class="py-2.5 px-3">Vendedor</th>
                <th class="py-2.5 px-3 text-right">Deals</th>
                <th class="py-2.5 px-3 text-right">Win Rate</th>
                <th class="py-2.5 px-3 text-right">Receita Bruta</th>
                <th class="py-2.5 px-3 text-right">Glosa Perdida</th>
                <th class="py-2.5 px-3 text-right">% Glosa</th>
                <th class="py-2.5 px-3 text-right">DSO Médio</th>
                <th class="py-2.5 px-3 text-right">Ciclo Médio</th>
                <th class="py-2.5 px-3 text-right text-[#E2B93B]">Capital Preso Est.</th>
              </tr>
            </thead>
            <tbody class="divide-y divide-[#133B3A]/60 font-medium">
"""

for s in seller_profiles:
    wr_color = "text-[#52E1B9] font-bold" if s['wr'] >= 54 else ("text-[#E2B93B]" if s['wr'] >= 48 else "text-[#FF6568]")
    glosa_color = "text-[#FF6568] font-bold" if s['tx_glosa'] >= 4.5 else ("text-[#E2B93B]" if s['tx_glosa'] >= 3.0 else "text-[#52E1B9]")
    cap_color = "text-[#FF6568] font-bold" if s['cap'] >= 10000000 else ("text-[#E2B93B]" if s['cap'] >= 5000000 else "text-[#52E1B9]")
    html_content += f"""
              <tr class="hover:bg-[#002424]/40 transition-colors">
                <td class="py-2.5 px-3 font-bold text-[#FAF6E6]">{s['name']}</td>
                <td class="py-2.5 px-3 text-right text-[#CECABB]">{s['deals']}</td>
                <td class="py-2.5 px-3 text-right {wr_color}">{s['wr']}%</td>
                <td class="py-2.5 px-3 text-right font-bold text-[#52E1B9]">R$ {s['rec']:,.2f}</td>
                <td class="py-2.5 px-3 text-right text-[#FF6568]">R$ {s['glosa_p']:,.2f}</td>
                <td class="py-2.5 px-3 text-right {glosa_color}">{s['tx_glosa']}%</td>
                <td class="py-2.5 px-3 text-right text-[#CECABB]">{s['dso']:.1f}d</td>
                <td class="py-2.5 px-3 text-right text-[#CECABB]">{s['ciclo']:.1f}d</td>
                <td class="py-2.5 px-3 text-right {cap_color}">R$ {s['cap']/1e6:.2f}M</td>
              </tr>"""

html_content += f"""
            </tbody>
          </table>
        </div>
      </div>

    </div>

    <!-- ===================================================================================== -->
    <!-- TAB 6: CMO -->
    <!-- ===================================================================================== -->
    <div id="tab-cmo" class="tab-content hidden space-y-6">
      
      <div class="fh-card rounded-2xl p-5 sm:p-6 border-l-4 border-l-[#C2EAE8] space-y-3">
        <div class="flex flex-col sm:flex-row sm:items-center justify-between gap-3">
          <div>
            <span class="px-2.5 py-0.5 rounded-full text-[10px] font-bold bg-[#C2EAE8]/20 text-[#C2EAE8] border border-[#C2EAE8]/40 uppercase tracking-wider">Diretriz do CMO</span>
            <h2 class="text-xl font-bold text-[#FAF6E6] mt-1">Mix de Portfólio & Neutralização de Perdas por Preço</h2>
            <p class="text-xs text-[#CECABB]">Criação de pacotes cirúrgicos (Bundling) para combater os R$ 37,56M perdidos por preço e programas de fidelização médica.</p>
          </div>
          <div class="flex items-center gap-3 bg-[#001716] p-3 rounded-xl border border-[#133B3A]">
            <div>
              <div class="text-[10px] text-[#CECABB] uppercase">Perda por Preço</div>
              <div class="text-base font-bold text-[#FF6568]">R$ 37,56M</div>
            </div>
            <div class="h-7 w-px bg-[#133B3A]"></div>
            <div>
              <div class="text-[10px] text-[#CECABB] uppercase">Top Produto</div>
              <div class="text-base font-bold text-[#52E1B9]">Implante Quadril</div>
            </div>
          </div>
        </div>
      </div>

      <div class="grid grid-cols-1 lg:grid-cols-2 gap-6">
        <div class="fh-card p-5 rounded-2xl space-y-3">
          <h4 class="text-sm font-bold text-[#FAF6E6] flex items-center gap-2">
            <i data-lucide="package" class="w-4 h-4 text-[#C2EAE8]"></i>
            Receita Ganha por Produto (R$ Milhões)
          </h4>
          <div class="h-64">
            <canvas id="chartCmoProducts"></canvas>
          </div>
        </div>
        <div class="fh-card p-5 rounded-2xl space-y-3">
          <h4 class="text-sm font-bold text-[#FAF6E6] flex items-center gap-2">
            <i data-lucide="bar-chart" class="w-4 h-4 text-[#FF6568]"></i>
            Pareto de Motivos de Perda de Negócios (R$ Milhões)
          </h4>
          <div class="h-64">
            <canvas id="chartCmoLossPareto"></canvas>
          </div>
        </div>
      </div>

    </div>

  </main>

  <!-- Footer Bar -->
  <footer class="border-t border-[#133B3A] bg-[#001716] py-5 text-center text-xs text-[#CECABB]">
    <div class="max-w-7xl mx-auto px-4 flex flex-col sm:flex-row items-center justify-between gap-2">
      <div class="flex items-center gap-2">
        <span class="w-2 h-2 rounded-full bg-[#2AC59E]"></span>
        <span class="font-bold text-[#FAF6E6]">FH DATA</span>
        <span class="text-[#CECABB]/60">• Inteligência Estratégica C-Suite</span>
      </div>
      <div>
        <span>Design e Paleta inspirados em fhdata.com.br</span>
      </div>
    </div>
  </footer>

  <!-- Scripts -->
  <script>
    const dataBundle = {json.dumps(data, ensure_ascii=False)};

    function switchTab(tabId) {{
      const tabs = ['overview', 'dilemmas', 'ceo', 'cfo', 'coo', 'chro', 'cmo'];
      tabs.forEach(t => {{
        const content = document.getElementById('tab-' + t);
        const btn = document.getElementById('tab-btn-' + t);
        if (content && btn) {{
          if (t === tabId) {{
            content.classList.remove('hidden');
            btn.classList.add('fh-tab-active');
          }} else {{
            content.classList.add('hidden');
            btn.classList.remove('fh-tab-active');
          }}
        }}
      }});
      setTimeout(() => {{
        window.dispatchEvent(new Event('resize'));
      }}, 50);
    }}

    function filterSellerTable() {{
      const input = document.getElementById('sellerSearch').value.toLowerCase();
      const rows = document.querySelectorAll('#sellerTable tbody tr');
      rows.forEach(r => {{
        const name = r.cells[0].innerText.toLowerCase();
        if (name.includes(input)) {{
          r.style.display = '';
        }} else {{
          r.style.display = 'none';
        }}
      }});
    }}

    Chart.defaults.color = '#CECABB';
    Chart.defaults.font.family = "'Plus Jakarta Sans', sans-serif";
    Chart.defaults.plugins.legend.labels.usePointStyle = true;

    document.addEventListener('DOMContentLoaded', () => {{
      lucide.createIcons();

      // Chart 1: Overview YoY
      const ctxOverviewYoY = document.getElementById('chartOverviewYoY').getContext('2d');
      new Chart(ctxOverviewYoY, {{
        type: 'bar',
        data: {{
          labels: dataBundle.years.map(y => y.ano),
          datasets: [
            {{
              label: 'Receita Ganha (R$ M)',
              data: dataBundle.years.map(y => (y.receita_ganha / 1e6).toFixed(2)),
              backgroundColor: '#2AC59E',
              borderRadius: 6,
            }},
            {{
              label: 'Valor Perdido (R$ M)',
              data: dataBundle.years.map(y => (y.valor_perdido / 1e6).toFixed(2)),
              backgroundColor: '#FF6568',
              borderRadius: 6,
            }},
            {{
              label: 'Receita Líquida (R$ M)',
              data: dataBundle.years.map(y => (y.receita_liquida / 1e6).toFixed(2)),
              type: 'line',
              borderColor: '#52E1B9',
              backgroundColor: '#52E1B9',
              borderWidth: 2,
              pointRadius: 4,
            }}
          ]
        }},
        options: {{
          responsive: true,
          maintainAspectRatio: false,
          scales: {{
            y: {{ grid: {{ color: 'rgba(206, 202, 187, 0.08)' }}, title: {{ display: true, text: 'R$ Milhões' }} }},
            x: {{ grid: {{ display: false }} }}
          }}
        }}
      }});

      // Chart 2: Overview Losses
      const topLosses = dataBundle.loss_reasons.slice(0, 6);
      const ctxOverviewLosses = document.getElementById('chartOverviewLosses').getContext('2d');
      new Chart(ctxOverviewLosses, {{
        type: 'doughnut',
        data: {{
          labels: topLosses.map(l => l.motivo),
          datasets: [{{
            data: topLosses.map(l => (l.valor_perdido / 1e6).toFixed(2)),
            backgroundColor: ['#FF6568', '#EB5757', '#E2B93B', '#2AC59E', '#52E1B9', '#C2EAE8'],
            borderWidth: 0
          }}]
        }},
        options: {{
          responsive: true,
          maintainAspectRatio: false,
          plugins: {{
            legend: {{ position: 'right', labels: {{ boxWidth: 10, font: {{ size: 9 }} }} }}
          }}
        }}
      }});

      // Chart 3: CEO States
      const ctxCeoStates = document.getElementById('chartCeoStates').getContext('2d');
      new Chart(ctxCeoStates, {{
        type: 'bar',
        data: {{
          labels: dataBundle.states.map(s => s.estado + ' (' + s.win_rate + '%)'),
          datasets: [{{
            label: 'Receita Ganha (R$ M)',
            data: dataBundle.states.map(s => (s.receita_ganha / 1e6).toFixed(2)),
            backgroundColor: ['#2AC59E', '#52E1B9', '#E2B93B', '#C2EAE8'],
            borderRadius: 6
          }}]
        }},
        options: {{
          responsive: true,
          maintainAspectRatio: false,
          scales: {{
            y: {{ grid: {{ color: 'rgba(206, 202, 187, 0.08)' }}, title: {{ display: true, text: 'R$ Milhões' }} }},
            x: {{ grid: {{ display: false }} }}
          }}
        }}
      }});

      // Chart 4: CEO Lines
      const ctxCeoLines = document.getElementById('chartCeoLines').getContext('2d');
      new Chart(ctxCeoLines, {{
        type: 'pie',
        data: {{
          labels: dataBundle.lines.map(l => l.linha),
          datasets: [{{
            data: dataBundle.lines.map(l => (l.receita_ganha / 1e6).toFixed(2)),
            backgroundColor: ['#2AC59E', '#52E1B9', '#E2B93B'],
            borderWidth: 0
          }}]
        }},
        options: {{
          responsive: true,
          maintainAspectRatio: false,
          plugins: {{
            legend: {{ position: 'bottom', labels: {{ boxWidth: 12 }} }}
          }}
        }}
      }});

      // Chart 5: CFO Glosas
      const ctxCfoGlosas = document.getElementById('chartCfoGlosas').getContext('2d');
      new Chart(ctxCfoGlosas, {{
        type: 'bar',
        data: {{
          labels: dataBundle.payers.map(p => p.tipo),
          datasets: [
            {{
              label: 'Glosa Total Aplicada (R$ M)',
              data: dataBundle.payers.map(p => (p.valor_glosado / 1e6).toFixed(2)),
              backgroundColor: '#E2B93B',
              borderRadius: 6
            }},
            {{
              label: 'Glosa Não Recuperada (R$ M)',
              data: dataBundle.payers.map(p => (p.glosa_nao_recuperada / 1e6).toFixed(2)),
              backgroundColor: '#FF6568',
              borderRadius: 6
            }}
          ]
        }},
        options: {{
          responsive: true,
          maintainAspectRatio: false,
          scales: {{
            y: {{ grid: {{ color: 'rgba(206, 202, 187, 0.08)' }}, title: {{ display: true, text: 'R$ Milhões' }} }},
            x: {{ grid: {{ display: false }} }}
          }}
        }}
      }});

      // Chart 6: CFO DSO
      const ctxCfoDso = document.getElementById('chartCfoDso').getContext('2d');
      new Chart(ctxCfoDso, {{
        type: 'bar',
        data: {{
          labels: dataBundle.payers.map(p => p.tipo),
          datasets: [
            {{
              label: 'DSO Pagamento (Dias)',
              data: dataBundle.payers.map(p => p.dias_pagamento_medio),
              backgroundColor: '#2AC59E',
              borderRadius: 6
            }},
            {{
              label: 'Dias Consignação',
              data: dataBundle.payers.map(p => p.dias_consignacao_medio),
              backgroundColor: '#52E1B9',
              borderRadius: 6
            }}
          ]
        }},
        options: {{
          responsive: true,
          maintainAspectRatio: false,
          scales: {{
            y: {{ grid: {{ color: 'rgba(206, 202, 187, 0.08)' }}, title: {{ display: true, text: 'Dias Corridos' }} }},
            x: {{ grid: {{ display: false }} }}
          }}
        }}
      }});

      // Chart 7: COO Stages
      const ctxCooStages = document.getElementById('chartCooStages').getContext('2d');
      new Chart(ctxCooStages, {{
        type: 'bar',
        data: {{
          labels: dataBundle.loss_stages.map(s => s.etapa),
          datasets: [{{
            label: 'Valor Perdido por Etapa (R$ M)',
            data: dataBundle.loss_stages.map(s => (s.valor_perdido / 1e6).toFixed(2)),
            backgroundColor: ['#2AC59E', '#52E1B9', '#E2B93B', '#FF6568'],
            borderRadius: 6
          }}]
        }},
        options: {{
          responsive: true,
          maintainAspectRatio: false,
          scales: {{
            y: {{ grid: {{ color: 'rgba(206, 202, 187, 0.08)' }}, title: {{ display: true, text: 'R$ Milhões' }} }},
            x: {{ grid: {{ display: false }} }}
          }}
        }}
      }});

      // Chart 8: COO Operational Losses
      const opLosses = dataBundle.loss_reasons.filter(l => [
        'Cotação respondida fora do prazo', 
        'Produto indisponível em estoque', 
        'Divergência na folha de sala', 
        'Material devolvido sem uso', 
        'Extravio intra-hospitalar'
      ].includes(l.motivo));
      const ctxCooOp = document.getElementById('chartCooOperationalLosses').getContext('2d');
      new Chart(ctxCooOp, {{
        type: 'doughnut',
        data: {{
          labels: opLosses.map(l => l.motivo),
          datasets: [{{
            data: opLosses.map(l => (l.valor_perdido / 1e6).toFixed(2)),
            backgroundColor: ['#FF6568', '#EB5757', '#E2B93B', '#2AC59E', '#C2EAE8'],
            borderWidth: 0
          }}]
        }},
        options: {{
          responsive: true,
          maintainAspectRatio: false,
          plugins: {{
            legend: {{ position: 'right', labels: {{ boxWidth: 10, font: {{ size: 9 }} }} }}
          }}
        }}
      }});

      // Chart 9: CHRO Revenue
      const topSellers = dataBundle.sellers.slice(0, 10);
      const ctxChroRev = document.getElementById('chartChroRevenue').getContext('2d');
      new Chart(ctxChroRev, {{
        type: 'bar',
        data: {{
          labels: topSellers.map(s => s.vendedor),
          datasets: [{{
            label: 'Receita Ganha (R$ M)',
            data: topSellers.map(s => (s.receita_ganha / 1e6).toFixed(2)),
            backgroundColor: '#2AC59E',
            borderRadius: 6
          }}]
        }},
        options: {{
          responsive: true,
          maintainAspectRatio: false,
          indexAxis: 'y',
          scales: {{
            x: {{ grid: {{ color: 'rgba(206, 202, 187, 0.08)' }}, title: {{ display: true, text: 'R$ Milhões' }} }},
            y: {{ grid: {{ display: false }} }}
          }}
        }}
      }});

      // Chart 10: CHRO Win Rate
      const ctxChroWr = document.getElementById('chartChroWinRate').getContext('2d');
      new Chart(ctxChroWr, {{
        type: 'bar',
        data: {{
          labels: topSellers.map(s => s.vendedor),
          datasets: [
            {{
              label: 'Win Rate (%)',
              data: topSellers.map(s => s.win_rate),
              backgroundColor: '#52E1B9',
              borderRadius: 6
            }},
            {{
              label: '% Glosa Perdida (%)',
              data: topSellers.map(s => s.taxa_glosa_perdida),
              backgroundColor: '#FF6568',
              borderRadius: 6
            }}
          ]
        }},
        options: {{
          responsive: true,
          maintainAspectRatio: false,
          scales: {{
            y: {{ grid: {{ color: 'rgba(206, 202, 187, 0.08)' }}, title: {{ display: true, text: 'Percentual (%)' }} }},
            x: {{ grid: {{ display: false }} }}
          }}
        }}
      }});

      // Chart 11: CMO Products
      const ctxCmoProd = document.getElementById('chartCmoProducts').getContext('2d');
      new Chart(ctxCmoProd, {{
        type: 'bar',
        data: {{
          labels: dataBundle.products.slice(0, 8).map(p => p.produto),
          datasets: [{{
            label: 'Receita Ganha (R$ M)',
            data: dataBundle.products.slice(0, 8).map(p => (p.receita_ganha / 1e6).toFixed(2)),
            backgroundColor: '#2AC59E',
            borderRadius: 6
          }}]
        }},
        options: {{
          responsive: true,
          maintainAspectRatio: false,
          indexAxis: 'y',
          scales: {{
            x: {{ grid: {{ color: 'rgba(206, 202, 187, 0.08)' }}, title: {{ display: true, text: 'R$ Milhões' }} }},
            y: {{ grid: {{ display: false }} }}
          }}
        }}
      }});

      // Chart 12: CMO Loss Pareto
      const top8Loss = dataBundle.loss_reasons.slice(0, 8);
      const ctxCmoLoss = document.getElementById('chartCmoLossPareto').getContext('2d');
      new Chart(ctxCmoLoss, {{
        type: 'bar',
        data: {{
          labels: top8Loss.map(l => l.motivo),
          datasets: [{{
            label: 'Valor Perdido (R$ M)',
            data: top8Loss.map(l => (l.valor_perdido / 1e6).toFixed(2)),
            backgroundColor: '#FF6568',
            borderRadius: 6
          }}]
        }},
        options: {{
          responsive: true,
          maintainAspectRatio: false,
          scales: {{
            y: {{ grid: {{ color: 'rgba(206, 202, 187, 0.08)' }}, title: {{ display: true, text: 'R$ Milhões' }} }},
            x: {{ grid: {{ display: false }}, ticks: {{ maxRotation: 45, minRotation: 45, font: {{ size: 9 }} }} }}
          }}
        }}
      }});

    }});
  </script>
</body>
</html>
"""

with open('dashboard_csuite_fhsaude.html', 'w', encoding='utf-8') as f:
    f.write(html_content)

print("Regenerated dashboard_csuite_fhsaude.html with exact FH Data palette and mobile-first design!")
