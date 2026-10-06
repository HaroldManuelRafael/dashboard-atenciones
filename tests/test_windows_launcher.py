import importlib.util
from pathlib import Path

import pytest

LAUNCHER_PATH = Path(__file__).parents[1] / "packaging" / "windows" / "launcher.py"
SPEC = importlib.util.spec_from_file_location("dashboard_windows_launcher", LAUNCHER_PATH)
assert SPEC and SPEC.loader
launcher = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(launcher)


def test_log_path_uses_local_app_data(monkeypatch, tmp_path):
    monkeypatch.setenv("LOCALAPPDATA", str(tmp_path))

    assert launcher._log_path() == tmp_path / "DashboardAtenciones" / "logs" / "launcher.log"


def test_validate_resources_requires_app_and_sample_csv(tmp_path):
    (tmp_path / "src").mkdir()
    (tmp_path / "data").mkdir()
    app_path = tmp_path / "src" / "app.py"
    sample_path = tmp_path / "data" / "sample_atenciones.csv"
    app_path.write_text("", encoding="utf-8")
    sample_path.write_text("", encoding="utf-8")

    assert launcher._validate_resources(tmp_path) == (app_path, sample_path)

    sample_path.unlink()
    with pytest.raises(FileNotFoundError, match="sample_atenciones.csv"):
        launcher._validate_resources(tmp_path)


def test_wait_and_open_browser_opens_only_after_server_is_ready(monkeypatch):
    opened = []
    monkeypatch.setattr(launcher, "_wait_for_server", lambda url: True)
    monkeypatch.setattr(launcher.webbrowser, "open_new_tab", opened.append)

    launcher._wait_and_open_browser("http://127.0.0.1:8501")

    assert opened == ["http://127.0.0.1:8501"]
