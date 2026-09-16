# Environnement Docker TP 4G/5G — guide enseignant

## Contenu de l'image
| Composant | Version | Rôle |
|---|---|---|
| Ubuntu | 22.04 | base |
| OMNeT++ | 6.1.0 (headless, sans IDE ni Qtenv) | moteur de simulation |
| INET | 4.5.4 | pile TCP/IP, mobilité, radio |
| Simu5G | 1.3.0 | LTE / NR : eNB, gNB, UE, schedulers, numérologies, DC, MEC, D2D |
| Python | 3.10 + pandas, matplotlib, JupyterLab | analyse des résultats |

Simu5G 1.3.0 demande OMNeT++ ≥ 6.0.3 et INET ≥ 4.5 ; les versions ci-dessus sont figées dans le `Dockerfile` (`ARG`), vous pouvez les changer à un seul endroit.

Scripts ajoutés dans l'image (`/usr/local/bin`) :
- `tp-run <Config> [0..N]` : lance une config du `omnetpp.ini` courant en Cmdenv, runs en parallèle (`opp_runall`).
- `tp-export [dir] [out.csv]` : exporte les scalaires en CSV long (`opp_scavetool`).
- `tp-export-vec <nom> [dir] [out.csv]` : idem pour les vecteurs.

## Construire et publier (à faire une fois)
```bash
docker build -t tp5g:2026 .              # 30-45 min selon la machine, image ≈ 4 Go
docker run --rm tp5g:2026 simu5g -h      # vérification rapide
# publication sur GitHub Container Registry (ou le registre UVSQ/Harbor si disponible)
docker tag tp5g:2026 ghcr.io/<votre-org>/tp5g:2026
docker push ghcr.io/<votre-org>/tp5g:2026
```
Puis mettez le nom d'image dans `docker-compose.yml` et distribuez aux étudiants le dossier `tp/` + `docker-compose.yml` (un zip ou un dépôt Git). Ils n'ont **pas** besoin du Dockerfile.

Le `Dockerfile` contient un test de fumée (1 s de la simu `LTE/tutorial`) : si le build passe, la chaîne complète fonctionne.

## Choix de conception
- **Pas d'IDE Eclipse, pas de Qtenv** : tout se fait par `.ini` + ligne de commande + notebook. Ça tourne sur Docker Desktop (Windows/WSL2, macOS Intel et Apple Silicon via émulation amd64, Linux), c'est reproductible, et le notebook fait office de compte-rendu. Si vous voulez une séance avec visualisation, ajoutez un service noVNC + `WITH_QTENV=yes` (compte ~1,5 Go de plus).
- Les TP sont **montés en volume** (`./tp:/tp`) : le travail des étudiants reste sur leur disque même si le conteneur est supprimé.
- Les réseaux `.ned` d'exemple de Simu5G sont accessibles via `-n` (script `simu5g`), donc un `.ini` de TP peut référencer `simu5g.simulations.LTE.networks.SingleCell` sans copier de fichier.

## Structure du dossier `tp/`
```
tp/
├── common/tpanalyse.py            # chargement CSV-R -> pandas, KPI par run
└── TP2_prise_en_main/
    ├── TP2_sujet.md               # sujet étudiant
    ├── omnetpp.ini                # configs : SingleCell-DL/UL, Charge-DL, Mobile-DL
    ├── demo.xml                   # adressage IPv4 (configurator)
    └── TP2_analyse.ipynb          # squelette de compte-rendu
```
Les TP suivants (TP3 scheduling, TP4 handover, TP5 numérologie, TP6 DC/MEC, TP7 V2X, TP8 RL) suivront le même gabarit : un `.ini` avec des `${var=...}` pour les balayages, un notebook, un sujet.

## Corrigé TP2 — repères attendus
- Ex.1 Q4 : ~40 B / 20 ms ≈ 16 kbit/s applicatif (≈ 30-40 kbit/s avec en-têtes RTP/UDP/IP + RLC/MAC) ; 25 RB × ~150 kbit/s ≈ 3,75 Mbit/s → ordre de grandeur 100 flux VoIP simultanés à 5 MHz, hors gain de suppression de silence.
- Ex.3 : le délai reste plat (quelques ms) tant que la cellule n'est pas saturée puis explose ; la perte suit. Le point de rupture se déplace quasi proportionnellement à `numBands`. Les UE en bord de zone (mauvais CQI) décrochent d'abord avec MAXCI.
- Ex.4 : à ces vitesses et avec `StationaryMobility`→`LinearMobility` dans une seule cellule, l'effet est faible (variation de CQI, quelques retransmissions HARQ). Le vrai effet vient avec 2 eNB + X2 (TP4).
- Ex.5 UL : saturation plus précoce (puissance UE limitée, scheduler UL par allocation contiguë).

## Pièges connus
- `numUEs` grand (≥150) + `vector-recording = true` → fichiers `.vec` de plusieurs centaines de Mo. Le laisser à `false` par défaut.
- Sur Apple Silicon, l'image amd64 tourne en émulation : 3-5× plus lent. Réduire `sim-time-limit` ou le balayage pour ces machines.
- `opp_runall -j` utilise tous les cœurs : sur un portable, ajouter `-j2` dans `tp-run` si ça chauffe.
