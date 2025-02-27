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
    },
    "Auto Elettriche": {
        "Renault Zoe": {"prezzo": 30000, "consumo": 17.2},
        "Nissan Leaf": {"prezzo": 35000, "consumo": 15.0},
        "Tesla Model 3": {"prezzo": 50000, "consumo": 14.0},
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

st.sidebar.header("Selezione del veicolo")
tipo_veicolo = st.sidebar.selectbox("Seleziona il tipo di veicolo", options=["Auto Termiche", "Auto Elettriche"])
modello = st.sidebar.selectbox("Seleziona il modello", options=list(veicoli[tipo_veicolo].keys()))

# Recupero dei dati del veicolo selezionato
dati_veicolo = veicoli[tipo_veicolo][modello]
prezzo = dati_veicolo["prezzo"]
consumo = dati_veicolo["consumo"]

st.sidebar.write(f"**Prezzo d'acquisto:** €{prezzo}")
st.sidebar.write(f"**Consumo medio:** {consumo} {'L/100km' if tipo_veicolo == 'Auto Termiche' else 'kWh/100km'}")

# Dati generali
km_annui = st.number_input("Chilometraggio annuo (km)", value=15000)
anni_possesso = st.number_input("Durata del possesso (anni)", value=5)

st.write(f"**Prezzo medio benzina:** €{prezzo_benzina}/L")
st.write(f"**Prezzo medio energia elettrica:** €{prezzo_energia}/kWh")

# Calcoli dei costi totali
costo_totale_termica = (
    prezzo
    + ((km_annui / 100) * consumo * prezzo_benzina * anni_possesso)
)

costo_totale_elettrica = (
    prezzo
    + ((km_annui / 100) * consumo * prezzo_energia * anni_possesso)
)

# Visualizzazione dei risultati
st.subheader("Risultati del confronto")
st.write(f"**Costo totale auto termica:** €{costo_totale_termica:,.2f}")
st.write(f"**Costo totale auto elettrica:** €{costo_totale_elettrica:,.2f}")

if costo_totale_elettrica < costo_totale_termica:
    st.success("L'auto elettrica è più conveniente! ✅")
else:
    st.warning("L'auto termica è più conveniente! 🔥")

# Grafico comparativo
anni = list(range(1, anni_possesso + 1))
costi_termica = [
    prezzo + ((km_annui / 100) * consumo * prezzo_benzina * i)
    for i in anni
]
costi_elettrica = [
    prezzo + ((km_annui / 100) * consumo * prezzo_energia * i)
    for i in anni
]

df = pd.DataFrame({"Anno": anni, "Auto Termica (€)": costi_termica, "Auto Elettrica (€)": costi_elettrica})
st.line_chart(df.set_index("Anno"))
