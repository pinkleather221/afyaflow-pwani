from afyaflow import __version__


def test_package_version_exists() -> None:
    assert __version__ == "0.1.0"
