import os
import yt_dlp
import sys

# ────────────────────────────────
# FUNZIONI DI SUPPORTO
# ────────────────────────────────

def create_directory(path):
    """Crea la cartella se non esiste."""
    if not os.path.exists(path):
        os.makedirs(path)

def clean_filename(name, max_length=100):
    """Pulisce il nome del file da caratteri non validi e lo tronca se troppo lungo."""
    invalid_chars = r'<>:"/\|?*'
    for ch in invalid_chars:
        name = name.replace(ch, '_')
    return name[:max_length]

# ────────────────────────────────
# FUNZIONE DI STATO (barra di avanzamento)
# ────────────────────────────────

def progress_hook(d):
    """Mostra lo stato del download in tempo reale."""
    if d['status'] == 'downloading':
        percent = d.get('_percent_str', '').strip()
        speed = d.get('_speed_str', '').strip()
        eta = d.get('_eta_str', '').strip()
        sys.stdout.write(f"\r⬇️  {percent} | {speed} | ETA: {eta}   ")
        sys.stdout.flush()
    elif d['status'] == 'finished':
        print("\n✅ Download completato, sto unendo i file...\n")

# ────────────────────────────────
# FUNZIONI DI DOWNLOAD
# ────────────────────────────────

def download_yt_video(url, playlist_name):
    """Scarica video o playlist in formato MP4 fino a 1080p."""
    video_dir = os.path.join('download', 'video', clean_filename(playlist_name))
    create_directory(video_dir)

    ydl_opts = {
        'format': 'bestvideo[height<=1080][ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]',
        'outtmpl': os.path.join(video_dir, '%(title).100s.%(ext)s'),
        'noplaylist': False,
        'ignoreerrors': True,
        'merge_output_format': 'mp4',
        'player_client': 'android',  # Evita bug nsig/SSAP
        'postprocessors': [{
            'key': 'FFmpegVideoConvertor',
            'preferedformat': 'mp4',
        }],
        'progress_hooks': [progress_hook]
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        print(f"\n🎬 Inizio download video in: {video_dir}\n")
        ydl.download([url])


def download_yt_audio(url, playlist_name):
    """Scarica solo audio in formato MP3 (192 kbps)."""
    audio_dir = os.path.join('download', 'audio', clean_filename(playlist_name))
    create_directory(audio_dir)

    ydl_opts = {
        'format': 'bestaudio/best',
        'outtmpl': os.path.join(audio_dir, '%(title).100s.%(ext)s'),
        'noplaylist': False,
        'ignoreerrors': True,
        'player_client': 'android',
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }],
        'progress_hooks': [progress_hook]
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        print(f"\n🎵 Inizio download audio in: {audio_dir}\n")
        ydl.download([url])

# ────────────────────────────────
# BLOCCO PRINCIPALE CON LOOP
# ────────────────────────────────

def main():
    """Loop principale del programma."""
    print("=== YouTube Downloader v3.1 ===")
    print("Aggiorna yt-dlp con: python3 -m pip install -U yt-dlp\n")

    while True:
        try:
            choice = input("Vuoi scaricare video o audio? (v/a): ").strip().lower()
            if choice not in ('v', 'a'):
                print("❌ Scelta non valida. Usa 'v' per video o 'a' per audio.\n")
                continue

            video_url = input("Inserisci l'URL del video o della playlist di YouTube: ").strip()
            if not video_url:
                print("❌ URL non valido.\n")
                continue

            playlist_name = "single_video"
            if "list=" in video_url:
                playlist_name = video_url.split("list=")[-1].split("&")[0]

            if choice == 'v':
                download_yt_video(video_url, playlist_name)
            else:
                download_yt_audio(video_url, playlist_name)

            print("\n🎉 Download completato!\n")
        except Exception as e:
            print(f"\n❌ Errore durante il download: {e}\n")

        again = input("Vuoi scaricare un altro video/audio? (s/n): ").strip().lower()
        if again != 's':
            print("\n👋 Uscita dal programma. Alla prossima!\n")
            break


if __name__ == "__main__":
    main()