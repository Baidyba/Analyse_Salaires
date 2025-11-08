# Application Streamlit :Analyse des Salaires

import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import streamlit as st

# Configuration de la page Streamlit
st.set_page_config(page_title="Analyse des Salaires", layout="wide")

# st.set_page_config: configure des paramètres globaux de l'app streamlit
# layout="wide": demande un affichage large(utilise toute la largeur de la page)

# Titre principal de l'application
st.title("Tableau de bord interactif - Analyse des salaires des employés")

# Téchargement du fichier
fichier = st.file_uploader("Importer un fichier CSV contenant les salaires", type=['csv'])

# st.file_uploader: widget qui permet à l'utilisateur d'uploader un fichier

if fichier is not None:
    # Lecture du CSV en DataFrame
    df = pd.read_csv(fichier)
    st.subheader("Aperçu des données importées")
    st.dataframe(df.head())  # affiche un tableau interactif dans l'app

    # Nettoyage basique des données
    df['Salaire'] = pd.to_numeric(df['Salaire'], errors='coerce')
    df = df.dropna(subset=['Salaire'])

    # Statistique descriptives
    st.subheader("Statistiques sur les salaires")
    st.write(df['Salaire'].describe())  # Affiche proprement

    # Widget : slider pour filter par seuil
    seuil = st.slider(
        "Sélectionner un seuil de salaire",
        int(df['Salaire'].min()),
        int(df['Salaire'].max()),
        int(df['Salaire'].median())
    )

    st.markdown(f" Employés gagnant plus de **{seuil:,}**")
    df_filtre = df[df['Salaire'] > seuil]
    st.dataframe(df_filtre)


    # Catégorisation (colonne calculée)
    def categorie_salaire(s):
        if s < 200000:
            return "Faible revenu"
        elif s < 400000:
            return "Revenu moyen"
        else:
            return "Haut revenu"


    df['Catégorie'] = df['Salaire'].apply(categorie_salaire)

    st.subheader("Répartion des catégories de salaire")
    st.bar_chart(df['Catégorie'].value_counts())

    # Histogramme avec seaborn / matplotlibstream
    st.subheader("Distribution des salaires")
    fig, ax = plt.subplots()
    sns.histplot(df['Salaire'], kde=True, ax=ax, color="orange")
    st.pyplot(fig)

    # Moyenne par département
    st.subheader("Salaire moyen par département")
    salaire_par_dept = df.groupby("Département")["Salaire"].mean().sort_values(ascending=False)
    st.bar_chart(salaire_par_dept)

    # Bouton de téchargement
    st.download_button(
        "Télécharger la liste filtrée (CSV)",
        df_filtre.to_csv(index=False).encode('utf-8'),
        file_name='agents_filtres.csv',
        mime='text/csv'
    )
else:
    st.info(" Importer un fichier CSV pour commencer l'analyse.")
