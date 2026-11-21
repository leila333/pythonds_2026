import numpy as np
import pandas as pd
import seaborn as sns
import os
import matplotlib.pyplot as plt
from IPython.display import display


############# But de ce script #############
# explorer les données et visualiser afin de savoir lesquels mettre dans le rapport final

# 1) Fonctions utiles
# 2) Fonction de visualisation




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


# Dictionnaire utilisée dans la fonction creer_df_stats_continues()
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

# Renvoie un df contenant des stats desc sur les variables qui doivent être continues
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


# Affiche un tableau de statistique descriptives
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



########################## 2) Fonctions de visualisation


def piechart_pondere(df, titre, var, nom_var, poids, labels, couleurs):
    sub = df[[var, poids]].dropna(subset=[poids])

    manquantes = sub[var].isna()
    poids_total = sub[poids].sum()

    parts = [
        100 * sub.loc[~manquantes & (sub[var] == 1), poids].sum() / poids_total,
        100 * sub.loc[~manquantes & (sub[var] == 0), poids].sum() / poids_total,
        100 * sub.loc[manquantes, poids].sum() / poids_total
    ]

    plt.figure(figsize=(3.5, 3.5))

    plt.pie(
        parts,
        labels=labels,
        colors=couleurs,
        autopct="%1.1f%%",
        startangle=90
    )

    plt.title(titre)
    plt.show()


def heatmap_covid(df, var_y, titre, ylabel, ax):
    d = df.dropna(subset=["dissimulation_covid", var_y])

    table_pct = pd.crosstab(
        d[var_y],
        d["dissimulation_covid"],
        normalize="index"
    ) * 100

    # Inverser l'ordre de l'ordonnée
    table_pct = table_pct.iloc[::-1]

    sns.heatmap(
        table_pct,
        annot=True,
        fmt=".1f",
        cmap="Blues",
        vmin=0,
        vmax=32,
        ax=ax
    )

    ax.set_title(titre)
    ax.set_xlabel("Dissimulation du Covid")
    ax.set_ylabel(ylabel)


def barplot_covid(df, x_var, titre, xlabel, ax):
    d = df.dropna(subset=["dissimulation_covid", x_var]).copy()

    # Regrouper l'axe des abscisses en 10 catégories
    if d[x_var].nunique() > 10:
        d[x_var] = pd.cut(d[x_var], bins=10)

    sns.countplot(
        data=d,
        x=x_var,
        hue="dissimulation_covid",
        palette="crest",
        ax=ax
    )

    ax.set_title(titre)
    ax.set_xlabel(xlabel)
    ax.set_ylabel("Nombre de personnes")
    ax.tick_params(axis="x", rotation=45)
    ax.legend(title="Dissimulation du Covid")


def violinplot_covid(df, var_y, titre, ylabel):
    d = df.dropna(subset=["dissimulation_covid", var_y])

    plt.figure(figsize=(6, 4))

    sns.violinplot(
        data=d,
        x="dissimulation_covid",
        y=var_y,
        hue="dissimulation_covid",
        palette="Blues",
        inner="quart",
        legend=False
    )

    plt.title(titre)
    plt.xlabel("Dissimulation du Covid")
    plt.ylabel(ylabel)

    plt.tight_layout()
    plt.show()

