import os
import yt_dlp
import sys
import shutil

# Versione dell'applicazione
VERSION = "5.1"

# ────────────────────────────────
# FUNZIONI DI SUPPORTO
# ────────────────────────────────

def get_ffmpeg_path():
    """Tenta di trovare il percorso di ffmpeg."""
    # 1. Controlla nel PATH di sistema (usa shutil.which per la massima compatibilità)
    sys_path = shutil.which("ffmpeg")
    if sys_path:
        return sys_path  # Restituisci il path esplicito se trovato nel PATH

    # 2. Controlla percorsi comuni su macOS/Linux (se non in PATH)
    common_paths = [
        "/usr/local/bin/ffmpeg",
        "/opt/homebrew/bin/ffmpeg",
        "/usr/bin/ffmpeg",
        "/bin/ffmpeg"
    ]
    for path in common_paths:
        if os.path.exists(path) and os.access(path, os.X_OK):
            return path

    # 3. Controlla nella directory dell'eseguibile (o root del progetto)
    if getattr(sys, 'frozen', False):
        base_path = os.path.dirname(sys.executable)
    else:
        base_path = os.path.dirname(os.path.abspath(__file__))

    # Cerca ffmpeg (o ffmpeg.exe su Windows)
    potential_ffmpeg = os.path.join(base_path, "ffmpeg")
    if os.path.exists(potential_ffmpeg) or os.path.exists(potential_ffmpeg + ".exe"):
        return potential_ffmpeg

    return False

def check_ffmpeg_availability():
    """Verifica se ffmpeg è disponibile e restituisce True/False."""
    # Se get_ffmpeg_path restituisce un percorso valido, siamo a posto
    if get_ffmpeg_path():
        return True
    return False

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

def extract_playlist_name(url):
    """Estrae il nome della playlist dall'URL, se presente."""
    if "list=" in url:
        try:
            return url.split("list=")[-1].split("&")[0]
        except:
            pass
    return "single_video"

# ────────────────────────────────
# LOGGER & HOOKS
# ────────────────────────────────

class MyLogger:
    """Logger personalizzato per filtrare warning non critici."""
    def debug(self, msg):
        pass

    def warning(self, msg):
        ignored_warnings = [
            "No supported JavaScript runtime could be found",
            "forcing SABR streaming",
            "missing a url",
        ]
        if any(w in msg for w in ignored_warnings):
            return
        print(f"⚠️  WARNING: {msg}")

    def error(self, msg):
        print(f"❌ ERROR: {msg}")

def make_progress_hook(callback):
    """Crea una funzione hook che invoca la callback con lo stato."""
    def hook(d):
        if d['status'] == 'downloading':
            percent = d.get('_percent_str', '').strip()
            speed = d.get('_speed_str', '').strip()
            eta = d.get('_eta_str', '').strip()
            msg = f"⬇️  {percent} | {speed} | ETA: {eta}"
            if callback:
                callback(msg)
        elif d['status'] == 'finished':
            msg = "✅ Download completato, elaborazione..."
            if callback:
                callback(msg)
    return hook

# ────────────────────────────────
# FUNZIONI DI DOWNLOAD
# ────────────────────────────────

def get_download_path(subfolder):
    """Restituisce il percorso di download appropriato (Cartella Download utente o locale)."""
    # Usa la cartella Downloads dell'utente come base predefinita per facilitare l'accesso
    base_dir = os.path.join(os.path.expanduser("~"), "Downloads", "YouTubeDownloader")
    return os.path.join(base_dir, subfolder)

def download_yt_video(url, playlist_name, progress_callback=None):
    """Scarica video o playlist in formato MP4 fino a 1080p."""
    video_dir = os.path.join(get_download_path('video'), clean_filename(playlist_name))
    create_directory(video_dir)

    ydl_opts = {
        'format': 'bestvideo[height<=1080][ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]',
        'outtmpl': os.path.join(video_dir, '%(title).100s.%(ext)s'),
        'noplaylist': False,
        'ignoreerrors': True,
        'nocheckcertificate': True,
        'merge_output_format': 'mp4',
        'player_client': 'android',
        'concurrent_fragment_downloads': 4, # Parallelizza il download dei frammenti
        'postprocessors': [{
            'key': 'FFmpegVideoConvertor',
            'preferedformat': 'mp4',
        }],
        'logger': MyLogger(),
        'progress_hooks': [make_progress_hook(progress_callback)] if progress_callback else []
    }

    # Aggiungi ffmpeg_location se trovato localmente
    ffmpeg_loc = get_ffmpeg_path()
    if ffmpeg_loc:
        ydl_opts['ffmpeg_location'] = ffmpeg_loc

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        if progress_callback:
            progress_callback(f"Inizio download video in: {video_dir}")
        ydl.download([url])

def download_yt_audio(url, playlist_name, progress_callback=None):
    """Scarica solo audio in formato MP3 (192 kbps)."""
    audio_dir = os.path.join(get_download_path('audio'), clean_filename(playlist_name))
    create_directory(audio_dir)

    ydl_opts = {
        'format': 'bestaudio/best',
        'outtmpl': os.path.join(audio_dir, '%(title).100s.%(ext)s'),
        'noplaylist': False,
        'ignoreerrors': True,
        'nocheckcertificate': True,
        'player_client': 'android',
        'concurrent_fragment_downloads': 4, # Parallelizza il download dei frammenti
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }],
        'logger': MyLogger(),
        'progress_hooks': [make_progress_hook(progress_callback)] if progress_callback else []
    }

    # Aggiungi ffmpeg_location se trovato localmente
    ffmpeg_loc = get_ffmpeg_path()
    if ffmpeg_loc:
        ydl_opts['ffmpeg_location'] = ffmpeg_loc

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        if progress_callback:
            progress_callback(f"Inizio download audio in: {audio_dir}")
        ydl.download([url])
