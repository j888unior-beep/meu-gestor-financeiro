import streamlit as st

st.title("💰 Meu Simulador de Lucro Mensal")
st.markdown("---")

# Entradas de dados
ganho_mensal = st.number_input("Quanto você ganha no mês? (R$)", min_value=0.0, value=1700.0)
despesas_fixas = st.number_input("Total de Despesas Fixas (R$)", min_value=0.0, value=200.0)
bobeiras = st.number_input("Gastos não necessários / Bobeiras (R$)", min_value=0.0, value=200.0)
investimento = st.number_input("Quanto pretende investir? (R$)", min_value=0.0, value=0.0)

# O Cálculo
gasto_total = despesas_fixas + bobeiras + investimento
saldo_final = ganho_mensal - gasto_total

st.markdown("---")
st.subheader("Resultado do Mês")

if saldo_final >= 0:
    st.success(f"Mandou bem! Sobrou R$ {saldo_final:.2f} no seu bolso.")
else:
    st.error(f"Atenção! Você está no vermelho: R$ {saldo_final:.2f}")

# Barra de progresso do gasto
porcentagem_gasta = (gasto_total / ganho_mensal) if ganho_mensal > 0 else 0
st.write(f"Você já comprometeu **{porcentagem_gasta*100:.1f}%** da sua renda.")
st.progress(min(porcentagem_gasta, 1.0))

# Cálculo da porcentagem de bobeiras
if ganho_mensal > 0:
    perc_bobeiras = (bobeiras / ganho_mensal) * 100
else:
    perc_bobeiras = 0

st.subheader("Análise de Gastos Desnecessários")

# Exibe a métrica com uma cor
if perc_bobeiras <= 10:
    st.success(f"Excelente! Você gasta apenas {perc_bobeiras:.1f}% com bobeiras. Tá focado!")
elif perc_bobeiras <= 20:
    st.warning(f"Cuidado. {perc_bobeiras:.1f}% do seu ganho vai para bobeiras. Tente reduzir um pouco.")
else:
    st.error(f"Alerta Vermelho! {perc_bobeiras:.1f}% em bobeiras é muito. Você está queimando dinheiro!")

# Criando colunas para um visual mais limpo
col1, col2 = st.columns(2)
col1.metric("Saldo Livre", f"R$ {saldo_final:.2f}")
col2.metric("Total de Gastos", f"R$ {gasto_total:.2f}")