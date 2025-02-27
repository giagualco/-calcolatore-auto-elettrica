import streamlit as st
import requests
import pandas as pd

st.title("Confronto Auto Elettrica vs Termica 🚗⚡")

# Dizionario dei veicoli con i loro dati
veicoli = {
    "Auto Termiche": {
        "Fiat Panda 1.2": {"prezzo": 15000, "consumo": 5.7},
        "Volkswagen Golf 1.5": {"prezzo": 25000, "consumo": 6.0},
        "Ford Focus 1.0": {"prezzo": 22000, "consumo": 5.5},
        "Porsche Macan": {"prezzo": 70000, "consumo": 10.5},
    },
    "Auto Elettriche": {
        "Renault Zoe": {"prezzo": 30000, "consumo": 17.2},
        "Nissan Leaf": {"prezzo": 35000, "consumo": 15.0},
        "Tesla Model 3": {"prezzo": 50000, "consumo": 14.0},
        "BMW i4": {"prezzo": 60000, "consumo": 16.5},
    },
}

# Funzione per ottenere il prezzo medio della benzina
def get_prezzo_benzina():
    try:
        url = "https://www.mimit.gov.it/it/prezzo-medio-carburanti/regioni"
        response = requests.get(url)
        prezzo_benzina = 1.75  # Prezzo di esempio, da aggiornare con parsing effettivo
        return prezzo_benzina
    except:
        return 1.75  # Valore di fallback

# Funzione per ottenere il prezzo medio dell'energia elettrica
def get_prezzo_energia():
    try:
        url = "https://www.arera.it/area-operatori/prezzi-e-tariffe"
        response = requests.get(url)
        prezzo_energia = 0.22  # Prezzo di esempio, da aggiornare con parsing effettivo
        return prezzo_energia
    except:
        return 0.22  # Valore di fallback

# Ottenere i prezzi aggiornati
prezzo_benzina = get_prezzo_benzina()
prezzo_energia = get_prezzo_energia()

st.sidebar.header("Selezione del veicolo termico")
modello_termico = st.sidebar.selectbox("Seleziona il modello termico", options=list(veicoli["Auto Termiche"].keys()))

st.sidebar.header("Selezione del veicolo elettrico")
modello_elettrico = st.sidebar.selectbox("Seleziona il modello elettrico", options=list(veicoli["Auto Elettriche"].keys()))

# Recupero dei dati del veicolo selezionato
dati_termico = veicoli["Auto Termiche"][modello_termico]
dati_elettrico = veicoli["Auto Elettriche"][modello_elettrico]

prezzo_termico = dati_termico["prezzo"]
consumo_termico = dati_termico["consumo"]

prezzo_elettrico = dati_elettrico["prezzo"]
consumo_elettrico = dati_elettrico["consumo"]

st.sidebar.write(f"**{modello_termico}** - Prezzo: €{prezzo_termico}, Consumo: {consumo_termico} L/100km")
st.sidebar.write(f"**{modello_elettrico}** - Prezzo: €{prezzo_elettrico}, Consumo: {consumo_elettrico} kWh/100km")

# Dati generali
km_annui = st.number_input("Chilometraggio annuo (km)", value=15000)
anni_possesso = st.number_input("Durata del possesso (anni)", value=5)

# Prezzi carburante ed energia modificabili dall'utente
st.sidebar.header("Prezzi Energia e Carburanti")
prezzo_benzina = st.sidebar.number_input("Prezzo benzina (€/L)", value=prezzo_benzina, format="%.2f")
prezzo_energia = st.sidebar.number_input("Prezzo energia elettrica (€/kWh)", value=prezzo_energia, format="%.2f")

st.write(f"**Prezzo medio benzina:** €{prezzo_benzina}/L (Modificabile)")
st.write(f"**Prezzo medio energia elettrica:** €{prezzo_energia}/kWh (Modificabile)")

# Calcoli dei costi totali
costo_totale_termica = (
    prezzo_termico
    + ((km_annui / 100) * consumo_termico * prezzo_benzina * anni_possesso)
)

costo_totale_elettrica = (
    prezzo_elettrico
    + ((km_annui / 100) * consumo_elettrico * prezzo_energia * anni_possesso)
)

# Visualizzazione dei risultati
st.subheader("Risultati del confronto")
st.write(f"**Costo totale {modello_termico} (termico):** €{costo_totale_termica:,.2f}")
st.write(f"**Costo totale {modello_elettrico} (elettrico):** €{costo_totale_elettrica:,.2f}")

if costo_totale_elettrica < costo_totale_termica:
    st.success(f"L'auto elettrica ({modello_elettrico}) è più conveniente! ✅")
else:
    st.warning(f"L'auto termica ({modello_termico}) è più conveniente! 🔥")

# Grafico comparativo
anni = list(range(1, anni_possesso + 1))
costi_termica = [
    prezzo_termico + ((km_annui / 100) * consumo_termico * prezzo_benzina * i)
    for i in anni
]
costi_elettrica = [
    prezzo_elettrico + ((km_annui / 100) * consumo_elettrico * prezzo_energia * i)
    for i in anni
]

df = pd.DataFrame({"Anno": anni, f"{modello_termico} (€)": costi_termica, f"{modello_elettrico} (€)": costi_elettrica})
st.line_chart(df.set_index("Anno"))
