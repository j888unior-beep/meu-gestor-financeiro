import streamlit as st
import pandas as pd
import plotly.express as px
import random

st.set_page_config(page_title="Meu Gestor Financeiro", page_icon="💰", layout="wide")

if 'historico' not in st.session_state:
    st.session_state.historico = []

st.markdown("""
    <style>
    /* Ajuste das métricas para funcionar em qualquer tema */
    .stMetric { 
        border: 1px solid #4B5563; 
        padding: 15px; 
        border-radius: 10px; 
        background-color: rgba(255, 255, 255, 0.05);
    }
    /* Melhora a visibilidade do texto nos inputs */
    .stNumberInput input {
        font-weight: bold;
    }
    </style>
    """, unsafe_allow_html=True)

st.title("Gestor Financeiro ")
st.caption("Transformando números em liberdade financeira.")

st.sidebar.header("Lançamentos do Mês")

ganho = st.sidebar.number_input("Ganho Mensal (R$)", min_value=0.0, value=0.0, step=100.0, format="%.2f")
fixas = st.sidebar.number_input("Despesas (R$)", min_value=0.0, value=0.0, step=10.0, format="%.2f")
bobeiras = st.sidebar.number_input("Bobeiras/Lazer (R$)", min_value=0.0, value=0.0, step=10.0, format="%.2f")
investimento = st.sidebar.number_input("Investimentos (R$)", min_value=0.0, value=0.0, step=10.0, format="%.2f")

ganho_val = float(ganho)
fixas_val = float(fixas)
bobeiras_val = float(bobeiras)
invest_val = float(investimento)

gasto_total = fixas_val + bobeiras_val + invest_val
saldo_final = ganho_val - gasto_total
perc_bobeiras = (bobeiras_val / ganho_val * 100) if ganho_val > 0 else 0

col1, col2, col3, col4 = st.columns(4)
col1.metric("Saldo Livre", f"R$ {saldo_final:.2f}")
col2.metric("Total Gasto", f"R$ {gasto_total:.2f}")
col3.metric("Investido", f"R$ {invest_val:.2f}")
col4.metric("% Bobeiras", f"{perc_bobeiras:.1f}%")

st.divider()

c_grafico, c_conselho = st.columns([2, 1])

with c_grafico:
    st.subheader("Distribuição do Orçamento")
    if ganho_val > 0:
        labels = ['Fixo', 'Bobeiras', 'Investimento', 'Sobra']
        valores = [fixas_val, bobeiras_val, invest_val, max(0, saldo_final)]
        fig = px.pie(names=labels, values=valores, hole=0.4, 
                     color_discrete_sequence=px.colors.qualitative.Safe)
        fig.update_layout(paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)')
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.info("Insira seus ganhos na barra lateral para ver o gráfico.")

with c_conselho:
    st.subheader("Dica do Gestor Financeiro")
    
    frases_boas = [
        "Que tal investir uma parte desse saldo positivo?",
        "Você está no caminho certo. Constância é a chave da riqueza!",
        "Dinheiro guardado hoje é tranquilidade garantida amanhã."
    ]
    
    frases_alerta = [
        "O orçamento está apertado. Tente reduzir os gastos não essenciais.",
        "Pequenas economias geram grandes resultados a longo prazo."
    ]

    if saldo_final > 0:
        st.success(random.choice(frases_boas))
        if saldo_final > (ganho_val * 0.3):
            st.balloons()
    elif ganho_val > 0:
        st.warning(random.choice(frases_alerta))

st.divider()
st.subheader(" Calculadora de Metas")
col_m1, col_m2 = st.columns(2)

with col_m1:
    meta_nome = st.text_input("Qual seu objetivo?", placeholder="Ex: Viagem, Notebook...")
    meta_valor = st.number_input("Valor da meta (R$)", min_value=0.0, value=0.0)

with col_m2:
    if meta_valor > 0 and saldo_final > 0:
        meses = meta_valor / saldo_final
        st.info(f"Para atingir **{meta_nome}**, você precisa poupar por **{meses:.1f} meses**.")
    elif meta_valor > 0:
        st.error("Aumente seu saldo livre para calcular o tempo da meta.")

st.divider()
st.subheader("Histórico de Registros")

col_h1, col_h2 = st.columns([1, 5])
with col_h1:
    if st.button("Salvar Dados"):
        if ganho_val > 0:
            st.session_state.historico.append({
                "Mês": len(st.session_state.historico) + 1,
                "Ganho": ganho_val,
                "Saldo": saldo_final,
                "Bobeiras": bobeiras_val
            })
            st.rerun()

    if st.button("Limpar Tudo"):
        st.session_state.historico = []
        st.rerun()

if st.session_state.historico:
    df = pd.DataFrame(st.session_state.historico)
    st.table(df)
    
    st.write("Evolução do seu Saldo:")
    st.bar_chart(df, x="Mês", y="Saldo")
    
    csv = df.to_csv(index=False).encode('utf-8')
    st.download_button("Baixar Planilha (CSV)", data=csv, file_name="meu_financeiro.csv")

st.markdown("---")
st.markdown(
    """
    <div style='text-align: center;'>
        <p style='color: gray; font-size: 0.8em;'>
            Desenvolvido por <b>Junior</b> para fins didáticos e cálculos precisos. 🚀<br>
            <i>Feito com Python e Streamlit</i>
        </p>
    </div>
    """, 
    unsafe_allow_html=True
)
