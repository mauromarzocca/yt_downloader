import sys
import os
import multiprocessing

class NullWriter:
    def write(self, data): pass
    def flush(self): pass

if __name__ == "__main__":
    # Crucial for PyInstaller frozen apps (especially on Windows, but safe elsewhere)
    multiprocessing.freeze_support()

    # Fix for macOS/Windows GUI crash (when stdout/stderr are invalid)
    if getattr(sys, 'frozen', False):
        # Redirect stdout/stderr to devnull to prevent crashes on writes.
        # This handles cases where sys.stdout is None or a closed descriptor.
        try:
            # On macOS, we need to redirect the low-level file descriptors (1 and 2)
            # because some C-extensions or subprocesses write directly to them.
            if sys.platform == 'darwin':
                devnull_fd = os.open(os.devnull, os.O_WRONLY)
                os.dup2(devnull_fd, 1) # Redirect stdout (FD 1)
                os.dup2(devnull_fd, 2) # Redirect stderr (FD 2)
                # Note: We don't close devnull_fd here because it's now duplicated to 1 and 2.

            # Also update Python's sys.stdout/stderr objects to match
            devnull = open(os.devnull, 'w')
            sys.stdout = devnull
            sys.stderr = devnull
        except Exception:
            # Fallback if opening devnull fails
            sys.stdout = NullWriter()
            sys.stderr = NullWriter()

    try:
        # Defer imports of ui and cli until after stdout/stderr are patched.
        import ui
        import cli

        # Check for CLI arguments
        if len(sys.argv) > 1 and (sys.argv[1] == '--cli' or sys.argv[1] == '-c'):
            cli.run_cli()
        else:
            # Launch the GUI application
            ui.run_gui()
    except Exception:
        # Emergency Crash Logger: writes traceback to a file on Desktop
        import traceback
        try:
            log_path = os.path.join(os.path.expanduser("~"), "Desktop", "YouTubeDownloader_Errore.txt")
            with open(log_path, "w") as f:
                traceback.print_exc(file=f)
        except:
            pass
        sys.exit(1)