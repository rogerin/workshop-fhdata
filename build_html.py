import json

with open('data_bundle.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

html_content = f"""<!DOCTYPE html>
<html lang="pt-BR" class="h-full bg-slate-950 text-slate-100">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>FH Saúde | Painel Estratégico Executivo C-Suite & Dilemas Sistêmicos</title>
  <!-- Tailwind CSS -->
  <script src="https://cdn.tailwindcss.com"></script>
  <!-- Chart.js -->
  <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
  <!-- Lucide Icons -->
  <script src="https://unpkg.com/lucide@latest"></script>
  <script>
    tailwind.config = {{
      darkMode: 'class',
      theme: {{
        extend: {{
          colors: {{
            brand: {{
              50: '#f0f9ff',
              100: '#e0f2fe',
              500: '#0284c7',
              600: '#0369a1',
              700: '#075985',
              900: '#0c4a6e',
            }},
            csuite: {{
              ceo: '#6366f1',
              cfo: '#10b981',
              coo: '#f59e0b',
              chro: '#ec4899',
              cmo: '#8b5cf6',
            }}
          }}
        }}
      }}
    }}
  </script>
  <style>
    @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@300;400;500;600;700;800&display=swap');
    body {{
      font-family: 'Plus Jakarta Sans', sans-serif;
    }}
    .glass-card {{
      background: rgba(15, 23, 42, 0.75);
      backdrop-filter: blur(12px);
      border: 1px solid rgba(255, 255, 255, 0.08);
    }}
    .glass-card:hover {{
      border-color: rgba(255, 255, 255, 0.16);
    }}
    .tab-active {{
      background: rgba(30, 41, 59, 1);
      border-bottom: 2px solid #38bdf8;
      color: #38bdf8 !important;
      font-weight: 600;
    }}
    .custom-scrollbar::-webkit-scrollbar {{
      width: 6px;
      height: 6px;
    }}
    .custom-scrollbar::-webkit-scrollbar-track {{
      background: rgba(15, 23, 42, 0.6);
    }}
    .custom-scrollbar::-webkit-scrollbar-thumb {{
      background: rgba(51, 65, 85, 0.8);
      border-radius: 9999px;
    }}
  </style>
</head>
<body class="min-h-screen flex flex-col custom-scrollbar antialiased selection:bg-sky-500 selection:text-white">

  <!-- Top Navigation Bar -->
  <header class="border-b border-slate-800/80 bg-slate-900/90 backdrop-blur-md sticky top-0 z-50">
    <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
      <div class="flex items-center justify-between h-16">
        <!-- Logo & Title -->
        <div class="flex items-center gap-3">
          <div class="w-10 h-10 rounded-xl bg-gradient-to-tr from-sky-600 to-indigo-600 flex items-center justify-center shadow-lg shadow-sky-500/20">
            <i data-lucide="activity" class="w-5 h-5 text-white"></i>
          </div>
          <div>
            <div class="flex items-center gap-2">
              <h1 class="text-lg font-bold text-white tracking-tight">FH Saúde</h1>
              <span class="px-2 py-0.5 text-xs font-semibold rounded-full bg-sky-500/10 text-sky-400 border border-sky-500/20">C-Suite Intelligence</span>
            </div>
            <p class="text-xs text-slate-400">Análise Estratégica Individual: CEO • CFO • COO • CHRO • CMO</p>
          </div>
        </div>

        <!-- Meta 110M Badge -->
        <div class="hidden lg:flex items-center gap-3 text-xs bg-slate-800/80 py-1.5 px-3 rounded-full border border-indigo-500/30">
          <span class="w-2 h-2 rounded-full bg-indigo-400 animate-ping"></span>
          <span class="text-slate-300 font-medium">Meta 5 Anos:</span>
          <span class="font-bold text-indigo-300">R$ 110M Autofinanciados (Sem Dívida / Sem Diluição)</span>
        </div>

        <!-- Action / Print -->
        <div class="flex items-center gap-2">
          <button onclick="window.print()" class="px-3 py-1.5 rounded-lg bg-slate-800 hover:bg-slate-700 text-xs font-medium text-slate-200 border border-slate-700 flex items-center gap-1.5 transition-colors">
            <i data-lucide="printer" class="w-3.5 h-3.5"></i>
            <span>Exportar / Imprimir</span>
          </button>
        </div>
      </div>

      <!-- Navigation Tabs -->
      <nav class="flex space-x-1 overflow-x-auto custom-scrollbar border-t border-slate-800/60 py-1">
        <button onclick="switchTab('overview')" id="tab-btn-overview" class="tab-button tab-active px-3 py-2 text-xs font-medium rounded-lg text-slate-300 hover:text-white hover:bg-slate-800/50 flex items-center gap-2 transition-all shrink-0">
          <i data-lucide="layout-grid" class="w-4 h-4"></i>
          <span>Visão Geral C-Suite</span>
        </button>
        <button onclick="switchTab('dilemmas')" id="tab-btn-dilemmas" class="tab-button px-3 py-2 text-xs font-medium rounded-lg text-amber-300 hover:text-white hover:bg-slate-800/50 flex items-center gap-2 transition-all shrink-0 border border-amber-500/30">
          <i data-lucide="help-circle" class="w-4 h-4 text-amber-400"></i>
          <span>Sessões de Perguntas & Dilemas de OKR</span>
        </button>
        <button onclick="switchTab('ceo')" id="tab-btn-ceo" class="tab-button px-3 py-2 text-xs font-medium rounded-lg text-slate-300 hover:text-white hover:bg-slate-800/50 flex items-center gap-2 transition-all shrink-0">
          <i data-lucide="crown" class="w-4 h-4 text-indigo-400"></i>
          <span>CEO • Estratégia & Escala (R$ 110M)</span>
        </button>
        <button onclick="switchTab('cfo')" id="tab-btn-cfo" class="tab-button px-3 py-2 text-xs font-medium rounded-lg text-slate-300 hover:text-white hover:bg-slate-800/50 flex items-center gap-2 transition-all shrink-0">
          <i data-lucide="dollar-sign" class="w-4 h-4 text-emerald-400"></i>
          <span>CFO • Finanças, Glosas & Capital de Giro</span>
        </button>
        <button onclick="switchTab('coo')" id="tab-btn-coo" class="tab-button px-3 py-2 text-xs font-medium rounded-lg text-slate-300 hover:text-white hover:bg-slate-800/50 flex items-center gap-2 transition-all shrink-0">
          <i data-lucide="sliders" class="w-4 h-4 text-amber-400"></i>
          <span>COO • Headcount & Consignação</span>
        </button>
        <button onclick="switchTab('chro')" id="tab-btn-chro" class="tab-button px-3 py-2 text-xs font-medium rounded-lg text-slate-300 hover:text-white hover:bg-slate-800/50 flex items-center gap-2 transition-all shrink-0">
          <i data-lucide="users" class="w-4 h-4 text-pink-400"></i>
          <span>CHRO • Qualidade Comercial vs Consumo de Capital</span>
        </button>
        <button onclick="switchTab('cmo')" id="tab-btn-cmo" class="tab-button px-3 py-2 text-xs font-medium rounded-lg text-slate-300 hover:text-white hover:bg-slate-800/50 flex items-center gap-2 transition-all shrink-0">
          <i data-lucide="target" class="w-4 h-4 text-purple-400"></i>
          <span>CMO • Portfólio, Preço & Expansão</span>
        </button>
      </nav>
    </div>
  </header>

  <!-- Main Container -->
  <main class="flex-1 max-w-7xl w-full mx-auto px-4 sm:px-6 lg:px-8 py-6 space-y-6">

    <!-- ===================================================================================== -->
    <!-- TAB: DILEMAS DE OKR & SESSÕES DE PERGUNTAS ESTRATÉGICAS -->
    <!-- ===================================================================================== -->
    <div id="tab-dilemmas" class="tab-content hidden space-y-6">
      
      <!-- Banner Dilemas -->
      <div class="glass-card rounded-2xl p-6 border-l-4 border-l-amber-500 relative overflow-hidden bg-gradient-to-r from-slate-900 via-amber-950/20 to-slate-900">
        <div class="space-y-1.5">
          <div class="flex items-center gap-2">
            <span class="px-2.5 py-0.5 rounded-full text-xs font-bold bg-amber-500/20 text-amber-300 border border-amber-500/30">Diagnóstico Crítico de Alinhamento Executivo</span>
            <span class="text-xs text-slate-400">Os Grandes Dilemas Estratégicos & Pontos Cegos</span>
          </div>
          <h2 class="text-2xl font-black text-white">Sessões Estratégicas: Pergunta, OKR, Vício de Incentivo & Ponto Cego Sistêmico</h2>
          <p class="text-sm text-slate-300 max-w-4xl">
            Quando cada C-Level tenta bater sua meta isoladamente ("em silos"), o resultado é a destruição silenciosa de capital. Abaixo estão as respostas profundas para as perguntas centrais de cada executivo da FH Saúde.
          </p>
        </div>
      </div>

      <!-- SESSÃO 1: CEO -->
      <div class="glass-card rounded-2xl p-6 border border-indigo-500/30 space-y-4">
        <div class="flex flex-col md:flex-row md:items-center justify-between gap-2 border-b border-slate-800 pb-3">
          <div class="flex items-center gap-3">
            <div class="w-9 h-9 rounded-xl bg-indigo-500/20 border border-indigo-500/30 flex items-center justify-center text-indigo-300 font-bold text-sm">
              CEO
            </div>
            <div>
              <span class="text-[11px] uppercase tracking-wider text-indigo-400 font-bold">Pergunta Central do CEO</span>
              <h3 class="text-lg font-bold text-white">"Qual é a meta do ano que vem e dos próximos cinco anos?"</h3>
            </div>
          </div>
          <div class="px-3 py-1 rounded-lg bg-indigo-950/60 border border-indigo-500/30 text-xs text-indigo-300 font-semibold">
            Meta: R$ 110M em 5 anos • Bootstrapping
          </div>
        </div>

        <div class="grid grid-cols-1 md:grid-cols-3 gap-4 text-xs">
          <div class="p-4 rounded-xl bg-slate-900/80 border border-slate-800 space-y-2">
            <div class="font-bold text-indigo-300 flex items-center gap-1.5">
              <i data-lucide="target" class="w-4 h-4"></i>
              <span>1. O OKR Definido</span>
            </div>
            <p class="text-slate-300 leading-relaxed">
              Chegar a <strong>R$ 110 Milhões em 5 anos</strong> (2030) e assumir a <strong>liderança regional no Nordeste</strong>, mantendo o controle total: <strong>sem captar dívida bancária cara e sem diluir a sociedade</strong>.
            </p>
            <div class="text-[11px] text-slate-400 bg-slate-950 p-2 rounded border border-slate-800">
              Base 2025: R$ 48,6M → Meta 2026: R$ 57,2M (+17,7%) → Meta 2030: R$ 110M (+126,3% total).
            </div>
          </div>

          <div class="p-4 rounded-xl bg-slate-900/80 border border-amber-500/20 space-y-2">
            <div class="font-bold text-amber-300 flex items-center gap-1.5">
              <i data-lucide="alert-triangle" class="w-4 h-4"></i>
              <span>2. O que o OKR empurra a fazer</span>
            </div>
            <p class="text-slate-300 leading-relaxed">
              Cobrar crescimento agressivo de receita de todo mundo o tempo todo. Pressionar a força comercial a fechar qualquer cotação de alto valor, sem olhar prazos de pagamento ou perfil do pagador.
            </p>
          </div>

          <div class="p-4 rounded-xl bg-rose-950/30 border border-rose-500/30 space-y-2">
            <div class="font-bold text-rose-300 flex items-center gap-1.5">
              <i data-lucide="shield-alert" class="w-4 h-4"></i>
              <span>3. Onde ele erra sozinho (Ponto Cego)</span>
            </div>
            <p class="text-slate-300 leading-relaxed">
              <strong class="text-rose-200">Trata a restrição de capital como detalhe do CFO</strong>, quando ela é exatamente o que define a <em>velocidade máxima de crescimento sustentável da empresa inteira</em>.
            </p>
            <p class="text-slate-400 text-[11px]">
              Se a FH Saúde crescer vendendo para operadoras que demoram 136 dias para pagar com 9% de glosa, para faturar R$ 110M a empresa precisará de <strong>R$ 49,6 Milhões de capital de giro imobilizado</strong>. Sem dívida/diluição, a empresa quebra por falta de caixa antes de chegar a R$ 70M!
            </p>
          </div>
        </div>
      </div>

      <!-- SESSÃO 2: CHRO -->
      <div class="glass-card rounded-2xl p-6 border border-pink-500/30 space-y-4">
        <div class="flex flex-col md:flex-row md:items-center justify-between gap-2 border-b border-slate-800 pb-3">
          <div class="flex items-center gap-3">
            <div class="w-9 h-9 rounded-xl bg-pink-500/20 border border-pink-500/30 flex items-center justify-center text-pink-300 font-bold text-sm">
              CHRO
            </div>
            <div>
              <span class="text-[11px] uppercase tracking-wider text-pink-400 font-bold">Pergunta Central do CHRO</span>
              <h3 class="text-lg font-bold text-white">"Qual dos meus vendedores performa melhor?"</h3>
            </div>
          </div>
          <div class="px-3 py-1 rounded-lg bg-pink-950/60 border border-pink-500/30 text-xs text-pink-300 font-semibold">
            Meta: Reter Top 3 • Turnover &lt; 15%
          </div>
        </div>

        <div class="grid grid-cols-1 md:grid-cols-3 gap-4 text-xs">
          <div class="p-4 rounded-xl bg-slate-900/80 border border-slate-800 space-y-2">
            <div class="font-bold text-pink-300 flex items-center gap-1.5">
              <i data-lucide="target" class="w-4 h-4"></i>
              <span>1. O OKR Definido</span>
            </div>
            <p class="text-slate-300 leading-relaxed">
              Reter os três melhores vendedores da equipe e reduzir o turnover comercial para <strong>menos de 15% ao ano</strong>, blindando o relacionamento com hospitais e médicos cirurgiões.
            </p>
          </div>

          <div class="p-4 rounded-xl bg-slate-900/80 border border-amber-500/20 space-y-2">
            <div class="font-bold text-amber-300 flex items-center gap-1.5">
              <i data-lucide="alert-triangle" class="w-4 h-4"></i>
              <span>2. O que o OKR empurra a fazer</span>
            </div>
            <p class="text-slate-300 leading-relaxed">
              Ranquear a equipe simplesmente pelo total de receita bruta faturada e premiar com bônus e viagens o topo da lista (Ricardo Aragão com R$ 41,2M, Marcelo Bastos com R$ 25,5M e Diego Fontes com R$ 18,8M).
            </p>
          </div>

          <div class="p-4 rounded-xl bg-rose-950/30 border border-rose-500/30 space-y-2">
            <div class="font-bold text-rose-300 flex items-center gap-1.5">
              <i data-lucide="shield-alert" class="w-4 h-4"></i>
              <span>3. Onde ele erra sozinho (Ponto Cego)</span>
            </div>
            <p class="text-slate-300 leading-relaxed">
              <strong class="text-rose-200">O ranking puro por receita premia exatamente quem consome mais capital da empresa!</strong>
            </p>
            <p class="text-slate-400 text-[11px]">
              Ricardo Aragão lidera o faturamento (R$ 41,2M), mas possui um ciclo médio de <strong>220,6 dias</strong> (DSO de 158 dias + 62 dias de consignação), imobilizando <strong>R$ 24,91 Milhões de capital de giro</strong> e gerando <strong>R$ 2,41 Milhões de glosas perdidas (5,8%)</strong>!
            </p>
          </div>
        </div>
      </div>

      <!-- SESSÃO 3: COO (HEADCOUNT & CAPITAL DE GIRO DE CONSIGNAÇÃO) -->
      <div class="glass-card rounded-2xl p-6 border border-amber-500/30 space-y-4">
        <div class="flex flex-col md:flex-row md:items-center justify-between gap-2 border-b border-slate-800 pb-3">
          <div class="flex items-center gap-3">
            <div class="w-9 h-9 rounded-xl bg-amber-500/20 border border-amber-500/30 flex items-center justify-center text-amber-300 font-bold text-sm">
              COO
            </div>
            <div>
              <span class="text-[11px] uppercase tracking-wider text-amber-400 font-bold">Pergunta Central do COO</span>
              <h3 class="text-lg font-bold text-white">"Quantas pessoas preciso contratar nos próximos cinco anos?"</h3>
            </div>
          </div>
          <div class="px-3 py-1 rounded-lg bg-amber-950/60 border border-amber-500/30 text-xs text-amber-300 font-semibold">
            Meta: SLA 24x7 sem estourar custo fixo
          </div>
        </div>

        <div class="grid grid-cols-1 md:grid-cols-3 gap-4 text-xs">
          <div class="p-4 rounded-xl bg-slate-900/80 border border-slate-800 space-y-2">
            <div class="font-bold text-amber-300 flex items-center gap-1.5">
              <i data-lucide="target" class="w-4 h-4"></i>
              <span>1. O OKR Definido</span>
            </div>
            <p class="text-slate-300 leading-relaxed">
              Sustentar nível de serviço **24x7** com crescimento de receita sem estourar o custo fixo da operação, assegurando entrega pontual de caixas cirúrgicas e suporte em sala.
            </p>
          </div>

          <div class="p-4 rounded-xl bg-slate-900/80 border border-amber-500/20 space-y-2">
            <div class="font-bold text-amber-300 flex items-center gap-1.5">
              <i data-lucide="alert-triangle" class="w-4 h-4"></i>
              <span>2. O que o OKR empurra a fazer</span>
            </div>
            <p class="text-slate-300 leading-relaxed">
              Dimensionar equipe pela simples **projeção linear de demanda cirúrgica** (ex: se o volume de cirurgias mais do que dobrar para bater R$ 110M, contratar 20 novos vendedores, 15 instrumentadores e 8 motoristas).
            </p>
          </div>

          <div class="p-4 rounded-xl bg-rose-950/30 border border-rose-500/30 space-y-2">
            <div class="font-bold text-rose-300 flex items-center gap-1.5">
              <i data-lucide="shield-alert" class="w-4 h-4"></i>
              <span>3. Onde ele erra sozinho (Ponto Cego)</span>
            </div>
            <p class="text-slate-300 leading-relaxed">
              <strong class="text-rose-200">Contratar vendedor sem capital de giro para bancar a consignação que ele vai gerar é contratar prejuízo e asfixia de caixa!</strong>
            </p>
            <p class="text-slate-400 text-[11px]">
              No setor de OPME, cada novo vendedor abre novas frentes cirúrgicas e imobiliza **R$ 500k a R$ 1,5M em kits cirúrgicos consignados parados em hospitais**. Contratar 20 vendedores sem ter R$ 25M de capital para caixas adicionais gera estoques desabastecidos, rupturas (R$ 16,6M perdidos) e ociosidade de equipe.
              A solução é **aumentar a produtividade da equipe atual com RFID e app de folha de sala**, contratando apenas conforme o caixa for liberado pelo giro rápido do estoque!
            </p>
          </div>
        </div>
      </div>

      <!-- SESSÃO 4: CFO -->
      <div class="glass-card rounded-2xl p-6 border border-emerald-500/30 space-y-4">
        <div class="flex flex-col md:flex-row md:items-center justify-between gap-2 border-b border-slate-800 pb-3">
          <div class="flex items-center gap-3">
            <div class="w-9 h-9 rounded-xl bg-emerald-500/20 border border-emerald-500/30 flex items-center justify-center text-emerald-300 font-bold text-sm">
              CFO
            </div>
            <div>
              <span class="text-[11px] uppercase tracking-wider text-emerald-400 font-bold">Pergunta Central do CFO</span>
              <h3 class="text-lg font-bold text-white">"Como financiar o crescimento e estancar a perda de caixa sem tomar dívida bancária?"</h3>
            </div>
          </div>
          <div class="px-3 py-1 rounded-lg bg-emerald-950/60 border border-emerald-500/30 text-xs text-emerald-300 font-semibold">
            Meta: DSO &lt; 90 dias • Recuperação de Glosas &gt; 75%
          </div>
        </div>

        <div class="grid grid-cols-1 md:grid-cols-3 gap-4 text-xs">
          <div class="p-4 rounded-xl bg-slate-900/80 border border-slate-800 space-y-2">
            <div class="font-bold text-emerald-300 flex items-center gap-1.5">
              <i data-lucide="target" class="w-4 h-4"></i>
              <span>1. O OKR Definido</span>
            </div>
            <p class="text-slate-300 leading-relaxed">
              Encurtar o DSO geral de 125,1 para menos de 90 dias, elevar a taxa de recuperação de glosas de 50,15% para >75% e estancar as perdas de R$ 7,22M em glosas definitivas para liberar R$ 18M em caixa livre.
            </p>
          </div>
          <div class="p-4 rounded-xl bg-slate-900/80 border border-amber-500/20 space-y-2">
            <div class="font-bold text-amber-300 flex items-center gap-1.5">
              <i data-lucide="alert-triangle" class="w-4 h-4"></i>
              <span>2. O que o OKR empurra a fazer</span>
            </div>
            <p class="text-slate-300 leading-relaxed">
              Bloquear crédito e cotações de forma generalizada para clientes com histórico de atraso ou glosa, e cortar despesas operacionais da equipe de campo.
            </p>
          </div>
          <div class="p-4 rounded-xl bg-rose-950/30 border border-rose-500/30 space-y-2">
            <div class="font-bold text-rose-300 flex items-center gap-1.5">
              <i data-lucide="shield-alert" class="w-4 h-4"></i>
              <span>3. Onde ele erra sozinho (Ponto Cego)</span>
            </div>
            <p class="text-slate-300 leading-relaxed">
              <strong class="text-rose-200">Se bloquear clientes de ciclo longo indiscriminadamente, mata 60% da receita (Operadoras Verticais) e inviabiliza o plano de R$ 110M do CEO.</strong>
            </p>
          </div>
        </div>
      </div>

      <!-- SESSÃO 5: CMO -->
      <div class="glass-card rounded-2xl p-6 border border-purple-500/30 space-y-4">
        <div class="flex flex-col md:flex-row md:items-center justify-between gap-2 border-b border-slate-800 pb-3">
          <div class="flex items-center gap-3">
            <div class="w-9 h-9 rounded-xl bg-purple-500/20 border border-purple-500/30 flex items-center justify-center text-purple-300 font-bold text-sm">
              CMO
            </div>
            <div>
              <span class="text-[11px] uppercase tracking-wider text-purple-400 font-bold">Pergunta Central do CMO</span>
              <h3 class="text-lg font-bold text-white">"Qual o mix de produtos e canais para bater R$ 110M com alta margem?"</h3>
            </div>
          </div>
          <div class="px-3 py-1 rounded-lg bg-purple-950/60 border border-purple-500/30 text-xs text-purple-300 font-semibold">
            Meta: Win Rate Orto/Cardio &gt; 58% • Desconcentração
          </div>
        </div>

        <div class="grid grid-cols-1 md:grid-cols-3 gap-4 text-xs">
          <div class="p-4 rounded-xl bg-slate-900/80 border border-slate-800 space-y-2">
            <div class="font-bold text-purple-300 flex items-center gap-1.5">
              <i data-lucide="target" class="w-4 h-4"></i>
              <span>1. O OKR Definido</span>
            </div>
            <p class="text-slate-300 leading-relaxed">
              Elevar o Win Rate geral de 50,5% para >58%, reverter as perdas de R$ 37,6M por preço e expandir a penetração em hospitais privados e nos estados de PB, RN e AL.
            </p>
          </div>
          <div class="p-4 rounded-xl bg-slate-900/80 border border-amber-500/20 space-y-2">
            <div class="font-bold text-amber-300 flex items-center gap-1.5">
              <i data-lucide="alert-triangle" class="w-4 h-4"></i>
              <span>2. O que o OKR empurra a fazer</span>
            </div>
            <p class="text-slate-300 leading-relaxed">
              Conceder descontos lineares de preço para ganhar propostas contra concorrentes asiáticos e aceitar cotar em qualquer pagador sem histórico de crédito.
            </p>
          </div>
          <div class="p-4 rounded-xl bg-rose-950/30 border border-rose-500/30 space-y-2">
            <div class="font-bold text-rose-300 flex items-center gap-1.5">
              <i data-lucide="shield-alert" class="w-4 h-4"></i>
              <span>3. Onde ele erra sozinho (Ponto Cego)</span>
            </div>
            <p class="text-slate-300 leading-relaxed">
              <strong class="text-rose-200">Dar desconto linear destrói a margem bruta necessária para financiar o plano de R$ 110M sem dívida.</strong>
            </p>
          </div>
        </div>
      </div>

    </div>

    <!-- TAB 1: OVERVIEW -->
    <div id="tab-overview" class="tab-content space-y-6">
      <div class="relative overflow-hidden rounded-2xl bg-gradient-to-r from-slate-900 via-slate-800 to-indigo-950 p-6 border border-slate-700/60 shadow-2xl">
        <div class="relative z-10 flex flex-col md:flex-row md:items-center justify-between gap-4">
          <div class="space-y-1.5">
            <div class="flex items-center gap-2">
              <span class="px-2.5 py-0.5 text-xs font-bold rounded bg-indigo-500/20 text-indigo-300 border border-indigo-500/30">Diagnóstico Executivo Multidimensional</span>
              <span class="text-xs text-slate-400">Dados Consolidados: 2021 a 2025</span>
            </div>
            <h2 class="text-2xl font-black text-white tracking-tight">Painel de Decisão Estratégica Integrada</h2>
            <p class="text-sm text-slate-300 max-w-3xl">
              Análise dos 2.371 negócios médicos da FH Saúde. Como cada diretor executivo (CEO, CFO, COO, CHRO, CMO) deve interpretar os dados, mitigar perdas e orquestrar a expansão autofinanciada de R$ 110M.
            </p>
          </div>
          <div class="flex items-center gap-3">
            <button onclick="switchTab('dilemmas')" class="px-4 py-2 rounded-xl bg-amber-500 hover:bg-amber-400 text-slate-950 font-bold text-xs shadow-lg shadow-amber-500/20 flex items-center gap-2 transition-all">
              <i data-lucide="help-circle" class="w-4 h-4"></i>
              <span>Ver Dilemas de OKR & Perguntas</span>
            </button>
          </div>
        </div>
      </div>

      <!-- Top KPI Cards -->
      <div class="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-6 gap-3">
        <div class="glass-card p-4 rounded-xl space-y-1">
          <div class="flex items-center justify-between text-slate-400 text-xs">
            <span>Pipeline Total</span>
            <i data-lucide="layers" class="w-4 h-4 text-sky-400"></i>
          </div>
          <div class="text-lg font-bold text-white">R$ 369,25M</div>
          <div class="text-[11px] text-slate-400">2.371 oportunidades</div>
        </div>
        <div class="glass-card p-4 rounded-xl space-y-1">
          <div class="flex items-center justify-between text-slate-400 text-xs">
            <span>Receita Ganha</span>
            <i data-lucide="check-circle" class="w-4 h-4 text-emerald-400"></i>
          </div>
          <div class="text-lg font-bold text-emerald-400">R$ 176,30M</div>
          <div class="text-[11px] text-emerald-400/80">1.198 cirurgias ganhas</div>
        </div>
        <div class="glass-card p-4 rounded-xl space-y-1">
          <div class="flex items-center justify-between text-slate-400 text-xs">
            <span>Valor Perdido</span>
            <i data-lucide="x-circle" class="w-4 h-4 text-rose-400"></i>
          </div>
          <div class="text-lg font-bold text-rose-400">R$ 192,95M</div>
          <div class="text-[11px] text-rose-400/80">1.173 cotações perdidas</div>
        </div>
        <div class="glass-card p-4 rounded-xl space-y-1">
          <div class="flex items-center justify-between text-slate-400 text-xs">
            <span>Glosas Aplicadas</span>
            <i data-lucide="alert-triangle" class="w-4 h-4 text-amber-400"></i>
          </div>
          <div class="text-lg font-bold text-amber-400">R$ 14,49M</div>
          <div class="text-[11px] text-slate-400">8,2% da receita bruta</div>
        </div>
        <div class="glass-card p-4 rounded-xl space-y-1">
          <div class="flex items-center justify-between text-slate-400 text-xs">
            <span>Glosa Não Recup.</span>
            <i data-lucide="shield-alert" class="w-4 h-4 text-red-500"></i>
          </div>
          <div class="text-lg font-bold text-red-400">R$ 7,22M</div>
          <div class="text-[11px] text-red-400/80">Perda financeira real</div>
        </div>
        <div class="glass-card p-4 rounded-xl space-y-1">
          <div class="flex items-center justify-between text-slate-400 text-xs">
            <span>Ciclo Médio Total</span>
            <i data-lucide="clock" class="w-4 h-4 text-purple-400"></i>
          </div>
          <div class="text-lg font-bold text-purple-400">164,7 dias</div>
          <div class="text-[11px] text-slate-400">Cotação ao Pagamento</div>
        </div>
      </div>

      <!-- YoY Chart -->
      <div class="grid grid-cols-1 lg:grid-cols-2 gap-6">
        <div class="glass-card p-5 rounded-2xl space-y-3">
          <h4 class="text-sm font-bold text-white flex items-center gap-2">
            <i data-lucide="trending-up" class="w-4 h-4 text-sky-400"></i>
            Evolução Histórica Anual (Receita Ganha vs Perdida)
          </h4>
          <div class="h-64">
            <canvas id="chartOverviewYoY"></canvas>
          </div>
        </div>
        <div class="glass-card p-5 rounded-2xl space-y-3">
          <h4 class="text-sm font-bold text-white flex items-center gap-2">
            <i data-lucide="pie-chart" class="w-4 h-4 text-rose-400"></i>
            Principais Ofensores de Perda de Faturamento (R$)
          </h4>
          <div class="h-64">
            <canvas id="chartOverviewLosses"></canvas>
          </div>
        </div>
      </div>
    </div>

    <!-- TAB 2: CEO -->
    <div id="tab-ceo" class="tab-content hidden space-y-6">
      <div class="glass-card rounded-2xl p-6 border-l-4 border-l-indigo-500 relative overflow-hidden">
        <div class="flex flex-col md:flex-row md:items-center justify-between gap-4">
          <div class="space-y-1">
            <div class="flex items-center gap-2">
              <span class="px-2.5 py-0.5 rounded-full text-xs font-bold bg-indigo-500/20 text-indigo-300 border border-indigo-500/30">Visão do Chief Executive Officer (CEO)</span>
              <span class="text-xs text-slate-400">Estratégia Corporativa • Expansão • Governança</span>
            </div>
            <h2 class="text-xl font-bold text-white">Direcionamento Estratégico & Sustentabilidade do Negócio</h2>
            <p class="text-xs text-slate-300 max-w-3xl">
              Foco em escala de longo prazo, rentabilidade do portfólio, expansão regional e mitigação de vulnerabilidades de concentração de receita e clientes.
            </p>
          </div>
          <div class="flex items-center gap-4 bg-indigo-950/40 p-3 rounded-xl border border-indigo-500/20">
            <div>
              <div class="text-[10px] text-slate-400 uppercase tracking-wider">CAGR (2021-2025)</div>
              <div class="text-lg font-bold text-indigo-400">+19,3% a.a.</div>
            </div>
            <div class="h-8 w-px bg-slate-700"></div>
            <div>
              <div class="text-[10px] text-slate-400 uppercase tracking-wider">Meta 2030</div>
              <div class="text-lg font-bold text-emerald-400">R$ 110 Milhões</div>
            </div>
          </div>
        </div>
      </div>

      <!-- Projeção 5 Anos -->
      <div class="glass-card p-5 rounded-2xl space-y-4">
        <div class="flex items-center justify-between border-b border-slate-800 pb-3">
          <div>
            <h4 class="text-sm font-bold text-white flex items-center gap-2">
              <i data-lucide="trending-up" class="w-4 h-4 text-indigo-400"></i>
              Curva de Expansão: R$ 48,6M (2025) ➔ R$ 110M (2030) e a Trava do Capital de Giro
            </h4>
            <p class="text-xs text-slate-400">Como a redução do ciclo financeiro permite crescer sem dívida</p>
          </div>
          <span class="px-2 py-0.5 rounded bg-indigo-500/20 text-indigo-300 text-xs font-semibold">Taxa CAGR Necessária: +17,7% a.a.</span>
        </div>

        <div class="grid grid-cols-2 md:grid-cols-6 gap-3 text-center">
          <div class="p-3 rounded-xl bg-slate-900/90 border border-slate-800">
            <div class="text-[10px] text-slate-400">2025 (Atual)</div>
            <div class="text-sm font-bold text-white">R$ 48,6M</div>
            <div class="text-[10px] text-amber-400 mt-1">Cap. Preso: R$ 21,9M</div>
          </div>
          <div class="p-3 rounded-xl bg-slate-900/90 border border-indigo-500/30">
            <div class="text-[10px] text-indigo-400 font-bold">2026 (Ano que vem)</div>
            <div class="text-sm font-bold text-indigo-300">R$ 57,2M</div>
            <div class="text-[10px] text-amber-400 mt-1">Cap. Preso: R$ 25,8M</div>
          </div>
          <div class="p-3 rounded-xl bg-slate-900/90 border border-slate-800">
            <div class="text-[10px] text-slate-400">2027</div>
            <div class="text-sm font-bold text-white">R$ 67,3M</div>
            <div class="text-[10px] text-amber-400 mt-1">Cap. Preso: R$ 30,4M</div>
          </div>
          <div class="p-3 rounded-xl bg-slate-900/90 border border-slate-800">
            <div class="text-[10px] text-slate-400">2028</div>
            <div class="text-sm font-bold text-white">R$ 79,2M</div>
            <div class="text-[10px] text-amber-400 mt-1">Cap. Preso: R$ 35,7M</div>
          </div>
          <div class="p-3 rounded-xl bg-slate-900/90 border border-slate-800">
            <div class="text-[10px] text-slate-400">2029</div>
            <div class="text-sm font-bold text-white">R$ 93,2M</div>
            <div class="text-[10px] text-amber-400 mt-1">Cap. Preso: R$ 42,0M</div>
          </div>
          <div class="p-3 rounded-xl bg-emerald-950/40 border border-emerald-500/40">
            <div class="text-[10px] text-emerald-400 font-bold">2030 (Meta)</div>
            <div class="text-sm font-bold text-emerald-400">R$ 110,0M</div>
            <div class="text-[10px] text-emerald-300 mt-1">Cap. Preso: R$ 49,6M</div>
          </div>
        </div>
      </div>

      <!-- Regional Charts -->
      <div class="grid grid-cols-1 lg:grid-cols-2 gap-6">
        <div class="glass-card p-5 rounded-2xl space-y-3">
          <h4 class="text-sm font-bold text-white flex items-center gap-2">
            <i data-lucide="map-pin" class="w-4 h-4 text-indigo-400"></i>
            Concentração de Receita por Estado (Nordeste)
          </h4>
          <div class="h-64">
            <canvas id="chartCeoStates"></canvas>
          </div>
        </div>
        <div class="glass-card p-5 rounded-2xl space-y-3">
          <h4 class="text-sm font-bold text-white flex items-center gap-2">
            <i data-lucide="pie-chart" class="w-4 h-4 text-sky-400"></i>
            Receita e Participação por Especialidade Médica
          </h4>
          <div class="h-64">
            <canvas id="chartCeoLines"></canvas>
          </div>
        </div>
      </div>
    </div>

    <!-- TAB 3: CFO -->
    <div id="tab-cfo" class="tab-content hidden space-y-6">
      <div class="glass-card rounded-2xl p-6 border-l-4 border-l-emerald-500 relative overflow-hidden">
        <div class="flex flex-col md:flex-row md:items-center justify-between gap-4">
          <div class="space-y-1">
            <div class="flex items-center gap-2">
              <span class="px-2.5 py-0.5 rounded-full text-xs font-bold bg-emerald-500/20 text-emerald-300 border border-emerald-500/30">Visão do Chief Financial Officer (CFO)</span>
              <span class="text-xs text-slate-400">Rentabilidade Líquida • Gestão de Glosas • Capital de Giro • DSO</span>
            </div>
            <h2 class="text-xl font-bold text-white">Controle Financeiro, Risco de Crédito & Eficiência de Caixa</h2>
            <p class="text-xs text-slate-300 max-w-3xl">
              Análise do impacto das glosas hospitalares, prazos médios de recebimento (DSO) de 125 dias, estoque consignado imobilizado e fluxo de caixa livre.
            </p>
          </div>
          <div class="flex items-center gap-4 bg-emerald-950/40 p-3 rounded-xl border border-emerald-500/20">
            <div>
              <div class="text-[10px] text-slate-400 uppercase tracking-wider">Taxa de Recup. de Glosa</div>
              <div class="text-lg font-bold text-amber-400">50,15%</div>
            </div>
            <div class="h-8 w-px bg-slate-700"></div>
            <div>
              <div class="text-[10px] text-slate-400 uppercase tracking-wider">Perda de Glosa Líquida</div>
              <div class="text-lg font-bold text-red-400">R$ 7,22M</div>
            </div>
          </div>
        </div>
      </div>

      <div class="grid grid-cols-1 lg:grid-cols-2 gap-6">
        <div class="glass-card p-5 rounded-2xl space-y-3">
          <h4 class="text-sm font-bold text-white flex items-center gap-2">
            <i data-lucide="bar-chart-2" class="w-4 h-4 text-emerald-400"></i>
            Glosas Totais vs Glosas Perdidas por Tipo de Pagador (R$)
          </h4>
          <div class="h-64">
            <canvas id="chartCfoGlosas"></canvas>
          </div>
        </div>
        <div class="glass-card p-5 rounded-2xl space-y-3">
          <h4 class="text-sm font-bold text-white flex items-center gap-2">
            <i data-lucide="calendar" class="w-4 h-4 text-amber-400"></i>
            Prazo Médio de Recebimento (DSO) por Tipo de Pagador
          </h4>
          <div class="h-64">
            <canvas id="chartCfoDso"></canvas>
          </div>
        </div>
      </div>
    </div>

    <!-- TAB 4: COO -->
    <div id="tab-coo" class="tab-content hidden space-y-6">
      <div class="glass-card rounded-2xl p-6 border-l-4 border-l-amber-500 relative overflow-hidden">
        <div class="flex flex-col md:flex-row md:items-center justify-between gap-4">
          <div class="space-y-1">
            <div class="flex items-center gap-2">
              <span class="px-2.5 py-0.5 rounded-full text-xs font-bold bg-amber-500/20 text-amber-300 border border-amber-500/30">Visão do Chief Operating Officer (COO)</span>
              <span class="text-xs text-slate-400">Eficiência Operacional • Dimensionamento de Headcount • Capital de Consignação</span>
            </div>
            <h2 class="text-xl font-bold text-white">Dimensionamento de Pessoal, Gestão de Consignação & SLAs</h2>
            <p class="text-xs text-slate-300 max-w-3xl">
              Como sustentar nível de serviço 24x7 sem contratar prejuízo. O dilema entre contratar equipe vs ter capital de giro para bancar caixas consignadas.
            </p>
          </div>
          <div class="flex items-center gap-4 bg-amber-950/40 p-3 rounded-xl border border-amber-500/20">
            <div>
              <div class="text-[10px] text-slate-400 uppercase tracking-wider">Cirurgia → Faturamento</div>
              <div class="text-lg font-bold text-rose-400">58,0 dias</div>
            </div>
            <div class="h-8 w-px bg-slate-700"></div>
            <div>
              <div class="text-[10px] text-slate-400 uppercase tracking-wider">Consignação Média</div>
              <div class="text-lg font-bold text-amber-400">39,6 dias</div>
            </div>
          </div>
        </div>
      </div>

      <!-- Lead Times -->
      <div class="grid grid-cols-1 md:grid-cols-5 gap-3">
        <div class="glass-card p-4 rounded-xl space-y-1 border-t-2 border-t-sky-400">
          <div class="text-xs text-slate-400">Etapa 1: Cotação→Autoriz.</div>
          <div class="text-xl font-bold text-sky-400">14,8 dias</div>
          <div class="text-[11px] text-slate-400">Mín: 3d | Máx: 26d</div>
        </div>
        <div class="glass-card p-4 rounded-xl space-y-1 border-t-2 border-t-indigo-400">
          <div class="text-xs text-slate-400">Etapa 2: Autoriz.→Cirurgia</div>
          <div class="text-xl font-bold text-indigo-400">~12,5 dias</div>
          <div class="text-[11px] text-slate-400">Agendamento & Envio</div>
        </div>
        <div class="glass-card p-4 rounded-xl space-y-1 border-t-2 border-t-rose-500">
          <div class="text-xs text-slate-400">Etapa 3: Cirurgia→Faturam.</div>
          <div class="text-xl font-bold text-rose-400">58,0 dias</div>
          <div class="text-[11px] text-rose-400 font-semibold">Gargalo Crítico!</div>
        </div>
        <div class="glass-card p-4 rounded-xl space-y-1 border-t-2 border-t-amber-400">
          <div class="text-xs text-slate-400">Etapa 4: Faturam.→Pagto</div>
          <div class="text-xl font-bold text-amber-400">125,1 dias</div>
          <div class="text-[11px] text-slate-400">DSO Financeiro</div>
        </div>
        <div class="glass-card p-4 rounded-xl space-y-1 border-t-2 border-t-purple-400">
          <div class="text-xs text-slate-400">Ciclo Operacional Total</div>
          <div class="text-xl font-bold text-purple-400">164,7 dias</div>
          <div class="text-[11px] text-slate-400">Lead time ponta a ponta</div>
        </div>
      </div>

      <div class="grid grid-cols-1 lg:grid-cols-2 gap-6">
        <div class="glass-card p-5 rounded-2xl space-y-3">
          <h4 class="text-sm font-bold text-white flex items-center gap-2">
            <i data-lucide="funnel" class="w-4 h-4 text-amber-400"></i>
            Perda Financeira por Etapa do Funil Cirúrgico (R$)
          </h4>
          <div class="h-64">
            <canvas id="chartCooStages"></canvas>
          </div>
        </div>
        <div class="glass-card p-5 rounded-2xl space-y-3">
          <h4 class="text-sm font-bold text-white flex items-center gap-2">
            <i data-lucide="alert-octagon" class="w-4 h-4 text-rose-400"></i>
            Perdas com Origem Puramente Operacional / Logística (R$)
          </h4>
          <div class="h-64">
            <canvas id="chartCooOperationalLosses"></canvas>
          </div>
        </div>
      </div>
    </div>

    <!-- TAB 5: CHRO -->
    <div id="tab-chro" class="tab-content hidden space-y-6">
      <div class="glass-card rounded-2xl p-6 border-l-4 border-l-pink-500 relative overflow-hidden">
        <div class="flex flex-col md:flex-row md:items-center justify-between gap-4">
          <div class="space-y-1">
            <div class="flex items-center gap-2">
              <span class="px-2.5 py-0.5 rounded-full text-xs font-bold bg-pink-500/20 text-pink-300 border border-pink-500/30">Visão do Chief Human Resources Officer (CHRO)</span>
              <span class="text-xs text-slate-400">Produtividade Comercial • Consumo de Capital de Giro • Qualidade & Glosas</span>
            </div>
            <h2 class="text-xl font-bold text-white">Desempenho Real da Equipe: Faturamento Bruto vs Capital Preso</h2>
            <p class="text-xs text-slate-300 max-w-3xl">
              Ricardo Aragão lidera R$ 41,2M em receita, mas consome R$ 24,9M em capital de giro e gerou R$ 2,41M em perdas de glosa. Descubra os verdadeiros geradores de caixa da FH Saúde.
            </p>
          </div>
          <div class="flex items-center gap-4 bg-pink-950/40 p-3 rounded-xl border border-pink-500/20">
            <div>
              <div class="text-[10px] text-slate-400 uppercase tracking-wider">Top 3 Vendedores</div>
              <div class="text-lg font-bold text-pink-400">48,5%</div>
              <div class="text-[10px] text-slate-400">da receita total</div>
            </div>
            <div class="h-8 w-px bg-slate-700"></div>
            <div>
              <div class="text-[10px] text-slate-400 uppercase tracking-wider">Capital Preso Top 3</div>
              <div class="text-lg font-bold text-rose-400">R$ 46,8 Milhões</div>
            </div>
          </div>
        </div>
      </div>

      <div class="grid grid-cols-1 lg:grid-cols-2 gap-6">
        <div class="glass-card p-5 rounded-2xl space-y-3">
          <h4 class="text-sm font-bold text-white flex items-center gap-2">
            <i data-lucide="award" class="w-4 h-4 text-pink-400"></i>
            Ranking de Receita Ganha por Vendedor (R$ Milhões)
          </h4>
          <div class="h-64">
            <canvas id="chartChroRevenue"></canvas>
          </div>
        </div>
        <div class="glass-card p-5 rounded-2xl space-y-3">
          <h4 class="text-sm font-bold text-white flex items-center gap-2">
            <i data-lucide="percent" class="w-4 h-4 text-sky-400"></i>
            Taxa de Conversão (% Win Rate) vs Taxa de Glosa Perdida (%)
          </h4>
          <div class="h-64">
            <canvas id="chartChroWinRate"></canvas>
          </div>
        </div>
      </div>

      <!-- Seller Table -->
      <div class="glass-card rounded-2xl p-5 space-y-4">
        <div class="flex items-center justify-between">
          <div>
            <h4 class="text-sm font-bold text-white flex items-center gap-2">
              <i data-lucide="users" class="w-4 h-4 text-pink-400"></i>
              Tabela de Produtividade, Qualidade & Consumo de Capital de Giro
            </h4>
            <p class="text-xs text-slate-400">Mostra claramente quem gera lucro líquido real vs quem consome caixa</p>
          </div>
          <input type="text" id="sellerSearch" onkeyup="filterSellerTable()" placeholder="Buscar vendedor..." class="px-3 py-1 bg-slate-900 border border-slate-700 rounded-lg text-xs text-white focus:outline-none focus:border-pink-500">
        </div>
        <div class="overflow-x-auto custom-scrollbar max-h-96">
          <table class="w-full text-xs text-left" id="sellerTable">
            <thead class="bg-slate-900/90 text-slate-400 uppercase text-[10px] tracking-wider border-b border-slate-800 sticky top-0">
              <tr>
                <th class="py-2.5 px-3">Vendedor</th>
                <th class="py-2.5 px-3 text-right">Deals</th>
                <th class="py-2.5 px-3 text-right">Win Rate</th>
                <th class="py-2.5 px-3 text-right">Receita Bruta</th>
                <th class="py-2.5 px-3 text-right">Glosa Perdida</th>
                <th class="py-2.5 px-3 text-right">% Glosa</th>
                <th class="py-2.5 px-3 text-right">DSO Médio</th>
                <th class="py-2.5 px-3 text-right">Ciclo Médio</th>
                <th class="py-2.5 px-3 text-right text-amber-300">Capital Preso Est.</th>
              </tr>
            </thead>
            <tbody class="divide-y divide-slate-800/60 font-medium">
"""

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

for s in seller_profiles:
    wr_color = "text-emerald-400 font-bold" if s['wr'] >= 54 else ("text-amber-400" if s['wr'] >= 48 else "text-rose-400")
    glosa_color = "text-red-400 font-bold" if s['tx_glosa'] >= 4.5 else ("text-amber-300" if s['tx_glosa'] >= 3.0 else "text-emerald-400")
    cap_color = "text-rose-400 font-bold" if s['cap'] >= 10000000 else ("text-amber-300" if s['cap'] >= 5000000 else "text-emerald-300")
    html_content += f"""
              <tr class="hover:bg-slate-800/30 transition-colors">
                <td class="py-2.5 px-3 font-bold text-white">{s['name']}</td>
                <td class="py-2.5 px-3 text-right text-slate-300">{s['deals']}</td>
                <td class="py-2.5 px-3 text-right {wr_color}">{s['wr']}%</td>
                <td class="py-2.5 px-3 text-right font-bold text-emerald-400">R$ {s['rec']:,.2f}</td>
                <td class="py-2.5 px-3 text-right text-rose-400">R$ {s['glosa_p']:,.2f}</td>
                <td class="py-2.5 px-3 text-right {glosa_color}">{s['tx_glosa']}%</td>
                <td class="py-2.5 px-3 text-right text-slate-300">{s['dso']:.1f}d</td>
                <td class="py-2.5 px-3 text-right text-slate-300">{s['ciclo']:.1f}d</td>
                <td class="py-2.5 px-3 text-right {cap_color}">R$ {s['cap']/1e6:.2f}M</td>
              </tr>"""

html_content += f"""
            </tbody>
          </table>
        </div>
      </div>
    </div>

    <!-- TAB 6: CMO -->
    <div id="tab-cmo" class="tab-content hidden space-y-6">
      <div class="glass-card rounded-2xl p-6 border-l-4 border-l-purple-500 relative overflow-hidden">
        <div class="flex flex-col md:flex-row md:items-center justify-between gap-4">
          <div class="space-y-1">
            <div class="flex items-center gap-2">
              <span class="px-2.5 py-0.5 rounded-full text-xs font-bold bg-purple-500/20 text-purple-300 border border-purple-500/30">Visão do Chief Marketing Officer (CMO)</span>
              <span class="text-xs text-slate-400">Mix de Produtos • Inteligência de Perdas • Posicionamento & Go-To-Market</span>
            </div>
            <h2 class="text-xl font-bold text-white">Análise de Mercado, Portfólio de Produtos & Motivos de Perda</h2>
            <p class="text-xs text-slate-300 max-w-3xl">
              Comportamento dos 12 produtos médicos, análise aprofundada dos R$ 192,9M perdidos (Preço alto causou R$ 37,6M; Fornecedor exclusivo R$ 22,2M) e penetração por cliente e pagador.
            </p>
          </div>
          <div class="flex items-center gap-4 bg-purple-950/40 p-3 rounded-xl border border-purple-500/20">
            <div>
              <div class="text-[10px] text-slate-400 uppercase tracking-wider">Perda por Preço Alto</div>
              <div class="text-lg font-bold text-rose-400">R$ 37,56M</div>
              <div class="text-[10px] text-slate-400">241 cotações</div>
            </div>
            <div class="h-8 w-px bg-slate-700"></div>
            <div>
              <div class="text-[10px] text-slate-400 uppercase tracking-wider">Produto Top Receita</div>
              <div class="text-lg font-bold text-purple-300">Implante Quadril</div>
              <div class="text-[10px] text-slate-400">R$ 25,46M</div>
            </div>
          </div>
        </div>
      </div>

      <div class="grid grid-cols-1 lg:grid-cols-2 gap-6">
        <div class="glass-card p-5 rounded-2xl space-y-3">
          <h4 class="text-sm font-bold text-white flex items-center gap-2">
            <i data-lucide="package" class="w-4 h-4 text-purple-400"></i>
            Receita Ganha por Produto (R$ Milhões)
          </h4>
          <div class="h-64">
            <canvas id="chartCmoProducts"></canvas>
          </div>
        </div>
        <div class="glass-card p-5 rounded-2xl space-y-3">
          <h4 class="text-sm font-bold text-white flex items-center gap-2">
            <i data-lucide="bar-chart" class="w-4 h-4 text-rose-400"></i>
            Pareto de Motivos de Perda de Negócios (R$ Milhões)
          </h4>
          <div class="h-64">
            <canvas id="chartCmoLossPareto"></canvas>
          </div>
        </div>
      </div>
    </div>

  </main>

  <!-- Footer -->
  <footer class="border-t border-slate-800/80 bg-slate-950 py-6 text-center text-xs text-slate-500">
    <div class="max-w-7xl mx-auto px-4 flex flex-col md:flex-row items-center justify-between gap-2">
      <div class="flex items-center gap-2">
        <i data-lucide="shield-check" class="w-4 h-4 text-sky-400"></i>
        <span>FH Saúde Inteligência Estratégica Executiva • Base de 2.371 Casos Reais</span>
      </div>
      <div>
        <span>Gerado para Análise Individual C-Suite: CEO • CFO • COO • CHRO • CMO</span>
      </div>
    </div>
  </footer>

  <!-- Embedded Script -->
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
            btn.classList.add('tab-active');
          }} else {{
            content.classList.add('hidden');
            btn.classList.remove('tab-active');
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

    Chart.defaults.color = '#94a3b8';
    Chart.defaults.font.family = "'Plus Jakarta Sans', sans-serif";
    Chart.defaults.plugins.legend.labels.usePointStyle = true;

    document.addEventListener('DOMContentLoaded', () => {{
      lucide.createIcons();

      // Chart Overview YoY
      const ctxOverviewYoY = document.getElementById('chartOverviewYoY').getContext('2d');
      new Chart(ctxOverviewYoY, {{
        type: 'bar',
        data: {{
          labels: dataBundle.years.map(y => y.ano),
          datasets: [
            {{
              label: 'Receita Ganha (R$ M)',
              data: dataBundle.years.map(y => (y.receita_ganha / 1e6).toFixed(2)),
              backgroundColor: '#10b981',
              borderRadius: 6,
            }},
            {{
              label: 'Valor Perdido (R$ M)',
              data: dataBundle.years.map(y => (y.valor_perdido / 1e6).toFixed(2)),
              backgroundColor: '#f43f5e',
              borderRadius: 6,
            }},
            {{
              label: 'Receita Líquida (R$ M)',
              data: dataBundle.years.map(y => (y.receita_liquida / 1e6).toFixed(2)),
              type: 'line',
              borderColor: '#38bdf8',
              backgroundColor: '#38bdf8',
              borderWidth: 2,
              pointRadius: 4,
            }}
          ]
        }},
        options: {{
          responsive: true,
          maintainAspectRatio: false,
          scales: {{
            y: {{ grid: {{ color: 'rgba(255,255,255,0.05)' }}, title: {{ display: true, text: 'R$ Milhões' }} }},
            x: {{ grid: {{ display: false }} }}
          }}
        }}
      }});

      // Chart Overview Losses (Top 6)
      const topLosses = dataBundle.loss_reasons.slice(0, 6);
      const ctxOverviewLosses = document.getElementById('chartOverviewLosses').getContext('2d');
      new Chart(ctxOverviewLosses, {{
        type: 'doughnut',
        data: {{
          labels: topLosses.map(l => l.motivo),
          datasets: [{{
            data: topLosses.map(l => (l.valor_perdido / 1e6).toFixed(2)),
            backgroundColor: ['#ef4444', '#f97316', '#f59e0b', '#8b5cf6', '#06b6d4', '#ec4899'],
            borderWidth: 0
          }}]
        }},
        options: {{
          responsive: true,
          maintainAspectRatio: false,
          plugins: {{
            legend: {{ position: 'right', labels: {{ boxWidth: 10, font: {{ size: 10 }} }} }}
          }}
        }}
      }});

      // Chart CEO States
      const ctxCeoStates = document.getElementById('chartCeoStates').getContext('2d');
      new Chart(ctxCeoStates, {{
        type: 'bar',
        data: {{
          labels: dataBundle.states.map(s => s.estado + ' (' + s.win_rate + '%)'),
          datasets: [{{
            label: 'Receita Ganha (R$ M)',
            data: dataBundle.states.map(s => (s.receita_ganha / 1e6).toFixed(2)),
            backgroundColor: ['#6366f1', '#38bdf8', '#10b981', '#f59e0b'],
            borderRadius: 6
          }}]
        }},
        options: {{
          responsive: true,
          maintainAspectRatio: false,
          scales: {{
            y: {{ grid: {{ color: 'rgba(255,255,255,0.05)' }}, title: {{ display: true, text: 'R$ Milhões' }} }},
            x: {{ grid: {{ display: false }} }}
          }}
        }}
      }});

      // Chart CEO Lines
      const ctxCeoLines = document.getElementById('chartCeoLines').getContext('2d');
      new Chart(ctxCeoLines, {{
        type: 'pie',
        data: {{
          labels: dataBundle.lines.map(l => l.linha),
          datasets: [{{
            data: dataBundle.lines.map(l => (l.receita_ganha / 1e6).toFixed(2)),
            backgroundColor: ['#3b82f6', '#10b981', '#8b5cf6'],
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

      // Chart CFO Glosas
      const ctxCfoGlosas = document.getElementById('chartCfoGlosas').getContext('2d');
      new Chart(ctxCfoGlosas, {{
        type: 'bar',
        data: {{
          labels: dataBundle.payers.map(p => p.tipo),
          datasets: [
            {{
              label: 'Glosa Total Aplicada (R$ M)',
              data: dataBundle.payers.map(p => (p.valor_glosado / 1e6).toFixed(2)),
              backgroundColor: '#f59e0b',
              borderRadius: 6
            }},
            {{
              label: 'Glosa Não Recuperada / Perda (R$ M)',
              data: dataBundle.payers.map(p => (p.glosa_nao_recuperada / 1e6).toFixed(2)),
              backgroundColor: '#ef4444',
              borderRadius: 6
            }}
          ]
        }},
        options: {{
          responsive: true,
          maintainAspectRatio: false,
          scales: {{
            y: {{ grid: {{ color: 'rgba(255,255,255,0.05)' }}, title: {{ display: true, text: 'R$ Milhões' }} }},
            x: {{ grid: {{ display: false }} }}
          }}
        }}
      }});

      // Chart CFO DSO
      const ctxCfoDso = document.getElementById('chartCfoDso').getContext('2d');
      new Chart(ctxCfoDso, {{
        type: 'bar',
        data: {{
          labels: dataBundle.payers.map(p => p.tipo),
          datasets: [
            {{
              label: 'Prazo Médio Pagamento DSO (Dias)',
              data: dataBundle.payers.map(p => p.dias_pagamento_medio),
              backgroundColor: '#10b981',
              borderRadius: 6
            }},
            {{
              label: 'Prazo Médio Consignação (Dias)',
              data: dataBundle.payers.map(p => p.dias_consignacao_medio),
              backgroundColor: '#0ea5e9',
              borderRadius: 6
            }}
          ]
        }},
        options: {{
          responsive: true,
          maintainAspectRatio: false,
          scales: {{
            y: {{ grid: {{ color: 'rgba(255,255,255,0.05)' }}, title: {{ display: true, text: 'Dias Corridos' }} }},
            x: {{ grid: {{ display: false }} }}
          }}
        }}
      }});

      // Chart COO Stages
      const ctxCooStages = document.getElementById('chartCooStages').getContext('2d');
      new Chart(ctxCooStages, {{
        type: 'bar',
        data: {{
          labels: dataBundle.loss_stages.map(s => s.etapa),
          datasets: [{{
            label: 'Valor Perdido por Etapa (R$ M)',
            data: dataBundle.loss_stages.map(s => (s.valor_perdido / 1e6).toFixed(2)),
            backgroundColor: ['#38bdf8', '#6366f1', '#f59e0b', '#ec4899'],
            borderRadius: 6
          }}]
        }},
        options: {{
          responsive: true,
          maintainAspectRatio: false,
          scales: {{
            y: {{ grid: {{ color: 'rgba(255,255,255,0.05)' }}, title: {{ display: true, text: 'R$ Milhões' }} }},
            x: {{ grid: {{ display: false }} }}
          }}
        }}
      }});

      // Chart COO Operational Losses
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
            backgroundColor: ['#f43f5e', '#fb923c', '#eab308', '#a855f7', '#06b6d4'],
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

      // Chart CHRO Revenue
      const topSellers = dataBundle.sellers.slice(0, 10);
      const ctxChroRev = document.getElementById('chartChroRevenue').getContext('2d');
      new Chart(ctxChroRev, {{
        type: 'bar',
        data: {{
          labels: topSellers.map(s => s.vendedor),
          datasets: [{{
            label: 'Receita Ganha (R$ M)',
            data: topSellers.map(s => (s.receita_ganha / 1e6).toFixed(2)),
            backgroundColor: '#ec4899',
            borderRadius: 6
          }}]
        }},
        options: {{
          responsive: true,
          maintainAspectRatio: false,
          indexAxis: 'y',
          scales: {{
            x: {{ grid: {{ color: 'rgba(255,255,255,0.05)' }}, title: {{ display: true, text: 'R$ Milhões' }} }},
            y: {{ grid: {{ display: false }} }}
          }}
        }}
      }});

      // Chart CHRO Win Rate
      const ctxChroWr = document.getElementById('chartChroWinRate').getContext('2d');
      new Chart(ctxChroWr, {{
        type: 'bar',
        data: {{
          labels: topSellers.map(s => s.vendedor),
          datasets: [
            {{
              label: 'Win Rate (%)',
              data: topSellers.map(s => s.win_rate),
              backgroundColor: '#10b981',
              borderRadius: 6
            }},
            {{
              label: '% Glosa Perdida / Rec (%)',
              data: topSellers.map(s => s.taxa_glosa_perdida),
              backgroundColor: '#ef4444',
              borderRadius: 6
            }}
          ]
        }},
        options: {{
          responsive: true,
          maintainAspectRatio: false,
          scales: {{
            y: {{ grid: {{ color: 'rgba(255,255,255,0.05)' }}, title: {{ display: true, text: 'Percentual (%)' }} }},
            x: {{ grid: {{ display: false }} }}
          }}
        }}
      }});

      // Chart CMO Products
      const ctxCmoProd = document.getElementById('chartCmoProducts').getContext('2d');
      new Chart(ctxCmoProd, {{
        type: 'bar',
        data: {{
          labels: dataBundle.products.slice(0, 8).map(p => p.produto),
          datasets: [{{
            label: 'Receita Ganha (R$ M)',
            data: dataBundle.products.slice(0, 8).map(p => (p.receita_ganha / 1e6).toFixed(2)),
            backgroundColor: '#8b5cf6',
            borderRadius: 6
          }}]
        }},
        options: {{
          responsive: true,
          maintainAspectRatio: false,
          indexAxis: 'y',
          scales: {{
            x: {{ grid: {{ color: 'rgba(255,255,255,0.05)' }}, title: {{ display: true, text: 'R$ Milhões' }} }},
            y: {{ grid: {{ display: false }} }}
          }}
        }}
      }});

      // Chart CMO Loss Pareto
      const top8Loss = dataBundle.loss_reasons.slice(0, 8);
      const ctxCmoLoss = document.getElementById('chartCmoLossPareto').getContext('2d');
      new Chart(ctxCmoLoss, {{
        type: 'bar',
        data: {{
          labels: top8Loss.map(l => l.motivo),
          datasets: [{{
            label: 'Valor Perdido (R$ M)',
            data: top8Loss.map(l => (l.valor_perdido / 1e6).toFixed(2)),
            backgroundColor: '#f43f5e',
            borderRadius: 6
          }}]
        }},
        options: {{
          responsive: true,
          maintainAspectRatio: false,
          scales: {{
            y: {{ grid: {{ color: 'rgba(255,255,255,0.05)' }}, title: {{ display: true, text: 'R$ Milhões' }} }},
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

print("Regenerated dashboard_csuite_fhsaude.html successfully with updated COO headount & working capital dilema!")
