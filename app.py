import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

st.title("Confronto Auto Elettrica vs Termica 🚗⚡")

# Input dell'utente
st.sidebar.header("Dati auto termica")
prezzo_termica = st.sidebar.number_input("Prezzo d'acquisto (€)", value=25000)
consumo_termica = st.sidebar.number_input("Consumo carburante (L/100km)", value=6.5)
costo_carburante = st.sidebar.number_input("Costo carburante (€/L)", value=1.9)
manutenzione_termica = st.sidebar.number_input("Manutenzione annua (€)", value=500)

st.sidebar.header("Dati auto elettrica")
prezzo_elettrica = st.sidebar.number_input("Prezzo d'acquisto (€)", value=35000)
consumo_elettrica = st.sidebar.number_input("Consumo energia (kWh/100km)", value=15)
costo_energia = st.sidebar.number_input("Costo energia (€/kWh)", value=0.25)
manutenzione_elettrica = st.sidebar.number_input("Manutenzione annua (€)", value=200)

# Dati generali
km_annui = st.number_input("Chilometraggio annuo (km)", value=15000)
anni_possesso = st.number_input("Durata del possesso (anni)", value=5)

# Calcoli dei costi totali
costo_totale_termica = (
    prezzo_termica
    + ((km_annui / 100) * consumo_termica * costo_carburante * anni_possesso)
    + (manutenzione_termica * anni_possesso)
)

costo_totale_elettrica = (
    prezzo_elettrica
    + ((km_annui / 100) * consumo_elettrica * costo_energia * anni_possesso)
    + (manutenzione_elettrica * anni_possesso)
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
    prezzo_termica + ((km_annui / 100) * consumo_termica * costo_carburante * i) + (manutenzione_termica * i)
    for i in anni
]
costi_elettrica = [
    prezzo_elettrica + ((km_annui / 100) * consumo_elettrica * costo_energia * i) + (manutenzione_elettrica * i)
    for i in anni
]

df = pd.DataFrame({"Anno": anni, "Auto Termica (€)": costi_termica, "Auto Elettrica (€)": costi_elettrica})
st.line_chart(df.set_index("Anno"))
