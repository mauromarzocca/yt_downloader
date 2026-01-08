import ui
import cli
import sys
import os

class NullWriter:
    def write(self, data): pass
    def flush(self): pass

if __name__ == "__main__":
    # Fix for macOS/Windows GUI crash (when stdout/stderr are invalid)
    if getattr(sys, 'frozen', False):
        # If we are in a frozen app, checks if we have a valid stdout
        # In windowed mode (noconsole), sys.stdout might be None or a generic wrapper that fails on write
        try:
            sys.stdout.write("")
        except Exception:
            sys.stdout = NullWriter()
            sys.stderr = NullWriter()

    # Check for CLI arguments
    if len(sys.argv) > 1 and (sys.argv[1] == '--cli' or sys.argv[1] == '-c'):
        cli.run_cli()
    else:
        # Launch the GUI application
        ui.run_gui()
