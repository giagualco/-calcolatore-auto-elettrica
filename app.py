import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px

# =============================
# Caricamento font & CSS extra
# =============================
def load_custom_css():
    """
    Carica Google Fonts e applica alcune regole CSS 
    per migliorare tipografia e layout.
    """
    custom_css = """
    <style>
    /* Caricamento Google Font: Roboto */
    @import url('https://fonts.googleapis.com/css2?family=Roboto:wght@300;400;500;700&display=swap');

    html, body, [class*="css"] {
        font-family: 'Roboto', sans-serif;
    }
    h1, h2, h3, h4, h5, h6 {
        font-weight: 700;
    }
    .main-title {
        color: #2C3E50;
        font-size: 36px;
        margin-bottom: 10px;
    }
    .section-title {
        color: #2C3E50;
        font-size: 24px;
        margin-top: 40px;
        margin-bottom: 10px;
        font-weight: 700;
    }
    .description {
        color: #555555;
        font-size: 16px;
        line-height: 1.6;
        margin-bottom: 20px;
    }
    /* Pulsanti e slider personalizzati */
    .stButton button {
        background-color: #1ABC9C !important;
        color: #FFFFFF !important;
        border-radius: 5px !important;
        font-weight: 500 !important;
        padding: 0.6em 1.2em !important;
    }
    .stButton button:hover {
        background-color: #16A085 !important;
    }
    /* Box input (number_input, text_input, ecc.) */
    .stTextInput, .stNumberInput, .stSelectbox {
        margin-bottom: 1em;
    }
    /* Rimozione del margine eccessivo sotto i plot */
    .element-container {
        padding-bottom: 0 !important;
    }
    </style>
    """
    st.markdown(custom_css, unsafe_allow_html=True)

# =============================
# Configurazione generale
# =============================
st.set_page_config(
    page_title="Configuratore Auto - Elettrica vs Termica",
    page_icon="🚗",
    layout="wide"
)

# Carica lo stile personalizzato
load_custom_css()

# =============================
# Header / Titolo
# =============================
st.markdown("<h1 class='main-title'>Configuratore Auto</h1>", unsafe_allow_html=True)
st.write("Benvenuto nel **Configuratore Auto**: qui puoi confrontare i costi e le emissioni di diverse tipologie di veicoli.")

# =============================
# Layout a sezioni e colonne
# =============================
st.markdown("<div class='section-title'>1. Inserisci i Dati delle Auto</div>", unsafe_allow_html=True)
st.markdown("<p class='description'>Compila i campi per confrontare due modelli (ad es. un'auto elettrica e una a benzina).</p>", unsafe_allow_html=True)

# Sezione input in due colonne
col1, col2 = st.columns(2)

with col1:
    st.subheader("Auto 1")
    tipo_auto1 = st.selectbox("Tipo di auto 1", ["Benzina", "Diesel", "Ibrido", "Elettrico"], key="auto1")
    modello_auto1 = st.text_input("Modello auto 1", value="Auto 1", key="modello1")
    costo_iniziale_auto1 = st.number_input("Prezzo d'acquisto (€)", value=25000, step=1000, format="%d", key="costo1")
    if tipo_auto1 in ["Benzina", "Diesel", "Ibrido"]:
        consumo_auto1 = st.number_input("Consumo medio (L/100km)", value=6, step=1, format="%d", key="consumo1")
    else:
        consumo_auto1 = st.number_input("Consumo medio (kWh/100km)", value=15, step=1, format="%d", key="consumo1")

with col2:
    st.subheader("Auto 2")
    tipo_auto2 = st.selectbox("Tipo di auto 2", ["Benzina", "Diesel", "Ibrido", "Elettrico"], key="auto2")
    modello_auto2 = st.text_input("Modello auto 2", value="Auto 2", key="modello2")
    costo_iniziale_auto2 = st.number_input("Prezzo d'acquisto (€)", value=35000, step=1000, format="%d", key="costo2")
    if tipo_auto2 in ["Benzina", "Diesel", "Ibrido"]:
        consumo_auto2 = st.number_input("Consumo medio (L/100km)", value=5, step=1, format="%d", key="consumo2")
    else:
        consumo_auto2 = st.number_input("Consumo medio (kWh/100km)", value=15, step=1, format="%d", key="consumo2")

# =============================
# Altri dati: Carburante, Energia, Chilometri annui
# =============================
st.markdown("<div class='section-title'>2. Costi del Carburante e Dati di Utilizzo</div>", unsafe_allow_html=True)
st.markdown("<p class='description'>Imposta i prezzi di benzina, diesel ed energia elettrica, oltre ai km percorsi in un anno.</p>", unsafe_allow_html=True)

col3, col4, col5 = st.columns(3)

with col3:
    prezzo_benzina = st.number_input("Prezzo benzina (€/L)", value=1.90, step=0.01, format="%.2f", key="benzina")
    prezzo_diesel = st.number_input("Prezzo diesel (€/L)", value=1.80, step=0.01, format="%.2f", key="diesel")
with col4:
    prezzo_energia = st.number_input("Prezzo energia elettrica (€/kWh)", value=0.25, step=0.01, format="%.2f", key="energia")
with col5:
    km_annui = st.number_input("Chilometri annui percorsi", value=15000, step=500, format="%d")

# =============================
# Funzione di calcolo costi ed emissioni
# =============================
def calcola_costi_e_emissioni(tipo_auto, consumo, km_annui, prezzo_benzina, prezzo_diesel, prezzo_energia):
    """
    Calcola i costi annui e le emissioni di CO2 in base al tipo di auto.
    """
    if tipo_auto == "Benzina":
        costo_annuo = (km_annui / 100) * consumo * prezzo_benzina
        co2_emessa = (km_annui / 100) * consumo * 2.3  # kg CO2 per litro di benzina
    elif tipo_auto == "Diesel":
        costo_annuo = (km_annui / 100) * consumo * prezzo_diesel
        co2_emessa = (km_annui / 100) * consumo * 2.6  # kg CO2 per litro di diesel (circa)
    elif tipo_auto == "Ibrido":
        # Stima semplificata, assume un consumo medio a metà tra benzina e un piccolo vantaggio
        costo_annuo = (km_annui / 100) * consumo * (prezzo_benzina * 0.8)
        co2_emessa = (km_annui / 100) * consumo * 2.0
    else:  # Elettrico
        costo_annuo = (km_annui / 100) * consumo * prezzo_energia
        co2_emessa = (km_annui / 100) * consumo * 0.5  # kg CO2 per kWh (stima generica)
    return costo_annuo, co2_emessa

# =============================
# Calcolo e risultati
# =============================
costo1, co2_1 = calcola_costi_e_emissioni(tipo_auto1, consumo_auto1, km_annui, prezzo_benzina, prezzo_diesel, prezzo_energia)
costo2, co2_2 = calcola_costi_e_emissioni(tipo_auto2, consumo_auto2, km_annui, prezzo_benzina, prezzo_diesel, prezzo_energia)

st.markdown("<div class='section-title'>3. Risultati e Confronto</div>", unsafe_allow_html=True)
st.markdown("<p class='description'>Visualizza il riepilogo di costi ed emissioni per entrambe le auto.</p>", unsafe_allow_html=True)

# Riepilogo testuale
st.write(f"**{modello_auto1} ({tipo_auto1})** - Costo annuo: **€{int(costo1):,}**, Emissioni: **{int(co2_1):,} kg CO₂/anno**")
st.write(f"**{modello_auto2} ({tipo_auto2})** - Costo annuo: **€{int(costo2):,}**, Emissioni: **{int(co2_2):,} kg CO₂/anno**")

# =============================
# Grafici interattivi con Plotly
# =============================
# 1) Confronto Costi
df_costi = pd.DataFrame({
    "Auto": [f"{modello_auto1} ({tipo_auto1})", f"{modello_auto2} ({tipo_auto2})"],
    "Costo annuo (€)": [costo1, costo2]
})
fig_costi = px.bar(
    df_costi,
    x="Auto",
    y="Costo annuo (€)",
    color="Auto",
    text="Costo annuo (€)",
    color_discrete_sequence=["#1ABC9C", "#34495E"]
)
fig_costi.update_layout(
    title="Confronto Costi Annuali",
    showlegend=False
)
fig_costi.update_traces(texttemplate='%{text:.0f} €', textposition='outside')

# 2) Confronto Emissioni
df_emissioni = pd.DataFrame({
    "Auto": [f"{modello_auto1} ({tipo_auto1})", f"{modello_auto2} ({tipo_auto2})"],
    "Emissioni CO₂ (kg/anno)": [co2_1, co2_2]
})
fig_emissioni = px.bar(
    df_emissioni,
    x="Auto",
    y="Emissioni CO₂ (kg/anno)",
    color="Auto",
    text="Emissioni CO₂ (kg/anno)",
    color_discrete_sequence=["#1ABC9C", "#34495E"]
)
fig_emissioni.update_layout(
    title="Confronto Emissioni di CO₂",
    showlegend=False
)
fig_emissioni.update_traces(texttemplate='%{text:.0f} kg', textposition='outside')

# Visualizza i grafici in due colonne
col_g1, col_g2 = st.columns(2)
with col_g1:
    st.plotly_chart(fig_costi, use_container_width=True)
with col_g2:
    st.plotly_chart(fig_emissioni, use_container_width=True)

st.markdown("<br>", unsafe_allow_html=True)
st.markdown("<p class='description'>⚡ <strong>Scegli la soluzione più efficiente e sostenibile!</strong> 🚀</p>", unsafe_allow_html=True)
