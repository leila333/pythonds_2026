import numpy as np
import pandas as pd
import os
import matplotlib.pyplot as plt


############# But de ce script #############
# explorer les données et visualiser afin de savoir lesquels mettre dans le rapport final

# 1) Fonctions utiles
# 2) Brouillon (ne pas regarder)




########################## 1) Fonctions utiles ################################################


# --- Fonctions utilitaires pondérées ---
def moyenne_ponderee(x, w):
    return np.average(x, weights=w)


def ecart_type_pondere(x, w):
    m = np.average(x, weights=w)
    return np.sqrt(np.average((x - m) ** 2, weights=w))


def quantile_pondere(x, w, q):
    idx = np.argsort(x.values)
    x_s, w_s = x.values[idx], w.values[idx]
    cum = (np.cumsum(w_s) - 0.5 * w_s) / w_s.sum()
    return np.interp(q, cum, x_s)


# --- Tableau 1 : variables continues ---

# Dictionnaire utilisée dans la fonction stats_continues()
libelles = {
    "confiance_institutions": "Confiance dans les institutions (0-10)",
    "score_socioeco": "Score socio-économique (0-1)",
    "radicalite_politique": "Radicalité politique (0-5)",
    "confiance_science": "Confiance dans la science (0-10)",
    "degre_religiosite": "Degré de religiosité (0-10)",
    "age": "Âge (années)",
    "zone_rurale": "Zone rurale (0/1)",
    "score_complot": "Score de complotisme (0-10)",
    "dissimulation_covid": "Perception de dissimulation Covid (ordinale)",
    "adhesion_complot_forte": "Adhésion forte aux théories du complot",
}

def creer_df_stats_continues(df, variables, poids):
    lignes = {}
    for v in variables:
        sub = df[[v, poids]].dropna()
        x, w = sub[v], sub[poids]
        lignes[libelles.get(v, v)] = {
            "N valides": len(sub),
            "Moyenne (pond.)": moyenne_ponderee(x, w),
            "Écart-type (pond.)": ecart_type_pondere(x, w),
            "Q1 (pond.)": quantile_pondere(x, w, 0.25),
            "Médiane (pond.)": quantile_pondere(x, w, 0.50),
            "Q3 (pond.)": quantile_pondere(x, w, 0.75),
        }
    return pd.DataFrame(lignes).T.round(2)


def display_stats_desc(df, titre):
    display(
    df.style
    .format({
        "N valides": "{:.0f}",
        "% manquants": "{:.1f}",
        "Moyenne (pond.)": "{:.2f}",
        "Écart-type (pond.)": "{:.2f}",
        "Min": "{:.2f}",
        "Q1 (pond.)": "{:.2f}",
        "Médiane (pond.)": "{:.2f}",
        "Q3 (pond.)": "{:.2f}",
        "Max": "{:.2f}",
    })
    .set_caption(titre)
)

# "N valides": "{:.0f}",
     #   "Moyenne (pond.)": "{:.2f}",
     #   "Écart-type (pond.)": "{:.2f}",
     #   "Q1 (pond.)": "{:.2f}",
     #   "Médiane (pond.)": "{:.2f}",
      #  "Q3 (pond.)": "{:.2f}",



########################## 2) BROUILLON ################################################





############# Préparation des données #############

#from preparation_data import recuperer_donnees, dico_doi, select_colonne, suppr_colonne, renommer_colonne
#from preparation_data import colonnes_a_garder, nouveaux_noms, complot_cols, inst_cols, variable_expliqué, variables_explicatives, variable_finaux


#df_ess_2020 = recuperer_donnees(2020)
#print(df_ess_2020.shape)
#print(df_ess_2020.head())

# Filtrage puis renommage
#df_filtre = select_colonne(df_ess_2020, colonnes_a_garder)
#df_clean = renommer_colonne(df_filtre, colonnes_a_garder, nouveaux_noms)

#print("Dimensions après filtrage :", df_clean.shape)
#print(df_clean.head())





############# Création de variables #############

# 1,2) création des indicateurs synthétiques
# A) Score moyen continu de complotisme (ramené de 0 à 10)
#df_clean["score_complot"] = (df_clean[complot_cols].mean(axis=1) - 1) * 2.5

# B) adhésion forte binaire (1 si au moins 2 réponses >= 4/5, sinon 0)
#df_clean["adhesion_complot_forte"] = ((df_clean[complot_cols] >= 4).sum(axis=1) >= 2).astype(int)

# C) confiance institutionnelle continue (moyenne de 0 à 10)
#df_clean["confiance_institutions"] = df_clean[inst_cols].mean(axis=1)

# D) score socio-économique continu (façon IDH, borné de 0 à 1)
#rev_norm = (df_clean["decile_revenu"] - 1) / 9.0
#edu_norm = df_clean["annees_etudes"] / 25.0
#df_clean["score_socioeco"] = (rev_norm + edu_norm) / 2.0

# E) radicalité politique (distance au centre 5 sur l'axe 0-10)
#df_clean["radicalite_politique"] = (df_clean["axe_gauche_droite"] - 5).abs()

# F) zone rurale (binaire : 1 si village ou campagne, 0 sinon)
#df_clean["zone_rurale"] = df_clean["milieu_residence"].isin([4, 5]).astype(int)





############# Exploration et visualisation des données #############

##### Valeurs manquantes #####
# Qqn peut regarder il y a cb de valeurs manquantes dans chaque colonne et envoyer ces resultat ds groupe
# Comme ça on se décide de comment on s'en occupe 
############# Valeurs manquantes #############

# Nombre et part de NaN par variable
#manquantes = pd.DataFrame({
    #"variable": df_clean.columns,
    #"nb_manquantes": df_clean.isna().sum().values,
    #"pct_manquantes": (df_clean.isna().mean() * 100).round(2).values,
#})

#manquantes = manquantes.sort_values("pct_manquantes", ascending=False).reset_index(drop=True)

# Affichage en tableau (console)
#print(manquantes.to_string(index=False))

# Dans un notebook (Jupyter, VSCode)
#manquantes.style.background_gradient(subset=["pct_manquantes"], cmap="Reds").format({"pct_manquantes": "{:.2f} %"})

#manquantes.to_csv("valeurs_manquantes.csv", index=False)
#manquantes.to_latex("valeurs_manquantes.tex", index=False, float_format="%.2f")

#on regarde les valeurs manquantes par pays : 
#manq_pays = (df_clean.drop(columns=["id"]).isna()
#             .groupby(df_clean["pays"]).mean().mul(100).round(1))

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
#df = df_clean.copy()

# Sécurité : codes de non-réponse (77, 88, 99, ...) -> NaN
#for v in ["confiance_science", "axe_gauche_droite", "confiance_politiques", "degre_religiosite"]:
#    df.loc[~df[v].between(0, 10), v] = np.nan
#df.loc[~df["interet_politique"].between(1, 4), "interet_politique"] = np.nan

# Dans l'ESS, polintr est codé 1 = très intéressé ... 4 = pas du tout : on inverse
# pour que "plus haut = plus intéressé" (comme les autres échelles)
#df["interet_politique"] = 5 - df["interet_politique"]

# Pays où confiance_science est (quasi) complète
#part_manq = df.groupby("pays")["confiance_science"].apply(lambda s: s.isna().mean())
#pays_science = part_manq[part_manq < SEUIL_MANQ].index
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










