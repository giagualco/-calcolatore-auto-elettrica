import streamlit as st
import pandas as pd
import json
from fpdf import FPDF

# Configurazione della pagina con colori personalizzati
st.set_page_config(page_title="Confronto Auto Elettrica vs Termica", page_icon="🚗", layout="wide")

# Definizione dei colori coerenti con il branding
sfondo_blu = "#0D1532"  # Blu scuro dell'immagine
testo_bianco = "#FFFFFF"
sidebar_grigio = "#192A56"  # Grigio già utilizzato

# Stile personalizzato
st.markdown(
    f'''
    <style>
        body {{
            font-family: 'Arial', sans-serif;
            background-color: {sfondo_blu};
            color: {testo_bianco};
        }}
        .title {{
            text-align: center;
            font-size: 36px;
            font-weight: bold;
            color: {testo_bianco};
        }}
        .stButton>button {{
            background-color: {testo_bianco};
            color: {sfondo_blu};
            font-size: 18px;
            font-weight: bold;
            border-radius: 8px;
        }}
        .sidebar .sidebar-content {{
            background-color: {sidebar_grigio};
            color: {testo_bianco};
        }}
    </style>
    ''',
    unsafe_allow_html=True
)

# Titolo principale
st.markdown("<h1 class='title'>Confronto Auto Elettrica vs Termica</h1>", unsafe_allow_html=True)

# Creazione di due colonne per migliorare l'organizzazione della UI
col1, col2 = st.columns(2)

with col1:
    st.subheader("Inserisci i dati del veicolo termico")
    modello_termico = st.text_input("Modello veicolo termico", value="")
    prezzo_termico = st.number_input("Prezzo d'acquisto (€) - Termico", value=25000, step=1000, format="%d")
    consumo_termico = st.number_input("Consumo carburante (L/100km)", value=6, step=1, format="%d")
    emissioni_termico = st.number_input("Emissioni CO2/km (g/km) - Termico", value=120, step=5, format="%d")

with col2:
    st.subheader("Inserisci i dati del veicolo elettrico")
    modello_elettrico = st.text_input("Modello veicolo elettrico", value="")
    prezzo_elettrico = st.number_input("Prezzo d'acquisto (€) - Elettrico", value=35000, step=1000, format="%d")
    consumo_elettrico = st.number_input("Consumo energia (kWh/100km)", value=15, step=1, format="%d")
    emissioni_elettrico = st.number_input("Emissioni CO2/km (g/km) - Elettrico", value=0, step=5, format="%d")

# Sezione costi energia e carburante
st.sidebar.header("Prezzi Energia e Carburante")
prezzo_benzina = st.sidebar.number_input("Prezzo benzina (€/L)", value=1.90, step=0.01, format="%.2f")
prezzo_energia = st.sidebar.number_input("Prezzo energia elettrica (€/kWh)", value=0.25, step=0.01, format="%.2f")

# Dati di utilizzo
st.sidebar.header("Dati di utilizzo")
km_annui = st.sidebar.number_input("Chilometraggio annuo (km)", value=15000, step=500, format="%d")

# Caricamento multiplo di file Google Takeout
st.sidebar.header("Carica i file Google Takeout")
uploaded_files = st.sidebar.file_uploader("Carica più file JSON", type=["json"], accept_multiple_files=True)

total_distance_km = 0
road_types = {"citta": 0, "extraurbano": 0, "autostrada": 0}

if uploaded_files:
    for uploaded_file in uploaded_files:
        data = json.load(uploaded_file)

        # Estrarre gli spostamenti
        activity_segments = [obj['activitySegment'] for obj in data["timelineObjects"] if 'activitySegment' in obj]

        # Sommare i chilometri percorsi e identificare il tipo di strada
        for segment in activity_segments:
            distance_km = segment.get('distance', 0) / 1000
            activity_type = segment.get('activityType', '').lower()

            total_distance_km += distance_km

            if "highway" in activity_type or "motorway" in activity_type or "expressway" in activity_type:
                road_types["autostrada"] += distance_km
            elif "city" in activity_type or "urban" in activity_type:
                road_types["citta"] += distance_km
            else:
                road_types["extraurbano"] += distance_km

    km_annui = int(total_distance_km)
    st.sidebar.success(f"Dati caricati con successo! Totale km percorsi: {km_annui} km")

# Slider per la suddivisione del percorso
st.sidebar.header("Distribuzione del percorso")
if uploaded_files:
    total_km = sum(road_types.values())
    perc_citta = round((road_types["citta"] / total_km) * 100) if total_km > 0 else 30
    perc_extraurbano = round((road_types["extraurbano"] / total_km) * 100) if total_km > 0 else 50
    perc_autostrada = 100 - perc_citta - perc_extraurbano
else:
    perc_citta = st.sidebar.slider("Città (%)", 0, 100, 30)
    perc_extraurbano = st.sidebar.slider("Strada Extraurbana (%)", 0, 100, 50)
    perc_autostrada = 100 - perc_citta - perc_extraurbano

# Emissioni CO2 per la costruzione dell'auto
emissioni_produzione_termico = 7000
emissioni_produzione_elettrico = 12000

# Calcoli dei costi totali
costo_totale_termica = prezzo_termico + ((km_annui / 100) * consumo_termico * prezzo_benzina * anni_possesso)
costo_totale_elettrica = prezzo_elettrico + ((km_annui / 100) * consumo_elettrico * prezzo_energia * anni_possesso)

# Calcolo delle emissioni totali di CO2
emissioni_totali_termica = (emissioni_termico * km_annui * anni_possesso / 1000) + emissioni_produzione_termico
emissioni_totali_elettrica = (emissioni_elettrico * km_annui * anni_possesso / 1000) + emissioni_produzione_elettrico

# Visualizzazione dei risultati
st.subheader("Risultati del confronto")

col1, col2 = st.columns(2)
with col1:
    st.metric(f"Costo totale {modello_termico if modello_termico else 'Auto Termica'}", f"€{int(costo_totale_termica):,}")
    st.metric(f"Emissioni totali CO2 {modello_termico if modello_termico else 'Auto Termica'}", f"{int(emissioni_totali_termica):,} kg")

with col2:
    st.metric(f"Costo totale {modello_elettrico if modello_elettrico else 'Auto Elettrica'}", f"€{int(costo_totale_elettrica):,}")
    st.metric(f"Emissioni totali CO2 {modello_elettrico if modello_elettrico else 'Auto Elettrica'}", f"{int(emissioni_totali_elettrica):,} kg")

st.markdown("Confronta i costi e le emissioni per scegliere la soluzione più efficiente e sostenibile.")
