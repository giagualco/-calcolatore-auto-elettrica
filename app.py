import streamlit as st
import pandas as pd
import json
import matplotlib.pyplot as plt

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

# Distribuzione percentuale del tipo di percorso
st.sidebar.header("Distribuzione del percorso (%)")
perc_citta = st.sidebar.slider("Città", 0, 100, 30)
perc_extraurbano = st.sidebar.slider("Strada Extraurbana", 0, 100, 50)
perc_autostrada = 100 - perc_citta - perc_extraurbano
st.sidebar.write(f"Autostrada: {perc_autostrada}%")

# Sezione per il caricamento dei file JSON da Google Takeout
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

# Calcolo delle emissioni di CO2 (indicativo: 2.3 kg CO2 per litro di benzina, 0.5 kg CO2 per kWh)
co2_termica = (km_annui / 100) * consumo_termico_medio * 2.3
co2_elettrica = (km_annui / 100) * consumo_elettrico_medio * 0.5
co2_risparmiata = co2_termica - co2_elettrica

# Visualizzazione dei risultati
st.subheader("Risultati del confronto")

col1, col2 = st.columns(2)
with col1:
    st.metric(f"Costo annuale {modello_termico}", f"€{int(costo_annuo_termico):,}")
    st.metric(f"Consumo medio {modello_termico}", f"{consumo_termico_medio:.1f} L/100km")

with col2:
    st.metric(f"Costo annuale {modello_elettrico}", f"€{int(costo_annuo_elettrico):,}")
    st.metric(f"Consumo medio {modello_elettrico}", f"{consumo_elettrico_medio:.1f} kWh/100km")

# Grafico con doppia asse (euro e CO2 in funzione degli anni)
st.subheader("Tempo di ritorno dell'investimento")

if anni_pareggio:
    anni = list(range(1, anni_pareggio + 2))  # +2 per un punto extra sulla curva
    costi_risparmiati = [delta_costo_annuo * i for i in anni]
    co2_risparmiata_totale = [co2_risparmiata * i for i in anni]

    fig, ax1 = plt.subplots(figsize=(8, 5))

    ax1.set_xlabel("Anni di utilizzo")
    ax1.set_ylabel("Risparmio economico (€)", color="blue")
    ax1.plot(anni, costi_risparmiati, label="Risparmio economico", color="blue", marker="o")
    ax1.tick_params(axis="y", labelcolor="blue")

    ax2 = ax1.twinx()
    ax2.set_ylabel("CO₂ risparmiata (kg)", color="green")
    ax2.plot(anni, co2_risparmiata_totale, label="CO₂ risparmiata", color="green", marker="s")
    ax2.tick_params(axis="y", labelcolor="green")

    fig.tight_layout()
    st.pyplot(fig)
else:
    st.warning("Il risparmio economico non è sufficiente per determinare un tempo di ritorno dell'investimento.")
    
st.markdown("Confronta i costi e scegli la soluzione più efficiente e sostenibile.")

