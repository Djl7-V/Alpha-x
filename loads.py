#!/usr/bin/env python3
"""Alpha-X — Téléchargeur de vidéos et audio.

Outil CLI basé sur yt-dlp pour télécharger des vidéos/audio
depuis YouTube, TikTok, Instagram, Twitter/X, Facebook, et 100+ plateformes.
En MP4 (vidéo) ou MP3 (audio).
"""

import sys
from pathlib import Path

import yt_dlp

DOWNLOAD_DIR = Path("downloads")

BAR_WIDTH = 30

# -- Couleurs ANSI --
RESET = "\033[0m"
BOLD = "\033[1m"
DIM = "\033[2m"
CYAN = "\033[36m"
GREEN = "\033[32m"
RED = "\033[31m"
YELLOW = "\033[33m"
WHITE = "\033[97m"
BG_CYAN = "\033[46m"
BG_DARK = "\033[48;5;236m"

BANNER = f"""{CYAN}{BOLD}
              /\\
             /  \\
            /    \\
           / /\\ /\\
          / /  V  \\
         / /       \\
        / /  \\   /  \\
       /_/    \\_/    \\_\\
{RESET}{DIM}       |  ALPHA - X  |
{RESET}"""

DIVIDER = f"{DIM}{'─' * 44}{RESET}"
CORNER_TL = "╭"
CORNER_TR = "╮"
CORNER_BL = "╰"
CORNER_BR = "╯"
LINE_H = "─"
LINE_V = "│"


def box(lines: list[str], width: int = 44) -> str:
    """Dessine une boîte avec des bordures unicode."""
    top = f"{CYAN}{CORNER_TL}{LINE_H * (width - 2)}{CORNER_TR}{RESET}"
    bottom = f"{CYAN}{CORNER_BL}{LINE_H * (width - 2)}{CORNER_BR}{RESET}"
    content = ""
    for line in lines:
        padded = line.ljust(width - 4)
        content += f"{CYAN}{LINE_V}{RESET} {padded} {CYAN}{LINE_V}{RESET}\n"
    return f"{top}\n{content}{bottom}"


def format_size(nbytes: float) -> str:
    """Formate une taille en octets."""
    for unit in ("o", "Ko", "Mo", "Go"):
        if nbytes < 1024 or unit == "Go":
            return f"{nbytes:.1f} {unit}"
        nbytes /= 1024
    return f"{nbytes:.1f} Go"


def progress_hook(d: dict) -> None:
    """Barre de progression colorée."""
    status = d.get("status")

    if status == "downloading":
        total = d.get("total_bytes") or d.get("total_bytes_estimate") or 0
        done = d.get("downloaded_bytes", 0)
        speed = d.get("speed")
        eta = d.get("eta")

        if total:
            pct = done / total
            filled = int(BAR_WIDTH * pct)
            empty = BAR_WIDTH - filled
            bar = f"{CYAN}{'█' * filled}{DIM}{'░' * empty}{RESET}"
            speed_txt = f" {DIM}│{RESET} {CYAN}{format_size(speed)}/s{RESET}" if speed else ""
            eta_txt = f" {DIM}│{RESET} {YELLOW}{eta}s{RESET}" if eta is not None else ""
            line = f"\r  {bar} {WHITE}{pct:5.1%}{RESET}{speed_txt}{eta_txt}"
        else:
            line = f"\r  {DIM}{format_size(done)} téléchargés...{RESET}"

        sys.stdout.write(line)
        sys.stdout.flush()

    elif status == "finished":
        sys.stdout.write(f"\r{' ' * 79}\r")
        print(f"  {GREEN}✓{RESET} Téléchargement terminé, conversion...")


def build_video_opts(quality: str, output_dir: Path) -> dict:
    selector = "bv*[ext=mp4]+ba[ext=m4a]/b[ext=mp4]/bv*+ba/b"
    if quality == "worst":
        selector = "wv*[ext=mp4]+wa[ext=m4a]/w[ext=mp4]/wv*+wa/w"
    return {
        "format": selector,
        "merge_output_format": "mp4",
        "outtmpl": str(output_dir / "%(title)s.%(ext)s"),
        "noplaylist": True,
        "quiet": True,
        "no_warnings": True,
        "progress_hooks": [progress_hook],
    }


def build_audio_opts(quality: str, output_dir: Path) -> dict:
    return {
        "format": "ba/wa" if quality == "worst" else "ba",
        "postprocessors": [{
            "key": "FFmpegExtractAudio",
            "preferredcodec": "mp3",
            "preferredquality": "192",
        }],
        "outtmpl": str(output_dir / "%(title)s.%(ext)s"),
        "noplaylist": True,
        "quiet": True,
        "no_warnings": True,
        "progress_hooks": [progress_hook],
    }


def download(url: str, fmt: str, quality: str, output_dir: Path) -> None:
    opts = build_video_opts(quality, output_dir) if fmt == "mp4" else build_audio_opts(quality, output_dir)

    with yt_dlp.YoutubeDL(opts) as ydl:
        info = ydl.extract_info(url, download=True)
        title = info.get("title", url)
        size_info = ""
        if fmt == "mp4":
            size_info = f" {DIM}({info.get('duration', '?')}s){RESET}"
        print(f"\n  {GREEN}✓{RESET} {WHITE}{title}{RESET}{size_info}")
        print(f"    {DIM}→ {output_dir}/{RESET} ({CYAN}{fmt.upper()}{RESET})")


def ask_choice(prompt: str, choices: dict) -> str:
    print(f"\n  {CYAN}◆{RESET} {prompt}")
    for key, (_, label) in choices.items():
        print(f"    {DIM}[{RESET}{WHITE}{key}{RESET}{DIM}]{RESET} {label}")
    while True:
        answer = input(f"  {CYAN}▸{RESET} ").strip()
        if answer in choices:
            return choices[answer][0]
        print(f"    {RED}✗{RESET} Choix invalide")


def main() -> None:
    print(BANNER)
    print(box([
        f"{WHITE}{BOLD}Alpha-X{RESET} {DIM}— Téléchargeur Vidéo & Audio{RESET}",
        f"{DIM}YouTube • TikTok • Instagram • X • 100+ plateformes{RESET}",
    ]))
    print()

    DOWNLOAD_DIR.mkdir(exist_ok=True)

    while True:
        url = input(f"  {CYAN}◆{RESET} Lien vidéo/audio ({DIM}q{RESET} = quitter) : ").strip()

        if not url:
            continue
        if url.lower() == "q":
            print(f"\n  {DIM}À bientôt !{RESET}\n")
            break

        if not url.startswith("http"):
            print(f"  {RED}✗{RESET} Lien invalide (commence par http/https)\n")
            continue

        fmt = ask_choice("Format :", {"1": ("mp4", "Vidéo (MP4)"), "2": ("mp3", "Audio (MP3)")})
        quality = ask_choice("Qualité :", {
            "1": ("best", "Meilleure qualité"),
            "2": ("worst", "Économiser"),
        })

        print(f"\n  {DIM}Téléchargement en cours...{RESET}\n")

        try:
            download(url, fmt, quality, DOWNLOAD_DIR)
        except yt_dlp.utils.DownloadError as e:
            print(f"  {RED}✗{RESET} {e}")
        except KeyboardInterrupt:
            print(f"\n  {YELLOW}⏸{RESET} Annulé.")
        except Exception as e:
            print(f"  {RED}✗{RESET} Erreur : {e}")

        print()


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print(f"\n\n  {DIM}À bientôt !{RESET}\n")
        sys.exit(0)
