import io
import os
import shutil
import tempfile
from unittest import mock

import flywheel
import fs
import pytest

from flywheel_cli import util
from flywheel_cli.walker.abstract_walker import FileInfo

TESTS_ROOT = os.path.dirname(__file__)
DATA_ROOT = os.path.join(TESTS_ROOT, "data")
DICOM_ROOT = os.path.join(DATA_ROOT, "DICOM")

pytest_plugins = "flywheel_cli.ingest.fixtures"


def pytest_configure(config):
    # register an additional marker
    config.addinivalue_line("markers", "db: database tests")


@pytest.fixture(scope="session")
def test_data_dir():
    return DATA_ROOT


@pytest.fixture(scope="function")
def dicom_file():
    def get_dicom_file(folder, filename):
        fd, path = tempfile.mkstemp(suffix=".dcm")
        os.close(fd)

        src_path = os.path.join(DICOM_ROOT, folder, filename)
        shutil.copy(src_path, path)

        return path

    return get_dicom_file


@pytest.fixture(scope="function")
def dicom_data():
    def get_dicom_file_data(folder, filename):
        src_path = os.path.join(DICOM_ROOT, folder, filename)
        with open(src_path, "rb") as f:
            data = f.read()

        return data

    return get_dicom_file_data


@pytest.fixture(scope="function")
def temp_fs():
    tempdirs = []

    def make_mock_fs(structure):
        tempdir = tempfile.TemporaryDirectory()
        tempdirs.append(tempdir)

        tmpfs_url = f"osfs://{tempdir.name}"
        tmpfs = fs.open_fs(tmpfs_url)

        for path, files in structure.items():
            with tmpfs.makedirs(path, recreate=True) as subdir:
                for name in files:
                    if isinstance(name, tuple):
                        name, content = name
                    else:
                        content = b"Hello World"

                    with subdir.open(name, "wb") as f:
                        f.write(content)

        return tmpfs, tmpfs_url

    yield make_mock_fs


class DummyWalker:
    def __init__(self, files):
        self._files = files

    def list_files(self, dir_):
        cnt = 0
        for f in self._files:
            cnt += 1
            if isinstance(f, tuple):
                filename, size = f
            else:
                filename, size = f, cnt
            yield FileInfo(filename, False, size=size)

    def open(self, path, *args, **kwargs):
        return io.BytesIO()


# TODO deprecate AttrDict pattern and use simple mocks instead
@pytest.fixture(scope="function")
def attr_dict():
    def attr_dict_init(dict_):
        return AttrDict(dict_)

    return attr_dict_init


class AttrDict(dict):
    """Utility class for creating mock objects with simple attr access"""

    def __init__(self, values, allow_default=False):
        super().__init__(values)
        self.allow_default = allow_default

    def __getattr__(self, attr, default=None):
        try:
            value = self[attr]
        except KeyError:
            if self.allow_default:
                return default
            raise AttributeError(attr)
        if isinstance(value, dict):
            value = AttrDict(value)
        return value

    def __deepcopy__(self, *_):
        return self.to_dict()

    def get(self, key, default=None):
        try:
            return getattr(self, key)
        except AttributeError:
            return default

    def to_dict(self):
        return self


@pytest.fixture(scope="function")
def get_sdk_mock(mocker):
    mocker.patch("flywheel_cli.util.get_api_key")
    spec = dir(flywheel.Flywheel)
    spec.extend(dir(flywheel.Client))
    spec.extend(dir(util.SDKClient))
    spec.extend(["api_client", "deid_log"])
    sdk_mock = mock.Mock(spec=spec)
    get_sdk_mock = mocker.patch(
        "flywheel_cli.util.get_sdk_client", return_value=sdk_mock
    )
    util.get_sdk_client_for_current_user.cache_clear()
    return get_sdk_mock


@pytest.fixture(scope="function")
def sdk_mock(get_sdk_mock):
    return get_sdk_mock.return_value
