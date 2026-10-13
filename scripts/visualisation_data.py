import numpy as np
import pandas as pd
from preparation_data import recuperer_donnees, dico_doi, select_colonne, suppr_colonne, renommer_colonne


############# But de ce script #############
# explorer les données et visualiser afin de savoir lesquels mettre dans le rapport final





############# Préparation des données #############

df_ess_2023 = recuperer_donnees(2023)
print(df_ess_2023.shape)
print(df_ess_2023.head())

colonne_a_garder = ["idno"] # écrire les noms de colonnes potentiellement pertinentes
# Voir les variables disponilbles ici : https://ess.sikt.no/en/datafile/242aaa39-3bbb-40f5-98bf-bfb1ce53d8ef



# Utiliser les fonctions de preparation_data.py pour renommer, 
# garder les colonnes utiles, supprimer les colonnes inutiles






############# Exploration et visualisation des données #############

##### Valeurs manquantes #####
# Qqn peut regarder il y a cb de valeurs manquantes dans chaque colonne et envoyer ces resultat ds groupe
# Comme ça on se décide de comment on s'en occupe 




# regarder la moyenne, ecart-type des différents colonnes etc




##### Graphiques #####
# Faire des graphiques au feeling pour avoir une idée des différentes variables














