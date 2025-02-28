import streamlit as st
import pandas as pd
import numpy as np
import json
import plotly.graph_objects as go

# =============================
# 1. Configurazione e CSS
# =============================
st.set_page_config(
    page_title="Configuratore Auto - ROI e JSON",
    page_icon="🚗",
    layout="wide"
)

def load_custom_css():
    """
    Carica Google Fonts e regole CSS personalizzate
    per un design moderno e leggibile.
    """
    custom_css = """
    <style>
    /* Google Font: Roboto */
    @import url('https://fonts.googleapis.com/css2?family=Roboto:wght@300;400;700&display=swap');

    html, body, [class*="css"]  {
        font-family: 'Roboto', sans-serif;
        background-color: #FFFFFF; /* Forza sfondo bianco */
        color: #333333;
    }
    h1, h2, h3, h4, h5, h6 {
        font-weight: 700;
        margin-top: 0.5em;
        margin-bottom: 0.5em;
        color: #2C3E50;
    }
    .main-title {
        font-size: 36px;
        color: #2C3E50;
        margin-bottom: 0.2em;
    }
    .section-title {
        font-size: 24px;
        color: #2C3E50;
        margin-top: 1.5em;
        margin-bottom: 0.2em;
    }
    .description {
        color: #555555;
        font-size: 16px;
        line-height: 1.5;
        margin-bottom: 1em;
    }
    /* Stile per i pulsanti Streamlit */
    .stButton button {
        background-color: #1ABC9C !important; /* Verde acqua */
        color: #FFFFFF !important;
        border-radius: 5px !important;
        font-weight: 500 !important;
        padding: 0.6em 1.2em !important;
        border: none !important;
    }
    .stButton button:hover {
        background-color: #16A085 !important;
    }
    /* Stile per input e selectbox */
    .stTextInput, .stNumberInput, .stSelectbox, .stFileUploader {
        margin-bottom: 1em;
    }
    /* Link YouTube */
    .youtube-link {
        color: #E52D27 !important; /* Rosso YouTube */
        text-decoration: none !important;
        font-weight: 700;
    }
    .youtube-link:hover {
        text-decoration: underline !important;
    }
    </style>
    """
    st.markdown(custom_css, unsafe_allow_html=True)

load_custom_css()

# =============================
# 2. Titolo e link YouTube
# =============================
st.markdown("<h1 class='main-title'>Configuratore Auto: Confronto Costi & ROI</h1>", unsafe_allow_html=True)
st.markdown(
    '<p class="description">'
    'Benvenuto nel configuratore auto. Confronta i costi di due tipologie di veicoli, '
    'analizza le emissioni e scopri se e quando l’investimento si ripaga nel tempo.<br>'
    'Visita anche il mio <a class="youtube-link" href="https://www.youtube.com/@giagualco" target="_blank">Canale YouTube</a> '
    'per approfondimenti!</p>',
    unsafe_allow_html=True
)

# =============================
# 3. Sidebar per input utente
# =============================
st.sidebar.header("Dati delle Auto")

# --- Auto 1 ---
st.sidebar.subheader("Auto 1")
tipo_auto1 = st.sidebar.selectbox("Tipo di auto 1", ["Benzina", "Diesel", "Ibrido", "Elettrico"], key="auto1")
modello_auto1 = st.sidebar.text_input("Modello auto 1", value="Auto 1", key="modello1")
costo_iniziale_auto1 = st.sidebar.number_input("Prezzo d'acquisto (€)", value=25000, step=1000, format="%d", key="costo1")
if tipo_auto1 in ["Benzina", "Diesel", "Ibrido"]:
    consumo_auto1 = st.sidebar.number_input("Consumo medio (L/100km)", value=6, step=1, format="%d", key="consumo1")
else:
    consumo_auto1 = st.sidebar.number_input("Consumo medio (kWh/100km)", value=15, step=1, format="%d", key="consumo1")

# --- Auto 2 ---
st.sidebar.subheader("Auto 2")
tipo_auto2 = st.sidebar.selectbox("Tipo di auto 2", ["Benzina", "Diesel", "Ibrido", "Elettrico"], key="auto2")
modello_auto2 = st.sidebar.text_input("Modello auto 2", value="Auto 2", key="modello2")
costo_iniziale_auto2 = st.sidebar.number_input("Prezzo d'acquisto (€)", value=35000, step=1000, format="%d", key="costo2")
if tipo_auto2 in ["Benzina", "Diesel", "Ibrido"]:
    consumo_auto2 = st.sidebar.number_input("Consumo medio (L/100km)", value=5, step=1, format="%d", key="consumo2")
else:
    consumo_auto2 = st.sidebar.number_input("Consumo medio (kWh/100km)", value=15, step=1, format="%d", key="consumo2")

st.sidebar.header("Costi Carburante / Energia")
prezzo_benzina = st.sidebar.number_input("Prezzo benzina (€/L)", value=1.90, step=0.01, format="%.2f", key="benzina")
prezzo_diesel = st.sidebar.number_input("Prezzo diesel (€/L)", value=1.80, step=0.01, format="%.2f", key="diesel")
prezzo_energia = st.sidebar.number_input("Prezzo energia elettrica (€/kWh)", value=0.25, step=0.01, format="%.2f", key="energia")

st.sidebar.header("Dati di Utilizzo")
km_annui = st.sidebar.number_input("Chilometri annui percorsi", value=15000, step=500, format="%d")

# --- Caricamento file JSON di Google Takeout ---
st.sidebar.header("Carica File JSON (Google Takeout)")
uploaded_files = st.sidebar.file_uploader("Seleziona uno o più file JSON", type=["json"], accept_multiple_files=True)

if uploaded_files:
    total_distance_km = 0
    for uploaded_file in uploaded_files:
        try:
            data = json.load(uploaded_file)
            activity_segments = [
                obj['activitySegment']
                for obj in data.get("timelineObjects", [])
                if 'activitySegment' in obj
            ]
            for segment in activity_segments:
                total_distance_km += segment.get('distance', 0) / 1000
        except Exception as e:
            st.sidebar.error(f"Errore nel file {uploaded_file.name}: {e}")

    if total_distance_km > 0:
        st.sidebar.success(f"Totale km caricati: {int(total_distance_km)} km")
        km_annui = int(total_distance_km)

# =============================
# 4. Funzione calcolo costi & emissioni
# =============================
def calcola_costi_e_emissioni(tipo_auto, consumo, km_annui, prezzo_benzina, prezzo_diesel, prezzo_energia):
    """
    Restituisce:
      - costo_annuo: spesa annuale in €
      - co2_emessa: emissioni annue in kg di CO2
    """
    if tipo_auto == "Benzina":
        costo_annuo = (km_annui / 100) * consumo * prezzo_benzina
        co2_emessa = (km_annui / 100) * consumo * 2.3  # kg CO2 per litro di benzina
    elif tipo_auto == "Diesel":
        costo_annuo = (km_annui / 100) * consumo * prezzo_diesel
        co2_emessa = (km_annui / 100) * consumo * 2.6  # kg CO2 per litro di diesel (circa)
    elif tipo_auto == "Ibrido":
        # Stima semplificata: riduzione di ~20% su benzina
        costo_annuo = (km_annui / 100) * consumo * (prezzo_benzina * 0.8)
        co2_emessa = (km_annui / 100) * consumo * 2.0
    else:  # Elettrico
        costo_annuo = (km_annui / 100) * consumo * prezzo_energia
        co2_emessa = (km_annui / 100) * consumo * 0.5  # kg CO2 per kWh (stima generica)
    return costo_annuo, co2_emessa

# =============================
# 5. Calcolo costi annui & break-even
# =============================
costo_annuo_auto1, co2_auto1 = calcola_costi_e_emissioni(
    tipo_auto1, consumo_auto1, km_annui, prezzo_benzina, prezzo_diesel, prezzo_energia
)
costo_annuo_auto2, co2_auto2 = calcola_costi_e_emissioni(
    tipo_auto2, consumo_auto2, km_annui, prezzo_benzina, prezzo_diesel, prezzo_energia
)

# Funzione per calcolo break-even
def calcola_break_even(costo_iniziale1, annuo1, costo_iniziale2, annuo2):
    """
    Restituisce (anni_pareggio) se esiste un break-even,
    altrimenti None.
    """
    # Se l'auto2 è più costosa inizialmente, ma ha costi annui minori,
    # si calcola il tempo in cui si recupera la differenza iniziale.
    delta_iniziale = costo_iniziale2 - costo_iniziale1
    delta_annuo = annuo1 - annuo2
    if delta_iniziale > 0 and delta_annuo > 0:
        return delta_iniziale / delta_annuo
    # Se l'auto1 è più costosa e l'auto2 costa meno all'anno, inverti i parametri
    delta_iniziale_bis = costo_iniziale1 - costo_iniziale2
    delta_annuo_bis = annuo2 - annuo1
    if delta_iniziale_bis > 0 and delta_annuo_bis > 0:
        return delta_iniziale_bis / delta_annuo_bis
    return None

anni_pareggio = calcola_break_even(
    costo_iniziale_auto1, costo_annuo_auto1,
    costo_iniziale_auto2, costo_annuo_auto2
)

# =============================
# 6. Mostra risultati testuali
# =============================
st.subheader("Riepilogo del Confronto")

col_r1, col_r2 = st.columns(2)
with col_r1:
    st.write(f"**{modello_auto1} ({tipo_auto1})**")
    st.write(f"- Costo annuo: **€{int(costo_annuo_auto1):,}**")
    st.write(f"- Emissioni: **{int(co2_auto1):,} kg CO₂/anno**")
    st.write(f"- Costo iniziale: **€{int(costo_iniziale_auto1):,}**")

with col_r2:
    st.write(f"**{modello_auto2} ({tipo_auto2})**")
    st.write(f"- Costo annuo: **€{int(costo_annuo_auto2):,}**")
    st.write(f"- Emissioni: **{int(co2_auto2):,} kg CO₂/anno**")
    st.write(f"- Costo iniziale: **€{int(costo_iniziale_auto2):,}**")

if anni_pareggio:
    st.success(f"Tempo di ritorno dell'investimento: circa **{anni_pareggio:.1f} anni**.")
else:
    st.warning("Non si raggiunge un break-even con i dati attuali, oppure i costi sono equivalenti.")

# =============================
# 7. Grafico costi cumulativi nel tempo
# =============================
st.subheader("Confronto del Costo Cumulativo nel Tempo")

# Calcoliamo i costi cumulativi anno per anno
anni_range = np.arange(0, 11)  # 0..10 anni
cumul_auto1 = [costo_iniziale_auto1 + (anno * costo_annuo_auto1) for anno in anni_range]
cumul_auto2 = [costo_iniziale_auto2 + (anno * costo_annuo_auto2) for anno in anni_range]

fig_costi = go.Figure()
fig_costi.add_trace(go.Scatter(
    x=anni_range,
    y=cumul_auto1,
    mode='lines+markers',
    name=f"{modello_auto1} ({tipo_auto1})",
    line=dict(color='#1ABC9C', width=3),
    marker=dict(size=6)
))
fig_costi.add_trace(go.Scatter(
    x=anni_range,
    y=cumul_auto2,
    mode='lines+markers',
    name=f"{modello_auto2} ({tipo_auto2})",
    line=dict(color='#E67E22', width=3),
    marker=dict(size=6)
))

fig_costi.update_layout(
    title="Costo Cumulativo per 10 anni",
    xaxis_title="Anni di utilizzo",
    yaxis_title="Costo Cumulativo (€)",
    hovermode="x unified",
    template="simple_white"
)

st.plotly_chart(fig_costi, use_container_width=True)

# =============================
# 8. Grafico emissioni (bar chart)
# =============================
st.subheader("Confronto delle Emissioni di CO₂")

fig_emissioni = go.Figure(data=[
    go.Bar(
        x=[f"{modello_auto1} ({tipo_auto1})", f"{modello_auto2} ({tipo_auto2})"],
        y=[co2_auto1, co2_auto2],
        marker_color=['#1ABC9C', '#E67E22']
    )
])
fig_emissioni.update_layout(
    title="Emissioni di CO₂ (kg/anno)",
    xaxis_title="Modello",
    yaxis_title="kg di CO₂ all'anno",
    template="simple_white"
)
st.plotly_chart(fig_emissioni, use_container_width=True)

st.markdown(
    "<p class='description'>"
    "⚡ <strong>Scegli la soluzione più efficiente e sostenibile!</strong> 🚀"
    "</p>",
    unsafe_allow_html=True
)
