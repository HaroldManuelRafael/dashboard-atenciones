import json

import pytest

from application.services.settings import (
    Settings,
    load_settings,
    resolve_settings,
    save_settings,
    settings_path,
    validate_settings,
)


def test_missing_settings_defaults_to_local(tmp_path):
    assert load_settings(tmp_path / "settings.json") == Settings()


def test_valid_settings_are_loaded_and_environment_overrides_them(monkeypatch, tmp_path):
    path = tmp_path / "settings.json"
    path.write_text(
        json.dumps(
            {
                "data_source": "google_sheets",
                "spreadsheet_id": "saved-id",
                "worksheet_name": "Saved",
                "google_service_account_file": "credentials.json",
            }
        ),
        encoding="utf-8",
    )
    monkeypatch.setenv("DASHBOARD_DATA_SOURCE", "local")
    assert resolve_settings(path).data_source == "local"
    assert resolve_settings(path).spreadsheet_id == "saved-id"


def test_corrupt_settings_raise_clear_error(tmp_path):
    path = tmp_path / "settings.json"
    path.write_text("{invalid", encoding="utf-8")
    with pytest.raises(ValueError, match="settings.json"):
        load_settings(path)


def test_invalid_source_is_rejected(tmp_path):
    path = tmp_path / "settings.json"
    path.write_text(json.dumps({"data_source": "csv"}), encoding="utf-8")
    with pytest.raises(ValueError, match="local.*google_sheets"):
        load_settings(path)


def test_save_does_not_write_secrets(tmp_path):
    path = tmp_path / "settings.json"
    save_settings(Settings("local"), path)
    contents = path.read_text(encoding="utf-8")
    assert "private_key" not in contents
    assert "access_token" not in contents
    assert json.loads(contents)["data_source"] == "local"


def test_google_settings_require_existing_credentials(tmp_path):
    settings = Settings("google_sheets", "id", "Hoja", str(tmp_path / "missing.json"))
    with pytest.raises(ValueError, match="no existe"):
        validate_settings(settings)


def test_windows_settings_path_uses_appdata(monkeypatch, tmp_path):
    monkeypatch.setenv("APPDATA", str(tmp_path))
    assert settings_path() == tmp_path / "DashboardAtenciones" / "config" / "settings.json"
