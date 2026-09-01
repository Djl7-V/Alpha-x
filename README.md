# Alpha-X — Téléchargeur Vidéo & Audio

Outil en ligne de commande simples et gratuit pour télécharger des vidéos et audio en **MP4** (vidéo) ou **MP3** (audio) depuis YouTube, TikTok, Instagram, X, Facebook et 100+ plateformes.

Basé sur [yt-dlp](https://github.com/yt-dlp/yt-dlp) — nécessite [FFmpeg](https://ffmpeg.org/) pour l'extraction audio.

## Installation

```bash
git clone https://github.com/<ton-compte>/alpha-x.git
cd alpha-x
pip install -r requirements.txt
```

> FFmpeg doit être installé sur ton système (`sudo apt install ffmpeg` sous Debian/Ubuntu).

## Utilisation

```bash
python loads.py
```

Puis suis les instructions :

1. Colle un lien vidéo/audio (n'importe quelle plateforme, `q` pour quitter)
2. Choisis le format : `1` = MP4 (vidéo), `2` = MP3 (audio)
3. Choisis la qualité : meilleure ou pire

Les fichiers sont enregistrés dans le dossier `downloads/`.

## ⚠️ Avertissement légal

Cet outil est **uniquement destiné à un usage personnel et privé** (vidéos que vous possédez ou pour lesquelles vous avez l'autorisation). Le téléchargement peut être soumis à des **restrictions des plateformes** et à la **législation sur les droits d'auteur** de votre pays. Il est de votre responsabilité de vous conformer aux conditions d'utilisation des sites et aux lois applicables. Ce projet est fourni à titre éducatif — l'auteur décline toute responsabilité en cas de mauvaise utilisation.

## Fonctionnalités

- Téléchargement vidéo MP4 (meilleure/pire qualité) depuis 100+ plateformes
- Extraction audio MP3
- Téléchargement en lot : plusieurs liens sans relancer
- Gestion des erreurs (lien invalide, réseau, vidéo indisponible)

## Licence

[MIT](LICENSE)

---

_Créé par **DJL & FA-G**._