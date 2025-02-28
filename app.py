import streamlit as st
import pandas as pd
import json

# Configurazione della pagina
st.set_page_config(page_title="Confronto Auto Elettrica vs Termica", page_icon="🚗", layout="wide")

# Titolo principale
st.title("Confronto Auto Elettrica vs Termica")

# Sezione per l'inserimento dei dati del veicolo termico
st.header("Dati del veicolo termico")
modello_termico = st.text_input("Modello veicolo termico")
prezzo_termico = st.number_input("Prezzo d'acquisto (€)", min_value=0)
consumo_termico_medio = st.number_input("Consumo medio (L/100km)", min_value=0.0, format="%.2f")

# Sezione per l'inserimento dei dati del veicolo elettrico
st.header("Dati del veicolo elettrico")
modello_elettrico = st.text_input("Modello veicolo elettrico")
prezzo_elettrico = st.number_input("Prezzo d'acquisto (€)", min_value=0)
consumo_elettrico_medio = st.number_input("Consumo medio (kWh/100km)", min_value=0.0, format="%.2f")

# Sezione per i costi del carburante e dell'energia
st.header("Costi del carburante e dell'energia")
prezzo_benzina = st.number_input("Prezzo benzina (€/L)", min_value=0.0, format="%.2f")
prezzo_energia = st.number_input("Prezzo energia elettrica (€/kWh)", min_value=0.0, format="%.2f")

# Sezione per i dati di utilizzo
st.header("Dati di utilizzo")
km_annui = st.number_input("Chilometri annui percorsi", min_value=0)

# Distribuzione percentuale del tipo di percorso
st.header("Distribuzione del percorso (%)")
perc_citta = st.slider("Città", min_value=0, max_value=100, value=30)
perc_extraurbano = st.slider("Extraurbano", min_value=0, max_value=100, value=50)
perc_autostrada = 100 - perc_citta - perc_extraurbano
st.write(f"Autostrada: {perc_autostrada}%")

# Coefficienti di consumo relativi al tipo di percorso
coeff_termico = {
    "citta": 1.2,        # Consumo aumenta del 20% in città
    "extraurbano": 0.9,  # Consumo diminuisce del 10% in extraurbano
    "autostrada": 1.1    # Consumo aumenta del 10% in autostrada
}

coeff_elettrico = {
    "citta": 1.1,        # Consumo aumenta del 10% in città
    "extraurbano": 0.95, # Consumo diminuisce del 5% in extraurbano
    "autostrada": 1.2    # Consumo aumenta del 20% in autostrada
}

# Calcolo del consumo ponderato per il veicolo termico
consumo_termico_ponderato = (
    consumo_termico_medio * (
        (perc_citta / 100) * coeff_termico["citta"] +
        (perc_extraurbano / 100) * coeff_termico["extraurbano"] +
        (perc_autostrada / 100) * coeff_termico["autostrada"]
    )
)

# Calcolo del consumo ponderato per il veicolo elettrico
consumo_elettrico_ponderato = (
    consumo_elettrico_medio * (
        (perc_citta / 100) * coeff_elettrico["citta"] +
        (perc_extraurbano / 100) * coeff_elettrico["extraurbano"] +
        (perc_autostrada / 100) * coeff_elettrico["autostrada"]
    )
)

# Calcolo dei costi annuali
costo_annuo_termico = (km_annui / 100) * consumo_termico_ponderato * prezzo_benzina
costo_annuo_elettrico = (km_annui / 100) * consumo_elettrico_ponderato * prezzo_energia

# Visualizzazione dei risultati
st.header("Risultati")
st.write(f"**Consumo medio ponderato veicolo termico:** {consumo_termico_ponderato:.2f} L/100km")
st.write(f"**Consumo medio ponderato veicolo elettrico:** {consumo_elettrico_ponderato:.2f} kWh/100km")
st.write(f"**Costo annuale veicolo termico:** €{costo_annuo_termico:.2f}")
st.write(f"**Costo annuale veicolo elettrico:** €{costo_annuo_elettrico:.2f}")
