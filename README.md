# yt_downloader

---

- [yt\_downloader](#yt_downloader)
  - [Struttura delle Directory](#struttura-delle-directory)
  - [Dipendenze](#dipendenze)
    - [Installazione di FFmpeg](#installazione-di-ffmpeg)
  - [Utilizzo](#utilizzo)
  - [Note](#note)
  - [Contributi](#contributi)
  - [Licenza](#licenza)
    - [Istruzioni per l'uso](#istruzioni-per-luso)

---

![icon](icon.png)

Questo progetto è un downloader per video e audio da YouTube, che supporta il download di intere playlist. I file scaricati vengono organizzati in una struttura di directory specifica.

## Struttura delle Directory

I file scaricati verranno salvati nella seguente struttura:

```

.
├── main.py
└── download
    ├── audio
    ├── video
    └── <nome_playlist>
```

## Dipendenze

Questo progetto richiede `yt-dlp` e `ffmpeg` per il download e la conversione dei file audio. Puoi installare le dipendenze utilizzando `pip`:

```bash
pip install yt-dlp
```

### Installazione di FFmpeg

Assicurati di avere `ffmpeg` installato sul tuo sistema. Puoi installarlo seguendo le istruzioni per il tuo sistema operativo:

- **Windows**: Puoi scaricare FFmpeg da [ffmpeg.org](https://ffmpeg.org/download.html) e seguire le istruzioni per l'installazione.
- **macOS**: Puoi installare FFmpeg utilizzando Homebrew:
  
  ```bash
  brew install ffmpeg
  ```

- **Linux**: Puoi installare FFmpeg utilizzando il gestore di pacchetti della tua distribuzione. Ad esempio, su Ubuntu:

  ```bash
  sudo apt update
  sudo apt install ffmpeg
  ```

## Utilizzo

1. Clona il repository:

   ```bash
   git clone https://github.com/mauromarzocca/yt_downloader.git
   cd yt_downloader
   ```

2. Esegui lo script:

   ```bash
   python main.py
   ```

3. Segui le istruzioni a schermo per scegliere se scaricare video o audio e inserisci l'URL del video o della playlist di YouTube.

## Note

- Se un video non è disponibile nella playlist, verrà automaticamente ignorato e il download continuerà con gli altri video disponibili.
- Assicurati di avere i permessi necessari per creare directory e scrivere file nel percorso specificato.

## Contributi

Se desideri contribuire a questo progetto, sentiti libero di aprire un problema o inviare una richiesta di pull.

## Licenza

Questo progetto è concesso in licenza sotto la [MIT License](LICENSE).

### Istruzioni per l'uso

- Sostituisci `<URL_DEL_REPOSITORY>` con l'URL del tuo repository Git.
- Sostituisci `<NOME_DEL_REPOSITORY>` con il nome della cartella del tuo repository.
- Assicurati di avere un file `LICENSE` se intendi includere una licenza nel tuo progetto.

Puoi copiare e incollare questo testo nel tuo file `README.md` per fornire una documentazione chiara e utile per gli utenti del tuo progetto.
