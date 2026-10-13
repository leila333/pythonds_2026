import numpy as np
import pandas as pd

# Ce script contient les fonctions pour : 
#   récupèrer les données avec l'API
#   explorer et préparer ces données avant leur utilisation



############# Récupération données par l'ESS API #############

# Le dico qui à une année renvoie le DOI des données correspondants
dico_doi = {2023: "10.21338/ess11e04_2",
            2020: "10.21338/ess10e03_3",
            2018: "10.21338/ess9e03_3"}


def recuperer_donnees(annee):
    host = "https://api.ess.sikt.no"
    user_id = input("Saisis ESS User ID : ")
    doi = dico_doi[annee]
    url = f"{host}/v1/data/dataFile/{doi}?userId={user_id}&recodeMissingValues"
    df = pd.read_parquet(url)
    return df




############# Préparations des données #############

##### 1) Garder les colonnes utilisées





