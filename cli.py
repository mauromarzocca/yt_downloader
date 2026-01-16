import sys
import core

def cli_progress_callback(msg):
    """Callback per aggiornare la riga di comando."""
    # Aggiungiamo spazi alla fine per pulire residui di stringhe precedenti più lunghe
    sys.stdout.write(f"\r{msg}   ")
    sys.stdout.flush()

def run_cli():
    """Loop principale del programma in modalità CLI."""
    print(f"=== YouTube Downloader CLI v{core.VERSION} ===")
    print("Aggiorna yt-dlp con: python3 -m pip install -U yt-dlp")

    # Controlla aggiornamenti
    print("\n🔍 Controllo aggiornamenti...", end="", flush=True)
    update = core.check_for_updates()
    if update:
        print(f"\r✨ NUOVA VERSIONE DISPONIBILE: v{update['version']} ✨")
        print(f"Novità: {update['changelog'].splitlines()[0]}...") # Mostra solo prima riga
        print(f"Scarica qui: {update['url']}\n")
    else:
        print("\rAggiornamenti: Nessun aggiornamento disponibile.   \n")

    while True:
        try:
            choice = input("\nVuoi scaricare video o audio? (v/a): ").strip().lower()
            if choice not in ('v', 'a'):
                print("❌ Scelta non valida. Usa 'v' per video o 'a' per audio.")
                continue

            video_url = input("Inserisci l'URL del video o della playlist di YouTube: ").strip()
            if not video_url:
                print("❌ URL non valido.")
                continue

            playlist_name = core.extract_playlist_name(video_url)

            print("") # Newline prima del download
            if choice == 'v':
                print("⏳ Analisi risoluzioni disponibili...")
                resolutions = core.get_video_resolutions(video_url)
                selected_res = None
                
                if resolutions:
                    print("\nRisoluzioni disponibili:")
                    for idx, res in enumerate(resolutions, 1):
                        print(f"{idx}. {res}")
                    print(f"{len(resolutions)+1}. Migliore disponibile (Default)")
                    
                    try:
                        res_choice = input("\nSeleziona una risoluzione (numero): ").strip()
                        if res_choice and res_choice.isdigit():
                            idx = int(res_choice) - 1
                            if 0 <= idx < len(resolutions):
                                selected_res = resolutions[idx]
                                print(f"✅ Selezionato: {selected_res}")
                    except ValueError:
                        pass
                
                if not selected_res:
                    print("ℹ️  Uso risoluzione migliore disponibile (o 1080p limit).")

                core.download_yt_video(video_url, playlist_name, progress_callback=cli_progress_callback, resolution=selected_res)
            else:
                core.download_yt_audio(video_url, playlist_name, progress_callback=cli_progress_callback)

            print("\n\n🎉 Download completato!")
        except Exception as e:
            print(f"\n\n❌ Errore durante il download: {e}")
        except KeyboardInterrupt:
            print("\n\nInterruzione manuale.")
            break

        print("")
        again = input("Vuoi scaricare un altro video/audio? (s/n): ").strip().lower()
        if again != 's':
            print("\n👋 Uscita dal programma. Alla prossima!\n")
            break

if __name__ == "__main__":
    run_cli()
