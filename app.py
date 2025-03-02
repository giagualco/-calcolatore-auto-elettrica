import streamlit as st
import pandas as pd
import numpy as np
import json
import plotly.graph_objects as go

# =============================
# 1. Configurazione Streamlit & CSS
# =============================
st.set_page_config(
    page_title="Configuratore Avanzato Auto",
    page_icon="🚗",
    layout="wide"
)

def load_custom_css():
    """
    Carica Google Fonts e regole CSS personalizzate, 
    incluse media queries per dispositivi mobili.
    """
    css = """
    <style>
    /* Google Font: Roboto */
    @import url('https://fonts.googleapis.com/css2?family=Roboto:wght@300;400;700&display=swap');
    
    html, body, [class*="css"] {
        font-family: 'Roboto', sans-serif;
        background-color: #FFFFFF;
        color: #333333;
    }
    h1, h2, h3, h4, h5, h6 {
        font-weight: 700;
        color: #2C3E50;
        margin: 0.5em 0 0.3em 0;
    }
    .main-title {
        font-size: 36px;
        margin-bottom: 0.2em;
    }
    .section-title {
        font-size: 24px;
        margin-top: 1.5em;
        margin-bottom: 0.2em;
    }
    .description {
        color: #555555;
        font-size: 16px;
        line-height: 1.5;
        margin-bottom: 1em;
    }
    /* Pulsanti e widget di input */
    .stButton button {
        background-color: #1ABC9C !important;
        color: #FFFFFF !important;
        border-radius: 5px !important;
        font-weight: 500 !important;
        padding: 0.6em 1.2em !important;
        border: none !important;
        transition: background-color 0.3s ease;
    }
    .stButton button:hover {
        background-color: #16A085 !important;
    }
    .stTextInput, .stNumberInput, .stSelectbox, .stFileUploader {
        margin-bottom: 1em;
    }
    /* Link YouTube */
    .youtube-link {
        color: #E52D27 !important;
        text-decoration: none !important;
        font-weight: 700;
    }
    .youtube-link:hover {
        text-decoration: underline !important;
    }
    /* Media Queries per dispositivi mobili */
    @media screen and (max-width: 768px) {
        .main-title {
            font-size: 28px !important;
        }
        .section-title {
            font-size: 20px !important;
        }
        .description {
            font-size: 14px !important;
        }
        /* Le colonne verranno visualizzate in verticale */
        [data-testid="stHorizontalBlock"] {
            flex-direction: column !important;
        }
        /* Riduci padding e margini per schermi piccoli */
        .css-1d391kg, .css-1d391kg * {
            padding: 0.5em !important;
        }
    }
    </style>
    """
    st.markdown(css, unsafe_allow_html=True)

load_custom_css()

# =============================
# 2. Prezzi Impostati dall'Utente (Default)
# =============================
# Ora non viene scaricato il CSV, i prezzi vengono impostati tramite input.
# Valori di default: Benzina 1.90 €/L, Diesel 1.80 €/L, Energia 0.25 €/kWh.

prezzo_benzina_default = 1.90
prezzo_diesel_default = 1.80
prezzo_energia_default = 0.25

# =============================
# 3. Titolo e Link al Canale YouTube
# =============================
st.markdown("<h1 class='main-title'>Configuratore Avanzato Auto</h1>", unsafe_allow_html=True)
st.markdown(
    '<p class="description">'
    'Benvenuto! Confronta due veicoli (combustione o elettrici) inserendo un singolo valore WLTP, '
    'analizza costi annui, emissioni di CO₂ e break-even.<br>'
    'Visita il mio <a class="youtube-link" href="https://www.youtube.com/@giagualco" target="_blank">Canale YouTube</a> '
    'per approfondimenti!</p>',
    unsafe_allow_html=True
)

# =============================
# 4. Sidebar: Impostazioni Unità di Misura
# =============================
st.sidebar.header("Impostazioni Unità di Misura")
unit_fuel = st.sidebar.selectbox("Unità per veicoli a combustione", ["L/100km", "km/l"], key="unit_fuel")
unit_electric = st.sidebar.selectbox("Unità per veicoli elettrici", ["kWh/100km", "km/kWh"], key="unit_electric")

# =============================
# 5. Sidebar: Dati delle Auto
# =============================
st.sidebar.header("Dati delle Auto")

# --- Auto 1 ---
st.sidebar.markdown("**Auto 1**")
tipo_auto1 = st.sidebar.selectbox("Tipo di auto 1", ["Benzina", "Diesel", "Ibrido", "Elettrico"], key="tipo_auto1")
modello_auto1 = st.sidebar.text_input("Modello auto 1", value="Auto 1", key="modello_auto1")
costo_iniziale_auto1 = st.sidebar.number_input("Prezzo d'acquisto (€)", value=25000, step=1000, format="%d", key="costo_iniziale1")

if tipo_auto1 in ["Benzina", "Diesel", "Ibrido"]:
    if unit_fuel == "L/100km":
        wltp1 = st.sidebar.number_input("Consumo WLTP (L/100km)", value=6.0, step=0.1, format="%.1f", key="wltp_auto1")
        consumo_urbano1 = wltp1
        consumo_extra1 = wltp1
        consumo_autostrada1 = wltp1
    else:
        wltp1_kml = st.sidebar.number_input("Consumo WLTP (km/l)", value=15.0, step=0.1, format="%.1f", key="wltp_auto1")
        base_1 = 100 / wltp1_kml if wltp1_kml > 0 else 0
        consumo_urbano1 = base_1
        consumo_extra1 = base_1
        consumo_autostrada1 = base_1
else:
    if unit_electric == "kWh/100km":
        wltp1 = st.sidebar.number_input("Consumo WLTP (kWh/100km)", value=16.0, step=0.1, format="%.1f", key="wltp_auto1")
        consumo_urbano1 = wltp1
        consumo_extra1 = wltp1
        consumo_autostrada1 = wltp1
    else:
        wltp1_kmkwh = st.sidebar.number_input("Consumo WLTP (km/kWh)", value=4.0, step=0.1, format="%.1f", key="wltp_auto1")
        base_1 = 100 / wltp1_kmkwh if wltp1_kmkwh > 0 else 0
        consumo_urbano1 = base_1
        consumo_extra1 = base_1
        consumo_autostrada1 = base_1

# --- Auto 2 ---
st.sidebar.markdown("**Auto 2**")
tipo_auto2 = st.sidebar.selectbox("Tipo di auto 2", ["Benzina", "Diesel", "Ibrido", "Elettrico"], key="tipo_auto2")
modello_auto2 = st.sidebar.text_input("Modello auto 2", value="Auto 2", key="modello_auto2")
costo_iniziale_auto2 = st.sidebar.number_input("Prezzo d'acquisto (€)", value=35000, step=1000, format="%d", key="costo_iniziale2")

if tipo_auto2 in ["Benzina", "Diesel", "Ibrido"]:
    if unit_fuel == "L/100km":
        wltp2 = st.sidebar.number_input("Consumo WLTP (L/100km)", value=6.5, step=0.1, format="%.1f", key="wltp_auto2")
        consumo_urbano2 = wltp2
        consumo_extra2 = wltp2
        consumo_autostrada2 = wltp2
    else:
        wltp2_kml = st.sidebar.number_input("Consumo WLTP (km/l)", value=14.0, step=0.1, format="%.1f", key="wltp_auto2")
        base_2 = 100 / wltp2_kml if wltp2_kml > 0 else 0
        consumo_urbano2 = base_2
        consumo_extra2 = base_2
        consumo_autostrada2 = base_2
else:
    if unit_electric == "kWh/100km":
        wltp2 = st.sidebar.number_input("Consumo WLTP (kWh/100km)", value=17.0, step=0.1, format="%.1f", key="wltp_auto2")
        consumo_urbano2 = wltp2
        consumo_extra2 = wltp2
        consumo_autostrada2 = wltp2
    else:
        wltp2_kmkwh = st.sidebar.number_input("Consumo WLTP (km/kWh)", value=3.8, step=0.1, format="%.1f", key="wltp_auto2")
        base_2 = 100 / wltp2_kmkwh if wltp2_kmkwh > 0 else 0
        consumo_urbano2 = base_2
        consumo_extra2 = base_2
        consumo_autostrada2 = base_2

# =============================
# 6. Sidebar: Percentuali di Guida (Urbano ed Extraurbano; Autostrada è calcolato)
# =============================
st.sidebar.header("Percentuali di Guida (%)")
perc_urbano = st.sidebar.slider("Urbano (%)", min_value=0.0, max_value=100.0, value=40.0, step=1.0, key="perc_urb")
perc_extra = st.sidebar.slider("Extraurbano (%)", min_value=0.0, max_value=100.0, value=40.0, step=1.0, key="perc_ext")
# Calcoliamo automaticamente la percentuale di Autostrada
perc_autostrada = 100.0 - (perc_urbano + perc_extra)
if perc_autostrada < 0:
    st.sidebar.error("La somma di Urbano ed Extraurbano supera il 100%. Riduci i valori.")
    perc_autostrada = 0.0
st.sidebar.write(f"**Autostrada:** {perc_autostrada:.1f}%")

# =============================
# 7. Sidebar: Costi Carburante/Energia e Dati di Utilizzo
# =============================
st.sidebar.header("Costi Carburante / Energia")
prezzo_benzina = st.sidebar.number_input("Prezzo benzina (€/L)", value=prezzo_benzina_default, step=0.01, format="%.2f", key="benzina")
prezzo_diesel = st.sidebar.number_input("Prezzo diesel (€/L)", value=prezzo_diesel_default, step=0.01, format="%.2f", key="diesel")
prezzo_energia = st.sidebar.number_input("Prezzo energia elettrica (€/kWh)", value=prezzo_energia_default, step=0.01, format="%.2f", key="energia")

st.sidebar.header("Dati di Utilizzo")
km_annui = st.sidebar.number_input("Chilometri annui percorsi", value=15000, step=500, format="%d")

# =============================
# 8. Caricamento File JSON (Google Takeout) - opzionale
# =============================
st.sidebar.header("Carica File JSON (opzionale)")
uploaded_files = st.sidebar.file_uploader("Seleziona uno o più file JSON", type=["json"], accept_multiple_files=True)
if uploaded_files:
    total_distance_km = 0
    for uploaded_file in uploaded_files:
        try:
            data = json.load(uploaded_file)
            activity_segments = [obj['activitySegment'] for obj in data.get("timelineObjects", []) if 'activitySegment' in obj]
            for segment in activity_segments:
                total_distance_km += segment.get('distance', 0) / 1000
        except Exception as e:
            st.sidebar.error(f"Errore nel file {uploaded_file.name}: {e}")
    if total_distance_km > 0:
        st.sidebar.success(f"Totale km caricati: {int(total_distance_km)} km")
        km_annui = int(total_distance_km)

# =============================
# 9. Funzioni di Calcolo
# =============================
def fattore_co2(tipo_auto):
    if tipo_auto == "Benzina":
        return 2.3
    elif tipo_auto == "Diesel":
        return 2.6
    elif tipo_auto == "Ibrido":
        return 2.0
    else:
        return 0.5

def prezzo_unita(tipo_auto, p_benz, p_diesel, p_en):
    if tipo_auto in ["Benzina", "Ibrido"]:
        return p_benz
    elif tipo_auto == "Diesel":
        return p_diesel
    else:
        return p_en

def calcola_consumo_medio(cons_urb, cons_ext, cons_aut, perc_urb, perc_ext, perc_aut):
    tot = perc_urb + perc_ext + perc_aut
    if tot <= 0:
        return (cons_urb + cons_ext + cons_aut) / 3.0
    return (cons_urb * (perc_urb / 100.0)
            + cons_ext * (perc_ext / 100.0)
            + cons_aut * (perc_aut / 100.0))

def calcola_costi_ed_emissioni(tipo_auto, cons_urb, cons_ext, cons_aut,
                               perc_urb, perc_ext, perc_aut,
                               p_benz, p_die, p_en, km):
    consumo_medio = calcola_consumo_medio(cons_urb, cons_ext, cons_aut, perc_urb, perc_ext, perc_aut)
    p_unitario = prezzo_unita(tipo_auto, p_benz, p_die, p_en)
    co2_factor = fattore_co2(tipo_auto)
    costo_annuo = (km / 100.0) * consumo_medio * p_unitario
    co2_annua = (km / 100.0) * consumo_medio * co2_factor
    return costo_annuo, co2_annua

def calcola_break_even(capex1, annuo1, capex2, annuo2):
    delta_iniziale = capex2 - capex1
    delta_annuo = annuo1 - annuo2
    if delta_iniziale > 0 and delta_annuo > 0:
        return delta_iniziale / delta_annuo
    delta_iniziale_bis = capex1 - capex2
    delta_annuo_bis = annuo2 - annuo1
    if delta_iniziale_bis > 0 and delta_annuo_bis > 0:
        return delta_iniziale_bis / delta_annuo_bis
    return None

# =============================
# 10. Calcoli Finali
# =============================
costo_annuo_auto1, co2_auto1 = calcola_costi_ed_emissioni(
    tipo_auto1,
    consumo_urbano1, consumo_extra1, consumo_autostrada1,
    perc_urbano, perc_extra, perc_autostrada,
    prezzo_benzina, prezzo_diesel, prezzo_energia,
    km_annui
)

costo_annuo_auto2, co2_auto2 = calcola_costi_ed_emissioni(
    tipo_auto2,
    consumo_urbano2, consumo_extra2, consumo_autostrada2,
    perc_urbano, perc_extra, perc_autostrada,
    prezzo_benzina, prezzo_diesel, prezzo_energia,
    km_annui
)

anni_pareggio = calcola_break_even(
    costo_iniziale_auto1, costo_annuo_auto1,
    costo_iniziale_auto2, costo_annuo_auto2
)

# =============================
# 11. Output Testuale
# =============================
st.subheader("Riepilogo del Confronto")

col1, col2 = st.columns(2)
with col1:
    st.write(f"**{modello_auto1} ({tipo_auto1})**")
    st.write(f"- **Costo iniziale:** €{int(costo_iniziale_auto1):,}")
    st.write(f"- **Costo annuo (ponderato):** €{int(costo_annuo_auto1):,}")
    st.write(f"- **Emissioni annue:** {int(co2_auto1):,} kg CO₂")
with col2:
    st.write(f"**{modello_auto2} ({tipo_auto2})**")
    st.write(f"- **Costo iniziale:** €{int(costo_iniziale_auto2):,}")
    st.write(f"- **Costo annuo (ponderato):** €{int(costo_annuo_auto2):,}")
    st.write(f"- **Emissioni annue:** {int(co2_auto2):,} kg CO₂")

if anni_pareggio:
    st.success(f"Tempo di ritorno dell'investimento: circa {anni_pareggio:.1f} anni.")
else:
    st.warning("Non si raggiunge un break-even con i dati attuali o i costi sono equivalenti.")

# =============================
# 12. Grafico: Costo Cumulativo (10 anni)
# =============================
st.subheader("Confronto del Costo Cumulativo (10 anni)")

anni_range = np.arange(0, 11)
cumul_auto1 = [costo_iniziale_auto1 + anno * costo_annuo_auto1 for anno in anni_range]
cumul_auto2 = [costo_iniziale_auto2 + anno * costo_annuo_auto2 for anno in anni_range]

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
    title="Evoluzione del Costo Totale nel Tempo",
    xaxis_title="Anni di utilizzo",
    yaxis_title="Costo Cumulativo (€)",
    hovermode="x unified",
    template="simple_white"
)
st.plotly_chart(fig_costi, use_container_width=True)

# =============================
# 13. Grafico: Emissioni Annue
# =============================
st.subheader("Confronto delle Emissioni di CO₂ (annue)")

fig_emiss = go.Figure(data=[
    go.Bar(
        x=[f"{modello_auto1} ({tipo_auto1})", f"{modello_auto2} ({tipo_auto2})"],
        y=[co2_auto1, co2_auto2],
        marker_color=['#1ABC9C', '#E67E22']
    )
])
fig_emiss.update_layout(
    title="Emissioni di CO₂ (kg/anno)",
    xaxis_title="Modello",
    yaxis_title="Emissioni (kg/anno)",
    template="simple_white"
)
st.plotly_chart(fig_emiss, use_container_width=True)

# =============================
# 14. Conclusione
# =============================
st.markdown(
    "<p class='description'>"
    "⚡ <strong>Scegli la soluzione più efficiente e sostenibile!</strong> 🚀"
    "</p>",
    unsafe_allow_html=True
)
