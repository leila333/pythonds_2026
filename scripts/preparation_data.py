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

def select_colonne(df: pd.DataFrame, liste_colonnes: list[str]) -> pd.DataFrame:
    """
    Sélectionne un sous-ensemble de colonnes dans un DataFrame pandas.

    Paramètre :
    ----------
    df : pd.DataFrame (le DataFrame source)
    liste_colonnes : list of str (liste des noms des colonnes à conserver)

    Retourne :
    -------
    pd.DataFrame (nouveau DataFrame ne contenant que les colonnes sélectionnées)
    """
    return df[liste_colonnes].copy()



def suppr_colonne(df: pd.DataFrame, liste_colonnes: list[str]) -> pd.DataFrame:
    """
    Supprime une liste de colonnes d'un DataFrame pandas.

    Paramètre :
    ----------
    df : pd.DataFrame (le DataFrame source)
    liste_colonnes : list of str (liste des noms des colonnes à supprimer)

    Retourne :
    -------
    pd.DataFrame (nouveau DataFrame sans les colonnes spécifiées)
    """
    return df.drop(columns=liste_colonnes)


def renommer_colonne(df: pd.DataFrame, liste_ancien_nom: list[str], liste_nouveau_nom: list[str]) -> pd.DataFrame:
    """
    Renomme des colonnes d'un DataFrame à partir de deux listes ordonnées.

    Paramètre :
    ----------
    df : pd.DataFrame (le DataFrame source)
    liste_ancien_nom : list of str (liste des anciens noms de colonnes)
    liste_nouveau_nom : list of str (liste des nouveaux noms correspondants)

    Retourne :
    -------
    pd.DataFrame (nouveau DataFrame avec les colonnes renommées)
    """
    if len(liste_ancien_nom) != len(liste_nouveau_nom):
        raise ValueError(
            "Les deux listes doivent avoir exactement la même longueur."
        )

    mapping = dict(zip(liste_ancien_nom, liste_nouveau_nom))
    return df.rename(columns=mapping)

def normaliser_df(df):
    # Faut juste attendre qu'on ait nos variables pour pouvoir écrire cette fonction
    return df



