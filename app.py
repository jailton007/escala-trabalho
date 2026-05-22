import streamlit as st
import calendar
from datetime import date
import holidays

# Configuração da página
st.set_page_config(page_title="Escala de Trabalho", layout="centered")

# Inicializa estados de navegação
if 'mes_atual' not in st.session_state:
    st.session_state.mes_atual = date.today().month
if 'ano_atual' not in st.session_state:
    st.session_state.ano_atual = date.today().year

# Tradução e Configurações
meses_pt = ["Janeiro", "Fevereiro", "Março", "Abril", "Maio", "Junho", 
            "Julho", "Agosto", "Setembro", "Outubro", "Novembro", "Dezembro"]

st.sidebar.header("⚙️ Configurações")
tipo_escala = st.sidebar.selectbox("Tipo de Escala", ["6x2", "5x2"])
data_inicio = st.sidebar.date_input("Início do ciclo", date.today())
cor_folga = st.sidebar.color_picker("Cor da folga", "#4CAF50")

# Navegação de meses
st.title("🗓️ Escala de Trabalho")
col1, col2, col3 = st.columns([1, 2, 1])

with col1:
    if st.button("◀ Anterior"):
        st.session_state.mes_atual -= 1
        if st.session_state.mes_atual < 1:
            st.session_state.mes_atual = 12
            st.session_state.ano_atual -= 1
            st.rerun()
        st.rerun()

with col2:
    st.markdown(f"<h3 style='text-align: center;'>{meses_pt[st.session_state.mes_atual-1]} / {st.session_state.ano_atual}</h3>", unsafe_allow_html=True)

with col3:
    if st.button("Próximo ▶"):
        st.session_state.mes_atual += 1
        if st.session_state.mes_atual > 12:
            st.session_state.mes_atual = 1
            st.session_state.ano_atual += 1
            st.rerun()
        st.rerun()

# Gerador de Calendário
def gerar_calendario(ano, mes, inicio, escala, cor):
    cal = calendar.monthcalendar(ano, mes)
    feriados = holidays.Brazil(years=ano)
    html = f"""
    <style>
        .folga {{background-color: {cor}; color: white; border-radius: 50%; display: inline-block; width: 30px; height: 30px; line-height: 30px;}}
        .feriado {{color: red; font-weight: bold;}}
        table {{width: 100%; border-collapse: collapse;}}
        td {{text-align: center; padding: 10px;}}
    </style>
    <table><tr><th>Seg</th><th>Ter</th><th>Qua</th><th>Qui</th><th>Sex</th><th>Sáb</th><th>Dom</th></tr>
    """
    for semana in cal:
        html += "<tr>"
        for dia in semana:
            if dia == 0:
                html += "<td></td>"
            else:
                data = date(ano, mes, dia)
                dias_passados = (data - inicio).days
                is_folga = False
                if dias_passados >= 0:
                    if escala == "6x2": is_folga = (dias_passados % 8) >= 6
                    else: is_folga = (dias_passados % 7) >= 5
                
                classe = "folga" if is_folga else ""
                estilo_feriado = "feriado" if data in feriados else ""
                html += f"<td><span class='{classe} {estilo_feriado}'>{dia}</span></td>"
        html += "</tr>"
    return html + "</table>"

st.markdown(gerar_calendario(st.session_state.ano_atual, st.session_state.mes_atual, data_inicio, tipo_escala, cor_folga), unsafe_allow_html=True)