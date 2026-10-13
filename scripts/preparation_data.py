import numpy as np
import pandas as pd

############# But de ce script #############
# récupèrer les données avec l'API
# préparer ces données avant leur utilisation

# On pourra utiliser ce dataframe pour tester les fonctions
df_exemple = pd.DataFrame({
    "nom": ["Alice", "Bob", "Chloé"],
    "age": [25, 30, 28],
    "ville": ["Paris", "Lyon", "Nantes"],
})



############# Récupération données par l'ESS API #############

# Le dico qui, à une année, renvoie le DOI des données correspondants
dico_doi = {2023: "10.21338/ess11e04_2",
            2020: "10.21338/ess10e03_3",
            2018: "10.21338/ess9e03_3",
            2016: "10.21338/ess8e02_3",
            2014: "10.21338/ess7e02_3"}


# Cette fonction récupère les données de l'ESS
def recuperer_donnees(annee):
    host = "https://api.ess.sikt.no"
    user_id = input("Saisis ESS User ID : ")
    doi = dico_doi[annee]
    url = f"{host}/v1/data/dataFile/{doi}?userId={user_id}&recodeMissingValues"
    df = pd.read_parquet(url)
    return df



############# Préparations des données #############

def select_colonne(df, liste_colonnes):
    # liste_colonnes sera de la forme ["nom_colonne1_a_garder", "nom_colonne2_a_garder"]
    return df


def suppr_colonne(df, liste_colonnes):
    # liste_colonnes sera de la forme ["nom_colonne1_a_supprimer", "nom_colonne2_a_supprimer"]
    return df


def renommer_colonne(df, liste_ancien_nom, liste_nouveau_nom):
    # si liste_old_nom = ["polyintr", "idno"]
    # et liste_new_nom = ["interet_politique", "identifiant"]
    # alors cette fonction renvoie un dataframe où la colonne 
    # "polyintr" a été renommé "interet_politique" etc.
    return df


def normaliser_df(df):
    # Faut juste attendre qu'on ait nos variables pour pouvoir écrire cette fonction
    return df
