import streamlit as st
import pandas as pd
import json
import matplotlib.pyplot as plt
import numpy as np

# Configurazione della pagina
st.set_page_config(page_title="Confronto Auto Elettrica vs Termica", page_icon="🚗", layout="wide")

# Stile CSS per migliorare l'aspetto grafico
st.markdown(
    """
    <style>
    .stApp { background-color: #F5F7FA; }
    .stTitle { color: #2E3B55; font-size: 28px; font-weight: bold; }
    .stSubtitle { color: #3E4C6E; font-size: 24px; font-weight: bold; }
    .stText { color: #4A4A4A; font-size: 18px; }
    </style>
    """,
    unsafe_allow_html=True
)

# Titolo principale
st.markdown('<h1 class="stTitle">🔋 Confronto Auto Elettrica vs Termica ⛽</h1>', unsafe_allow_html=True)

# Sezione per i dati del veicolo termico
st.sidebar.header("🚗 Dati del veicolo termico")
modello_termico = st.sidebar.text_input("Modello veicolo termico", value="Auto Termica")
prezzo_termico = st.sidebar.number_input("Prezzo d'acquisto (€)", value=25000, step=1000, format="%d")
consumo_termico_medio = st.sidebar.number_input("Consumo medio (L/100km)", value=6, step=1, format="%d")

# Sezione per i dati del veicolo elettrico
st.sidebar.header("⚡ Dati del veicolo elettrico")
modello_elettrico = st.sidebar.text_input("Modello veicolo elettrico", value="Auto Elettrica")
prezzo_elettrico = st.sidebar.number_input("Prezzo d'acquisto (€)", value=35000, step=1000, format="%d")
consumo_elettrico_medio = st.sidebar.number_input("Consumo medio (kWh/100km)", value=15, step=1, format="%d")

# Sezione per i costi del carburante e dell'energia
st.sidebar.header("💰 Costi del carburante e dell'energia")
prezzo_benzina = st.sidebar.number_input("Prezzo benzina (€/L)", value=1.90, step=0.01, format="%.2f")
prezzo_energia = st.sidebar.number_input("Prezzo energia elettrica (€/kWh)", value=0.25, step=0.01, format="%.2f")

# Sezione per i dati di utilizzo
st.sidebar.header("📊 Dati di utilizzo")
km_annui = st.sidebar.number_input("Chilometri annui percorsi", value=15000, step=500, format="%d")

# Sezione per il caricamento dei file JSON da Google Takeout
st.sidebar.header("📂 Carica i file Google Takeout")
uploaded_files = st.sidebar.file_uploader("Carica più file JSON", type=["json"], accept_multiple_files=True)

# Elaborazione dei file caricati per calcolare automaticamente i km annui
if uploaded_files:
    total_distance_km = 0
    for uploaded_file in uploaded_files:
        data = json.load(uploaded_file)
        activity_segments = [obj['activitySegment'] for obj in data["timelineObjects"] if 'activitySegment' in obj]
        for segment in activity_segments:
            total_distance_km += segment.get('distance', 0) / 1000

    st.sidebar.success(f"📊 Dati caricati! Totale km percorsi: {int(total_distance_km)} km")
    km_annui = int(total_distance_km)

# Calcolo dei costi annuali
costo_annuo_termico = (km_annui / 100) * consumo_termico_medio * prezzo_benzina
costo_annuo_elettrico = (km_annui / 100) * consumo_elettrico_medio * prezzo_energia

# Calcolo del tempo di ritorno dell'investimento
delta_costo_annuo = costo_annuo_termico - costo_annuo_elettrico
delta_prezzo_acquisto = prezzo_elettrico - prezzo_termico

if delta_costo_annuo > 0:
    anni_pareggio = int(delta_prezzo_acquisto / delta_costo_annuo)
else:
    anni_pareggio = None

# Calcolo delle emissioni di CO₂
co2_termica = (km_annui / 100) * consumo_termico_medio * 2.3
co2_elettrica = (km_annui / 100) * consumo_elettrico_medio * 0.5
co2_risparmiata = co2_termica - co2_elettrica

# Riepilogo testuale
st.markdown('<h2 class="stSubtitle">🔎 Riepilogo del Confronto</h2>', unsafe_allow_html=True)

riepilogo_testuale = f"""
- **Costo annuo di utilizzo**:
  - **{modello_termico}**: €{int(costo_annuo_termico):,} all'anno
  - **{modello_elettrico}**: €{int(costo_annuo_elettrico):,} all'anno

- **Costo totale dopo {anni_pareggio} anni**:
  - **{modello_termico}**: €{int(prezzo_termico + anni_pareggio * costo_annuo_termico):,}
  - **{modello_elettrico}**: €{int(prezzo_elettrico + anni_pareggio * costo_annuo_elettrico):,}

- **Tempo di ritorno dell'investimento**:
  - {"Il tempo di ritorno è di circa " + str(anni_pareggio) + " anni." if anni_pareggio else "Non si raggiunge un ritorno dell'investimento con i dati attuali."}

- **Riduzione delle emissioni di CO₂**:
  - {"Passando all'auto elettrica si risparmierebbero circa " + str(int(co2_risparmiata * anni_pareggio)) + " kg di CO₂ in " + str(anni_pareggio) + " anni." if co2_risparmiata > 0 else "Nessuna riduzione significativa delle emissioni di CO₂ osservata."}
"""
st.markdown(f'<p class="stText">{riepilogo_testuale}</p>', unsafe_allow_html=True)

# Grafico migliorato
st.subheader("📈 Confronto del costo cumulativo nel tempo")
anni = np.arange(0, anni_pareggio + 2) if anni_pareggio else np.arange(0, 11)
costo_totale_benzina = prezzo_termico + anni * costo_annuo_termico
costo_totale_elettrico = prezzo_elettrico + anni * costo_annuo_elettrico

fig, ax = plt.subplots(figsize=(8, 5))
ax.plot(anni, costo_totale_benzina, label="Auto a Benzina", color="red", linestyle="-", linewidth=2, marker="o")
ax.plot(anni, costo_totale_elettrico, label="Auto Elettrica", color="blue", linestyle="-", linewidth=2, marker="s")
ax.fill_between(anni, costo_totale_elettrico, costo_totale_benzina, color="lightgray", alpha=0.3)
ax.set_xlabel("Anni di utilizzo")
ax.set_ylabel("Costo cumulativo (€)")
ax.set_title("📊 Confronto del costo cumulativo")
ax.legend()
ax.grid(True, linestyle="--", alpha=0.5)
st.pyplot(fig)

st.markdown("⚡ **Scegli la soluzione più efficiente e sostenibile!** 🚀")
