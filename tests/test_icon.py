"""An application icon reaches the exe resource and the Inno Setup installer."""

import pathlib
from types import SimpleNamespace

from installer_builder.new_inno_command import create_installer_config


def builder(dist_dir: pathlib.Path, icon):
    metadata = SimpleNamespace(name="Example", version="1.0.0", author="Accessible Apps",
                               description="Example app")
    return SimpleNamespace(distribution=SimpleNamespace(metadata=metadata),
                           register_startup=False, icon=icon)


def test_installer_uses_the_resolved_icon_path(tmp_path):
    (tmp_path / "Example.exe").write_bytes(b"MZ")
    icon = tmp_path / "example.ico"
    icon.write_bytes(b"\0\0\1\0")

    installer = create_installer_config(builder(tmp_path, str(icon)), tmp_path)

    assert installer.setup_icon_file == str(icon.resolve())


def test_installer_without_icon_keeps_the_default(tmp_path):
    (tmp_path / "Example.exe").write_bytes(b"MZ")

    installer = create_installer_config(builder(tmp_path, None), tmp_path)

    assert installer.setup_icon_file is None
