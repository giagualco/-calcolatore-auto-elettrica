import streamlit as st
import pandas as pd
import json

# Configurazione della pagina con colori personalizzati
st.set_page_config(page_title="Confronto Auto Elettrica vs Termica", page_icon="🚗", layout="wide")

# Stile personalizzato CSS
st.markdown("""
    <style>
        body {
            font-family: 'Arial', sans-serif;
            background-color: #0D1532; /* Blu scuro */
            color: #FFFFFF;
        }
        .title {
            text-align: center;
            font-size: 36px;
            font-weight: bold;
            color: #FFD700; /* Giallo */
        }
        .stButton>button {
            background-color: #FFD700;
            color: #0D1532;
            font-size: 18px;
            font-weight: bold;
            border-radius: 8px;
        }
        .sidebar .sidebar-content {
            background-color: #192A56; /* Grigio scuro */
            color: #FFFFFF;
        }
        .metric-container {
            text-align: center;
            font-size: 22px;
            font-weight: bold;
        }
    </style>
""", unsafe_allow_html=True)

# Titolo principale con stile
st.markdown("<h1 class='title'>🔋 Confronto Auto Elettrica vs Termica 🚗</h1>", unsafe_allow_html=True)

# Sezione per il caricamento dei file JSON da Google Takeout
st.sidebar.header("📂 Carica i file Google Takeout")
uploaded_files = st.sidebar.file_uploader("Carica più file JSON", type=["json"], accept_multiple_files=True)

# Variabili per il calcolo dei km annui e del tipo di percorso
total_distance_km = None
road_types = {"citta": 0, "extraurbano": 0, "autostrada": 0}

# Elaborazione dei file caricati
if uploaded_files:
    total_distance_km = 0
    for uploaded_file in uploaded_files:
        data = json.load(uploaded_file)

        # Estrazione dei segmenti di percorso
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

    st.sidebar.success(f"✅ Dati caricati! Totale km percorsi: {int(total_distance_km)} km")

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
st.sidebar.header("⛽ Costi del carburante e dell'energia")
prezzo_benzina = st.sidebar.number_input("Prezzo benzina (€/L)", value=1.90, step=0.01, format="%.2f")
prezzo_energia = st.sidebar.number_input("Prezzo energia elettrica (€/kWh)", value=0.25, step=0.01, format="%.2f")

# Sezione per i dati di utilizzo
st.sidebar.header("📊 Dati di utilizzo")

if total_distance_km is not None:
    st.sidebar.text(f"📌 Chilometraggio annuo calcolato: {int(total_distance_km)} km")
    km_annui = int(total_distance_km)
else:
    km_annui = st.sidebar.number_input("Chilometri annui percorsi", value=15000, step=500, format="%d")

# Distribuzione percentuale del tipo di percorso
st.sidebar.header("🛣️ Distribuzione del percorso (%)")
if uploaded_files:
    total_km = sum(road_types.values())
    perc_citta = round((road_types["citta"] / total_km) * 100) if total_km > 0 else 30
    perc_extraurbano = round((road_types["extraurbano"] / total_km) * 100) if total_km > 0 else 50
    perc_autostrada = 100 - perc_citta - perc_extraurbano
else:
    perc_citta = st.sidebar.slider("Città", 0, 100, 30)
    perc_extraurbano = st.sidebar.slider("Strada Extraurbana", 0, 100, 50)
    perc_autostrada = 100 - perc_citta - perc_extraurbano

st.sidebar.write(f"🚙 Autostrada: {perc_autostrada}%")

# Calcolo dei costi e consumi ponderati
costo_annuo_termico = (km_annui / 100) * consumo_termico_medio * prezzo_benzina
costo_annuo_elettrico = (km_annui / 100) * consumo_elettrico_medio * prezzo_energia

# Visualizzazione dei risultati
st.subheader("📊 Risultati del confronto")

col1, col2 = st.columns(2)
with col1:
    st.metric(f"Costo annuale {modello_termico}", f"€{int(costo_annuo_termico):,}")
    st.metric(f"Consumo medio {modello_termico}", f"{consumo_termico_medio:.1f} L/100km")

with col2:
    st.metric(f"Costo annuale {modello_elettrico}", f"€{int(costo_annuo_elettrico):,}")
    st.metric(f"Consumo medio {modello_elettrico}", f"{consumo_elettrico_medio:.1f} kWh/100km")

st.markdown("⚡ **Confronta i costi e scegli la soluzione più efficiente e sostenibile!** 🚀")
