# TP Réseaux mobiles 2G → 5G — environnement Simu5G

Environnement de simulation prêt à l'emploi (OMNeT++ 6.2 + INET 4.5.4 + Simu5G 1.3.0 + JupyterLab).

## Démarrer en 2 clics
1. Bouton vert **Code** → onglet **Codespaces** → **Create codespace on main**.
2. Attendez 2-3 min : VS Code s'ouvre dans le navigateur. Menu **Terminal → New Terminal** : vous êtes dans l'environnement Simu5G, dossier `/tp`.

## Les TP
| Dossier | TP | Support |
|---|---|---|
| `tp/TP0_dimensionnement` | TP0 — Dimensionnement cellulaire, GSM (2G) | Google Colab |
| `tp/TP1_umts` | TP1 — Du GSM (2G) à l'UMTS (3G) | Google Colab |
| `tp/TP2_prise_en_main` | TP2 — Prise en main Simu5G, cellule LTE (4G) | Codespace |
| `tp/TP3_scheduling` | TP3 — Scheduling LTE (4G) | Codespace |
| `tp/TP4_handover` | TP4 — Mobilité et handover LTE (4G) | Codespace |

Chaque dossier contient le sujet (`TPx_Sujet_Etudiants.pdf`), les fichiers de simulation (`omnetpp.ini`) et le notebook à compléter (`TPx_analyse.ipynb`).

## Commandes utiles
```
cd /tp/TP2_prise_en_main
tp-run SingleCell-DL          # lance une config, run 0
tp-run Charge-DL 0..5         # plusieurs runs en parallèle
tp-export results results.csv # résultats -> CSV pour le notebook
tp-export-vec servingCell:vector results/AvecHO cell.csv   # séries temporelles (TP4)
```
Pour le notebook : ouvrez le `.ipynb`, choisissez le noyau **Python (Simu5G)** s'il est proposé, sinon n'importe quel Python 3 : la première cellule du notebook rend les bibliothèques disponibles.

En fin de séance, sauvegardez votre travail : **Source Control** (icône à gauche) → message → **Commit** → **Sync**.

## Alternative locale
Voir `README_etudiant.md` (Docker Desktop + `docker compose up`).
