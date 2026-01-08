import tkinter as tk
from tkinter import ttk, messagebox
import threading
import core
import sys
import os

def resource_path(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)

class DownloaderApp:
    def __init__(self, root):
        self.root = root
        self.root.title(f"YouTube Downloader v{core.VERSION}")
        self.root.geometry("450x300")
        self.root.resizable(False, False)

        try:
            # Load icon handling PyInstaller path
            icon_path = resource_path("icon.png")
            img = tk.PhotoImage(file=icon_path)
            self.root.iconphoto(False, img)
        except Exception:
            pass

        # Title and Subtitle
        self.title_label = ttk.Label(root, text="YouTube Downloader", font=("Helvetica", 16, "bold"))
        self.title_label.pack(pady=(10, 0))

        self.subtitle_label = ttk.Label(root, text="Un programma di Mauro Marzocca", font=("Helvetica", 10, "italic"))
        self.subtitle_label.pack(pady=(0, 10))
        
        self.subtitle_label = ttk.Label(root, text="Versione 5.1", font=("Helvetica", 10, "italic"))
        self.subtitle_label.pack(pady=(0, 10))

        # URL Input
        self.url_label = ttk.Label(root, text="URL:")
        self.url_label.pack(pady=(5, 5))

        self.url_entry = ttk.Entry(root, width=50)
        self.url_entry.pack(pady=5, padx=20)

        # Radio buttons
        self.download_type = tk.StringVar(value="v")

        frame_radio = ttk.Frame(root)
        frame_radio.pack(pady=10)

        self.rb_video = ttk.Radiobutton(frame_radio, text="VIDEO", variable=self.download_type, value="v")
        self.rb_video.pack(side=tk.LEFT, padx=10)

        self.rb_audio = ttk.Radiobutton(frame_radio, text="AUDIO", variable=self.download_type, value="a")
        self.rb_audio.pack(side=tk.LEFT, padx=10)

        # Download Button
        self.btn_download = ttk.Button(root, text="Download", command=self.start_download)
        self.btn_download.pack(pady=10)

        # Status Label
        self.status_var = tk.StringVar(value="Status: In attesa")
        self.lbl_status = ttk.Label(root, textvariable=self.status_var)
        self.lbl_status.pack(pady=10)

        # Check FFmpeg on startup
        self.check_dependencies()

    def check_dependencies(self):
        """Verifica le dipendenze (FFmpeg) all'avvio."""
        if not core.check_ffmpeg_availability():
            messagebox.showwarning(
                "FFmpeg mancante",
                "Attenzione: FFmpeg non è stato trovato.\n\n"
                "Senza FFmpeg, i video scaricati potrebbero non essere uniti (video/audio separati) "
                "o convertiti nel formato corretto (MP4/MP3).\n\n"
                "Per risolvere, installa FFmpeg o posiziona l'eseguibile nella cartella dell'app."
            )
            self.update_status("⚠️ FFmpeg non trovato")

    def update_status(self, message):
        """Updates the status label. Thread-safe."""
        self.root.after(0, lambda: self.status_var.set(f"Status: {message}"))

    def start_download(self):
        url = self.url_entry.get().strip()
        if not url:
            messagebox.showerror("Errore", "Inserisci un URL valido.")
            return

        choice = self.download_type.get()

        # Disable button during download
        self.btn_download.config(state=tk.DISABLED)
        self.update_status("Avvio download...")

        # Run download in a separate thread
        thread = threading.Thread(target=self.run_download, args=(url, choice))
        thread.daemon = True
        thread.start()

    def run_download(self, url, choice):
        try:
            playlist_name = core.extract_playlist_name(url)

            if choice == 'v':
                core.download_yt_video(url, playlist_name, progress_callback=self.update_status)
            else:
                core.download_yt_audio(url, playlist_name, progress_callback=self.update_status)

            self.update_status("100% - Completato!")
            self.root.after(0, lambda: messagebox.showinfo("Fatto", "Download completato!"))
        except Exception as e:
            self.update_status("Errore")
            self.root.after(0, lambda: messagebox.showerror("Errore", str(e)))
        finally:
            self.root.after(0, lambda: self.btn_download.config(state=tk.NORMAL))

def run_gui():
    root = tk.Tk()
    app = DownloaderApp(root)
    root.mainloop()

if __name__ == "__main__":
    run_gui()
