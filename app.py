import streamlit as st
import pandas as pd

# Configurazione della pagina con colori personalizzati
st.set_page_config(page_title="Confronto Auto Elettrica vs Termica", page_icon="🚗", layout="wide")

# Stile personalizzato con colori e font coerenti con il branding dell'utente
st.markdown(
    '''
    <style>
        body {
            font-family: 'Arial', sans-serif;
            background-color: #0D1532;
            color: white;
        }
        .title {
            text-align: center;
            font-size: 36px;
            font-weight: bold;
            color: #FFD700;
        }
        .stButton>button {
            background-color: #FFD700;
            color: #0D1532;
            font-size: 18px;
            font-weight: bold;
            border-radius: 8px;
        }
        .stMetric {
            font-size: 20px;
            font-weight: bold;
        }
        .sidebar .sidebar-content {
            background-color: #192A56;
            color: white;
        }
    </style>
    ''',
    unsafe_allow_html=True
)

# Titolo principale
st.markdown("<h1 class='title'>Confronto Auto Elettrica vs Termica 🚗⚡</h1>", unsafe_allow_html=True)

# Creazione di due colonne per migliorare l'organizzazione della UI
col1, col2 = st.columns(2)

with col1:
    st.subheader("🔧 Inserisci i dati del veicolo termico")
    modello_termico = st.text_input("Modello veicolo termico", value="")
    prezzo_termico = st.number_input("Prezzo d'acquisto (€) - Termico", value=25000, step=1000, format="%d")
    consumo_termico = st.number_input("Consumo carburante (L/100km)", value=6, step=1, format="%d")
    emissioni_termico = st.number_input("Emissioni CO2/km (g/km) - Termico", value=120, step=5, format="%d")

with col2:
    st.subheader("🔋 Inserisci i dati del veicolo elettrico")
    modello_elettrico = st.text_input("Modello veicolo elettrico", value="")
    prezzo_elettrico = st.number_input("Prezzo d'acquisto (€) - Elettrico", value=35000, step=1000, format="%d")
    consumo_elettrico = st.number_input("Consumo energia (kWh/100km)", value=15, step=1, format="%d")
    emissioni_elettrico = st.number_input("Emissioni CO2/km (g/km) - Elettrico", value=0, step=5, format="%d")

# Sezione costi energia e carburante
st.sidebar.header("⛽ Prezzi Energia e Carburante")
prezzo_benzina = st.sidebar.number_input("Prezzo benzina (€/L)", value=1.90, step=0.01, format="%.2f")
prezzo_energia = st.sidebar.number_input("Prezzo energia elettrica (€/kWh)", value=0.25, step=0.01, format="%.2f")

# Dati di utilizzo
st.sidebar.header("🚗 Dati di utilizzo")
km_annui = st.sidebar.number_input("Chilometraggio annuo (km)", value=15000, step=500, format="%d")
anni_possesso = st.sidebar.number_input("Durata del possesso (anni)", value=5, step=1, format="%d")

# Emissioni CO2 per la costruzione dell'auto
emissioni_produzione_termico = 7000  # kg di CO2 per veicolo termico
emissioni_produzione_elettrico = 12000  # kg di CO2 per veicolo elettrico (batterie incluse)

# Calcoli dei costi totali
costo_totale_termica = (
    prezzo_termico + ((km_annui / 100) * consumo_termico * prezzo_benzina * anni_possesso)
)

costo_totale_elettrica = (
    prezzo_elettrico + ((km_annui / 100) * consumo_elettrico * prezzo_energia * anni_possesso)
)

# Calcolo delle emissioni totali di CO2
emissioni_totali_termica = (
    (emissioni_termico * km_annui * anni_possesso / 1000) + emissioni_produzione_termico
)
emissioni_totali_elettrica = (
    (emissioni_elettrico * km_annui * anni_possesso / 1000) + emissioni_produzione_elettrico
)

# Visualizzazione dei risultati
st.subheader("📊 Risultati del confronto")

col1, col2 = st.columns(2)
with col1:
    st.metric(f"💰 Costo totale {modello_termico if modello_termico else 'Auto Termica'}", f"€{int(costo_totale_termica):,}")
    st.metric(f"🌍 Emissioni totali CO2 {modello_termico if modello_termico else 'Auto Termica'}", f"{int(emissioni_totali_termica):,} kg")

with col2:
    st.metric(f"💰 Costo totale {modello_elettrico if modello_elettrico else 'Auto Elettrica'}", f"€{int(costo_totale_elettrica):,}")
    st.metric(f"🌍 Emissioni totali CO2 {modello_elettrico if modello_elettrico else 'Auto Elettrica'}", f"{int(emissioni_totali_elettrica):,} kg")

if costo_totale_elettrica < costo_totale_termica:
    st.success(f"✅ L'auto elettrica ({modello_elettrico if modello_elettrico else 'Elettrica'}) è più conveniente!")
else:
    st.warning(f"🔥 L'auto termica ({modello_termico if modello_termico else 'Termica'}) è più conveniente!")

st.markdown("🔍 **Confronta i costi e le emissioni per scegliere la soluzione più efficiente e sostenibile!**")
