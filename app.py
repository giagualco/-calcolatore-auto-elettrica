import streamlit as st
import pandas as pd

# Configurazione della pagina
st.set_page_config(page_title="Confronto Auto Elettrica vs Termica", page_icon="🚗", layout="wide")

# Titolo principale
st.markdown("<h1 style='text-align: center; color: #007BFF;'>Confronto Auto Elettrica vs Termica 🚗⚡</h1>", unsafe_allow_html=True)

# Creazione di due colonne per migliorare l'organizzazione della UI
col1, col2 = st.columns(2)

with col1:
    st.subheader("🔧 Inserisci i dati del veicolo termico")
    modello_termico = st.text_input("Modello veicolo termico", value="")
    prezzo_termico = st.number_input("Prezzo d'acquisto (€) - Termico", value=25000)
    consumo_termico = st.number_input("Consumo carburante (L/100km)", value=6.5)
    emissioni_termico = st.number_input("Emissioni CO2/km (g/km) - Termico", value=120)

with col2:
    st.subheader("🔋 Inserisci i dati del veicolo elettrico")
    modello_elettrico = st.text_input("Modello veicolo elettrico", value="")
    prezzo_elettrico = st.number_input("Prezzo d'acquisto (€) - Elettrico", value=35000)
    consumo_elettrico = st.number_input("Consumo energia (kWh/100km)", value=15.0)
    emissioni_elettrico = st.number_input("Emissioni CO2/km (g/km) - Elettrico", value=0)

# Sezione costi energia e carburante
st.sidebar.header("⛽ Prezzi Energia e Carburante")
prezzo_benzina = st.sidebar.number_input("Prezzo benzina (€/L)", value=1.9, format="%.2f")
prezzo_energia = st.sidebar.number_input("Prezzo energia elettrica (€/kWh)", value=0.25, format="%.2f")

# Dati di utilizzo
st.sidebar.header("🚗 Dati di utilizzo")
km_annui = st.sidebar.number_input("Chilometraggio annuo (km)", value=15000)
anni_possesso = st.sidebar.number_input("Durata del possesso (anni)", value=5)

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
    st.metric(f"💰 Costo totale {modello_termico if modello_termico else 'Auto Termica'}", f"€{costo_totale_termica:,.2f}")
    st.metric(f"🌍 Emissioni totali CO2 {modello_termico if modello_termico else 'Auto Termica'}", f"{emissioni_totali_termica:,.2f} kg")

with col2:
    st.metric(f"💰 Costo totale {modello_elettrico if modello_elettrico else 'Auto Elettrica'}", f"€{costo_totale_elettrica:,.2f}")
    st.metric(f"🌍 Emissioni totali CO2 {modello_elettrico if modello_elettrico else 'Auto Elettrica'}", f"{emissioni_totali_elettrica:,.2f} kg")

if costo_totale_elettrica < costo_totale_termica:
    st.success(f"✅ L'auto elettrica ({modello_elettrico if modello_elettrico else 'Elettrica'}) è più conveniente!")
else:
    st.warning(f"🔥 L'auto termica ({modello_termico if modello_termico else 'Termica'}) è più conveniente!")

# Grafico comparativo costi ed emissioni
anni = list(range(1, anni_possesso + 1))
costi_termica = [
    prezzo_termico + ((km_annui / 100) * consumo_termico * prezzo_benzina * i)
    for i in anni
]
costi_elettrica = [
    prezzo_elettrico + ((km_annui / 100) * consumo_elettrico * prezzo_energia * i)
    for i in anni
]
emissioni_termica_anni = [
    (emissioni_termico * km_annui * i / 1000) + emissioni_produzione_termico for i in anni
]
emissioni_elettrica_anni = [
    (emissioni_elettrico * km_annui * i / 1000) + emissioni_produzione_elettrico for i in anni
]

df_costi = pd.DataFrame({
    "Anno": anni,
    f"{modello_termico if modello_termico else 'Auto Termica'} (€)": costi_termica,
    f"{modello_elettrico if modello_elettrico else 'Auto Elettrica'} (€)": costi_elettrica,
})
df_emissioni = pd.DataFrame({
    "Anno": anni,
    f"{modello_termico if modello_termico else 'Auto Termica'} (kg CO2)": emissioni_termica_anni,
    f"{modello_elettrico if modello_elettrico else 'Auto Elettrica'} (kg CO2)": emissioni_elettrica_anni,
})

st.subheader("📈 Andamento dei costi nel tempo")
st.line_chart(df_costi.set_index("Anno"))

st.subheader("📉 Andamento delle emissioni di CO2 nel tempo")
st.line_chart(df_emissioni.set_index("Anno"))

st.markdown("🔍 **Confronta i costi e le emissioni per scegliere la soluzione più efficiente e sostenibile!**")
