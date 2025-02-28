import streamlit as st
import pandas as pd
import json
import matplotlib.pyplot as plt
import numpy as np

# Configurazione della pagina
st.set_page_config(page_title="Confronto Auto Elettrica vs Termica", page_icon="🚗", layout="wide")

# =============================
# Funzione per generare CSS minimale
# =============================
def get_css():
    """
    Restituisce un blocco CSS semplice con colori ad alto contrasto
    per garantire la massima leggibilità.
    """
    css = """
    <style>
    .stApp {
        background-color: #FFFFFF; /* Sfondo bianco */
    }
    .stTitle {
        color: #2C3E50; /* Blu scuro */
        font-size: 32px;
        font-weight: bold;
        margin-bottom: 20px;
    }
    .stSubtitle {
        color: #34495E; /* Blu medio */
        font-size: 24px;
        font-weight: bold;
        margin-bottom: 15px;
    }
    .stText {
        color: #333333; /* Testo scuro */
        font-size: 18px;
        line-height: 1.6;
    }
    .youtube-link {
        position: fixed;
        top: 10px;
        left: 10px;
        color: #FF0000 !important; /* Rosso YouTube */
        font-size: 16px;
        font-weight: bold;
        text-decoration: none;
    }
    .youtube-link:hover {
        text-decoration: underline;
    }
    </style>
    """
    return css

# Applica il CSS
st.markdown(get_css(), unsafe_allow_html=True)

# Link al canale YouTube (fisso in alto a sinistra)
st.markdown(
    '<a class="youtube-link" href="https://www.youtube.com/@giagualco" target="_blank">🎥 Canale YouTube</a>',
    unsafe_allow_html=True
)

# Titolo principale
st.markdown('<h1 class="stTitle">🔋 Confronto Auto Elettrica vs Termica ⛽</h1>', unsafe_allow_html=True)

# =============================
# Sidebar per input utente
# =============================
with st.sidebar:
    st.markdown('<h2 class="stSubtitle">🚗 Dati delle Auto</h2>', unsafe_allow_html=True)

    # Auto 1
    st.markdown("**Auto 1**")
    tipo_auto1 = st.selectbox("Tipo di auto 1", ["Benzina", "Diesel", "Ibrido", "Elettrico"], key="auto1")
    modello_auto1 = st.text_input("Modello auto 1", value="Auto 1", key="modello1")
    costo_iniziale_auto1 = st.number_input("Prezzo d'acquisto (€)", value=25000, step=1000, format="%d", key="costo1")
    if tipo_auto1 in ["Benzina", "Diesel", "Ibrido"]:
        consumo_auto1 = st.number_input("Consumo medio (L/100km)", value=6, step=1, format="%d", key="consumo1")
    else:
        consumo_auto1 = st.number_input("Consumo medio (kWh/100km)", value=15, step=1, format="%d", key="consumo1")

    # Auto 2
    st.markdown("**Auto 2**")
    tipo_auto2 = st.selectbox("Tipo di auto 2", ["Benzina", "Diesel", "Ibrido", "Elettrico"], key="auto2")
    modello_auto2 = st.text_input("Modello auto 2", value="Auto 2", key="modello2")
    costo_iniziale_auto2 = st.number_input("Prezzo d'acquisto (€)", value=35000, step=1000, format="%d", key="costo2")
    if tipo_auto2 in ["Benzina", "Diesel", "Ibrido"]:
        consumo_auto2 = st.number_input("Consumo medio (L/100km)", value=5, step=1, format="%d", key="consumo2")
    else:
        consumo_auto2 = st.number_input("Consumo medio (kWh/100km)", value=15, step=1, format="%d", key="consumo2")

    # Costi carburante e energia
    st.markdown('<h2 class="stSubtitle">💰 Costi del Carburante e dell\'Energia</h2>', unsafe_allow_html=True)
    prezzo_benzina = st.number_input("Prezzo benzina (€/L)", value=1.90, step=0.01, format="%.2f", key="benzina")
    prezzo_diesel = st.number_input("Prezzo diesel (€/L)", value=1.80, step=0.01, format="%.2f", key="diesel")
    prezzo_energia = st.number_input("Prezzo energia elettrica (€/kWh)", value=0.25, step=0.01, format="%.2f", key="energia")

    # Dati di utilizzo
    st.markdown('<h2 class="stSubtitle">📊 Dati di Utilizzo</h2>', unsafe_allow_html=True)
    km_annui = st.number_input("Chilometri annui percorsi", value=15000, step=500, format="%d")

    # Caricamento file JSON di Google
    st.markdown('<h2 class="stSubtitle">📂 Carica File JSON di Google</h2>', unsafe_allow_html=True)
    uploaded_files = st.file_uploader("Carica i file JSON di Google Takeout", type=["json"], accept_multiple_files=True)

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
                st.error(f"Errore nel caricamento del file {uploaded_file.name}: {e}")
        if total_distance_km > 0:
            st.success(f"📊 Dati caricati! Totale km percorsi: {int(total_distance_km)} km")
            km_annui = int(total_distance_km)

# =============================
# Funzione di calcolo costi ed emissioni
# =============================
def calcola_costi_e_emissioni(tipo_auto, consumo, km_annui, prezzo_carburante, prezzo_energia):
    """
    Calcola i costi annui e le emissioni di CO2 per una specifica tipologia di auto.
    - tipo_auto: "Benzina", "Diesel", "Ibrido" o "Elettrico"
    - consumo: L/100km o kWh/100km
    - km_annui: chilometri percorsi in un anno
    - prezzo_carburante: costo per L (benzina/diesel) se l'auto non è elettrica
    - prezzo_energia: costo per kWh se l'auto è elettrica
    """
    if tipo_auto in ["Benzina", "Diesel", "Ibrido"]:
        costo_annuo = (km_annui / 100) * consumo * prezzo_carburante
        co2_emessa = (km_annui / 100) * consumo * 2.3  # Emissioni CO2 per litro di carburante
    else:
        costo_annuo = (km_annui / 100) * consumo * prezzo_energia
        co2_emessa = (km_annui / 100) * consumo * 0.5  # Emissioni CO2 per kWh
    return costo_annuo, co2_emessa

# Calcoli per Auto 1
costo_annuo_auto1, co2_auto1 = calcola_costi_e_emissioni(
    tipo_auto1,
    consumo_auto1,
    km_annui,
    prezzo_benzina if tipo_auto1 == "Benzina" else prezzo_diesel,
    prezzo_energia
)

# Calcoli per Auto 2
costo_annuo_auto2, co2_auto2 = calcola_costi_e_emissioni(
    tipo_auto2,
    consumo_auto2,
    km_annui,
    prezzo_benzina if tipo_auto2 == "Benzina" else prezzo_diesel,
    prezzo_energia
)

# =============================
# Riepilogo testuale
# =============================
st.markdown('<h2 class="stSubtitle">🔎 Riepilogo del Confronto</h2>', unsafe_allow_html=True)

riepilogo_testuale = f"""
- **Costo annuo di utilizzo**:
  - **{modello_auto1}** ({tipo_auto1}): €{int(costo_annuo_auto1):,} all'anno
  - **{modello_auto2}** ({tipo_auto2}): €{int(costo_annuo_auto2):,} all'anno

- **Emissioni di CO₂**:
  - **{modello_auto1}** ({tipo_auto1}): {int(co2_auto1)} kg di CO₂ all'anno
  - **{modello_auto2}** ({tipo_auto2}): {int(co2_auto2)} kg di CO₂ all'anno
"""

st.markdown(f'<p class="stText">{riepilogo_testuale}</p>', unsafe_allow_html=True)

# =============================
# Grafico del costo cumulativo
# =============================
st.markdown('<h2 class="stSubtitle">📈 Confronto del Costo Cumulativo</h2>', unsafe_allow_html=True)

anni_range = np.arange(0, 11)
costo_totale_auto1 = costo_iniziale_auto1 + anni_range * costo_annuo_auto1
costo_totale_auto2 = costo_iniziale_auto2 + anni_range * costo_annuo_auto2

fig, ax = plt.subplots(figsize=(10, 6))
ax.plot(
    anni_range, costo_totale_auto1,
    label=f"{modello_auto1} ({tipo_auto1})",
    color="#1f77b4", linestyle="-", linewidth=2, marker="o"
)
ax.plot(
    anni_range, costo_totale_auto2,
    label=f"{modello_auto2} ({tipo_auto2})",
    color="#ff7f0e", linestyle="-", linewidth=2, marker="s"
)
ax.fill_between(
    anni_range,
    costo_totale_auto1,
    costo_totale_auto2,
    color="#f0f2f6",
    alpha=0.3
)

ax.set_xlabel("Anni di utilizzo", fontsize=12, color="#2C3E50")
ax.set_ylabel("Costo Cumulativo (€)", fontsize=12, color="#2C3E50")
ax.set_title("Confronto del Costo Cumulativo", fontsize=16, color="#2C3E50", pad=20)
ax.legend(loc="upper left", fontsize=12)
ax.grid(True, linestyle="--", alpha=0.5)
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)
st.pyplot(fig)

# =============================
# Grafico delle emissioni di CO₂
# =============================
st.markdown('<h2 class="stSubtitle">🌍 Confronto delle Emissioni di CO₂</h2>', unsafe_allow_html=True)

fig2, ax2 = plt.subplots(figsize=(8, 6))
ax2.bar(
    [f"{modello_auto1} ({tipo_auto1})", f"{modello_auto2} ({tipo_auto2})"],
    [co2_auto1, co2_auto2],
    color=["#1f77b4", "#ff7f0e"]
)
ax2.set_xlabel("Modello", fontsize=12, color="#2C3E50")
ax2.set_ylabel("Emissioni di CO₂ (kg/anno)", fontsize=12, color="#2C3E50")
ax2.set_title("Confronto delle Emissioni di CO₂", fontsize=16, color="#2C3E50", pad=20)
ax2.grid(True, linestyle="--", alpha=0.5, axis="y")
ax2.spines['top'].set_visible(False)
ax2.spines['right'].set_visible(False)
st.pyplot(fig2)

# Messaggio finale
st.markdown('<p class="stText">⚡ <strong>Scegli la soluzione più efficiente e sostenibile!</strong> 🚀</p>', unsafe_allow_html=True)
