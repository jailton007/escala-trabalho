import streamlit as st
import calendar
from datetime import date
import holidays

# Configuração da página e ícone do app
st.set_page_config(page_title="Minha Escala", page_icon="📅", layout="centered")

st.title("🗓️ Escala de Folgas Inteligente")
st.markdown("Veja seus dias de trabalho e folga em um calendário infinito.")

# --- BARRA LATERAL PARA CONFIGURAÇÕES ---
st.sidebar.header("⚙️ Configurações da Escala")

# 1. Tipo de Escala
tipo_escala = st.sidebar.radio("Selecione sua Escala:", ["6x2", "5x2"])

# 2. Data de Início da Escala (Primeiro dia de trabalho do ciclo)
data_inicio = st.sidebar.date_input("Data de Início do Ciclo:", date.today())

# 3. Cor da Folga
cor_folga = st.sidebar.color_picker("Escolha a cor dos dias de folga:", "#4CAF50")

# --- SELEÇÃO DE MÊS E ANO ---
col1, col2 = st.columns(2)
with col1:
    mes_selecionado = st.selectbox("Mês:", range(1, 13), format_func=lambda x: calendar.month_name[x].capitalize())
with col2:
    ano_selecionado = st.number_input("Ano:", min_value=2000, max_value=2100, value=date.today().year, step=1)

# --- LÓGICA DO CALENDÁRIO ---
def gerar_calendario_html(ano, mes, inicio_ciclo, escala, cor):
    cal = calendar.monthcalendar(ano, mes)
    feriados_br = holidays.Brazil(years=ano)
    
    # CSS básico para a tabela ficar bonita no celular
    html = f"""
    <style>
        .cal-table {{ width: 100%; text-align: center; border-collapse: collapse; font-family: sans-serif; }}
        .cal-table th {{ padding: 10px; background-color: #f0f2f6; color: #333; }}
        .cal-table td {{ padding: 15px; border: 1px solid #ddd; font-size: 16px; }}
        .folga {{ background-color: {cor}; color: white; font-weight: bold; border-radius: 5px; }}
        .feriado {{ text-decoration: underline; text-decoration-color: #ff4b4b; text-decoration-thickness: 3px; font-weight: bold; }}
    </style>
    <table class="cal-table">
        <tr><th>Seg</th><th>Ter</th><th>Qua</th><th>Qui</th><th>Sex</th><th>Sáb</th><th>Dom</th></tr>
    """
    
    for semana in cal:
        html += "<tr>"
        for dia in semana:
            if dia == 0:
                html += "<td></td>" # Dias vazios do mês
            else:
                data_atual = date(ano, mes, dia)
                dias_passados = (data_atual - inicio_ciclo).days
                
                # Calcula se é folga baseado no tipo de escala
                is_folga = False
                if dias_passados >= 0:
                    if escala == "6x2":
                        # Ciclo de 8 dias: trabalha 6, folga 2
                        is_folga = (dias_passados % 8) >= 6
                    elif escala == "5x2":
                        # Ciclo de 7 dias: trabalha 5, folga 2
                        is_folga = (dias_passados % 7) >= 5
                
                # Verifica se é feriado
                is_feriado = data_atual in feriados_br
                
                # Aplica as classes CSS
                classes = []
                if is_folga: classes.append("folga")
                if is_feriado: classes.append("feriado")
                
                class_str = " ".join(classes)
                html += f"<td class='{class_str}'>{dia}</td>"
        html += "</tr>"
    
    html += "</table>"
    return html

# Renderiza o calendário na tela
st.markdown("### Calendário")
calendario_pronto = gerar_calendario_html(ano_selecionado, mes_selecionado, data_inicio, tipo_escala, cor_folga)
st.markdown(calendario_pronto, unsafe_allow_html=True)

st.caption("🔴 Dias com sublinhado vermelho indicam feriados nacionais.")