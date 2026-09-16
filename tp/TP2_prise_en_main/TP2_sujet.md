# TP2 — Prise en main d'OMNeT++ / Simu5G : une cellule LTE sous charge

**Module** : Réseaux mobiles 4G/5G — **Durée** : 3 h — **Rendu** : le notebook `TP2_analyse.ipynb` complété + le fichier `omnetpp.ini` final.

## Objectifs
- Comprendre la chaîne *fichier `.ini` → simulation → fichiers `.sca/.vec` → analyse Python*.
- Identifier les paramètres clés d'une cellule LTE dans Simu5G (bande, puissance, scheduler, mobilité, trafic).
- Mesurer la capacité VoIP d'une cellule et le comportement du délai/perte quand la charge augmente.

## Prérequis
Le conteneur `tp5g` démarré (`docker compose up`) et JupyterLab ouvert sur http://localhost:8888. Les commandes shell se tapent dans un **Terminal** de JupyterLab (File → New → Terminal), dans le dossier `/tp/TP2_prise_en_main`.

---

## Exercice 1 — Lire la configuration (30 min)
Ouvrez `omnetpp.ini` et le réseau `SingleCell.ned` (chemin : `/opt/simu5g/simulations/LTE/networks/SingleCell.ned`).

1. Dessinez la topologie : quels nœuds ? quels liens ? Par où passe un paquet VoIP du serveur vers un UE (nommez les modules traversés : `server` → … → `ue[k]`) ?
2. Que signifient `**.numBands = 25`, `warmup-period = 2s`, `${numUEs=5}` ? À quoi sert `${repetition}` dans le nom des fichiers de résultats ?
3. Quelle est la différence entre `*.ue[*].app[0]` et `**.app[*]` dans la syntaxe des motifs OMNeT++ ?
4. Le trafic VoIP de Simu5G émet des trames de 40 octets toutes les 20 ms (avec des silences). Calculez le débit crête d'un flux, puis le nombre de flux que 25 RB peuvent porter en ordre de grandeur (on prendra ≈ 150 kbit/s par RB en MCS moyen). Gardez ce chiffre pour l'exercice 3.

## Exercice 2 — Première simulation (30 min)
```bash
cd /tp/TP2_prise_en_main
tp-run SingleCell-DL            # 5 UE, VoIP descendant, 10 s simulées
ls results/SingleCell-DL/        # -> un .sca (scalaires) et un .vec (vecteurs, vide ici)
tp-export results results.csv
```
Dans le notebook, section 1 : listez les scalaires disponibles et répondez à **Q2.1**.

> Pour voir la simulation « en direct » (mode non express) : `simu5g -u Cmdenv -c SingleCell-DL --cmdenv-express-mode=false | head -100`. Repérez les événements MAC/PHY.

## Exercice 3 — Montée en charge (60 min)
```bash
tp-run Charge-DL 0..4            # numUEs = 5, 20, 50, 100, 150  (5 runs en parallèle)
tp-export results/Charge-DL charge.csv
```
Notebook section 2 : tracez délai et perte en fonction du nombre d'UE, répondez à **Q2.2**.

Puis passez la cellule à 10 MHz (`numBands = 50`) et 20 MHz (`numBands = 100`), relancez, exportez dans `charge50.csv` et `charge100.csv`, et complétez **Q2.3** (les trois courbes sur un même graphe). Comparez avec votre estimation de l'exercice 1.

## Exercice 4 — Mobilité (30 min)
```bash
tp-run Mobile-DL 0..3            # 20 UE, vitesse 1 / 5 / 15 / 30 m/s
tp-export results/Mobile-DL mobile.csv
```
Notebook section 3, **Q2.4**.

## Exercice 5 — À vous (30 min, au choix)
- **Uplink** : refaites l'exercice 3 avec `SingleCell-UL`. Le seuil de saturation est-il le même ? Pourquoi (puissance UE 26 dBm vs eNB 40 dBm, scheduler UL) ?
- **Scheduler** : remplacez `MAXCI` par `PF` dans le `.ini` et relancez `Charge-DL`. Quelle métrique change le plus ? (préparation du TP3)
- **Statistiques fines** : mettez `**.vector-recording = true`, relancez un run, puis `tp-export-vec voIPFrameDelay:vector results delay.csv` et tracez le délai d'un UE au cours du temps.

## Rendu et barème
| Élément | Points |
|---|---|
| Exercice 1 (topologie, paramètres, estimation de capacité) | 5 |
| Q2.1 – Q2.4 avec graphes lisibles (axes, unités, légende) | 10 |
| Exercice 5 + synthèse (10 lignes) | 5 |
Les graphes doivent être commentés : un graphe sans interprétation ne rapporte pas de point.
