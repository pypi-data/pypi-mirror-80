import collections
import copy
import datetime
from unittest import mock

import pytest

from flywheel_cli.config import Config
from flywheel_cli.importers import DicomScanner
from flywheel_cli.importers.container_factory import ContainerFactory
from flywheel_cli.importers.dicom_scan import InvalidLabel
from flywheel_cli.walker import PyFsWalker

from .test_container_factory import MockContainerResolver


class MockDCM(object):
    def __init__(self, **kwargs):
        self.raw = kwargs.get("raw")

    def get_manufacturer(self):
        return self.__dict__.get("Manufacturer")

    def get(self, value, default=None):
        return self.raw.get(value, default)


def mock_dcm(value):
    if isinstance(value, dict):
        return MockDCM(**{key: val for key, val in value.items()}, return_value=None)
    elif isinstance(value, list):
        return [mock_dcm(val) for val in value]
    else:
        return value


def test_resolve_acquisition():
    config = Config()
    dicom_scanner = DicomScanner(config)
    dcm = mock_dcm(
        {
            "raw": {
                "StudyInstanceUID": "1",
                "SeriesInstanceUID": "1",
                "StudyDate": "12341212121212",
                "StudyDescription": "Session",
                "SeriesDescription": "Acq",
                "SeriesDate": "19700101",
                "PatientID": "1",
            }
        }
    )
    acquisition = dicom_scanner.resolve_acquisition({}, dcm)
    assert acquisition.context["acquisition"]["label"] == "Acq"


def test_resolve_acquisition_secondary():
    config = Config()
    config.related_acquisitions = True
    dicom_scanner = DicomScanner(config)
    secondary_dcm_dict = {
        "PatientID": "626",
        "StudyInstanceUID": "study-uid",
        "SeriesInstanceUID": "series-uid-2",
        "StudyDate": "12341212121212",
        "StudyDescription": "Session",
        "SeriesDescription": "Acq",
        "SeriesDate": "19700101",
        "ReferencedFrameOfReferenceSequence": [
            {
                "RTReferencedStudySequence": [
                    {
                        "RTReferencedSeriesSequence": [
                            {"SeriesInstanceUID": "series-uid-1"}
                        ]
                    }
                ]
            }
        ],
    }
    secondary_dcm_dict["raw"] = copy.deepcopy(secondary_dcm_dict)
    secondary_dcm = mock_dcm(secondary_dcm_dict)
    acquisition = dicom_scanner.resolve_acquisition({}, secondary_dcm)

    assert (
        dicom_scanner.sessions["study-uid"].secondary_acquisitions["series-uid-1"]
        == acquisition
    )


def test_resolve_primary_after_secondary():
    config = Config()
    config.related_acquisitions = True
    dicom_scanner = DicomScanner(config)
    secondary_dcm_dict = {
        "PatientID": "626",
        "StudyInstanceUID": "study-uid",
        "SeriesInstanceUID": "series-uid-2",
        "StudyDate": "12341212121212",
        "StudyDescription": "Session",
        "SeriesDescription": "Acq",
        "SeriesDate": "19700101",
        "SOPInstanceUID": "1",
        "ReferencedFrameOfReferenceSequence": [
            {
                "RTReferencedStudySequence": [
                    {
                        "RTReferencedSeriesSequence": [
                            {"SeriesInstanceUID": "series-uid-1"}
                        ]
                    }
                ]
            }
        ],
    }
    secondary_dcm_dict["raw"] = copy.deepcopy(secondary_dcm_dict)
    secondary_dcm = mock_dcm(secondary_dcm_dict)
    acquisition = dicom_scanner.resolve_acquisition({}, secondary_dcm)
    # Add the file to the acquisition
    acquisition.files["series-uid-2"] = {"1": "filepath"}
    acquisition.filenames["series-uid-2"] = "secondary-filename"

    primary_dcm_dict = {
        "PatientID": "626",
        "StudyInstanceUID": "study-uid",
        "SeriesInstanceUID": "series-uid-1",
        "StudyDate": "12341212121212",
        "StudyDescription": "Session",
        "SeriesDescription": "Primary",
    }
    primary_dcm_dict["raw"] = copy.deepcopy(primary_dcm_dict)
    primary_dcm = mock_dcm(primary_dcm_dict)
    acquisition = dicom_scanner.resolve_acquisition({}, primary_dcm)

    assert not dicom_scanner.sessions["study-uid"].secondary_acquisitions.get(
        "sereies-uid-1"
    )
    assert (
        dicom_scanner.sessions["study-uid"].acquisitions["series-uid-1"] == acquisition
    )
    assert acquisition.files["series-uid-2"]["1"] == "filepath"
    assert acquisition.filenames["series-uid-2"] == "secondary-filename"


def test_resolve_primary_before_secondary():
    config = Config()
    config.related_acquisitions = True
    dicom_scanner = DicomScanner(config)

    primary_dcm_dict = {
        "PatientID": "626",
        "StudyInstanceUID": "study-uid",
        "SeriesInstanceUID": "series-uid-1",
        "StudyDate": "12341212121212",
        "StudyDescription": "Session",
        "SeriesDescription": "Primary",
    }
    primary_dcm_dict["raw"] = copy.deepcopy(primary_dcm_dict)
    primary_dcm = mock_dcm(primary_dcm_dict)
    acquisition = dicom_scanner.resolve_acquisition({}, primary_dcm)

    secondary_dcm_dict = {
        "PatientID": "626",
        "StudyInstanceUID": "study-uid",
        "SeriesInstanceUID": "series-uid-2",
        "StudyDate": "12341212121212",
        "StudyDescription": "Session",
        "SeriesDescription": "Acq",
        "SeriesDate": "19700101",
        "SOPInstanceUID": "1",
        "ReferencedFrameOfReferenceSequence": [
            {
                "RTReferencedStudySequence": [
                    {
                        "RTReferencedSeriesSequence": [
                            {"SeriesInstanceUID": "series-uid-1"}
                        ]
                    }
                ]
            }
        ],
    }
    secondary_dcm_dict["raw"] = copy.deepcopy(secondary_dcm_dict)
    secondary_dcm = mock_dcm(secondary_dcm_dict)
    acquisition = dicom_scanner.resolve_acquisition({}, secondary_dcm)
    # Add the file to the acquisition
    acquisition.files["series-uid-2"] = {"1": "filepath"}
    acquisition.filenames["series-uid-2"] = "secondary-filename"

    assert not dicom_scanner.sessions["study-uid"].secondary_acquisitions.get(
        "sereies-uid-1"
    )
    assert (
        dicom_scanner.sessions["study-uid"].acquisitions["series-uid-1"] == acquisition
    )
    assert acquisition.files["series-uid-2"]["1"] == "filepath"
    assert acquisition.filenames["series-uid-2"] == "secondary-filename"


def test_resolve_acquisition_malformed_secondary():
    config = Config()
    config.related_acquisitions = True
    dicom_scanner = DicomScanner(config)
    dcm_dict = {
        "PatientID": "626",
        "StudyInstanceUID": "1",
        "SeriesInstanceUID": "1",
        "StudyDate": "12341212121212",
        "StudyDescription": "Session",
        "SeriesDescription": "Acq",
        "SeriesDate": "19700101",
        "ReferencedFrameOfReferenceSequence": [{"RTReferencedStudySequence": 3}],
    }
    dcm_dict["raw"] = copy.deepcopy(dcm_dict)
    dcm = mock_dcm(dcm_dict)
    acquisition = dicom_scanner.resolve_acquisition({}, dcm)

    assert dicom_scanner.sessions["1"].acquisitions["1"] == acquisition


def test_dicom_uids(temp_fs, dicom_data):
    tmpfs, tmpfs_url = temp_fs(
        collections.OrderedDict(
            {
                "DICOM": [
                    (
                        "001.dcm",
                        dicom_data(
                            "16844_1_1_dicoms",
                            "MR.1.2.840.113619.2.408.5282380.5220731.23348.1516669692.164.dcm",
                        ),
                    )
                ],
            }
        )
    )

    config = Config()
    dicom_scanner = DicomScanner(config)

    resolver = MockContainerResolver()
    container_factory = ContainerFactory(resolver)

    context = {
        "group": {"_id": "my_group"},
        "project": {"label": "Dicom Scan"},
        "subject": {"label": "1001"},
    }

    walker = PyFsWalker(tmpfs_url, src_fs=tmpfs)
    dicom_scanner.discover(walker, context, container_factory)

    itr = iter(container_factory.walk_containers())

    _, child = next(itr)
    assert child.container_type == "group"
    assert child.id == "my_group"
    assert not child.exists

    _, child = next(itr)
    assert child.container_type == "project"
    assert child.label == "Dicom Scan"
    assert not child.exists
    assert len(child.files) == 0

    _, child = next(itr)
    assert child.container_type == "subject"
    assert child.label == "1001"
    assert not child.exists
    assert len(child.files) == 0

    _, child = next(itr)
    assert child.container_type == "session"
    assert child.label == "2018-01-24 17_35_01"
    assert child.uid == "1.2.840.113619.6.408.128090802883025653595086587293755801755"
    assert not child.exists
    assert len(child.files) == 0

    _, child = next(itr)
    assert child.container_type == "acquisition"
    assert child.label == "1 - 3Plane Loc fgre"
    assert child.uid == "1.2.840.113619.2.408.5282380.5220731.30424.1516669014.474"
    assert not child.exists
    assert len(child.files) == 0

    assert len(child.packfiles) == 1
    desc = child.packfiles[0]
    assert desc.packfile_type == "dicom"
    assert desc.path == ["DICOM/001.dcm"]
    assert desc.count == 1

    try:
        next(itr)
        pytest.fail("Unexpected container found")
    except StopIteration:
        pass


def test_dicom_uids_handle_session_rename(temp_fs, dicom_data):
    STUDY_UID = "1.2.840.113619.6.408.128090802883025653595086587293755801755"

    tmpfs, tmpfs_url = temp_fs(
        collections.OrderedDict(
            {
                "DICOM": [
                    (
                        "001.dcm",
                        dicom_data(
                            "16844_1_1_dicoms",
                            "MR.1.2.840.113619.2.408.5282380.5220731.23348.1516669692.164.dcm",
                        ),
                    )
                ],
            }
        )
    )

    config = Config()
    dicom_scanner = DicomScanner(config)

    resolver = MockContainerResolver(
        {
            "my_group": {
                "_meta": {"_id": "my_group"},
                "Dicom Scan": {
                    "_meta": {"_id": "project_id"},
                },
                "<id:project_id>": {
                    "_meta": {"_id": "project_id"},
                    "1001": {
                        "_meta": {"_id": "subject_id"},
                    },
                    "<id:subject_id>": {
                        "_meta": {"_id": "subject_id"},
                        "Renamed Session": {
                            "_meta": {
                                "_id": "session_id",
                                "uid": STUDY_UID,
                                "label": "Renamed Session",
                            }
                        },
                    },
                },
            },
        }
    )
    container_factory = ContainerFactory(resolver)

    context = {
        "group": {"_id": "my_group"},
        "project": {"label": "Dicom Scan"},
        "subject": {"label": "1001"},
    }

    walker = PyFsWalker(tmpfs_url, src_fs=tmpfs)
    dicom_scanner.discover(walker, context, container_factory)

    itr = iter(container_factory.walk_containers())

    _, child = next(itr)
    assert child.container_type == "group"
    assert child.id == "my_group"
    assert child.exists

    _, child = next(itr)
    assert child.container_type == "project"
    assert child.label == "Dicom Scan"
    assert child.exists
    assert child.id == "project_id"
    assert len(child.files) == 0

    _, child = next(itr)
    assert child.container_type == "subject"
    assert child.label == "1001"
    assert child.exists
    assert child.id == "subject_id"
    assert len(child.files) == 0

    _, child = next(itr)
    assert child.container_type == "session"
    assert child.label == "Renamed Session"
    assert child.uid == "1.2.840.113619.6.408.128090802883025653595086587293755801755"
    assert child.exists
    assert len(child.files) == 0

    _, child = next(itr)
    assert child.container_type == "acquisition"
    assert child.label == "1 - 3Plane Loc fgre"
    assert child.uid == "1.2.840.113619.2.408.5282380.5220731.30424.1516669014.474"
    assert len(child.files) == 0

    assert len(child.packfiles) == 1
    desc = child.packfiles[0]
    assert desc.packfile_type == "dicom"
    assert desc.path == ["DICOM/001.dcm"]
    assert desc.count == 1

    try:
        next(itr)
        pytest.fail("Unexpected container found")
    except StopIteration:
        pass


def test_dicom_uids_handle_acquisition_rename(temp_fs, dicom_data):
    STUDY_UID = "1.2.840.113619.6.408.128090802883025653595086587293755801755"
    SERIES_UID = "1.2.840.113619.2.408.5282380.5220731.30424.1516669014.474"

    tmpfs, tmpfs_url = temp_fs(
        collections.OrderedDict(
            {
                "DICOM": [
                    (
                        "001.dcm",
                        dicom_data(
                            "16844_1_1_dicoms",
                            "MR.1.2.840.113619.2.408.5282380.5220731.23348.1516669692.164.dcm",
                        ),
                    )
                ],
            }
        )
    )

    config = Config()
    dicom_scanner = DicomScanner(config)
    resolver = MockContainerResolver(
        {
            "my_group": {
                "_meta": {"_id": "my_group"},
                "Dicom Scan": {
                    "_meta": {"_id": "project_id"},
                },
                "<id:project_id>": {
                    "_meta": {"_id": "project_id"},
                    "1001": {
                        "_meta": {"_id": "subject_id"},
                    },
                    "<id:subject_id>": {
                        "_meta": {"_id": "subject_id"},
                        "Renamed Session": {
                            "_meta": {
                                "_id": "session_id",
                                "uid": STUDY_UID,
                                "label": "Renamed Session",
                            }
                        },
                        "<id:session_id>": {
                            "_meta": {
                                "_id": "session_id",
                                "uid": STUDY_UID,
                                "label": "Renamed Session",
                            },
                            "Renamed Acquisition": {
                                "_meta": {
                                    "_id": "acquisition_id",
                                    "uid": SERIES_UID,
                                    "label": "Renamed Acquisition",
                                }
                            },
                        },
                    },
                },
            },
        }
    )
    container_factory = ContainerFactory(resolver)

    context = {
        "group": {"_id": "my_group"},
        "project": {"label": "Dicom Scan"},
        "subject": {"label": "1001"},
    }

    walker = PyFsWalker(tmpfs_url, src_fs=tmpfs)
    dicom_scanner.discover(walker, context, container_factory)

    itr = iter(container_factory.walk_containers())

    _, child = next(itr)
    assert child.container_type == "group"
    assert child.id == "my_group"
    assert child.exists

    _, child = next(itr)
    assert child.container_type == "project"
    assert child.label == "Dicom Scan"
    assert child.exists
    assert child.id == "project_id"
    assert len(child.files) == 0

    _, child = next(itr)
    assert child.container_type == "subject"
    assert child.label == "1001"
    assert child.exists
    assert child.id == "subject_id"
    assert len(child.files) == 0

    _, child = next(itr)
    assert child.container_type == "session"
    assert child.label == "Renamed Session"
    assert child.uid == "1.2.840.113619.6.408.128090802883025653595086587293755801755"
    assert child.exists
    assert child.id == "session_id"
    assert len(child.files) == 0

    _, child = next(itr)
    assert child.container_type == "acquisition"
    assert child.label == "Renamed Acquisition"
    assert child.uid == "1.2.840.113619.2.408.5282380.5220731.30424.1516669014.474"
    assert child.exists
    assert child.id == "acquisition_id"
    assert len(child.files) == 0

    assert len(child.packfiles) == 1
    desc = child.packfiles[0]
    assert desc.packfile_type == "dicom"
    assert desc.path == ["DICOM/001.dcm"]
    assert desc.count == 1

    try:
        next(itr)
        pytest.fail("Unexpected container found")
    except StopIteration:
        pass


def test_move_uid_duplicates(temp_fs, dicom_data, mocker):
    tmpfs, tmpfs_url = temp_fs(
        collections.OrderedDict(
            {
                "DICOM": [
                    (
                        "001.dcm",
                        dicom_data(
                            "16844_1_1_dicoms",
                            "MR.1.2.840.113619.2.408.5282380.5220731.23348.1516669692.164.dcm",
                        ),
                    ),
                    (
                        "002.dcm",
                        dicom_data(
                            "16844_1_1_dicoms",
                            "MR.1.2.840.113619.2.408.5282380.5220731.23348.1516669692.164.dcm",
                        ),
                    ),
                ],
            }
        )
    )

    # SOPInstanceUID collision in the current import
    config = Config()
    config.check_unique_uids = True
    config.copy_duplicates = True
    mock_fs = mocker.patch("flywheel_cli.importers.dicom_scan.fs.open_fs")
    mock_copy = mocker.patch("flywheel_cli.importers.dicom_scan.fs.copy")
    dicom_scanner = DicomScanner(config)

    resolver = MockContainerResolver()
    container_factory = ContainerFactory(resolver)

    context = {
        "group": {"_id": "my_group"},
        "project": {"label": "Dicom Scan"},
        "subject": {"label": "1001"},
    }

    walker = PyFsWalker(tmpfs_url, src_fs=tmpfs)
    dicom_scanner.discover(walker, context, container_factory)
    mock_copy.copy_file.assert_called_once_with(
        mock.ANY, "DICOM/002.dcm", mock.ANY, "DICOM/002.dcm"
    )
    itr = iter(container_factory.walk_containers())

    _, child = next(itr)
    assert child.container_type == "group"
    assert child.id == "my_group"
    assert not child.exists

    _, child = next(itr)
    assert child.container_type == "project"
    assert child.label == "Dicom Scan"
    assert not child.exists
    assert len(child.files) == 0

    _, child = next(itr)
    assert child.container_type == "subject"
    assert child.label == "1001"
    assert not child.exists
    assert len(child.files) == 0

    _, child = next(itr)
    assert child.container_type == "session"
    assert child.label == "2018-01-24 17_35_01"
    assert child.uid == "1.2.840.113619.6.408.128090802883025653595086587293755801755"
    assert not child.exists
    assert len(child.files) == 0

    _, child = next(itr)
    assert child.container_type == "acquisition"
    assert child.label == "1 - 3Plane Loc fgre"
    assert child.uid == "1.2.840.113619.2.408.5282380.5220731.30424.1516669014.474"
    assert not child.exists
    assert len(child.files) == 0

    assert len(child.packfiles) == 1
    desc = child.packfiles[0]
    assert desc.packfile_type == "dicom"
    assert desc.path == ["DICOM/001.dcm"]
    assert desc.count == 1

    # acquision already exists in core
    resolver.reserved_uids = {
        "acquisitions": ["1.2.840.113619.2.408.5282380.5220731.30424.1516669014.474"]
    }
    container_factory = ContainerFactory(resolver)

    context = {
        "group": {"_id": "my_group"},
        "project": {"label": "Dicom Scan"},
        "subject": {"label": "1001"},
    }

    walker = PyFsWalker(tmpfs_url, src_fs=tmpfs)
    dicom_scanner.discover(walker, context, container_factory)
    mock_copy.copy_file.assert_any_call(
        mock.ANY, "DICOM/001.dcm", mock.ANY, "DICOM/001.dcm"
    )
    mock_copy.copy_file.assert_any_call(
        mock.ANY, "DICOM/002.dcm", mock.ANY, "DICOM/002.dcm"
    )
    itr = iter(container_factory.walk_containers())
    # nothing to import
    try:
        next(itr)
        pytest.fail("Unexpected container found")
    except StopIteration:
        pass
