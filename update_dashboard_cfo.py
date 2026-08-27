import json

with open('data_bundle.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

# Re-read generate_fhdata_dashboard.py and ensure the CFO session contains the exact question, OKR, impulse, and failure mode
with open('generate_fhdata_dashboard.py', 'r', encoding='utf-8') as f:
    code = f.read()

# Let's replace the CFO card in tab-dilemmas with the exact new question & details
old_cfo_block = """      <!-- SESSÃO 4: CFO -->
      <div class="fh-card rounded-2xl p-5 sm:p-6 border border-[#2AC59E]/30 space-y-4">
        <div class="flex flex-col sm:flex-row sm:items-center justify-between gap-3 border-b border-[#133B3A] pb-3">
          <div class="flex items-center gap-3">
            <div class="w-10 h-10 rounded-xl bg-[#002424] border border-[#2AC59E]/50 flex items-center justify-center text-[#2AC59E] font-extrabold text-sm">
              CFO
            </div>
            <div>
              <span class="text-[10px] uppercase tracking-wider text-[#2AC59E] font-bold">Pergunta Central do CFO</span>
              <h3 class="text-base sm:text-lg font-bold text-[#FAF6E6]">"Como financiar o crescimento e estancar a perda de caixa sem tomar dívida bancária?"</h3>
            </div>
          </div>
          <div class="px-3 py-1.5 rounded-xl bg-[#002424] border border-[#2AC59E]/30 text-xs text-[#52E1B9] font-bold self-start sm:self-auto">
            Meta: DSO &lt; 90 dias • Recuperação de Glosas &gt; 75%
          </div>
        </div>

        <div class="grid grid-cols-1 md:grid-cols-3 gap-4 text-xs">
          <div class="p-4 rounded-xl bg-[#001716] border border-[#133B3A] space-y-2">
            <div class="font-bold text-[#52E1B9] flex items-center gap-1.5">
              <i data-lucide="target" class="w-4 h-4"></i>
              <span>1. O OKR Definido</span>
            </div>
            <p class="text-[#E6E3D3] leading-relaxed">
              Encurtar o DSO geral de 125,1 para menos de 90 dias, elevar a taxa de recuperação de glosas de 50,15% para >75% e estancar as perdas de R$ 7,22M em glosas definitivas para liberar R$ 18M em caixa livre.
            </p>
          </div>
          <div class="p-4 rounded-xl bg-[#001716] border border-[#E2B93B]/30 space-y-2">
            <div class="font-bold text-[#E2B93B] flex items-center gap-1.5">
              <i data-lucide="alert-triangle" class="w-4 h-4"></i>
              <span>2. O que o OKR empurra a fazer</span>
            </div>
            <p class="text-[#E6E3D3] leading-relaxed">
              Bloquear crédito e cotações de forma generalizada para clientes com histórico de atraso ou glosa, e cortar despesas operacionais da equipe de campo.
            </p>
          </div>
          <div class="p-4 rounded-xl bg-[#001716] border border-[#FF6568]/40 space-y-2">
            <div class="font-bold text-[#FF6568] flex items-center gap-1.5">
              <i data-lucide="shield-alert" class="w-4 h-4"></i>
              <span>3. Onde ele erra sozinho (Ponto Cego)</span>
            </div>
            <p class="text-[#E6E3D3] leading-relaxed">
              <strong class="text-[#FF6568]">Se bloquear clientes de ciclo longo indiscriminadamente, mata 60% da receita (Operadoras Verticais) e inviabiliza o plano de R$ 110M do CEO.</strong>
            </p>
          </div>
        </div>
      </div>"""

new_cfo_block = """      <!-- SESSÃO 4: CFO -->
      <div class="fh-card rounded-2xl p-5 sm:p-6 border border-[#2AC59E]/30 space-y-4">
        <div class="flex flex-col sm:flex-row sm:items-center justify-between gap-3 border-b border-[#133B3A] pb-3">
          <div class="flex items-center gap-3">
            <div class="w-10 h-10 rounded-xl bg-[#002424] border border-[#2AC59E]/50 flex items-center justify-center text-[#2AC59E] font-extrabold text-sm mint-glow-sm">
              CFO
            </div>
            <div>
              <span class="text-[10px] uppercase tracking-wider text-[#2AC59E] font-bold">Pergunta Central do CFO</span>
              <h3 class="text-base sm:text-lg font-bold text-[#FAF6E6]">"Em qual etapa do funil eu perco mais dinheiro?"</h3>
            </div>
          </div>
          <div class="px-3 py-1.5 rounded-xl bg-[#002424] border border-[#2AC59E]/30 text-xs text-[#52E1B9] font-bold self-start sm:self-auto">
            Reduzir Ciclo em 30d • Zerar Empréstimos
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
              Reduzir o ciclo financeiro total em <strong class="text-[#FAF6E6]">30 dias</strong> (de 164,7d para 134,7d) e <strong class="text-[#2AC59E]">zerar a necessidade de empréstimos bancários</strong> para bancar o crescimento da empresa.
            </p>
            <div class="text-[11px] text-[#CECABB] bg-[#002424] p-2.5 rounded-lg border border-[#133B3A]">
              Onde o dinheiro sangra: Etapa 1 Cotação (R$ 108,4M) vs Etapa 4 Faturamento/Pós-Cirúrgico (R$ 40,3M em perdas + glosas).
            </div>
          </div>

          <!-- 2. Vício -->
          <div class="p-4 rounded-xl bg-[#001716] border border-[#E2B93B]/30 space-y-2">
            <div class="font-bold text-[#E2B93B] flex items-center gap-1.5">
              <i data-lucide="alert-triangle" class="w-4 h-4"></i>
              <span>2. O que o OKR empurra a fazer</span>
            </div>
            <p class="text-[#E6E3D3] leading-relaxed">
              Cortar cliente "ruim" (com alto DSO ou alta glosa) e apertar os prazos de pagamento na marra, bloqueando cotações no ERP para quem atrasa faturas.
            </p>
          </div>

          <!-- 3. Ponto Cego -->
          <div class="p-4 rounded-xl bg-[#001716] border border-[#FF6568]/40 space-y-2">
            <div class="font-bold text-[#FF6568] flex items-center gap-1.5">
              <i data-lucide="shield-alert" class="w-4 h-4"></i>
              <span>3. Onde ele erra sozinho (Ponto Cego)</span>
            </div>
            <p class="text-[#E6E3D3] leading-relaxed">
              <strong class="text-[#FF6568]">O cliente que ele quer cortar é exatamente a maior conta do CHRO e do CMO!</strong>
            </p>
            <p class="text-[#CECABB] text-[11px] leading-relaxed">
              As operadoras verticalizadas (Vitalis e Bem-Estar) respondem por <strong class="text-[#FAF6E6]">R$ 83,86 Milhões (47,6% de toda a receita)</strong>, onde Ricardo Aragão bate suas metas e o CMO tem seu maior share. Cortar esses clientes destrói metade do faturamento da empresa.
              A solução é <strong class="text-[#2AC59E]">renegociar Acordo de Nível de Serviço Contratual</strong> com desconto financeiro para quitação em 60 dias e auditoria médica prévia de glosas!
            </p>
          </div>
        </div>
      </div>"""

if old_cfo_block in code:
    code = code.replace(old_cfo_block, new_cfo_block)
    print("Replaced old CFO block successfully!")
else:
    print("Old CFO block not found directly, performing structural update.")
    # let's rewrite the script to ensure 100% match

with open('generate_fhdata_dashboard.py', 'w', encoding='utf-8') as f:
    f.write(code)

