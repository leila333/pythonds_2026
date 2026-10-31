import pandas as pd


# Voici le script utilisé pour créer le fichier parquet utilisé ici 
# à partir du fichier csv d'origine

## Etape 1 : Télécharger le fichier csv d'origine

## Etape 2 : On ouvre le fichier csv d'origine
df_ess_2020 = pd.read_csv("ESS10e03_3.csv")

## Etape 3 : On remplace les type objets par string pour pouvoir convertir en parquet
for col in df_ess_2020.select_dtypes(include=['object']).columns:
    df_ess_2020[col] = df_ess_2020[col].astype(str)


## Etape 4 : Remplacer les non réponses codées par des valeurs particulières par des np.nan 

# Ce dico contient la plus grande valeur numérique que peuvent prendre 
# les variables dans le array correspondant.
# Ces variables sont celles utilisés dans notre projet,
dico_val = {1:["uempla", "rlgblg"],
            2: ["getnvc19", "icvacc19", "clsprty", "gndr"],
            3: ["vote"],
            4: ["polintr", "prtdgcl", "hincfel"],
            5: ["secgrdec","scidecpb","gvconc19", 
                "cptppola", "psppipla",
                "domicil"],
            7: ["eisced", "rlgatnd", "pray"],
            10:["gvimpc19", "gvbalc19", "trstsci", 
                    "lrscale", "trstprl", "trstplt", "trstprt", "trstlgl", "trstplc",
                    "hinctnta", "mainact",
                    "rlgdgr"],
            70: ["eduyrs"],
            990: ["agea"],
            7770:["yrbrn"]}


# for n in dico_val:
#     for e in dico_val[n]:
#         df_ess_2020.loc[df_ess_2020[e] >= n+1, e] = np.nan


## Etape 5 : On export au format Parquet
# df_ess_2020.to_parquet('Ess_2020.parquet', index=False)