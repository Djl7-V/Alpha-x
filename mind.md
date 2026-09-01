# Alpha-X — Téléchargeur Vidéo & Audio (Plan du projet)

## Idée
Outil en ligne de commande (CLI) et interface web pour télécharger des vidéos et audio depuis YouTube, TikTok, Instagram, Twitter/X, Facebook, et 100+ plateformes. Simple, pro, open source.

## Objectifs
- Télécharger des vidéos en **MP4** (vidéo) depuis n'importe quelle plateforme
- Extraire l'audio en **MP3** depuis n'importe quelle plateforme
- Interface CLI colorée + interface web glassmorphism
- Code propre, structuré et maintenable
- Prêt pour GitHub (README, licence, .gitignore)

## Plateformes supportées
YouTube, TikTok, Instagram, Twitter/X, Facebook, Twitch, Vimeo, Dailymotion, Reddit, Bilibili, Pinterest, SoundCloud, et 100+ autres (via yt-dlp).

## Fonctionnalités
1. **Multi-plateformes** : toute URL supportée par yt-dlp
2. **Choix du format** : MP4 (vidéo) ou MP3 (audio)
3. **Choix de la qualité** : meilleure / économique
4. **Barre de progression** : en temps réel (CLI + web)
5. **Interface web** : glassmorphism dark avec Flask + Tailwind
6. **Gestion des erreurs** : messages clairs, pas de crash
7. **Boucle interactive** : télécharger plusieurs liens sans relancer

## Structure du projet
```
yt/
├── loads.py           # CLI principal (Alpha-X terminal)
├── app.py             # Flask backend (interface web)
├── templates/
│   ├── base.html      # layout + JS polling
│   └── index.html     # landing glassmorphism
├── requirements.txt   # dépendances (yt-dlp, flask)
├── README.md          # doc d'installation + usage
├── LICENSE            # licence MIT
├── .gitignore         # fichiers à ignorer
└── mind.md            # ce fichier
```

## Améliorations futures
- Téléchargement en lot (fichier `.txt` d'URLs)
- Support des playlists complètes
- Options en ligne de commande (`alpha-x <url> --format mp3`)
- Détection automatique de la plateforme avec affichage
