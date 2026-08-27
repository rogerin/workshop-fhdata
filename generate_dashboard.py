import csv
import json
from collections import defaultdict, Counter

# Load CSV
with open('fh-saude-vendas - fh-saude-vendas.csv.csv', mode='r', encoding='utf-8') as f:
    rows = list(csv.DictReader(f))

def to_f(v):
    try: return float(v) if v != '' else 0.0
    except: return 0.0

total_deals = len(rows)
ganhos = [r for r in rows if r['status'] == 'Ganho']
perdidos = [r for r in rows if r['status'] == 'Perdido']

# Global metrics
tot_pipeline = sum(to_f(r['valor']) for r in rows)
tot_rec_ganha = sum(to_f(r['receita_ganha']) for r in rows)
tot_perdido = sum(to_f(r['valor_perdido']) for r in rows)
tot_glosado = sum(to_f(r['valor_glosado']) for r in rows)
tot_recuperado = sum(to_f(r['valor_recuperado']) for r in rows)
tot_glosa_perdida = sum(to_f(r['glosa_nao_recuperada']) for r in rows)
tot_rec_liquida = tot_rec_ganha - tot_glosa_perdida
win_rate = len(ganhos) / total_deals * 100
tkt_medio = tot_rec_ganha / len(ganhos)
tx_recup_glosa = (tot_recuperado / tot_glosado * 100) if tot_glosado else 0

# Yearly metrics
years = sorted(list(set(r['ano'] for r in rows)))
years_summary = []
for y in years:
    yr_rows = [r for r in rows if r['ano'] == y]
    yr_g = [r for r in yr_rows if r['status'] == 'Ganho']
    yr_p = [r for r in yr_rows if r['status'] == 'Perdido']
    rec = sum(to_f(r['receita_ganha']) for r in yr_g)
    glosa = sum(to_f(r['valor_glosado']) for r in yr_g)
    glosa_rec = sum(to_f(r['valor_recuperado']) for r in yr_g)
    glosa_perd = sum(to_f(r['glosa_nao_recuperada']) for r in yr_g)
    perd = sum(to_f(r['valor_perdido']) for r in yr_p)
    years_summary.append({
        'ano': y,
        'deals': len(yr_rows),
        'ganhos': len(yr_g),
        'perdidos': len(yr_p),
        'win_rate': round(len(yr_g)/len(yr_rows)*100, 1),
        'receita_ganha': rec,
        'receita_liquida': rec - glosa_perd,
        'valor_perdido': perd,
        'valor_glosado': glosa,
        'valor_recuperado': glosa_rec,
        'glosa_nao_recuperada': glosa_perd,
        'taxa_glosa': round(glosa/rec*100, 1) if rec else 0,
        'ticket_medio': round(rec/len(yr_g), 2) if yr_g else 0
    })

# Monthly metrics for timeline charts
months = sorted(list(set(r['mes'] for r in rows)))
months_summary = []
for m in months:
    m_rows = [r for r in rows if r['mes'] == m]
    m_g = [r for r in m_rows if r['status'] == 'Ganho']
    m_p = [r for r in m_rows if r['status'] == 'Perdido']
    rec = sum(to_f(r['receita_ganha']) for r in m_g)
    glosa_perd = sum(to_f(r['glosa_nao_recuperada']) for r in m_g)
    months_summary.append({
        'mes': m,
        'deals': len(m_rows),
        'ganhos': len(m_g),
        'receita': rec,
        'receita_liquida': rec - glosa_perd,
        'win_rate': round(len(m_g)/len(m_rows)*100, 1) if m_rows else 0
    })

# Payer metrics
payers = sorted(list(set(r['tipo_pagador'] for r in rows)))
payers_summary = []
for p in payers:
    p_rows = [r for r in rows if r['tipo_pagador'] == p]
    p_g = [r for r in p_rows if r['status'] == 'Ganho']
    p_p = [r for r in p_rows if r['status'] == 'Perdido']
    rec = sum(to_f(r['receita_ganha']) for r in p_g)
    perd = sum(to_f(r['valor_perdido']) for r in p_p)
    glosa = sum(to_f(r['valor_glosado']) for r in p_g)
    glosa_rec = sum(to_f(r['valor_recuperado']) for r in p_g)
    glosa_perd = sum(to_f(r['glosa_nao_recuperada']) for r in p_g)
    dias_pag = [to_f(r['dias_pagamento']) for r in p_g if r['dias_pagamento']]
    dias_cons = [to_f(r['dias_consignacao']) for r in p_g if r['dias_consignacao']]
    payers_summary.append({
        'tipo': p,
        'deals': len(p_rows),
        'ganhos': len(p_g),
        'perdidos': len(p_p),
        'win_rate': round(len(p_g)/len(p_rows)*100, 1),
        'receita_ganha': rec,
        'receita_liquida': rec - glosa_perd,
        'valor_perdido': perd,
        'valor_glosado': glosa,
        'valor_recuperado': glosa_rec,
        'glosa_nao_recuperada': glosa_perd,
        'taxa_glosa': round(glosa/rec*100, 1) if rec else 0,
        'taxa_recuperacao': round(glosa_rec/glosa*100, 1) if glosa else 0,
        'dias_pagamento_medio': round(sum(dias_pag)/len(dias_pag), 1) if dias_pag else 0,
        'dias_consignacao_medio': round(sum(dias_cons)/len(dias_cons), 1) if dias_cons else 0
    })
payers_summary = sorted(payers_summary, key=lambda x: x['receita_ganha'], reverse=True)

# State metrics
states = sorted(list(set(r['estado'] for r in rows)))
states_summary = []
for s in states:
    s_rows = [r for r in rows if r['estado'] == s]
    s_g = [r for r in s_rows if r['status'] == 'Ganho']
    s_p = [r for r in s_rows if r['status'] == 'Perdido']
    rec = sum(to_f(r['receita_ganha']) for r in s_g)
    perd = sum(to_f(r['valor_perdido']) for r in s_p)
    glosa_perd = sum(to_f(r['glosa_nao_recuperada']) for r in s_g)
    dias_pag = [to_f(r['dias_pagamento']) for r in s_g if r['dias_pagamento']]
    dias_cons = [to_f(r['dias_consignacao']) for r in s_g if r['dias_consignacao']]
    states_summary.append({
        'estado': s,
        'deals': len(s_rows),
        'ganhos': len(s_g),
        'perdidos': len(s_p),
        'win_rate': round(len(s_g)/len(s_rows)*100, 1),
        'receita_ganha': rec,
        'receita_liquida': rec - glosa_perd,
        'glosa_nao_recuperada': glosa_perd,
        'dias_pagamento_medio': round(sum(dias_pag)/len(dias_pag), 1) if dias_pag else 0,
        'dias_consignacao_medio': round(sum(dias_cons)/len(dias_cons), 1) if dias_cons else 0
    })
states_summary = sorted(states_summary, key=lambda x: x['receita_ganha'], reverse=True)

# Product lines
lines = sorted(list(set(r['linha_produto'] for r in rows)))
lines_summary = []
for l in lines:
    l_rows = [r for r in rows if r['linha_produto'] == l]
    l_g = [r for r in l_rows if r['status'] == 'Ganho']
    l_p = [r for r in l_rows if r['status'] == 'Perdido']
    rec = sum(to_f(r['receita_ganha']) for r in l_g)
    perd = sum(to_f(r['valor_perdido']) for r in l_p)
    glosa = sum(to_f(r['valor_glosado']) for r in l_g)
    glosa_perd = sum(to_f(r['glosa_nao_recuperada']) for r in l_g)
    lines_summary.append({
        'linha': l,
        'deals': len(l_rows),
        'ganhos': len(l_g),
        'perdidos': len(l_p),
        'win_rate': round(len(l_g)/len(l_rows)*100, 1),
        'receita_ganha': rec,
        'receita_liquida': rec - glosa_perd,
        'valor_perdido': perd,
        'valor_glosado': glosa,
        'glosa_nao_recuperada': glosa_perd,
        'ticket_medio': round(rec/len(l_g), 2) if l_g else 0
    })
lines_summary = sorted(lines_summary, key=lambda x: x['receita_ganha'], reverse=True)

# Products
prods = sorted(list(set(r['produto'] for r in rows)))
prods_summary = []
for p in prods:
    p_rows = [r for r in rows if r['produto'] == p]
    p_g = [r for r in p_rows if r['status'] == 'Ganho']
    p_p = [r for r in p_rows if r['status'] == 'Perdido']
    rec = sum(to_f(r['receita_ganha']) for r in p_g)
    perd = sum(to_f(r['valor_perdido']) for r in p_p)
    glosa = sum(to_f(r['valor_glosado']) for r in p_g)
    glosa_perd = sum(to_f(r['glosa_nao_recuperada']) for r in p_g)
    linha = p_rows[0]['linha_produto'] if p_rows else ''
    prods_summary.append({
        'produto': p,
        'linha': linha,
        'deals': len(p_rows),
        'ganhos': len(p_g),
        'perdidos': len(p_p),
        'win_rate': round(len(p_g)/len(p_rows)*100, 1),
        'receita_ganha': rec,
        'receita_liquida': rec - glosa_perd,
        'valor_perdido': perd,
        'valor_glosado': glosa,
        'glosa_nao_recuperada': glosa_perd,
        'ticket_medio': round(rec/len(p_g), 2) if p_g else 0
    })
prods_summary = sorted(prods_summary, key=lambda x: x['receita_ganha'], reverse=True)

# Sellers
sellers = sorted(list(set(r['vendedor'] for r in rows)))
sellers_summary = []
for s in sellers:
    s_rows = [r for r in rows if r['vendedor'] == s]
    s_g = [r for r in s_rows if r['status'] == 'Ganho']
    s_p = [r for r in s_rows if r['status'] == 'Perdido']
    rec = sum(to_f(r['receita_ganha']) for r in s_g)
    perd = sum(to_f(r['valor_perdido']) for r in s_p)
    glosa = sum(to_f(r['valor_glosado']) for r in s_g)
    glosa_rec = sum(to_f(r['valor_recuperado']) for r in s_g)
    glosa_perd = sum(to_f(r['glosa_nao_recuperada']) for r in s_g)
    
    top_losses = Counter(r['motivo_perda'] for r in s_p if r['motivo_perda']).most_common(2)
    top_losses_str = ', '.join([f'{m} ({c})' for m, c in top_losses]) if top_losses else 'Nenhum'
    
    sellers_summary.append({
        'vendedor': s,
        'deals': len(s_rows),
        'ganhos': len(s_g),
        'perdidos': len(s_p),
        'win_rate': round(len(s_g)/len(s_rows)*100, 1),
        'receita_ganha': rec,
        'receita_liquida': rec - glosa_perd,
        'valor_perdido': perd,
        'valor_glosado': glosa,
        'valor_recuperado': glosa_rec,
        'glosa_nao_recuperada': glosa_perd,
        'taxa_glosa_perdida': round(glosa_perd/rec*100, 1) if rec else 0,
        'ticket_medio': round(rec/len(s_g), 2) if s_g else 0,
        'principais_perdas': top_losses_str
    })
sellers_summary = sorted(sellers_summary, key=lambda x: x['receita_ganha'], reverse=True)

# Top Clients
clients = sorted(list(set(r['cliente'] for r in rows)))
clients_summary = []
for c in clients:
    c_rows = [r for r in rows if r['cliente'] == c]
    c_g = [r for r in c_rows if r['status'] == 'Ganho']
    c_p = [r for r in c_rows if r['status'] == 'Perdido']
    rec = sum(to_f(r['receita_ganha']) for r in c_g)
    glosa = sum(to_f(r['valor_glosado']) for r in c_g)
    glosa_perd = sum(to_f(r['glosa_nao_recuperada']) for r in c_g)
    tipo = c_rows[0]['tipo_pagador'] if c_rows else ''
    estado = c_rows[0]['estado'] if c_rows else ''
    clients_summary.append({
        'cliente': c,
        'tipo': tipo,
        'estado': estado,
        'deals': len(c_rows),
        'ganhos': len(c_g),
        'win_rate': round(len(c_g)/len(c_rows)*100, 1) if c_rows else 0,
        'receita_ganha': rec,
        'glosa_nao_recuperada': glosa_perd
    })
clients_summary = sorted(clients_summary, key=lambda x: x['receita_ganha'], reverse=True)

# Loss reasons
loss_reasons = sorted(list(set(r['motivo_perda'] for r in rows if r['motivo_perda'])))
loss_reasons_summary = []
for m in loss_reasons:
    m_rows = [r for r in rows if r['motivo_perda'] == m]
    tot_val = sum(to_f(r['valor_perdido']) for r in m_rows)
    etapas = Counter(r['etapa_perda'] for r in m_rows).most_common(1)
    etapa_top = etapas[0][0] if etapas else ''
    linhas = Counter(r['linha_produto'] for r in m_rows).most_common(1)
    linha_top = linhas[0][0] if linhas else ''
    loss_reasons_summary.append({
        'motivo': m,
        'qtd': len(m_rows),
        'valor_perdido': tot_val,
        'percentual_valor': round(tot_val / tot_perdido * 100, 2),
        'etapa_principal': etapa_top,
        'linha_principal': linha_top
    })
loss_reasons_summary = sorted(loss_reasons_summary, key=lambda x: x['valor_perdido'], reverse=True)

# Loss stages
loss_stages = sorted(list(set(r['etapa_perda'] for r in rows if r['etapa_perda'])))
loss_stages_summary = []
for e in loss_stages:
    e_rows = [r for r in rows if r['etapa_perda'] == e]
    tot_val = sum(to_f(r['valor_perdido']) for r in e_rows)
    top_m = Counter(r['motivo_perda'] for r in e_rows).most_common(2)
    top_m_str = ', '.join([f'{m} ({c})' for m, c in top_m])
    loss_stages_summary.append({
        'etapa': e,
        'qtd': len(e_rows),
        'valor_perdido': tot_val,
        'percentual_valor': round(tot_val / tot_perdido * 100, 2),
        'principais_motivos': top_m_str
    })
loss_stages_summary = sorted(loss_stages_summary, key=lambda x: x['valor_perdido'], reverse=True)

# Cycle metrics
cycle_metrics = {
    'cotacao_autorizacao': round(sum(to_f(r['dias_cotacao_autorizacao']) for r in ganhos if r['dias_cotacao_autorizacao']) / len([r for r in ganhos if r['dias_cotacao_autorizacao']]), 1),
    'cirurgia_faturamento': round(sum(to_f(r['dias_cirurgia_faturamento']) for r in ganhos if r['dias_cirurgia_faturamento']) / len([r for r in ganhos if r['dias_cirurgia_faturamento']]), 1),
    'consignacao': round(sum(to_f(r['dias_consignacao']) for r in ganhos if r['dias_consignacao']) / len([r for r in ganhos if r['dias_consignacao']]), 1),
    'pagamento': round(sum(to_f(r['dias_pagamento']) for r in ganhos if r['dias_pagamento']) / len([r for r in ganhos if r['dias_pagamento']]), 1),
    'ciclo_total': round(sum(to_f(r['ciclo_total_dias']) for r in ganhos if r['ciclo_total_dias']) / len([r for r in ganhos if r['ciclo_total_dias']]), 1)
}

data_bundle = {
    'summary': {
        'total_deals': total_deals,
        'deals_ganhos': len(ganhos),
        'deals_perdidos': len(perdidos),
        'win_rate': round(win_rate, 2),
        'valor_pipeline': tot_pipeline,
        'receita_ganha': tot_rec_ganha,
        'valor_perdido': tot_perdido,
        'valor_glosado': tot_glosado,
        'valor_recuperado': tot_recuperado,
        'glosa_nao_recuperada': tot_glosa_perdida,
        'receita_liquida': tot_rec_liquida,
        'ticket_medio': round(tkt_medio, 2),
        'taxa_recuperacao_glosa': round(tx_recup_glosa, 2)
    },
    'years': years_summary,
    'months': months_summary,
    'payers': payers_summary,
    'states': states_summary,
    'lines': lines_summary,
    'products': prods_summary,
    'sellers': sellers_summary,
    'top_clients': clients_summary[:15],
    'loss_reasons': loss_reasons_summary,
    'loss_stages': loss_stages_summary,
    'cycles': cycle_metrics
}

print('Data bundle created successfully!')
with open('data_bundle.json', 'w', encoding='utf-8') as f:
    json.dump(data_bundle, f, ensure_ascii=False, indent=2)
print('Saved data_bundle.json')
