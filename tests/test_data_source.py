from pathlib import Path

import pytest

from application.services import data_source


def test_development_uses_sample_csv(monkeypatch, tmp_path):
    monkeypatch.delenv(data_source.EXPLICIT_DATA_PATH_ENV, raising=False)
    monkeypatch.setattr(data_source.sys, "frozen", False, raising=False)

    assert data_source.resolve_data_source() == Path("data/sample_atenciones.csv").resolve()


def test_explicit_development_path_is_supported(monkeypatch, tmp_path):
    custom_path = tmp_path / "custom.csv"
    monkeypatch.setenv(data_source.EXPLICIT_DATA_PATH_ENV, str(custom_path))
    monkeypatch.setattr(data_source.sys, "frozen", False, raising=False)

    assert data_source.resolve_data_source() == custom_path


def test_packaged_source_copies_sample_only_on_first_arrival(monkeypatch, tmp_path):
    bundle = tmp_path / "bundle"
    sample = bundle / "data" / data_source.SAMPLE_FILE_NAME
    sample.parent.mkdir(parents=True)
    sample.write_text("sample", encoding="utf-8")
    appdata = tmp_path / "appdata"
    monkeypatch.setenv("APPDATA", str(appdata))
    monkeypatch.setattr(data_source.sys, "frozen", True, raising=False)
    monkeypatch.setattr(data_source.sys, "_MEIPASS", str(bundle), raising=False)

    target = data_source.resolve_data_source()
    assert target == appdata / data_source.APP_NAME / "data" / data_source.DATA_FILE_NAME
    assert target.read_text(encoding="utf-8") == "sample"

    target.write_text("usuario", encoding="utf-8")
    assert data_source.resolve_data_source().read_text(encoding="utf-8") == "usuario"


def test_packaged_source_requires_appdata(monkeypatch):
    monkeypatch.delenv("APPDATA", raising=False)
    monkeypatch.setattr(data_source.sys, "frozen", True, raising=False)
    with pytest.raises(OSError, match="APPDATA"):
        data_source.resolve_data_source()
