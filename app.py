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
    includendo media queries per dispositivi mobili.
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
# 2. Titolo e Link al Canale YouTube
# =============================
st.markdown("<h1 class='main-title'>Configuratore Avanzato Auto</h1>", unsafe_allow_html=True)
st.markdown(
    '<p class="description">'
    'Confronta due veicoli considerando consumi specifici per percorso (urbano, extraurbano, autostrada), '
    'analizza costi annui, emissioni di CO₂ e calcola il break-even.<br>'
    'Approfondisci sul mio <a class="youtube-link" href="https://www.youtube.com/@giagualco" target="_blank">Canale YouTube</a>!'
    '</p>',
    unsafe_allow_html=True
)

# =============================
# 3. Sidebar: Dati per i Veicoli
# =============================
# --- Veicolo 1 ---
st.sidebar.header("Dati del Veicolo 1")
tipo_auto1 = st.sidebar.selectbox("Tipo di auto 1", ["Benzina", "Diesel", "Ibrido", "Elettrico"], key="auto1")
modello_auto1 = st.sidebar.text_input("Modello auto 1", value="Auto 1", key="modello1")
costo_iniziale_auto1 = st.sidebar.number_input("Prezzo d'acquisto (€)", value=25000, step=1000, format="%d", key="costo1")

st.sidebar.subheader("Consumi per Veicolo 1")
if tipo_auto1 in ["Benzina", "Diesel", "Ibrido"]:
    consumo_urbano1 = st.sidebar.number_input("Urbano (L/100km)", value=7.0, step=0.1, format="%.1f", key="c_urb1")
    consumo_extra1 = st.sidebar.number_input("Extraurbano (L/100km)", value=5.5, step=0.1, format="%.1f", key="c_ext1")
    consumo_autostrada1 = st.sidebar.number_input("Autostrada (L/100km)", value=6.5, step=0.1, format="%.1f", key="c_aut1")
else:
    consumo_urbano1 = st.sidebar.number_input("Urbano (kWh/100km)", value=16.0, step=0.1, format="%.1f", key="c_urb1")
    consumo_extra1 = st.sidebar.number_input("Extraurbano (kWh/100km)", value=13.0, step=0.1, format="%.1f", key="c_ext1")
    consumo_autostrada1 = st.sidebar.number_input("Autostrada (kWh/100km)", value=18.0, step=0.1, format="%.1f", key="c_aut1")

# --- Veicolo 2 ---
st.sidebar.header("Dati del Veicolo 2")
tipo_auto2 = st.sidebar.selectbox("Tipo di auto 2", ["Benzina", "Diesel", "Ibrido", "Elettrico"], key="auto2")
modello_auto2 = st.sidebar.text_input("Modello auto 2", value="Auto 2", key="modello2")
costo_iniziale_auto2 = st.sidebar.number_input("Prezzo d'acquisto (€)", value=35000, step=1000, format="%d", key="costo2")

st.sidebar.subheader("Consumi per Veicolo 2")
if tipo_auto2 in ["Benzina", "Diesel", "Ibrido"]:
    consumo_urbano2 = st.sidebar.number_input("Urbano (L/100km)", value=7.5, step=0.1, format="%.1f", key="c_urb2")
    consumo_extra2 = st.sidebar.number_input("Extraurbano (L/100km)", value=5.0, step=0.1, format="%.1f", key="c_ext2")
    consumo_autostrada2 = st.sidebar.number_input("Autostrada (L/100km)", value=6.0, step=0.1, format="%.1f", key="c_aut2")
else:
    consumo_urbano2 = st.sidebar.number_input("Urbano (kWh/100km)", value=17.0, step=0.1, format="%.1f", key="c_urb2")
    consumo_extra2 = st.sidebar.number_input("Extraurbano (kWh/100km)", value=12.0, step=0.1, format="%.1f", key="c_ext2")
    consumo_autostrada2 = st.sidebar.number_input("Autostrada (kWh/100km)", value=20.0, step=0.1, format="%.1f", key="c_aut2")

# =============================
# 4. Sidebar: Percentuali di Percorrenza & Costi Carburante/Energia
# =============================
st.sidebar.header("Percentuali di Guida (%)")
perc_urbano = st.sidebar.slider("Urbano (%)", min_value=0, max_value=100, value=40, step=5, key="perc_urb")
perc_extra = st.sidebar.slider("Extraurbano (%)", min_value=0, max_value=100, value=40, step=5, key="perc_ext")
perc_autostrada = st.sidebar.slider("Autostrada (%)", min_value=0, max_value=100, value=20, step=5, key="perc_aut")

if (perc_urbano + perc_extra + perc_autostrada) != 100:
    st.sidebar.warning("La somma delle percentuali deve essere 100%.")

st.sidebar.header("Costi Carburante / Energia")
prezzo_benzina = st.sidebar.number_input("Prezzo benzina (€/L)", value=1.90, step=0.01, format="%.2f", key="benzina")
prezzo_diesel = st.sidebar.number_input("Prezzo diesel (€/L)", value=1.80, step=0.01, format="%.2f", key="diesel")
prezzo_energia = st.sidebar.number_input("Prezzo energia elettrica (€/kWh)", value=0.25, step=0.01, format="%.2f", key="energia")

st.sidebar.header("Dati di Utilizzo")
km_annui = st.sidebar.number_input("Chilometri annui percorsi", value=15000, step=500, format="%d")

# =============================
# 5. Caricamento File JSON (Google Takeout)
# =============================
st.sidebar.header("Carica File JSON")
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
# 6. Funzioni di Calcolo
# =============================
def fattore_co2(tipo_auto):
    """
    Ritorna il fattore di emissione (kg CO₂ per unità) per il tipo di veicolo.
    """
    if tipo_auto == "Benzina":
        return 2.3
    elif tipo_auto == "Diesel":
        return 2.6
    elif tipo_auto == "Ibrido":
        return 2.0
    else:  # Elettrico
        return 0.5

def prezzo_unita(tipo_auto, p_benz, p_diesel, p_energia):
    """
    Ritorna il prezzo unitario (€/L o €/kWh) in base al tipo di auto.
    """
    if tipo_auto in ["Benzina", "Ibrido"]:
        return p_benz
    elif tipo_auto == "Diesel":
        return p_diesel
    else:
        return p_energia

def calcola_consumo_medio(cons_urb, cons_ext, cons_aut, perc_urb, perc_ext, perc_aut):
    """
    Calcola il consumo medio ponderato (L/100km o kWh/100km)
    in base alle percentuali di percorrenza.
    """
    tot = perc_urb + perc_ext + perc_aut
    if tot == 0:
        return (cons_urb + cons_ext + cons_aut) / 3
    return cons_urb * (perc_urb / 100) + cons_ext * (perc_ext / 100) + cons_aut * (perc_aut / 100)

def calcola_costi_ed_emissioni(tipo_auto, cons_urb, cons_ext, cons_aut, perc_urb, perc_ext, perc_aut,
                                p_benz, p_die, p_en, km_annui):
    """
    Calcola il costo annuo e le emissioni annue (kg CO₂) per un veicolo,
    considerando il consumo medio ponderato.
    """
    consumo_medio = calcola_consumo_medio(cons_urb, cons_ext, cons_aut, perc_urb, perc_ext, perc_aut)
    p_unitario = prezzo_unita(tipo_auto, p_benz, p_die, p_en)
    co2_factor = fattore_co2(tipo_auto)
    costo_annuo = (km_annui / 100.0) * consumo_medio * p_unitario
    co2_annua = (km_annui / 100.0) * consumo_medio * co2_factor
    return costo_annuo, co2_annua

def calcola_break_even(capex1, annuo1, capex2, annuo2):
    """
    Calcola in quanti anni si raggiunge il break-even tra due veicoli.
    Restituisce il tempo di recupero (anni) se esiste, altrimenti None.
    """
    delta_capex = capex2 - capex1
    delta_annuo = annuo1 - annuo2
    if delta_capex > 0 and delta_annuo > 0:
        return delta_capex / delta_annuo
    delta_capex_bis = capex1 - capex2
    delta_annuo_bis = annuo2 - annuo1
    if delta_capex_bis > 0 and delta_annuo_bis > 0:
        return delta_capex_bis / delta_annuo_bis
    return None

# =============================
# 7. Calcoli Finali
# =============================
costo_annuo_auto1, co2_auto1 = calcola_costi_ed_emissioni(
    tipo_auto1, consumo_urbano1, consumo_extra1, consumo_autostrada1,
    perc_urbano, perc_extra, perc_autostrada,
    prezzo_benzina, prezzo_diesel, prezzo_energia,
    km_annui
)

costo_annuo_auto2, co2_auto2 = calcola_costi_ed_emissioni(
    tipo_auto2, consumo_urbano2, consumo_extra2, consumo_autostrada2,
    perc_urbano, perc_extra, perc_autostrada,
    prezzo_benzina, prezzo_diesel, prezzo_energia,
    km_annui
)

anni_pareggio = calcola_break_even(costo_iniziale_auto1, costo_annuo_auto1,
                                    costo_iniziale_auto2, costo_annuo_auto2)

# =============================
# 8. Output Testuale
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
# 9. Grafico: Costo Cumulativo (10 anni)
# =============================
st.subheader("Confronto del Costo Cumulativo (10 anni)")

anni = np.arange(0, 11)
cumul_auto1 = [costo_iniziale_auto1 + anno * costo_annuo_auto1 for anno in anni]
cumul_auto2 = [costo_iniziale_auto2 + anno * costo_annuo_auto2 for anno in anni]

fig_costi = go.Figure()
fig_costi.add_trace(go.Scatter(
    x=anni,
    y=cumul_auto1,
    mode='lines+markers',
    name=f"{modello_auto1} ({tipo_auto1})",
    line=dict(color='#1ABC9C', width=3),
    marker=dict(size=6)
))
fig_costi.add_trace(go.Scatter(
    x=anni,
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
# 10. Grafico: Emissioni Annue
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
# 11. Conclusione
# =============================
st.markdown(
    "<p class='description'>"
    "⚡ <strong>Scegli la soluzione più efficiente e sostenibile!</strong> 🚀"
    "</p>",
    unsafe_allow_html=True
)
