import numpy as np
import pandas as pd
import os
import matplotlib.pyplot as plt
from preparation_data import recuperer_donnees, dico_doi, select_colonne, suppr_colonne, renommer_colonne


############# But de ce script #############
# explorer les données et visualiser afin de savoir lesquels mettre dans le rapport final





############# Préparation des données #############

df_ess_2020 = recuperer_donnees(2020)
print(df_ess_2020.shape)
print(df_ess_2020.head())

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

# Filtrage puis renommage
df_filtre = select_colonne(df_ess_2020, colonnes_a_garder)
df_clean = renommer_colonne(df_filtre, colonnes_a_garder, nouveaux_noms)

print("Dimensions après filtrage :", df_clean.shape)
print(df_clean.head())





############# Création de variables #############

# 1) Nettoyage des valeurs hors échelles (sécurité non-réponses)
complot_cols = ["complot_groupes_secrets", "complot_science_politique", "dissimulation_covid"]
for col in complot_cols:
    df_clean.loc[~df_clean[col].between(1, 5), col] = np.nan

inst_cols = ["confiance_parlement", "confiance_politiques", "confiance_partis", "confiance_justice"]
for col in inst_cols:
    df_clean.loc[~df_clean[col].between(0, 10), col] = np.nan

df_clean.loc[~df_clean["axe_gauche_droite"].between(0, 10), "axe_gauche_droite"] = np.nan
df_clean.loc[~df_clean["decile_revenu"].between(1, 10), "decile_revenu"] = np.nan
df_clean.loc[~df_clean["annees_etudes"].between(0, 25), "annees_etudes"] = np.nan
df_clean.loc[~df_clean["degre_religiosite"].between(0, 10), "degre_religiosite"] = np.nan


# 2) création des indicateurs synthétiques
# A) Score moyen continu de complotisme (ramené de 0 à 10)
df_clean["score_complot"] = (df_clean[complot_cols].mean(axis=1) - 1) * 2.5

# B) adhésion forte binaire (1 si au moins 2 réponses >= 4/5, sinon 0)
df_clean["adhesion_complot_forte"] = ((df_clean[complot_cols] >= 4).sum(axis=1) >= 2).astype(int)

# C) confiance institutionnelle continue (moyenne de 0 à 10)
df_clean["confiance_institutions"] = df_clean[inst_cols].mean(axis=1)

# D) score socio-économique continu (façon IDH, borné de 0 à 1)
rev_norm = (df_clean["decile_revenu"] - 1) / 9.0
edu_norm = df_clean["annees_etudes"] / 25.0
df_clean["score_socioeco"] = (rev_norm + edu_norm) / 2.0

# E) radicalité politique (distance au centre 5 sur l'axe 0-10)
df_clean["radicalite_politique"] = (df_clean["axe_gauche_droite"] - 5).abs()

# F) zone rurale (binaire : 1 si village ou campagne, 0 sinon)
df_clean["zone_rurale"] = df_clean["milieu_residence"].isin([4, 5]).astype(int)


# 3) Renseignement des catégories finales
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
















############# Exploration et visualisation des données #############

##### Valeurs manquantes #####
# Qqn peut regarder il y a cb de valeurs manquantes dans chaque colonne et envoyer ces resultat ds groupe
# Comme ça on se décide de comment on s'en occupe 
############# Valeurs manquantes #############

# Nombre et part de NaN par variable
manquantes = pd.DataFrame({
    "variable": df_clean.columns,
    "nb_manquantes": df_clean.isna().sum().values,
    "pct_manquantes": (df_clean.isna().mean() * 100).round(2).values,
})

manquantes = manquantes.sort_values("pct_manquantes", ascending=False).reset_index(drop=True)

# Affichage en tableau (console)
#print(manquantes.to_string(index=False))

# Dans un notebook (Jupyter, VSCode)
manquantes.style.background_gradient(subset=["pct_manquantes"], cmap="Reds").format({"pct_manquantes": "{:.2f} %"})

#manquantes.to_csv("valeurs_manquantes.csv", index=False)
#manquantes.to_latex("valeurs_manquantes.tex", index=False, float_format="%.2f")

#on regarde les valeurs manquantes par pays : 
manq_pays = (df_clean.drop(columns=["id"]).isna()
             .groupby(df_clean["pays"]).mean().mul(100).round(1))

# Variables clés
cles = ["complot_groupes_secrets", "complot_science_politique", "dissimulation_covid",
        "confiance_science", "statut_vaccine", "decile_revenu"]
#print(manq_pays[cles].T.to_string())

#for v in cles:
    #pays_absents = manq_pays.index[manq_pays[v] > 90].tolist()
    #print(v, "→", pays_absents)


# regarder la moyenne, ecart-type des différents colonnes etc
############# Statistiques descriptives & graphiques #############
# À placer à la suite du script de préparation (df_clean doit exister).
# Variables : confiance_science (pays où elle est posée), axe_gauche_droite,
# confiance_politiques, degre_religiosite, interet_politique.



############# Paramètres #############
POIDS = "poids_analyse"   # anweight : proportionnel à pspwght au sein d'un pays, adapté aux comparaisons entre pays
SEUIL_MANQ = 0.5          # un pays est exclu pour confiance_science si > 50 % de manquantes
DOSSIER_FIG = "figures"
#os.makedirs(DOSSIER_FIG, exist_ok=True)
#print("Figures enregistrées dans :", os.path.abspath(DOSSIER_FIG))

variables = {
    "confiance_science":    "Confiance dans la science (0-10)",
    "axe_gauche_droite":    "Positionnement gauche-droite (0-10)",
    "confiance_politiques": "Confiance dans les politiques (0-10)",
    "degre_religiosite":    "Degré de religiosité (0-10)",
    "interet_politique":    "Intérêt pour la politique (1-4, 4 = très intéressé)",
}

############# Nettoyage #############
df = df_clean.copy()

# Sécurité : codes de non-réponse (77, 88, 99, ...) -> NaN
for v in ["confiance_science", "axe_gauche_droite", "confiance_politiques", "degre_religiosite"]:
    df.loc[~df[v].between(0, 10), v] = np.nan
df.loc[~df["interet_politique"].between(1, 4), "interet_politique"] = np.nan

# Dans l'ESS, polintr est codé 1 = très intéressé ... 4 = pas du tout : on inverse
# pour que "plus haut = plus intéressé" (comme les autres échelles)
df["interet_politique"] = 5 - df["interet_politique"]

# Pays où confiance_science est (quasi) complète
part_manq = df.groupby("pays")["confiance_science"].apply(lambda s: s.isna().mean())
pays_science = part_manq[part_manq < SEUIL_MANQ].index
#print("Pays retenus pour confiance_science :", list(pays_science))
#print("Pays exclus :", list(part_manq[part_manq >= SEUIL_MANQ].index))


def donnees(var):
    """Sous-échantillon pays / variable / poids ; restreint aux pays retenus pour confiance_science."""
    d = df[["pays", var, POIDS]]
    if var == "confiance_science":
        d = d[d["pays"].isin(pays_science)]
    return d


############# Statistiques pondérées #############
def moy_pond(x, w):
    return np.average(x, weights=w)

def std_pond(x, w):
    m = np.average(x, weights=w)
    return np.sqrt(np.average((x - m) ** 2, weights=w))

def quant_pond(x, w, q):
    i = np.argsort(x)
    x, w = x[i], w[i]
    c = (np.cumsum(w) - 0.5 * w) / w.sum()
    return np.interp(q, c, x)

def stats(d, var):
    total = len(d)
    d = d.dropna(subset=[var, POIDS])
    if len(d) == 0:
        return pd.Series(dtype=float)
    x, w = d[var].to_numpy(float), d[POIDS].to_numpy(float)
    return pd.Series({
        "n": len(x),
        "% manquantes": round(100 * (1 - len(x) / total), 1),
        "moyenne": moy_pond(x, w),
        "écart-type": std_pond(x, w),
        "min": x.min(),
        "Q1": quant_pond(x, w, 0.25),
        "médiane": quant_pond(x, w, 0.5),
        "Q3": quant_pond(x, w, 0.75),
        "max": x.max(),
    })


############# 1) Tableau global #############
#glob = pd.DataFrame({v: stats(donnees(v), v) for v in variables}).T.round(2)
#print("\n=== Statistiques descriptives globales (pondérées) ===")
#print(glob.to_string())
#glob.to_csv("stats_globales.csv")

############# 2) Tableaux par pays #############
#par_pays = {
    #v: pd.DataFrame({p: stats(g, v) for p, g in donnees(v).groupby("pays")}).T
    #for v in variables
#}
#pd.concat(par_pays, names=["variable", "pays"]).round(2).to_csv("stats_par_pays.csv")

#for v, lab in variables.items():
    #print(f"\n=== {lab} : par pays ===")
    #print(par_pays[v].round(2).to_string())

# Moyennes pondérées : pays x variables
#moy_pays = pd.DataFrame({v: par_pays[v]["moyenne"] for v in variables}).round(2)
#print("\n=== Moyennes pondérées par pays ===")
#print(moy_pays.to_string())

############# 3) Graphiques #############
# 3a) Distribution globale (histogrammes pondérés)
#fig, axes = plt.subplots(2, 3, figsize=(15, 8))
#axes = axes.ravel()
#for ax, (v, lab) in zip(axes, variables.items()):
    #d = donnees(v).dropna(subset=[v, POIDS])
    #bins = np.arange(d[v].min() - 0.5, d[v].max() + 1.5, 1)
    #ax.hist(d[v], bins=bins, weights=d[POIDS], edgecolor="white")
    #ax.set_title(lab, fontsize=10)
    #ax.set_ylabel("Effectif pondéré")
#axes[-1].axis("off")
#fig.suptitle("Distribution des variables principales (ESS 10)", fontsize=13)
#fig.tight_layout()
#fig.savefig(f"{DOSSIER_FIG}/distributions.png", dpi=150)
#plt.show()

# 3b) Boîtes à moustaches par pays (pays triés par moyenne pondérée)
#fig, axes = plt.subplots(2, 3, figsize=(20, 10))
#axes = axes.ravel()
#for ax, (v, lab) in zip(axes, variables.items()):
    #d = donnees(v).dropna(subset=[v])
    #ordre = par_pays[v]["moyenne"].sort_values().index
    #ax.boxplot([d.loc[d["pays"] == p, v] for p in ordre], showfliers=False)
    #ax.set_xticks(range(1, len(ordre) + 1))
    #ax.set_xticklabels(ordre, rotation=90, fontsize=8)
    #ax.set_title(lab, fontsize=10)
#axes[-1].axis("off")
#fig.suptitle("Distribution par pays (non pondérée, triée par moyenne pondérée)", fontsize=13)
#fig.tight_layout()
#fig.savefig(f"{DOSSIER_FIG}/boxplots_par_pays.png", dpi=150)
#plt.show()

# 3c) Moyennes pondérées par pays (barres horizontales triées)
#fig, axes = plt.subplots(2, 3, figsize=(18, 10))
#axes = axes.ravel()
#for ax, v in zip(axes, variables):
    #m = moy_pays[v].dropna().sort_values()
    #ax.barh(m.index, m.values)
    #ax.axvline(glob.loc[v, "moyenne"], color="red", linestyle="--", linewidth=1, label="moyenne globale")
    #ax.set_title(variables[v], fontsize=10)
    #ax.tick_params(axis="y", labelsize=8)
#axes[0].legend(fontsize=8)
#axes[-1].axis("off")
#fig.suptitle("Moyennes pondérées par pays", fontsize=13)
#fig.tight_layout()
#fig.savefig(f"{DOSSIER_FIG}/moyennes_par_pays.png", dpi=150)
#plt.show()

# 3d) Heatmap pays x variables (couleur = écart à la moyenne des pays, standardisé par variable)
#z = (moy_pays - moy_pays.mean()) / moy_pays.std()
#fig, ax = plt.subplots(figsize=(9, 9))
#im = ax.imshow(z.to_numpy(float), cmap="RdBu_r", vmin=-2.5, vmax=2.5, aspect="auto")
#ax.set_xticks(range(len(variables)))
#ax.set_xticklabels([v.replace("_", "\n") for v in variables], fontsize=9)
#ax.set_yticks(range(len(moy_pays)))
#ax.set_yticklabels(moy_pays.index, fontsize=9)
#for i in range(moy_pays.shape[0]):
    #for j in range(moy_pays.shape[1]):
        #val = moy_pays.iloc[i, j]
        #if pd.notna(val):
        #    ax.text(j, i, f"{val:.1f}", ha="center", va="center", fontsize=8)
#fig.colorbar(im, ax=ax, label="Écart à la moyenne des pays (en écarts-types)")
#ax.set_title("Moyennes pondérées par pays (valeurs affichées, couleur standardisée)")
#fig.tight_layout()
#fig.savefig(f"{DOSSIER_FIG}/heatmap_pays.png", dpi=150)
#plt.show()



##### Graphiques #####
# Faire des graphiques au feeling pour avoir une idée des différentes variables












