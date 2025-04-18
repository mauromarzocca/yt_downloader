import os
import yt_dlp

def create_directory(path):
    if not os.path.exists(path):
        os.makedirs(path)

def download_yt_video(url, playlist_name):
    video_dir = os.path.join('download', 'video', playlist_name)
    create_directory(video_dir)

    ydl_opts = {
        'format': 'bestvideo[height<=1080]+bestaudio/best',  # Scarica video e audio migliori e li unisce
        'outtmpl': os.path.join(video_dir, '%(title)s.%(ext)s'),
        'noplaylist': False,
        'ignoreerrors': True,
        'merge_output_format': 'mp4',  # Converte il file finale in MP4
        'postprocessors': [{
            'key': 'FFmpegVideoConvertor',
            'preferedformat': 'mp4',
        }],
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        ydl.download([url])

def download_yt_audio(url, playlist_name):
    audio_dir = os.path.join('download', 'audio', playlist_name)
    create_directory(audio_dir)

    ydl_opts = {
        'format': 'bestaudio/best',
        'outtmpl': os.path.join(audio_dir, '%(title)s.%(ext)s'),
        'noplaylist': False,
        'ignoreerrors': True,
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }],
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        ydl.download([url])

if __name__ == "__main__":
    print("Version 2.0")
    choice = input("Vuoi scaricare video o audio? (v/a): ").strip().lower()
    video_url = input("Inserisci l'URL del video o della playlist di YouTube: ")

    playlist_name = video_url.split('list=')[-1] if 'list=' in video_url else 'single_video'

    if choice == 'v':
        download_yt_video(video_url, playlist_name)
    elif choice == 'a':
        download_yt_audio(video_url, playlist_name)
    else:
        print("Scelta non valida. Per favore, scegli 'v' per video o 'a' per audio.")