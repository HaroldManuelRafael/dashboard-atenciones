"""Start the bundled Streamlit dashboard and open one browser tab."""

from __future__ import annotations

import sys
import threading
import time
import urllib.error
import urllib.request
import webbrowser
from pathlib import Path

HOST = "127.0.0.1"
PORT = 8501


def _bundle_root() -> Path:
    if getattr(sys, "frozen", False) and hasattr(sys, "_MEIPASS"):
        return Path(sys._MEIPASS)
    return Path(__file__).resolve().parents[2]


def _run_streamlit(app_path: Path) -> None:
    from streamlit.web import cli as stcli

    sys.argv = [
        "streamlit",
        "run",
        str(app_path),
        f"--server.address={HOST}",
        f"--server.port={PORT}",
        "--server.headless=true",
        "--browser.gatherUsageStats=false",
    ]
    try:
        stcli.main()
    except SystemExit:
        pass


def _wait_for_server(url: str, timeout: float = 60.0) -> bool:
    deadline = time.monotonic() + timeout
    while time.monotonic() < deadline:
        try:
            with urllib.request.urlopen(url, timeout=1):
                return True
        except (OSError, urllib.error.URLError):
            time.sleep(0.25)
    return False


def main() -> None:
    app_path = _bundle_root() / "src" / "app.py"
    server_thread = threading.Thread(target=_run_streamlit, args=(app_path,), daemon=True)
    server_thread.start()

    url = f"http://{HOST}:{PORT}"
    if _wait_for_server(url):
        webbrowser.open_new_tab(url)
    else:
        raise RuntimeError("No se pudo iniciar el dashboard local en el puerto 8501.")

    server_thread.join()


if __name__ == "__main__":
    main()
