import importlib.util
import sys
from pathlib import Path
from types import ModuleType, SimpleNamespace

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


def test_run_streamlit_disables_development_mode(monkeypatch, tmp_path):
    captured = {}
    cli_module = SimpleNamespace(main=lambda: captured.update(argv=sys.argv.copy()))
    web_module = ModuleType("streamlit.web")
    web_module.cli = cli_module
    streamlit_module = ModuleType("streamlit")
    streamlit_module.web = web_module
    monkeypatch.setitem(sys.modules, "streamlit", streamlit_module)
    monkeypatch.setitem(sys.modules, "streamlit.web", web_module)

    launcher._run_streamlit(tmp_path / "app.py")

    assert "--global.developmentMode=false" in captured["argv"]
    assert "--server.address=127.0.0.1" in captured["argv"]
    assert "--server.port=8501" in captured["argv"]
    assert "--server.headless=true" in captured["argv"]
    assert "--browser.gatherUsageStats=false" in captured["argv"]
