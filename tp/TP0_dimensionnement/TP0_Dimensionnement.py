#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""TP0 - Dimensionnement et planification cellulaire : script autonome (corrige).
Execution : python TP0_Dimensionnement.py   (necessite numpy et matplotlib)
Genere depuis le notebook corrige ; les resultats sont strictement identiques."""

_fig = [1]

# ======================================================================
# TP0 : DIMENSIONNEMENT ET PLANIFICATION CELLULAIRE
# ======================================================================
import numpy as np
import matplotlib.pyplot as plt
from math import log10, sqrt, pi, ceil
plt.rcParams['figure.figsize'] = (10, 5)
print("✅ Bibliothèques chargées")

# ======================================================================
# EXERCICE 1 : BILAN DE LIAISON
# ======================================================================
c = 3e8; f = 900e6
P_e_W = 40; G_e_dB = 11; G_r_dB = 0
alpha = 3.5; k = 1
print(f"f = {f/1e6:.0f} MHz, P_e = {P_e_W} W, alpha = {alpha}")

# ======================================================================
# Q1.1 — Longueur d'onde λ = c / f
# ======================================================================
lambda_m = c / f
print(f"λ = {lambda_m:.4f} m = {lambda_m*100:.1f} cm")

# ======================================================================
# Q1.2 — Puissance émise en dBm : P_dBm = 10·log10(P_W × 1000)
# ======================================================================
P_e_dBm = 10 * log10(P_e_W * 1000)
print(f"P_e = {P_e_dBm:.2f} dBm")

# ======================================================================
# Q1.3 — Gains en linéaire : G = 10^(G_dB/10)
# ======================================================================
G_e_lin = 10 ** (G_e_dB / 10)
G_r_lin = 10 ** (G_r_dB / 10)
print(f"G_e = {G_e_lin:.2f}   G_r = {G_r_lin:.2f}")

# ======================================================================
# Q1.4 — Fonction puissance reçue (modèle à 3 étages)
# ======================================================================
def puissance_recue(r_m, P_e, G_e, G_r, lambda_m, alpha, k=1):
    """Renvoie (P_r en W, P_r en dBm) à la distance r_m (m)."""
    P_r_W = P_e * G_e * G_r * k * lambda_m**2 / r_m**alpha
    return P_r_W, 10 * log10(P_r_W * 1000)

for r in (1000, 5000):
    P_W, P_dBm = puissance_recue(r, P_e_W, G_e_lin, G_r_lin, lambda_m, alpha, k)
    print(f"r = {r/1000:.0f} km : P_r = {P_W:.2e} W = {P_dBm:.2f} dBm")

# ======================================================================
# **Q1.4 bis (réflexion)** — Pour α = 2 (espace libre), la formule de Friis donne P_r = P_e·G_e·G_r·(λ/4πr)².
# ======================================================================

# ======================================================================
# Q1.6 — Rayon maximal : r = [(P_e·G_e·G_r·k·λ²) / P_sens]^(1/α)
# ======================================================================
P_sens_dBm = -102
P_sens_W = 10 ** (P_sens_dBm / 10) / 1000
r_alpha = P_e_W * G_e_lin * G_r_lin * k * lambda_m**2 / P_sens_W
R_max = r_alpha ** (1 / alpha)
print(f"R_max = {R_max/1000:.2f} km")

# ======================================================================
# Graphique — puissance reçue en fonction de la distance
# ======================================================================
d = np.linspace(100, 25000, 300)
P = [puissance_recue(x, P_e_W, G_e_lin, G_r_lin, lambda_m, alpha, k)[1] for x in d]
plt.plot(d/1000, P, lw=2, label='Puissance reçue')
plt.axhline(P_sens_dBm, color='r', ls='--', label='Sensibilité (−102 dBm)')
plt.axvline(R_max/1000, color='g', ls='--', label=f'R_max = {R_max/1000:.1f} km')
plt.xlabel('Distance (km)'); plt.ylabel('P_r (dBm)'); plt.grid(alpha=.3); plt.legend()
plt.title('Bilan de liaison — Exercice 1'); plt.savefig(f'TP0_fig{_fig[0]}.png', dpi=120); _fig[0]+=1; plt.close()

# ======================================================================
# ---
# ======================================================================
P_e2, G_e2, G_r2, alpha2, R = 40, 1, 1, 4, 2000
CI_seuil_dB = 9

# ======================================================================
# Q2.1 — Signal utile C en bordure de cellule (r = R)
# ======================================================================
C, _ = puissance_recue(R, P_e2, G_e2, G_r2, lambda_m, alpha2, k)
print(f"C = {C:.2e} W")

# ======================================================================
# Q2.2 — Distance de réutilisation pour K = 3 : D = √(3K)·R
# ======================================================================
K = 3
D = sqrt(3 * K) * R
print(f"D = {D/1000:.2f} km")

# ======================================================================
# Q2.3 / Q2.4 — Interférence d'un co-canal, puis des 6 interféreurs
# ======================================================================
I1, _ = puissance_recue(D, P_e2, G_e2, G_r2, lambda_m, alpha2, k)
I_total = 6 * I1
print(f"I1 = {I1:.2e} W   I_total = {I_total:.2e} W")

# ======================================================================
# Q2.5 — Rapport C/I
# ======================================================================
CI_lin = C / I_total
CI_dB = 10 * log10(CI_lin)
print(f"C/I = {CI_lin:.1f} (lin) = {CI_dB:.2f} dB  → seuil {CI_seuil_dB} dB : {'✅ suffisant' if CI_dB >= CI_seuil_dB else '❌ insuffisant'}")

# ======================================================================
# Q2.6 — Valeur minimale de K
# ======================================================================
K_values = {1:[(1,0)], 3:[(1,1)], 4:[(2,0)], 7:[(2,1)], 9:[(3,0)], 12:[(2,2)], 13:[(3,1)]}
print(f"{'K':>3} {'(i,j)':>8} {'D (km)':>8} {'C/I (dB)':>9}  seuil 9 dB  seuil 18 dB")
for Kv, couples in K_values.items():
    Dk = sqrt(3*Kv) * R
    Ik, _ = puissance_recue(Dk, P_e2, G_e2, G_r2, lambda_m, alpha2, k)
    CIk = 10*log10(C / (6*Ik))
    print(f"{Kv:>3} {str(couples[0]):>8} {Dk/1000:>8.2f} {CIk:>9.2f}     {'✅' if CIk>=9 else '❌'}          {'✅' if CIk>=18 else '❌'}")

# ======================================================================
# **Réponse Q2.6** — K_min au seuil nominal = ___ ; K_min avec marge = ___ .
# ======================================================================

# ======================================================================
# Q2.7 — Canaux par cellule : bande 25 MHz, espacement 200 kHz, motif K = 7
# ======================================================================
bande_MHz, espacement_kHz, K_deploy = 25, 200, 7
nb_canaux_total = int(bande_MHz * 1000 / espacement_kHz)
canaux_par_cellule = nb_canaux_total // K_deploy
print(f"{nb_canaux_total} canaux au total → {canaux_par_cellule} canaux par cellule (K={K_deploy})")

# ======================================================================
# ---
# ======================================================================
surface_km2, rayon_km = 100, 1
nb_abonnes, trafic_mErl, P_b = 100_000, 25, 0.02
# Table d'Erlang B à P_b = 2 % : canaux -> trafic admissible (Erlang)
erlang_B = {10:5.08, 15:9.01, 20:13.2, 25:17.5, 30:22.0, 35:26.7, 40:31.0, 45:35.9, 50:40.8, 55:45.7, 60:50.6}

def trafic_admissible(n_canaux):
    """Trafic admissible (Erlang) par interpolation linéaire dans la table."""
    xs, ys = list(erlang_B.keys()), list(erlang_B.values())
    return float(np.interp(n_canaux, xs, ys))

# ======================================================================
# Q3.2 — Trafic total offert
# ======================================================================
trafic_total_Erl = nb_abonnes * trafic_mErl / 1000
print(f"Trafic total = {trafic_total_Erl:,.0f} Erlang")

# ======================================================================
# Q3.3 — Trafic admissible par cellule
# ======================================================================
trafic_par_cellule = trafic_admissible(canaux_par_cellule)
print(f"{canaux_par_cellule} canaux/cellule → {trafic_par_cellule:.1f} Erlang par cellule (P_b = 2 %)")

# ======================================================================
# Q3.4 — Nombre de cellules pour la COUVERTURE
# ======================================================================
surface_cellule = 2.6 * rayon_km**2
nb_cellules_couverture = ceil(surface_km2 / surface_cellule)
print(f"S_cell = {surface_cellule:.2f} km² → {nb_cellules_couverture} cellules pour couvrir {surface_km2} km²")

# ======================================================================
# Q3.5 — Nombre de cellules pour la CAPACITÉ
# ======================================================================
nb_cellules_capacite = ceil(trafic_total_Erl / trafic_par_cellule)
print(f"{trafic_total_Erl:.0f} Erl / {trafic_par_cellule:.1f} Erl par cellule → {nb_cellules_capacite} cellules")

# ======================================================================
# Q3.6 — Critère dimensionnant
# ======================================================================
nb_cellules_deploy = max(nb_cellules_couverture, nb_cellules_capacite)
critere = 'CAPACITÉ' if nb_cellules_capacite > nb_cellules_couverture else 'COUVERTURE'
print(f"Couverture : {nb_cellules_couverture}   Capacité : {nb_cellules_capacite}   → critère dimensionnant : {critere}")
print(f"→ Déployer {nb_cellules_deploy} cellules")

# ======================================================================
# **Réponse Q3.6** — Quel rayon de cellule effectif cela impose-t-il (R_eff = √(S / (2,6·N)) ) ? Que devient-il si le trafic par abonné double ?
# ======================================================================

# ======================================================================
# Q3.7 — Sites tri-sectorisés (1 site = 3 cellules)
# ======================================================================
nb_sites = ceil(nb_cellules_deploy / 3)
print(f"{nb_sites} sites tri-sectorisés")

# ======================================================================
# Q3.8 — Porteuses par cellule et bande réellement utilisée avec K = 7
# ======================================================================
porteuses_par_cellule = canaux_par_cellule
bande_utilisee_MHz = porteuses_par_cellule * K_deploy * espacement_kHz / 1000
print(f"{porteuses_par_cellule} porteuses/cellule ; bande utilisée = {bande_utilisee_MHz:.1f} MHz sur {bande_MHz} MHz")

# ======================================================================
# Synthèse graphique
# ======================================================================
cat = ['Couverture', 'Capacité', 'Déploiement']
val = [nb_cellules_couverture, nb_cellules_capacite, nb_cellules_deploy]
plt.bar(cat, val, color=['skyblue', 'coral', 'lightgreen'], edgecolor='k')
for i, v in enumerate(val): plt.text(i, v + 3, str(v), ha='center', fontweight='bold')
plt.ylabel('Nombre de cellules'); plt.title('Couverture vs capacité'); plt.grid(axis='y', alpha=.3); plt.savefig(f'TP0_fig{_fig[0]}.png', dpi=120); _fig[0]+=1; plt.close()

# ======================================================================
# ---
# ======================================================================
