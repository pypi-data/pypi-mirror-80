from pathlib import Path

import pytest
from yaml import dump, load

try:
    from yaml import CDumper as Dumper
    from yaml import CLoader as Loader
except ImportError:
    from yaml import Loader, Dumper

from .__main__ import main


@pytest.fixture
def config_source_target_perms(tmp_path_factory, disco_fix):
    configs = tmp_path_factory.mktemp("configs")
    data = {
        "hosts": {
            "foo-machine": {
                "bar-user": [
                    {"source": "file_1", "target": "file_1_target"},
                    {
                        "source": "file_2",
                        "target": "file_2_target",
                        "permissions": "0600",
                    },
                ]
            }
        }
    }
    # Create all the files
    (configs / "file_1").touch()
    (configs / "file_2").touch()
    return disco_fix(configs, data)


@pytest.fixture
def config_file_simple(tmp_path_factory, disco_fix):
    configs = tmp_path_factory.mktemp("configs")
    data = {
        "hosts": {
            "foo-machine": {
                "bar-user": [
                    "file_missing",
                    "file_1",
                    ".file_2",
                    "dir_2/file_3",
                    "dir_2/.file_4",
                ]
            }
        }
    }
    # Create all the files, but "file_missing"

    (configs / "file_1").touch()
    (configs / ".file_2").touch()
    dir2 = configs / "dir_2"
    dir2.mkdir()
    (dir2 / "file_3").touch()
    (dir2 / ".file_4").touch()

    return disco_fix(configs, data)


@pytest.fixture
def config_dir_simple(tmp_path_factory, disco_fix):
    configs = tmp_path_factory.mktemp("configs")
    data = {
        "hosts": {
            "foo-machine": {
                "bar-user": [
                    "dir_missing",
                    "dir_1",
                    ".dir_2",
                    "dir_3/dir_4",
                    "dir_3/.dir_5",
                ]
            }
        }
    }
    # Create all the directories, but "dir_missing"

    (configs / "dir_1").mkdir()
    (configs / ".dir_2").mkdir()
    (configs / "dir_3/dir_4").mkdir(parents=True)
    (configs / "dir_3/.dir_5").mkdir()

    return disco_fix(configs, data)


@pytest.fixture
def disco_fix(tmp_path_factory):
    def f(configs, data):
        target = tmp_path_factory.mktemp("target")

        output = dump(data, Dumper=Dumper)
        discoset = configs / "Discoset.yml"
        with open(discoset, "w") as f:
            f.write(output)
        return (discoset, "foo-machine", "bar-user", target)

    return f


class Test:
    def test_file_simple(self, config_file_simple):
        discoset, _, _, target = config_file_simple
        warnings = main(*config_file_simple)

        source_dir = discoset.parent

        f_missing = target / "file_missing"
        f_1 = target / "file_1"
        f_2 = target / ".file_2"
        f_3 = target / "dir_2/file_3"
        f_4 = target / "dir_2/.file_4"

        # All symlinks exist
        for f in (f_missing, f_1, f_2, f_3, f_4):
            assert f.is_symlink()

        # All symlinks point to the correct source
        for f, source in (
            (f_missing, "file_missing"),
            (f_1, "file_1"),
            (f_2, ".file_2"),
            (f_3, "dir_2/file_3"),
            (f_4, "dir_2/.file_4"),
        ):
            assert f.resolve().relative_to(source_dir) == Path(source)

        # A warning about the missing source file was given
        assert len(warnings) == 1
        assert "file_missing does not exist" in warnings[0]

    def test_dir_simple(self, config_dir_simple):
        discoset, _, _, target = config_dir_simple
        warnings = main(*config_dir_simple)

        source_dir = discoset.parent

        d_missing = target / "dir_missing"
        d_1 = target / "dir_1"
        d_2 = target / ".dir_2"
        d_3 = target / "dir_3/dir_4"
        d_4 = target / "dir_3/.dir_5"

        # All symlinks exist
        for d in (d_missing, d_1, d_2, d_3, d_4):
            assert d.is_symlink()

        # All symlinks point to the correct source
        for d, source in (
            (d_missing, "dir_missing"),
            (d_1, "dir_1"),
            (d_2, ".dir_2"),
            (d_3, "dir_3/dir_4"),
            (d_4, "dir_3/.dir_5"),
        ):
            assert d.resolve().relative_to(source_dir) == Path(source)

        # A warning about the missing source directory was given
        assert len(warnings) == 1
        assert "dir_missing does not exist" in warnings[0]

    def test_source_target_perms(self, config_source_target_perms):
        discoset, _, _, target = config_source_target_perms
        warnings = main(*config_source_target_perms)

        source_dir = discoset.parent

        f_1 = target / "file_1_target"
        f_2 = target / "file_2_target"

        # All symlinks exist
        for f in (f_1, f_2):
            assert f.is_symlink()

        # All symlinks point to the correct source
        for f, source in (
            (f_1, "file_1"),
            (f_2, "file_2"),
        ):
            assert f.resolve().relative_to(source_dir) == Path(source)

        # Permissions are correct
        # FIXME
