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
def get_css(theme):
    """
    Restituisce il blocco CSS in base al tema selezionato (Light/Dark).
    Colori ispirati all'immagine fornita: background navy e testo giallo/bianco per il dark theme,
    sfondo bianco e testo scuro per il light theme.
    """
    if theme == "Dark":
        background_color = "#0F2748"  # Navy scuro
        text_color = "#FFFFFF"
        title_color = "#F7D600"      # Giallo acceso
        subtitle_color = "#F7D600"
        chart_bg_color = "#0F2748"
        chart_grid_color = "#FFFFFF"
    else:
        background_color = "#FFFFFF"
        text_color = "#333333"
        title_color = "#0F2748"      # Navy scuro
        subtitle_color = "#457B9D"   # Blu più chiaro
        chart_bg_color = "#FFFFFF"
        chart_grid_color = "#333333"
        
    css = f"""
    <style>
    .stApp {{
        background-color: {background_color};
    }}
    .stTitle {{
        color: {title_color};
        font-size: 28px;
        font-weight: bold;
    }}
    .stSubtitle {{
        color: {subtitle_color};
        font-size: 24px;
        font-weight: bold;
    }}
    .stText {{
        color: {text_color};
        font-size: 18px;
    }}
    /* Colore dei widget e dei testi nella sidebar */
    .css-1d391kg p, .css-1d391kg label, .css-1d391kg, .css-qrbaxs, .css-1v0mbdj {{
        color: {text_color} !important;
    }}
    /* Sfondo della sidebar */
    .css-1d391kg {{
        background-color: {background_color} !important;
    }}
    /* Box e testo dei file uploader e alert */
    .css-12w0qpk, .stAlert, .stFileUploader {{
        background-color: #f0f2f6 !important; /* Leggermente più chiaro per contrastare */
        color: #333333 !important;
    }}
    </style>
    """
    return css, chart_bg_color, chart_grid_color, text_color

# =============================
# Selezione tema in sidebar
# =============================
theme_choice = st.sidebar.selectbox("Seleziona il tema:", ["Light", "Dark"])

# Ottieni CSS e impostazioni per il grafico in base al tema
css_code, chart_bg_color, chart_grid_color, chart_text_color = get_css(theme_choice)

# Applica il CSS
st.markdown(css_code, unsafe_allow_html=True)

# Titolo principale (usa classi stTitle per colorarlo dinamicamente)
st.markdown('<h1 class="stTitle">🔋 Confronto Auto Elettrica vs Termica ⛽</h1>', unsafe_allow_html=True)

# =============================
# Dati del veicolo
# =============================
st.sidebar.header("🚗 Dati del veicolo")
tipo_veicolo = st.sidebar.selectbox("Tipo di veicolo", ["Benzina", "Diesel", "Ibrido", "Elettrico"])
modello_veicolo = st.sidebar.text_input("Modello veicolo", value="Auto Termica")
costo_iniziale_veicolo = st.sidebar.number_input("Prezzo d'acquisto (€)", value=25000, step=1000, format="%d")

# Consumi medi in base al tipo di veicolo
if tipo_veicolo == "Benzina":
    consumo_medio = st.sidebar.number_input("Consumo medio (L/100km)", value=6, step=1, format="%d")
elif tipo_veicolo == "Diesel":
    consumo_medio = st.sidebar.number_input("Consumo medio (L/100km)", value=5, step=1, format="%d")
elif tipo_veicolo == "Ibrido":
    consumo_medio = st.sidebar.number_input("Consumo medio (L/100km)", value=4, step=1, format="%d")
elif tipo_veicolo == "Elettrico":
    consumo_medio = st.sidebar.number_input("Consumo medio (kWh/100km)", value=15, step=1, format="%d")

# =============================
# Costi carburante e energia
# =============================
st.sidebar.header("💰 Costi del carburante e dell'energia")
if tipo_veicolo in ["Benzina", "Diesel", "Ibrido"]:
    prezzo_carburante = st.sidebar.number_input(f"Prezzo {tipo_veicolo.lower()} (€/L)", value=1.90, step=0.01, format="%.2f")
else:
    prezzo_energia = st.sidebar.number_input("Prezzo energia elettrica (€/kWh)", value=0.25, step=0.01, format="%.2f")

# =============================
# Dati di utilizzo
# =============================
st.sidebar.header("📊 Dati di utilizzo")
km_annui = st.sidebar.number_input("Chilometri annui percorsi", value=15000, step=500, format="%d")

# =============================
# Calcoli dei costi ed emissioni
# =============================
if tipo_veicolo in ["Benzina", "Diesel", "Ibrido"]:
    costo_annuo = (km_annui / 100) * consumo_medio * prezzo_carburante
    co2_emessa = (km_annui / 100) * consumo_medio * 2.3  # Emissioni CO2 per litro di carburante
else:
    costo_annuo = (km_annui / 100) * consumo_medio * prezzo_energia
    co2_emessa = (km_annui / 100) * consumo_medio * 0.5  # Emissioni CO2 per kWh

# =============================
# Riepilogo testuale del confronto
# =============================
st.markdown('<h2 class="stSubtitle">🔎 Riepilogo del Confronto</h2>', unsafe_allow_html=True)

riepilogo_testuale = f"""
- **Costo annuo di utilizzo**:
  - **{modello_veicolo}**: €{int(costo_annuo):,} all'anno

- **Emissioni di CO₂**:
  - **{modello_veicolo}**: {int(co2_emessa)} kg di CO₂ all'anno
"""

st.markdown(f'<p class="stText">{riepilogo_testuale}</p>', unsafe_allow_html=True)

# =============================
# Grafico del costo cumulativo nel tempo
# =============================
st.subheader("📈 Confronto del costo cumulativo nel tempo")

anni_range = np.arange(0, 11)
costo_totale = costo_iniziale_veicolo + anni_range * costo_annuo

fig, ax = plt.subplots(figsize=(8, 5))

# Stili di colore del grafico in base al tema
if theme_choice == "Dark":
    line_color = "#F7D600"
    fill_color = "#F7D600"
    ax.set_facecolor(chart_bg_color)
    ax.spines["bottom"].set_color(chart_grid_color)
    ax.spines["top"].set_color(chart_grid_color)
    ax.spines["left"].set_color(chart_grid_color)
    ax.spines["right"].set_color(chart_grid_color)
    ax.xaxis.label.set_color(chart_text_color)
    ax.yaxis.label.set_color(chart_text_color)
    ax.tick_params(axis='x', colors=chart_text_color)
    ax.tick_params(axis='y', colors=chart_text_color)
    title_color = "#F7D600"
else:
    line_color = "#457B9D"
    fill_color = "lightgrey"
    ax.set_facecolor(chart_bg_color)
    title_color = "#0F2748"

ax.plot(anni_range, costo_totale, 
        label=f"{modello_veicolo}", 
        color=line_color, 
        linestyle="-", linewidth=2, marker="o")

ax.fill_between(anni_range, costo_totale, 
                color=fill_color, alpha=0.2)

ax.set_xlabel("Anni di utilizzo", fontsize=12)
ax.set_ylabel("Costo cumulativo (€)", fontsize=12)
ax.set_title("📊 Confronto del costo cumulativo", fontsize=14, color=title_color)
ax.legend()
ax.grid(True, linestyle="--", alpha=0.5)

st.pyplot(fig)

st.markdown("⚡ **Scegli la soluzione più efficiente e sostenibile!** 🚀")
