import tkinter as tk
from tkinter import ttk, messagebox, filedialog
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
        self.root.geometry("600x600") # Increased height
        self.root.resizable(False, False)

        self.custom_download_path = None
        self.video_resolutions = []

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
        self.subtitle_label.pack(pady=(0, 5))
        
        self.version_label = ttk.Label(root, text=f"Versione {core.VERSION}", font=("Helvetica", 10, "italic"))
        self.version_label.pack(pady=(0, 10))

        # URL Input
        self.url_frame = ttk.LabelFrame(root, text="1. Inserisci URL e Analizza")
        self.url_frame.pack(pady=5, padx=10, fill="x")

        self.url_entry = ttk.Entry(self.url_frame, width=40)
        self.url_entry.pack(side=tk.LEFT, padx=(10, 5), pady=10, expand=True, fill="x")
        
        self.btn_analyze = ttk.Button(self.url_frame, text="🔍 Analizza", command=self.analyze_url)
        self.btn_analyze.pack(side=tk.LEFT, padx=(0, 10), pady=10)

        # Settings Frame (Resolution & Type)
        self.settings_frame = ttk.LabelFrame(root, text="2. Opzioni di Download")
        self.settings_frame.pack(pady=5, padx=10, fill="x")

        # Radio buttons
        self.download_type = tk.StringVar(value="v")
        
        self.rb_frame = ttk.Frame(self.settings_frame)
        self.rb_frame.pack(pady=5, fill="x")
        
        ttk.Label(self.rb_frame, text="Tipo:").pack(side=tk.LEFT, padx=10)
        
        self.rb_video = ttk.Radiobutton(self.rb_frame, text="VIDEO (MP4)", variable=self.download_type, value="v", command=self.toggle_resolution_state)
        self.rb_video.pack(side=tk.LEFT, padx=5)

        self.rb_audio = ttk.Radiobutton(self.rb_frame, text="AUDIO (MP3)", variable=self.download_type, value="a", command=self.toggle_resolution_state)
        self.rb_audio.pack(side=tk.LEFT, padx=5)

        # Resolution Combobox
        self.res_frame = ttk.Frame(self.settings_frame)
        self.res_frame.pack(pady=5, fill="x")
        
        ttk.Label(self.res_frame, text="Risoluzione:").pack(side=tk.LEFT, padx=10)
        
        self.combo_res = ttk.Combobox(self.res_frame, state="disabled", width=25)
        self.combo_res.pack(side=tk.LEFT, padx=5)
        self.combo_res.set("Analizza URL prima...")

        # Path Frame
        self.path_frame = ttk.LabelFrame(root, text="3. Percorso di Salvataggio")
        self.path_frame.pack(pady=5, padx=10, fill="x")

        self.lbl_path = ttk.Label(self.path_frame, text="Default (Downloads)", foreground="gray")
        self.lbl_path.pack(side=tk.LEFT, padx=10, pady=10, fill="x", expand=True)
        
        self.btn_browse = ttk.Button(self.path_frame, text="Sfoglia...", command=self.browse_path)
        self.btn_browse.pack(side=tk.RIGHT, padx=10, pady=10)

        # Download Button
        self.btn_download = ttk.Button(root, text="AVVIA DOWNLOAD", command=self.start_download, state="disabled")
        self.btn_download.pack(pady=15, ipady=5)

        # Status Label
        self.status_var = tk.StringVar(value="Status: In attesa")
        self.lbl_status = ttk.Label(root, textvariable=self.status_var, relief=tk.SUNKEN, anchor=tk.W)
        self.lbl_status.pack(side=tk.BOTTOM, fill="x", padx=0, pady=0)

        # Check FFmpeg on startup
        self.check_dependencies()
        
        # Check updates in background
        self.root.after(2000, self.start_update_check)

    def start_update_check(self):
        thread = threading.Thread(target=self.check_updates_thread)
        thread.daemon = True
        thread.start()

    def check_updates_thread(self):
        update_info = core.check_for_updates()
        if update_info:
            self.root.after(0, lambda: self.show_update_dialog(update_info))

    def show_update_dialog(self, info):
        dialog = tk.Toplevel(self.root)
        dialog.title("Aggiornamento Disponibile")
        dialog.geometry("500x400")
        dialog.transient(self.root)
        dialog.grab_set()

        # Header
        lbl_header = ttk.Label(
            dialog, 
            text=f"Nuova versione {info['version']} disponibile!", 
            font=("Helvetica", 14, "bold"),
            foreground="green"
        )
        lbl_header.pack(pady=15)

        # Changelog area
        frame_text = ttk.Frame(dialog)
        frame_text.pack(expand=True, fill="both", padx=20, pady=5)
        
        lbl_new = ttk.Label(frame_text, text="Novità:", font=("Helvetica", 10, "bold"))
        lbl_new.pack(anchor="w")

        text_area = tk.Text(frame_text, height=10, width=50, wrap="word", font=("Courier", 10))
        text_area.insert("1.0", info['changelog'])
        text_area.config(state="disabled")
        
        scrollbar = ttk.Scrollbar(frame_text, orient="vertical", command=text_area.yview)
        text_area['yscrollcommand'] = scrollbar.set
        
        text_area.pack(side="left", expand=True, fill="both")
        scrollbar.pack(side="right", fill="y")

        # Buttons
        btn_frame = ttk.Frame(dialog)
        btn_frame.pack(pady=20, fill="x")

        def open_browser():
            import webbrowser
            if info['url']:
                webbrowser.open(info['url'])
            dialog.destroy()

        ttk.Button(btn_frame, text="Scarica Aggiornamento", command=open_browser).pack(side="left", expand=True, padx=10)
        ttk.Button(btn_frame, text="Ignora", command=dialog.destroy).pack(side="right", expand=True, padx=10)

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
    
    def toggle_download_button(self, state=True):
        state_val = tk.NORMAL if state else tk.DISABLED
        self.root.after(0, lambda: self.btn_download.config(state=state_val))

    def toggle_resolution_state(self):
        """Abilità/Disabilita combobox in base al tipo download."""
        if self.download_type.get() == 'v':
            if self.video_resolutions:
                self.combo_res.config(state="readonly")
            else:
                self.combo_res.config(state="disabled")
                self.combo_res.set("Analizza URL prima...")
        else:
            self.combo_res.config(state="disabled")
            self.combo_res.set("Non necessaria per Audio")

    def browse_path(self):
        path = filedialog.askdirectory()
        if path:
            self.custom_download_path = path
            # Tronca path lunghi per display
            display_path = path if len(path) < 40 else "..." + path[-37:]
            self.lbl_path.config(text=display_path, foreground="black")
        else:
            self.custom_download_path = None
            self.lbl_path.config(text="Default (Downloads)", foreground="gray")

    def analyze_url(self):
        url = self.url_entry.get().strip()
        if not url:
            messagebox.showerror("Errore", "Inserisci un URL valido.")
            return

        self.btn_analyze.config(state=tk.DISABLED)
        self.update_status("🔍 Analisi risoluzioni in corso...")
        
        thread = threading.Thread(target=self.run_analysis, args=(url,))
        thread.daemon = True
        thread.start()

    def run_analysis(self, url):
        resolutions = core.get_video_resolutions(url)
        
        def update_ui():
            self.video_resolutions = resolutions
            if resolutions:
                self.combo_res['values'] = resolutions
                self.combo_res.current(0) # Seleziona la prima (migliore)
                self.update_status("✅ Analisi completata!")
                
                if self.download_type.get() == 'v':
                    self.combo_res.config(state="readonly")
                
                self.btn_download.config(state=tk.NORMAL)
            else:
                self.update_status("⚠️ Nessuna risoluzione trovata o errore.")
                self.combo_res.set("Errore / Nessun dato")
                # Abilitiamo comunque il download (fallback best)
                self.btn_download.config(state=tk.NORMAL)
            
            self.btn_analyze.config(state=tk.NORMAL)

        self.root.after(0, update_ui)

    def start_download(self):
        url = self.url_entry.get().strip()
        if not url:
            messagebox.showerror("Errore", "Inserisci un URL valido.")
            return

        choice = self.download_type.get()
        resolution = self.combo_res.get() if choice == 'v' else None
        
        # Se l'utente non ha analizzato ma clicca download dopo aver inserito url (magari era disabilitato ma riabilitato per qualche motivo, o se decidiamo di abilitarlo di default)
        # Nel design attuale è disabilitato finché non analizzi. 
        # MA se l'analisi fallisce, lo abilitiamo per permettere "Best".
        
        # Disable button during download
        self.btn_download.config(state=tk.DISABLED)
        self.btn_analyze.config(state=tk.DISABLED)
        self.update_status("Avvio download...")

        # Run download in a separate thread
        thread = threading.Thread(target=self.run_download, args=(url, choice, resolution))
        thread.daemon = True
        thread.start()

    def run_download(self, url, choice, resolution):
        try:
            playlist_name = core.extract_playlist_name(url)
            path = self.custom_download_path

            if choice == 'v':
                # Se la resolution è "Analizza URL..." o simile, passiamo None (Best)
                if not resolution or "Analizza" in resolution or "Errore" in resolution:
                    resolution = None
                    
                core.download_yt_video(url, playlist_name, progress_callback=self.update_status, resolution=resolution, download_path=path)
            else:
                core.download_yt_audio(url, playlist_name, progress_callback=self.update_status, download_path=path)

            self.update_status("100% - Completato!")
            self.root.after(0, lambda: messagebox.showinfo("Fatto", "Download completato!"))
        except Exception as e:
            self.update_status("Errore")
            self.root.after(0, lambda: messagebox.showerror("Errore", str(e)))
        finally:
            self.root.after(0, lambda: self.btn_download.config(state=tk.NORMAL))
            self.root.after(0, lambda: self.btn_analyze.config(state=tk.NORMAL))

def run_gui():
    root = tk.Tk()
    app = DownloaderApp(root)
    root.mainloop()

if __name__ == "__main__":
    run_gui()
