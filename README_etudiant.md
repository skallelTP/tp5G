# TP 4G/5G — mise en place de l'environnement (10 min)

## 1. Installer Docker
- Windows 10/11 : Docker Desktop + WSL2 (activer « Use the WSL 2 based engine »).
- macOS : Docker Desktop (sur puce Apple, cochez « Use Rosetta for x86/amd64 emulation »).
- Linux : `sudo apt install docker.io docker-compose-v2` puis ajoutez-vous au groupe `docker`.

## 2. Récupérer le dossier des TP
Décompressez l'archive fournie (ou `git clone …`). Vous obtenez :
```
tp5g/
├── docker-compose.yml
└── tp/            <- vos fichiers de TP, ils restent sur votre disque
```

## 3. Démarrer
```bash
cd tp5g
docker compose pull      # une seule fois, ≈ 4 Go
docker compose up        # démarre JupyterLab
```
Ouvrez http://localhost:8888 dans votre navigateur. Le dossier `tp/` apparaît dans l'explorateur de gauche.

Pour un terminal dans l'environnement de simulation : dans JupyterLab, **File → New → Terminal**, ou depuis votre machine :
```bash
docker compose run --rm simu5g bash
```

## 4. Commandes utiles (dans le terminal du conteneur)
```bash
cd /tp/TP2_prise_en_main
tp-run SingleCell-DL              # lance la config SingleCell-DL, run 0
tp-run Charge-DL 0..4             # runs 0 à 4 (balayage de paramètres)
tp-export results results.csv     # convertit les résultats en CSV pour le notebook
simu5g -u Cmdenv -c SingleCell-DL -x   # liste les runs d'une config sans simuler
```

## 5. Arrêter
`Ctrl+C` dans le terminal où tourne `docker compose up`, puis `docker compose down`. Vos fichiers dans `tp/` sont conservés.

## Dépannage
| Symptôme | Solution |
|---|---|
| `port 8888 already in use` | changez `"8888:8888"` en `"8889:8888"` dans `docker-compose.yml` |
| Le notebook ne trouve pas `results.csv` | vous avez lancé `tp-export` depuis le mauvais dossier ; vérifiez `pwd` |
| Simulation très lente | réduisez `sim-time-limit` dans le `.ini` ou le nombre de runs |
| `Error: Cannot load library libINET` | l'image est corrompue : `docker compose pull` puis relancez |
