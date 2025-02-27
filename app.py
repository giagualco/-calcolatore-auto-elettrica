import streamlit as st
import pandas as pd

st.title("Confronto Auto Elettrica vs Termica 🚗⚡")

st.sidebar.header("Inserisci i dati del veicolo termico")
modello_termico = st.sidebar.text_input("Modello veicolo termico", value="")
prezzo_termico = st.sidebar.number_input("Prezzo d'acquisto (€) - Termico", value=25000)
consumo_termico = st.sidebar.number_input("Consumo carburante (L/100km)", value=6.5)

st.sidebar.header("Inserisci i dati del veicolo elettrico")
modello_elettrico = st.sidebar.text_input("Modello veicolo elettrico", value="")
prezzo_elettrico = st.sidebar.number_input("Prezzo d'acquisto (€) - Elettrico", value=35000)
consumo_elettrico = st.sidebar.number_input("Consumo energia (kWh/100km)", value=15.0)

st.sidebar.header("Inserisci i prezzi dell'energia e del carburante")
prezzo_benzina = st.sidebar.number_input("Prezzo benzina (€/L)", value=1.9, format="%.2f")
prezzo_energia = st.sidebar.number_input("Prezzo energia elettrica (€/kWh)", value=0.25, format="%.2f")

st.sidebar.header("Dati di utilizzo")
km_annui = st.sidebar.number_input("Chilometraggio annuo (km)", value=15000)
anni_possesso = st.sidebar.number_input("Durata del possesso (anni)", value=5)

st.write(f"**Prezzo medio benzina:** €{prezzo_benzina}/L (Modificabile)")
st.write(f"**Prezzo medio energia elettrica:** €{prezzo_energia}/kWh (Modificabile)")

# Calcoli dei costi totali
costo_totale_termica = (
    prezzo_termico + ((km_annui / 100) * consumo_termico * prezzo_benzina * anni_possesso)
)

costo_totale_elettrica = (
    prezzo_elettrico + ((km_annui / 100) * consumo_elettrico * prezzo_energia * anni_possesso)
)

# Visualizzazione dei risultati
st.subheader("Risultati del confronto")
st.write(f"**Costo totale {modello_termico if modello_termico else 'Auto Termica'}:** €{costo_totale_termica:,.2f}")
st.write(f"**Costo totale {modello_elettrico if modello_elettrico else 'Auto Elettrica'}:** €{costo_totale_elettrica:,.2f}")

if costo_totale_elettrica < costo_totale_termica:
    st.success(f"L'auto elettrica ({modello_elettrico if modello_elettrico else 'Elettrica'}) è più conveniente! ✅")
else:
    st.warning(f"L'auto termica ({modello_termico if modello_termico else 'Termica'}) è più conveniente! 🔥")

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

df = pd.DataFrame({"Anno": anni, f"{modello_termico if modello_termico else 'Auto Termica'} (€)": costi_termica, f"{modello_elettrico if modello_elettrico else 'Auto Elettrica'} (€)": costi_elettrica})
st.line_chart(df.set_index("Anno"))
