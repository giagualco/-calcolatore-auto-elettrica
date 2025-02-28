import streamlit as st
import pandas as pd
import json
import matplotlib.pyplot as plt
import numpy as np

# Configurazione della pagina
st.set_page_config(page_title="Confronto Auto Elettrica vs Termica", page_icon="🚗", layout="wide")

# Titolo principale
st.title("Confronto Auto Elettrica vs Termica")

# Sezione per i dati del veicolo termico
st.sidebar.header("Dati del veicolo termico")
modello_termico = st.sidebar.text_input("Modello veicolo termico", value="Auto Termica")
prezzo_termico = st.sidebar.number_input("Prezzo d'acquisto (€)", value=25000, step=1000, format="%d")
consumo_termico_medio = st.sidebar.number_input("Consumo medio (L/100km)", value=6, step=1, format="%d")

# Sezione per i dati del veicolo elettrico
st.sidebar.header("Dati del veicolo elettrico")
modello_elettrico = st.sidebar.text_input("Modello veicolo elettrico", value="Auto Elettrica")
prezzo_elettrico = st.sidebar.number_input("Prezzo d'acquisto (€)", value=35000, step=1000, format="%d")
consumo_elettrico_medio = st.sidebar.number_input("Consumo medio (kWh/100km)", value=15, step=1, format="%d")

# Sezione per i costi del carburante e dell'energia
st.sidebar.header("Costi del carburante e dell'energia")
prezzo_benzina = st.sidebar.number_input("Prezzo benzina (€/L)", value=1.90, step=0.01, format="%.2f")
prezzo_energia = st.sidebar.number_input("Prezzo energia elettrica (€/kWh)", value=0.25, step=0.01, format="%.2f")

# Sezione per i dati di utilizzo
st.sidebar.header("Dati di utilizzo")
km_annui = st.sidebar.number_input("Chilometri annui percorsi", value=15000, step=500, format="%d")

# Caricamento dei file JSON da Google Takeout
st.sidebar.header("Carica i file Google Takeout")
uploaded_files = st.sidebar.file_uploader("Carica più file JSON", type=["json"], accept_multiple_files=True)

# Variabili per il calcolo dei km annui e del tipo di percorso
total_distance_km = None

# Elaborazione dei file caricati
if uploaded_files:
    total_distance_km = 0
    for uploaded_file in uploaded_files:
        data = json.load(uploaded_file)

        # Estrazione dei segmenti di percorso
        activity_segments = [obj['activitySegment'] for obj in data["timelineObjects"] if 'activitySegment' in obj]

        # Sommare i chilometri percorsi
        for segment in activity_segments:
            distance_km = segment.get('distance', 0) / 1000
            total_distance_km += distance_km

    st.sidebar.success(f"Dati caricati! Totale km percorsi: {int(total_distance_km)} km")
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

# Simulazione dati per CO₂
co2_termica = (km_annui / 100) * consumo_termico_medio * 2.3
co2_elettrica = (km_annui / 100) * consumo_elettrico_medio * 0.5
co2_risparmiata = co2_termica - co2_elettrica

# Creazione dei grafici

# 1️⃣ Grafico del tempo di ritorno dell'investimento economico (€)
st.subheader("Tempo di ritorno dell'investimento economico")
anni = np.arange(0, anni_pareggio + 2) if anni_pareggio else np.arange(0, 11)

costo_totale_benzina = prezzo_termico + anni * costo_annuo_termico
costo_totale_elettrico = prezzo_elettrico + anni * costo_annuo_elettrico

fig1, ax1 = plt.subplots(figsize=(8, 5))
ax1.plot(anni, costo_totale_benzina, label="Auto a Benzina", color="red", linestyle="-", linewidth=2)
ax1.plot(anni, costo_totale_elettrico, label="Auto Elettrica", color="blue", linestyle="-", linewidth=2)
ax1.set_xlabel("Anni di utilizzo")
ax1.set_ylabel("Costo cumulativo (€)")
ax1.set_title("Tempo di ritorno dell'investimento economico")
ax1.legend()
ax1.grid(True)
st.pyplot(fig1)

# 2️⃣ Grafico del tempo di ritorno dell'investimento in CO₂
st.subheader("Tempo di ritorno dell'investimento in CO₂")

co2_totale_benzina = anni * co2_termica
co2_totale_elettrica = anni * co2_elettrica

fig2, ax2 = plt.subplots(figsize=(8, 5))
ax2.plot(anni, co2_totale_benzina, label="Auto a Benzina", color="red", linestyle="-", linewidth=2)
ax2.plot(anni, co2_totale_elettrica, label="Auto Elettrica", color="blue", linestyle="-", linewidth=2)
ax2.set_xlabel("Anni di utilizzo")
ax2.set_ylabel("CO₂ cumulativa (kg)")
ax2.set_title("Tempo di ritorno dell'investimento in CO₂")
ax2.legend()
ax2.grid(True)
st.pyplot(fig2)
