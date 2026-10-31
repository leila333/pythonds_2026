import numpy as np
import pandas as pd
import os


############# But de ce script #############
# 1) récupèrer les données avec l'API 
# 2) Fonctions utiles sur les dataframes
# 3) Préparer ces données avant leur utilisation




############# 1) Récupération données par l'ESS API ##########################

# Le dico qui, à une année, renvoie le DOI des données correspondants
dico_doi = {2023: "10.21338/ess11e04_2",
            2020: "10.21338/ess10e03_3",
            2018: "10.21338/ess9e03_3",
            2016: "10.21338/ess8e02_3",
            2014: "10.21338/ess7e02_3"}


# Cette fonction récupère les données de l'ESS (confère documentation de l'API)
def recuperer_donnees_API(annee):
    host = "https://api.ess.sikt.no"
    user_id = input("Saisis ESS User ID : ")
    doi = dico_doi[annee]
    url = f"{host}/v1/data/dataFile/{doi}?userId={user_id}&recodeMissingValues"
    df = pd.read_parquet(url)
    return df


# Cette fonction recupere les données avec le csv, au cas où l'API ne fonctionne plus
def recuperer_donnees():
    # On récupère les données
    if os.path.exists("data/ESS10e03_3.csv"):
        df = pd.read_csv("data/ESS10e03_3.csv")
    else:
        df = None
        print("Le fichier n'a pas été trouvé. Etes vous bien dans le dossier pythonds_2026 ?")
    
    # On remplace les valeurs de non réponse comme des valeurs manquantes
    

    return df




########################## 2) Fonction utiles ##########################

# On pourra utiliser ce dataframe pour tester les fonctions
df_exemple = pd.DataFrame({
    "nom": ["Alice", "Bob", "Chloé"],
    "age": [25, 30, 28],
    "ville": ["Paris", "Lyon", "Nantes"],
})


def select_colonne(df: pd.DataFrame, liste_colonnes: list[str]) -> pd.DataFrame:
    return df[liste_colonnes].copy()



def suppr_colonne(df: pd.DataFrame, liste_colonnes: list[str]) -> pd.DataFrame:
    return df.drop(columns=liste_colonnes)


def renommer_colonne(df: pd.DataFrame, liste_ancien_nom: list[str], liste_nouveau_nom: list[str]) -> pd.DataFrame:
    if len(liste_ancien_nom) != len(liste_nouveau_nom):
        raise ValueError(
            "Les deux listes doivent avoir exactement la même longueur."
        )

    mapping = dict(zip(liste_ancien_nom, liste_nouveau_nom))
    return df.rename(columns=mapping)



########################## 3) Préparations des données ##########################
# On utilise la documentation sur les variables : https://ess.sikt.no/en/datafile/242aaa39-3bbb-40f5-98bf-bfb1ce53d8ef

# 2. Valeurs manquantes

#Liste des colonnes potentiellement pertinentes pour l'étude sur les théories du complot (ESS Round 10)
colonnes_a_garder = [
    # --- 1) identifiants et pondérations méthodologiques ---
    "idno",       # Identifiant unique de l'individu
    "cntry",      # Pays de résidence (essentiel pour les comparaisons européennes)
    "anweight",   # Poids d'analyse (corrige les biais d'échantillonnage nationaux)
    "dweight",    # Poids de sondage (design weight)
    "pspwght",    # Poids post-stratification

    # --- 2) Ccoyances aux théories du complot & attitudes face à la science ---
    "secgrdec",   # Groupes secrets qui influencent/dirigent les décisions politiques
    "scidecpb",   # Scientifiques et figures politiques qui s'entendent en secret
    "gvconc19",   # Dissimulation par le gouvernement d'informations clés sur le Covid-19 et il est le résultat d'efforts délibéré des gouvernements/ d'une organisation
    "gvimpc19",   # Intention réelle derrière les mesures sanitaires (contrôle vs santé)
    "gvbalc19",   # Équilibre des décisions sanitaires perçu (santé vs intérêts)
    "trstsci",    # Confiance dans la science et les scientifiques
    "getnvc19",   # Raisons ou volonté de refus de la vaccination Covid-19
    "icvacc19",   # Statut vaccinal Covid-19 (a reçu le vaccin oui/non)

    # --- 3. positionnement politique & confiance institutionnelle ---
    "lrscale",    # Positionnement politique sur l'axe gauche-droite (échelle 0-10)
    "polintr",    # Degré d'intérêt pour la politique
    "vote",       # Participation électorale aux dernières élections
    "clsprty",    # Sentiment de proximité avec un parti politique en particulier
    "prtdgcl",    # Degré d'attachement à ce parti
    "trstprl",    # Confiance dans le parlement national
    "trstplt",    # Confiance dans les hommes et femmes politiques
    "trstprt",    # Confiance dans les partis politiques
    "trstlgl",    # Confiance dans la justice / le système judiciaire
    "trstplc",    # Confiance dans la police
    "cptppola",   # Sentiment d'efficacité politique (capacité des citoyens à peser sur le système)
    "psppipla",   # Sentiment que le système politique prend en compte les citoyens

    # --- 4. éducation & capital socio-économique ---
    "eisced",     # Plus haut diplôme obtenu (standard européen ES-ISCED)
    "eduyrs",     # Nombre d'années complètes d'études
    "hinctnta",   # Revenu net total du ménage (en déciles nationaux)
    "hincfel",    # Perception du niveau de revenu (vit confortablement / difficultés)
    "mainact",    # Activité principale (emploi, études, chômage, retraite...)
    "uempla",     # Situation de recherche d'emploi / chômage
    "domicil",    # Degré d'urbanisation de la zone de vie (métropole, banlieue, rural...)

    # --- 5. religion, croyances & spiritualité ---
    "rlgblg",     # Sentiment d'appartenance à une religion particulière (oui/non)
    "rlgdgr",     # Intensité du sentiment religieux (échelle 0-10)
    "rlgatnd",    # Fréquence de fréquentation des lieux de culte
    "pray",       # Fréquence de la prière en dehors des offices religieux

    # --- 6. données démographiques fondamentales ---
    "gndr",       # Genre (1 = Homme, 2 = Femme)
    "agea",       # Âge exact du répondant
    "yrbrn",      # Année de naissance
]

# Noms explicites en français correspondants exactement à colonnes_a_garder
nouveaux_noms = [
    # 1) identifiants & poids
    "id", "pays", "poids_analyse", "poids_design", "poids_poststrat",
    # 2) Ccoyances complotistes & science
    "complot_groupes_secrets", "complot_science_politique", "dissimulation_covid", 
    "mesures_sanitaires_controle", "mesures_sanitaires_equilibre", "confiance_science", 
    "refus_vaccin", "statut_vaccine",
    # 3) politique & institutions
    "axe_gauche_droite", "interet_politique", "a_vote", "proche_parti", "degre_proximite_parti",
    "confiance_parlement", "confiance_politiques", "confiance_partis", "confiance_justice", 
    "confiance_police", "efficacite_politique_citoyen", "prise_en_compte_citoyen",
    # 4) éducation & socio-éco
    "niveau_etudes_isced", "annees_etudes", "decile_revenu", "sentiment_revenu", 
    "activite_principale", "chomage", "milieu_residence",
    # 5) religion & spiritualité
    "appartenance_religieuse", "degre_religiosite", "frequence_culte", "frequence_priere",
    # 6) démographie
    "genre", "age", "annee_naissance"
]


# 3. Creation de variables aggrégées

# Variables contribuant à la futur nouvelle variable "score_complot"
complot_cols = ["complot_groupes_secrets", "complot_science_politique", "dissimulation_covid"]

# Variables contribuant à la futur nouvelle variable "confiance_institutions"
inst_cols = ["confiance_parlement", "confiance_politiques", "confiance_partis", "confiance_justice"]


# 3) Variables finales du dataframe df_final qui sera utilisé dans la partie III. du rapport
variable_expliqué = [
    "score_complot",             # Continue (0-10)
    "adhesion_complot_forte",    # Discrète binaire (0 ou 1)
    "dissimulation_covid",       # Discrète ordinale (1-5)
]

variables_explicatives = [
    "confiance_institutions",    # Continue (0-10)
    "confiance_science",         # Continue (0-10)
    "radicalite_politique",      # Continue (0-5)
    "score_socioeco",            # Continue (0-1)
    "degre_religiosite",         # Continue (0-10)
    "zone_rurale",               # Discrète binaire (0 ou 1)
    "age",                       # Continue
]

variable_finaux = variable_expliqué + variables_explicatives