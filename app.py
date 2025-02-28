import streamlit as st
import pandas as pd
import json
import matplotlib.pyplot as plt
import numpy as np

# Configurazione della pagina
st.set_page_config(page_title="Confronto Auto Elettrica vs Termica", page_icon="🚗", layout="wide")

# =============================
# Funzione per generare CSS dinamico
# =============================
def get_css():
    """
    Restituisce il blocco CSS con colori professionali e stile moderno.
    """
    css = """
    <style>
    .stApp {
        background-color: #F0F2F6; /* Sfondo grigio chiaro */
    }
    .stTitle {
        color: #0F2748; /* Blu scuro */
        font-size: 28px;
        font-weight: bold;
    }
    .stSubtitle {
        color: #457B9D; /* Blu medio */
        font-size: 24px;
        font-weight: bold;
    }
    .stText {
        color: #333333; /* Testo scuro */
        font-size: 18px;
    }
    /* Colore dei widget e dei testi nella sidebar */
    .css-1d391kg p, .css-1d391kg label, .css-1d391kg, .css-qrbaxs, .css-1v0mbdj {
        color: #333333 !important;
    }
    /* Sfondo della sidebar */
    .css-1d391kg {
        background-color: #FFFFFF !important; /* Bianco */
    }
    /* Box e testo dei file uploader e alert */
    .css-12w0qpk, .stAlert, .stFileUploader {
        background-color: #FFFFFF !important; /* Bianco */
        color: #333333 !important;
    }
    /* Link al canale YouTube */
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

# Link al canale YouTube
st.markdown(
    '<a class="youtube-link" href="https://www.youtube.com/@giagualco" target="_blank">🎥 Canale YouTube</a>',
    unsafe_allow_html=True
)

# Titolo principale
st.markdown('<h1 class="stTitle">🔋 Confronto Auto Elettrica vs Termica ⛽</h1>', unsafe_allow_html=True)

# =============================
# Dati delle due auto
# =============================
st.sidebar.header("🚗 Dati delle auto")

# Auto 1
st.sidebar.subheader("Auto 1")
tipo_auto1 = st.sidebar.selectbox("Tipo di auto 1", ["Benzina", "Diesel", "Ibrido", "Elettrico"], key="auto1")
modello_auto1 = st.sidebar.text_input("Modello auto 1", value="Auto 1", key="modello1")
costo_iniziale_auto1 = st.sidebar.number_input("Prezzo d'acquisto (€)", value=25000, step=1000, format="%d", key="costo1")
if tipo_auto1 in ["Benzina", "Diesel", "Ibrido"]:
    consumo_auto1 = st.sidebar.number_input("Consumo medio (L/100km)", value=6, step=1, format="%d", key="consumo1")
else:
    consumo_auto1 = st.sidebar.number_input("Consumo medio (kWh/100km)", value=15, step=1, format="%d", key="consumo1")

# Auto 2
st.sidebar.subheader("Auto 2")
tipo_auto2 = st.sidebar.selectbox("Tipo di auto 2", ["Benzina", "Diesel", "Ibrido", "Elettrico"], key="auto2")
modello_auto2 = st.sidebar.text_input("Modello auto 2", value="Auto 2", key="modello2")
costo_iniziale_auto2 = st.sidebar.number_input("Prezzo d'acquisto (€)", value=35000, step=1000, format="%d", key="costo2")
if tipo_auto2 in ["Benzina", "Diesel", "Ibrido"]:
    consumo_auto2 = st.sidebar.number_input("Consumo medio (L/100km)", value=5, step=1, format="%d", key="consumo2")
else:
    consumo_auto2 = st.sidebar.number_input("Consumo medio (kWh/100km)", value=15, step=1, format="%d", key="consumo2")

# =============================
# Costi carburante e energia
# =============================
st.sidebar.header("💰 Costi del carburante e dell'energia")
prezzo_benzina = st.sidebar.number_input("Prezzo benzina (€/L)", value=1.90, step=0.01, format="%.2f", key="benzina")
prezzo_diesel = st.sidebar.number_input("Prezzo diesel (€/L)", value=1.80, step=0.01, format="%.2f", key="diesel")
prezzo_energia = st.sidebar.number_input("Prezzo energia elettrica (€/kWh)", value=0.25, step=0.01, format="%.2f", key="energia")

# =============================
# Dati di utilizzo
# =============================
st.sidebar.header("📊 Dati di utilizzo")
km_annui = st.sidebar.number_input("Chilometri annui percorsi", value=15000, step=500, format="%d")

# =============================
# Calcoli dei costi ed emissioni
# =============================
def calcola_costi_e_emissioni(tipo_auto, consumo, km_annui, prezzo_carburante, prezzo_energia):
    if tipo_auto in ["Benzina", "Diesel", "Ibrido"]:
        costo_annuo = (km_annui / 100) * consumo * prezzo_carburante
        co2_emessa = (km_annui / 100) * consumo * 2.3  # Emissioni CO2 per litro di carburante
    else:
        costo_annuo = (km_annui / 100) * consumo * prezzo_energia
        co2_emessa = (km_annui / 100) * consumo * 0.5  # Emissioni CO2 per kWh
    return costo_annuo, co2_emessa

costo_annuo_auto1, co2_auto1 = calcola_costi_e_emissioni(tipo_auto1, consumo_auto1, km_annui, prezzo_benzina if tipo_auto1 == "Benzina" else prezzo_diesel, prezzo_energia)
costo_annuo_auto2, co2_auto2 = calcola_costi_e_emissioni(tipo_auto2, consumo_auto2, km_annui, prezzo_benzina if tipo_auto2 == "Benzina" else prezzo_diesel, prezzo_energia)

# =============================
# Riepilogo testuale del confronto
# =============================
st.markdown('<h2 class="stSubtitle">🔎 Riepilogo del Confronto</h2>', unsafe_allow_html=True)

riepilogo_testuale = f"""
- **Costo annuo di utilizzo**:
  - **{modello_auto1}**: €{int(costo_annuo_auto1):,} all'anno
  - **{modello_auto2}**: €{int(costo_annuo_auto2):,} all'anno

- **Emissioni di CO₂**:
  - **{modello_auto1}**: {int(co2_auto1)} kg di CO₂ all'anno
  - **{modello_auto2}**: {int(co2_auto2)} kg di CO₂ all'anno
"""

st.markdown(f'<p class="stText">{riepilogo_testuale}</p>', unsafe_allow_html=True)

# =============================
# Grafico del costo cumulativo nel tempo
# =============================
st.subheader("📈 Confronto del costo cumulativo nel tempo")

anni_range = np.arange(0, 11)
costo_totale_auto1 = costo_iniziale_auto1 + anni_range * costo_annuo_auto1
costo_totale_auto2 = costo_iniziale_auto2 + anni_range * costo_annuo_auto2

fig, ax = plt.subplots(figsize=(10, 6))

# Stili di colore del grafico
ax.plot(anni_range, costo_totale_auto1, label=f"{modello_auto1}", color="#457B9D", linestyle="-", linewidth=2, marker="o")
ax.plot(anni_range, costo_totale_auto2, label=f"{modello_auto2}", color="#E63946", linestyle="-", linewidth=2, marker="s")

ax.fill_between(anni_range, costo_totale_auto1, costo_totale_auto2, color="#F0F2F6", alpha=0.3)

ax.set_xlabel("Anni di utilizzo", fontsize=12, color="#333333")
ax.set_ylabel("Costo cumulativo (€)", fontsize=12, color="#333333")
ax.set_title("📊 Confronto del costo cumulativo", fontsize=14, color="#0F2748")
ax.legend()
ax.grid(True, linestyle="--", alpha=0.5)

st.pyplot(fig)

# =============================
# Grafico delle emissioni di CO₂
# =============================
st.subheader("🌍 Confronto delle emissioni di CO₂")

fig2, ax2 = plt.subplots(figsize=(10, 6))

# Barre per le emissioni
ax2.bar([modello_auto1, modello_auto2], [co2_auto1, co2_auto2], color=["#457B9D", "#E63946"])

ax2.set_xlabel("Modello", fontsize=12, color="#333333")
ax2.set_ylabel("Emissioni di CO₂ (kg/anno)", fontsize=12, color="#333333")
ax2.set_title("📊 Confronto delle emissioni di CO₂", fontsize=14, color="#0F2748")
ax2.grid(True, linestyle="--", alpha=0.5)

st.pyplot(fig2)

st.markdown("⚡ **Scegli la soluzione più efficiente e sostenibile!** 🚀")
