import numpy as np
import pandas as pd
from preparation_data import recuperer_donnees, dico_doi, select_colonne, suppr_colonne, renommer_colonne


############# But de ce script #############
# explorer les données et visualiser afin de savoir lesquels mettre dans le rapport final





############# Préparation des données #############

df_ess_2023 = recuperer_donnees(2023)
print(df_ess_2023.shape)
print(df_ess_2023.head())

#Liste des colonnes potentiellement pertinentes pour l'étude sur les théories du complot (ESS Round 10)
# Source des variables : https://ess.sikt.no/en/datafile/242aaa39-3bbb-40f5-98bf-bfb1ce53d8ef
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
    "gvconc19",   # Dissimulation par le gouvernement d'informations clés sur le Covid-19
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

# Utiliser les fonctions de preparation_data.py pour renommer, 
# garder les colonnes utiles, supprimer les colonnes inutiles






############# Exploration et visualisation des données #############

##### Valeurs manquantes #####
# Qqn peut regarder il y a cb de valeurs manquantes dans chaque colonne et envoyer ces resultat ds groupe
# Comme ça on se décide de comment on s'en occupe 




# regarder la moyenne, ecart-type des différents colonnes etc




##### Graphiques #####
# Faire des graphiques au feeling pour avoir une idée des différentes variables














