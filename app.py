import streamlit as st
import pandas as pd
import os
st.title("Analyse de la performance Etudiante")
# 1.  COLLECTE DES DONNEES
with st.form("form_etudiante"):
    nom = st.text_input("Nom de l'etudiant")
    etude = st.number_input("Heures d'etude par jour, min_value=0")
    sommeil = st.number_input("Heures de sommeil par nuit", min_value=0)
    moyenne = st.number_input("Moyenne academique (0-20)", min_value=0.0,max_value=20.0)
    stress = st.select_slider("Niveau de stress", options=["Faible", "Eleve"])
    soumettre =st.form_submit_button("Enregistrer les donnees")
# 2. STOCKAGE DES DONNEES
if soumettre:
    infos = pd.DataFrame([[nom, etude,
sommeil, moyenne, stress]])
    if not os.path.isfile("donnees_tp.csv"):            
        infos.to_csv("donnees_tp.csv",
index=False)
    else:
        infos.to_csv("donnees_tp.csv",
mode='a', header=False, index=False)
    st.success("Donnees enregistrees !")        
# 3. AFFICHAGE DES DONNEES (pour verifier)
if os.path.exists("donnees_tp.csv"):
    st.write("### Liste des etudiants enregistres")
    df = pd.read_csv("donnees_tp.csv")
    st.dataframe(df)            
# 4. ANALYSE DESCRIPTIVE
    st.write("### Statisques et Graphiques")
    col1, col2 = st.columns(2)
    col1.metric("Moyenne generale",round(df["Moyenne"].mean(),))
    col2.metric("Heures d'etude (Mediane)", df["Etude"].median())
    st.scatter_chart(data=df, x="Etude", y="Moyenne")
# 5. PREDICTION (IA / Machine Learning)
st.divider()
st.header("Prediction de Performance")
from sklearn.linear_model import LinearRegression
if os.path.exists("donnees_tp.csv") and len(df) > 1:
    x = df[["Etude"]].values
    y = df["Moyenne"].values
    modele = LinearRegression().fit(x, y)

    heures = st.slider("Simuler vos heures d'etude", 0, 15, 5)
    pred = modele.predict([[heures]])
    st.info(f"Prediction de ta moyenne : {round(pred[0], 2)}/20")
else:
    st.warning("Ajoute au moins 2 etudiants pour activer l'IA.")
