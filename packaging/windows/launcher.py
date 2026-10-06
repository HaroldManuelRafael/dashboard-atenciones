"""Start the bundled Streamlit dashboard and open one browser tab."""

from __future__ import annotations

import logging
import os
import sys
import tempfile
import threading
import time
import urllib.error
import urllib.request
import webbrowser
from pathlib import Path

HOST = "127.0.0.1"
PORT = 8501
APP_NAME = "DashboardAtenciones"
LOGGER = logging.getLogger(APP_NAME)


def _bundle_root() -> Path:
    if getattr(sys, "frozen", False) and hasattr(sys, "_MEIPASS"):
        return Path(sys._MEIPASS)
    return Path(__file__).resolve().parents[2]


def _log_path() -> Path:
    """Return the per-user launcher log location on Windows and a safe fallback."""
    local_app_data = os.environ.get("LOCALAPPDATA")
    if local_app_data:
        return Path(local_app_data) / APP_NAME / "logs" / "launcher.log"
    if os.name == "nt":
        return Path.home() / "AppData" / "Local" / APP_NAME / "logs" / "launcher.log"
    return Path(tempfile.gettempdir()) / APP_NAME / "logs" / "launcher.log"


def _configure_logging() -> None:
    log_path = _log_path()
    try:
        log_path.parent.mkdir(parents=True, exist_ok=True)
        handler = logging.FileHandler(log_path, encoding="utf-8")
    except OSError:
        fallback = Path(tempfile.gettempdir()) / APP_NAME / "logs" / "launcher.log"
        fallback.parent.mkdir(parents=True, exist_ok=True)
        handler = logging.FileHandler(fallback, encoding="utf-8")
        log_path = fallback
    handler.setFormatter(logging.Formatter("%(asctime)s %(levelname)s %(message)s"))
    LOGGER.handlers.clear()
    LOGGER.addHandler(handler)
    LOGGER.setLevel(logging.INFO)
    LOGGER.info("Launcher log: %s", log_path)


def _resource_paths(bundle_root: Path) -> tuple[Path, Path]:
    return bundle_root / "src" / "app.py", bundle_root / "data" / "sample_atenciones.csv"


def _validate_resources(bundle_root: Path) -> tuple[Path, Path]:
    app_path, sample_path = _resource_paths(bundle_root)
    LOGGER.info("Executable: %s", sys.executable)
    LOGGER.info("Bundle root: %s", bundle_root)
    LOGGER.info("Application path: %s (exists=%s)", app_path, app_path.is_file())
    LOGGER.info("Sample CSV path: %s (exists=%s)", sample_path, sample_path.is_file())
    missing = [str(path) for path in (app_path, sample_path) if not path.is_file()]
    if missing:
        raise FileNotFoundError("Faltan recursos requeridos en el bundle: " + ", ".join(missing))
    return app_path, sample_path


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
    stcli.main()


def _wait_for_server(url: str, timeout: float = 60.0) -> bool:
    deadline = time.monotonic() + timeout
    while time.monotonic() < deadline:
        try:
            with urllib.request.urlopen(url, timeout=1):
                return True
        except (OSError, urllib.error.URLError):
            time.sleep(0.25)
    return False


def _wait_and_open_browser(url: str) -> None:
    try:
        if _wait_for_server(url):
            webbrowser.open_new_tab(url)
            LOGGER.info("Opened browser at %s", url)
        else:
            LOGGER.error("Dashboard did not respond at %s before timeout", url)
    except Exception:
        LOGGER.exception("Failed while waiting for dashboard or opening browser at %s", url)


def main() -> None:
    _configure_logging()
    url = f"http://{HOST}:{PORT}"
    LOGGER.info("Starting dashboard on host=%s port=%s", HOST, PORT)
    try:
        bundle_root = _bundle_root()
        app_path, _ = _validate_resources(bundle_root)
        src_path = str(app_path.parent)
        if src_path not in sys.path:
            sys.path.insert(0, src_path)

        browser_thread = threading.Thread(
            target=_wait_and_open_browser,
            args=(url,),
            name="dashboard-browser-waiter",
            daemon=True,
        )
        browser_thread.start()
        _run_streamlit(app_path)
    except BaseException:
        LOGGER.exception("Dashboard launcher failed (host=%s port=%s)", HOST, PORT)
        raise


if __name__ == "__main__":
    main()
