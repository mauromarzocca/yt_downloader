# yt_downloader

---

- [yt\_downloader](#yt_downloader)
  - [Struttura delle Directory](#struttura-delle-directory)
  - [Dipendenze](#dipendenze)
    - [Installazione di FFmpeg](#installazione-di-ffmpeg)
  - [Utilizzo](#utilizzo)
  - [Build](#build)
  - [Note](#note)
  - [Contributi](#contributi)
  - [Licenza](#licenza)

---

![icon](icon.png)

Versione : 5.1 (GUI + CLI)

Questo progetto è un downloader per video e audio da YouTube, disponibile sia con interfaccia grafica (GUI) che da riga di comando (CLI).

## Struttura delle Directory

I file scaricati verranno salvati nella seguente struttura:

```sh
.
├── main.py
├── ui.py
├── cli.py
├── core.py
└── download
    ├── audio
    └── video
```

## Dipendenze

Questo progetto richiede `yt-dlp` e `ffmpeg`.

```bash
pip install -r requirements.txt
```

### Installazione di FFmpeg

- **Windows**: [ffmpeg.org](https://ffmpeg.org/download.html).
- **macOS**: `brew install ffmpeg`
- **Linux**: `sudo apt install ffmpeg`

## Utilizzo

### Versione Script Python

1. **GUI (Default)**:
   ```bash
   python main.py
   ```

2. **CLI (Riga di Comando)**:
   ```bash
   python main.py --cli
   # oppure
   python cli.py
   ```

## Build

Per creare gli eseguibili (GUI e CLI):

1. `pip install -r requirements.txt`
2. `python build.py`

Troverai due eseguibili nella cartella `dist`:
- **YouTubeDownloader**: Versione con interfaccia grafica.
- **YouTubeDownloader-CLI**: Versione da terminale.

## Note

- Se un video non è disponibile, verrà ignorato.
- Assicurati di avere i permessi di scrittura.
- Aggiorna yt-dlp se ci sono problemi: `pip install -U yt-dlp`.

## Contributi

Sentiti libero di aprire issue o PR.

## Licenza

MIT License.
