import streamlit as st
import pandas as pd
import plost 
import plotly.express as px
from PIL import Image


st.set_page_config(layout="wide")

#LIEN AVEC MON CSS
with open('style.css') as f:
    st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)

#LES TITRES
titre_2022 = pd.read_csv('titre2022.csv')
titre_2023 = pd.read_csv('titre2023.csv')
titre_2024 = pd.read_csv('titre2024.csv')
titre_2025 = pd.read_csv('titre2025.csv')

#LES AUTEURS
auteur_2022 = pd.read_csv('auteur2022.csv')
auteur_2023 = pd.read_csv('auteur2023.csv')
auteur_2024 = pd.read_csv('auteur2024.csv')
auteur_2025 = pd.read_csv('auteur2025.csv')

#LES PRIX
prix_2022 = pd.read_csv('prix2022.csv')
prix_2023 = pd.read_csv('prix2023.csv')
prix_2024 = pd.read_csv('prix2024.csv')
prix_2025 = pd.read_csv('prix2025.csv')

#LES FORMATS
format_2022 = pd.read_csv('format2022.csv')
format_2023 = pd.read_csv('format2023.csv')
format_2024 = pd.read_csv('format2024.csv')
format_2025 = pd.read_csv('format2025.csv')

#2022
df_2022 = pd.concat([auteur_2022, titre_2022, prix_2022, format_2022], axis=1)
df_2022['Année']=2022

#2023
df_2023 = pd.concat([auteur_2023, titre_2023, prix_2023,format_2023], axis=1)
df_2023['Année']=2023

#2024
df_2024 = pd.concat([auteur_2024, titre_2024, prix_2024, format_2024], axis=1)
df_2024['Année']=2024

#2025
df_2025 = pd.concat([auteur_2025, titre_2025, prix_2025, format_2025], axis=1)
df_2025['Année']=2025

#TOUTES LES ANNÉES
df_final = pd.concat([df_2022, df_2023, df_2024, df_2025], axis=0, ignore_index=True)


#SESSION STATE
if "auteur" not in st.session_state:
    st.session_state.auteur = None

if "format" not in st.session_state:
    st.session_state.format = None

if "titre" not in st.session_state:
    st.session_state.titre = None

if "annee" not in st.session_state:
    st.session_state.annee = sorted(df_final["Année"].unique(), reverse=True)

if "prix" not in st.session_state:
    st.session_state.prix = (
        float(df_final["Prix"].min()),
        float(df_final["Prix"].max())
    )

#LES FILRES
st.sidebar.header('Filtres')
st.sidebar.button("Réinitialiser", on_click=lambda:(
    st.session_state.update({
        "auteur":None,
        "format":None,
        "titre":None,
        "annee": sorted(df_final["Année"].unique(), reverse=True),
        "prix": (
            float(df_final["Prix"].min()),
            float(df_final["Prix"].max())
        )
    })
))
liste_auteur = sorted(df_final['Auteur'].unique().tolist())

#PAR AUTEUR
st.sidebar.markdown("---")
auteur_choisi = st.sidebar.selectbox(
    "Auteurs :",
    sorted(df_final["Auteur"].unique()),
    index=None,
    placeholder="Choisissez un auteur",
    key="auteur"#le contenue de cette clé serait éccrasé par le session state
)

#PAR FORMAT
st.sidebar.markdown("---")
liste_format= sorted(df_final['Format'].unique().tolist())
format_choisi = st.sidebar.selectbox(
    "Formats :",
    sorted(df_final["Format"].unique()),
    index=None,
    placeholder="Choisissez un format",
    key="format"
)

#PAR TITRE
st.sidebar.markdown("---")
liste_titre = sorted(df_final['Titre'].unique().tolist())
titre_choisi = st.sidebar.selectbox(
    "Titres :",
    sorted(df_final["Titre"].unique()),
    index=None,
    placeholder="Choisissez un titre",
    key="titre"
)

st.sidebar.markdown("---") 
st.sidebar.write("**Choisir l'année :**")

#PAR ANNÉE
liste_annees = sorted(df_final['Année'].unique().tolist(), reverse=True)
annee_choisie = st.sidebar.segmented_control(
    "Année",
    options=sorted(df_final["Année"].unique(), reverse=True),
    selection_mode="multi",
    key="annee"
)

st.sidebar.markdown("---")
prix_min = float(df_final["Prix"].min())
prix_max = float(df_final["Prix"].max())

prix_choisi = st.sidebar.slider(
    "Plage de prix (€)",
    min_value=float(df_final["Prix"].min()),
    max_value=float(df_final["Prix"].max()),
    key="prix"
)
df_affiche = df_final.copy()

#APPLICATION DES FILTRES 
if auteur_choisi:
    df_affiche = df_affiche[df_affiche["Auteur"]==auteur_choisi]

if format_choisi:
    df_affiche = df_affiche[df_affiche["Format"]==format_choisi]
    
if titre_choisi:
    df_affiche = df_affiche[df_affiche["Titre"]==titre_choisi]

if annee_choisie:
    df_affiche = df_affiche[df_affiche["Année"].isin(annee_choisie)]

df_affiche = df_affiche[
    (df_affiche["Prix"] >= prix_choisi[0]) &
    (df_affiche["Prix"] <= prix_choisi[1])
]

st.write("Lina Honoré")
st.header("**Amazon Top Ventes Livres Dashboard Interactif (2022-2025)**")
st.markdown("---")

#MISE EN PLACE DE 3 COLONNES 
a1, a2, a3 = st.columns(3)

if not df_affiche.empty:
    # AUTEUR FAVORI
    df_auteur_stats = df_affiche.groupby('Auteur').size().reset_index(name='Total')
    if not df_auteur_stats.empty:
        df_auteur_top_1 = df_auteur_stats.sort_values("Total",ascending=False).iloc[0]
        nom_auteur = df_auteur_top_1['Auteur']
        nombre_livres_auteur = df_auteur_top_1['Total']
   
    else:
        nom_auteur = "Aucun" #si les filtres ne correspondent pas on met 'Aucun' résultat
        nombre_livres_auteur = 0
    a1.metric("Auteur le plus populaire", nom_auteur, delta=f"{nombre_livres_auteur} livres dans le top")

    # LIVRE LE PLUS POPULAIRE
    
   # LIVRE LE PLUS POPULAIRE avec HTML
    df_titre_stats = df_affiche.groupby('Titre').size().reset_index(name='Total')
    if not df_titre_stats.empty:
        titre_top = df_titre_stats.sort_values(by='Total', ascending=False).iloc[0]

        with a2:
            st.markdown("**Livre le plus populaire**")
            st.markdown(
                f"""
                <div style="
                    font-size: 1.1rem;
                    font-weight: 600;
                    line-height: 1.3;
                    margin-top: 0.2rem;
                ">
                    {titre_top["Titre"]}
                </div>	
                <div style="
                    font-size: 0.9rem;
                    opacity: 0.7;
                ">
                    {titre_top["Total"]} fois dans le top
                </div>
                """,
                unsafe_allow_html=True
            )
    else:
        with a2:
            st.markdown("**Livre le plus populaire**")
            st.info("Aucun livre à afficher")

    # PRIX MOYEN
    prix_moyen = df_affiche["Prix"].mean()
    a3.metric("Prix moyen d'un livre",f"{round(prix_moyen,2)} €")

else:
    a1.metric("Auteur le plus populaire", "Aucun", delta="0 livres")
    a2.metric("Livre le plus populaire", "Aucun", delta="0 livres")
    a3.metric("Prix moyen d'un livre", "0 €")
    df_format_stats = pd.DataFrame(columns=["Format", "Total"])

b1, b2 = st.columns(2)

# FORMAT 
df_format_stats = df_affiche.groupby("Format").size().reset_index(name="Quantité")
if not df_format_stats.empty:
    fig = px.pie(
        df_format_stats, 
        values="Quantité", 
        names="Format", 
        hole=0.5,
        color_discrete_sequence=['#F8EDF5', '#EBCCE4', '#DEABD2','#D38DC3','#C468AF'] 
    )
    #fig.update_layout(showlegend=False, margin=dict(t=0, b=0, l=0, r=0), height=200)
    fig.update_traces(textinfo='percent+label')
    with b1:
        st.markdown('**Les formats**')
        st.plotly_chart(fig, use_container_width=True)
else:
    with b1:
        st.markdown('**Les formats**')
        st.info("Aucun format à afficher")

# TOP 15 AUTEURS (bar chart)
df_auteur_stats = df_affiche.groupby('Auteur').size().reset_index(name='Total')
df_auteur_top_15 = df_auteur_stats.sort_values(by='Total', ascending=False).head(15)
if not df_auteur_top_15.empty:
    with b2:
        st.markdown('**Top 15 Auteurs**')
        plost.bar_chart(
            data=df_auteur_top_15,
            bar='Total',
            value='Auteur',
            color='#D289C1',
            width='stretch',
            direction='horizontal'
        )
else:
    with b2:
        st.markdown('**Top 15 Auteurs**')
        st.info("Aucun auteur à afficher")


st.dataframe(df_affiche, use_container_width=True)
img=Image.open("images/logo.png")
st.image(img, width=100)
