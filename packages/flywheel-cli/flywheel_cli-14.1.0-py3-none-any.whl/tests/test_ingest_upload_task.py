import io
import tempfile
import zipfile
from unittest import mock

import pytest

from flywheel_cli.ingest import config
from flywheel_cli.ingest import schemas as s
from flywheel_cli.ingest.tasks import upload
from flywheel_cli.walker.factory import create_walker


@pytest.fixture(scope="function")
def create_upload_task(db, sdk_mock, test_data_dir):
    def _create(item_kwargs=None, task_kwargs=None):
        db.create_ingest(status="uploading", config={"src_fs": test_data_dir})
        group = db.create_container(
            level=0,
            path="grp",
            dst_path="grp",
            src_context={"_id": "grp"},
            dst_context={"_id": "grp", "label": "grp"},
        )
        project = db.create_container(
            parent_id=group.id,
            level=1,
            path="grp/prj",
            dst_path="grp/prj",
            src_context={"label": "prj"},
            dst_context={"_id": "prj_id", "label": "prj"},
        )
        subject = db.create_container(
            parent_id=project.id,
            level=2,
            path="grp/prj/subj",
            dst_path="grp/prj/subj",
            src_context={"label": "subj"},
            dst_context={"_id": "subj_id", "label": "subj"},
        )

        item_kwargs = item_kwargs or {}
        item_kwargs.setdefault("container_id", subject.id)
        item_kwargs.setdefault("type", "file")
        item_kwargs.setdefault("filename", "filename.txt")
        item_kwargs.setdefault("files", ["example.txt"])
        item_kwargs.setdefault("dir", "/")
        item = db.create_item(**item_kwargs)

        task_kwargs = task_kwargs or {}
        task_kwargs.setdefault("type", "upload")
        task_kwargs.setdefault("status", "running")
        task_kwargs.setdefault("item_id", item.id)
        task = db.create_task(**task_kwargs)
        task = s.TaskOut.from_orm(task)

        worker_config = config.WorkerConfig()

        return upload.UploadTask(db=db.client, task=task, worker_config=worker_config)

    return _create


def test_run_w_single_file(db, create_upload_task, sdk_mock):
    upload_task = create_upload_task()

    upload_task.run()

    assert db.client.get_task(upload_task.task.id).status == "completed"
    assert db.client.ingest.status == "finalizing"
    assert sdk_mock.upload.mock_calls == [
        mock.call("subject", "subj_id", "filename.txt", mock.ANY, None)
    ]


def test_run_w_safe_filename(db, create_upload_task, sdk_mock):
    upload_task = create_upload_task(item_kwargs={"safe_filename": "safe_filename.txt"})

    upload_task.run()

    assert db.client.get_task(upload_task.task.id).status == "completed"
    assert db.client.ingest.status == "finalizing"
    assert sdk_mock.upload.mock_calls == [
        mock.call(
            "subject",
            "subj_id",
            "safe_filename.txt",
            mock.ANY,
            {"info": {"source": "/filename.txt"}},
        )
    ]


def test_run_w_packfile(db, create_upload_task, sdk_mock):
    item_context = {
        "group": {"_id": "grp"},
        "project": {"label": "prj"},
        "packfile": {"type": "dicom"},
    }
    upload_task = create_upload_task(
        item_kwargs={
            "type": "packfile",
            "filename": "test.dicom.zip",
            "files": [
                "16844_1_1_dicoms/MR.1.2.840.113619.2.408.5282380.5220731.23348.1516669692.164.dcm"
            ],
            "dir": "DICOM",
            "context": item_context,
        }
    )

    upload_task.run()

    assert db.client.get_task(upload_task.task.id).status == "completed"
    assert db.client.ingest.status == "finalizing"
    assert sdk_mock.upload.call_count == 1
    args, _ = sdk_mock.upload.call_args
    assert args[0] == "subject"
    assert args[1] == "subj_id"
    assert args[2] == "test.dicom.zip"
    assert isinstance(args[3], tempfile.SpooledTemporaryFile)
    assert args[4] == {"name": "test.dicom.zip", "type": "dicom", "zip_member_count": 1}


def test_run_w_packfile_and_disable_tempfile_cache(db, create_upload_task, sdk_mock):
    item_context = {
        "group": {"_id": "grp"},
        "project": {"label": "prj"},
        "packfile": {"type": "dicom"},
    }
    upload_task = create_upload_task(
        item_kwargs={
            "type": "packfile",
            "filename": "test.dicom.zip",
            "files": [
                "16844_1_1_dicoms/MR.1.2.840.113619.2.408.5282380.5220731.23348.1516669692.164.dcm"
            ],
            "dir": "DICOM",
            "context": item_context,
        }
    )
    upload_task.worker_config.max_tempfile = 0

    upload_task.run()

    assert db.client.get_task(upload_task.task.id).status == "completed"
    assert db.client.ingest.status == "finalizing"
    assert sdk_mock.upload.call_count == 1
    args, _ = sdk_mock.upload.call_args
    assert args[0] == "subject"
    assert args[1] == "subj_id"
    assert args[2] == "test.dicom.zip"
    assert isinstance(args[3], io.IOBase)
    assert not isinstance(args[3], tempfile.SpooledTemporaryFile)
    assert args[4] == {"name": "test.dicom.zip", "type": "dicom", "zip_member_count": 1}


def test_run_w_packfile_and_deid_profile(db, create_upload_task, sdk_mock):
    item_context = {
        "group": {"_id": "grp"},
        "project": {"label": "prj"},
        "packfile": {"type": "dicom"},
    }
    upload_task = create_upload_task(
        item_kwargs={
            "type": "packfile",
            "filename": "test.dicom.zip",
            "files": [
                "16844_1_1_dicoms/MR.1.2.840.113619.2.408.5282380.5220731.23348.1516669692.164.dcm"
            ],
            "dir": "DICOM",
            "context": item_context,
        }
    )
    upload_task.ingest_config.deid_profiles = [
        {
            "name": "minimal",
            "description": "Dsc",
            "dicom": {
                "fields": [
                    {"name": "PatientBirthDate", "remove": True},
                    {"name": "PatientName", "remove": True},
                    {"name": "PatientID", "remove": False},
                ]
            },
        }
    ]
    upload_task.ingest_config.de_identify = True
    sdk_mock.post_deid_log.return_value = "log_id"

    upload_task.run()

    assert db.client.get_task(upload_task.task.id).status == "completed"
    assert db.client.ingest.status == "finalizing"
    assert sdk_mock.upload.call_count == 1
    args, _ = sdk_mock.upload.call_args
    assert args[0] == "subject"
    assert args[1] == "subj_id"
    assert args[2] == "test.dicom.zip"
    assert isinstance(args[3], tempfile.SpooledTemporaryFile)
    assert args[4] == {
        "name": "test.dicom.zip",
        "type": "dicom",
        "zip_member_count": 1,
        "deid_log_id": "log_id",
    }
    assert sdk_mock.post_deid_log.mock_calls == [
        mock.call(
            {
                "indexed_fields": {
                    "PatientBirthDate": "20000101",
                    "StudyDate": "20180124",
                    "SeriesDate": "20180124",
                    "StudyDescription": "Session Label",
                    "SeriesDescription": "3Plane Loc fgre",
                    "StudyInstanceUID": "1.2.840.113619.6.408.128090802883025653595086587293755801755",
                    "SeriesInstanceUID": "1.2.840.113619.2.408.5282380.5220731.30424.1516669014.474",
                    "PatientID": "flywheel/reaper",
                    "SeriesTime": "173623",
                    "PatientName": "Lastname^Firstname",
                    "StudyTime": "173501",
                    "AccessionNumber": "Accession",
                    "StudyID": "16844",
                },
                "deidentified_tags": {
                    "00100030": {"vr": "DA", "Value": ["20000101"]},
                    "00100010": {
                        "vr": "PN",
                        "Value": [{"Alphabetic": "Lastname^Firstname"}],
                    },
                    "00100020": {"vr": "LO", "Value": ["flywheel/reaper"]},
                },
            }
        )
    ]


def test_run_w_deid_profile_and_disable_deid_log_feature(
    db, create_upload_task, sdk_mock
):
    item_context = {
        "group": {"_id": "grp"},
        "project": {"label": "prj"},
        "packfile": {"type": "dicom"},
    }
    upload_task = create_upload_task(
        item_kwargs={
            "type": "packfile",
            "filename": "test.dicom.zip",
            "files": [
                "16844_1_1_dicoms/MR.1.2.840.113619.2.408.5282380.5220731.23348.1516669692.164.dcm"
            ],
            "dir": "DICOM",
            "context": item_context,
        }
    )
    upload_task.ingest_config.deid_profiles = [
        {
            "name": "minimal",
            "description": "Dsc",
            "dicom": {
                "fields": [
                    {"name": "PatientBirthDate", "remove": True},
                    {"name": "PatientName", "remove": True},
                    {"name": "PatientID", "remove": False},
                ]
            },
        }
    ]
    upload_task.ingest_config.de_identify = True
    sdk_mock.deid_log = False

    upload_task.run()

    assert db.client.get_task(upload_task.task.id).status == "completed"
    assert db.client.ingest.status == "finalizing"
    assert sdk_mock.upload.call_count == 1
    args, _ = sdk_mock.upload.call_args
    assert args[0] == "subject"
    assert args[1] == "subj_id"
    assert args[2] == "test.dicom.zip"
    assert isinstance(args[3], tempfile.SpooledTemporaryFile)
    assert args[4] == {
        "name": "test.dicom.zip",
        "type": "dicom",
        "zip_member_count": 1,
    }
    assert sdk_mock.post_deid_log.call_count == 0


def test_run_w_failure_retry(db, create_upload_task, sdk_mock):
    class UploadFailError(Exception):
        pass

    upload_task = create_upload_task()
    sdk_mock.upload.side_effect = UploadFailError("Upload failed")

    upload_task.run()

    assert db.client.ingest.status == "uploading"
    task = db.client.get_task(upload_task.task.id)
    assert task.status == "pending"
    assert task.retries == 1
    errors = list(db.client.get_all_errors())
    assert errors == []


def test_run_w_failure_exceed_max_retry(db, create_upload_task, sdk_mock):
    class UploadFailError(Exception):
        pass

    upload_task = create_upload_task(task_kwargs={"retries": 3})
    sdk_mock.upload.side_effect = UploadFailError("Upload failed")

    upload_task.run()

    assert db.client.ingest.status == "finalizing"
    task = db.client.get_task(upload_task.task.id)
    assert task.status == "failed"
    assert task.retries == 3
    errors = list(db.client.get_all_errors())
    assert len(errors) == 1
    assert errors[0].item_id == task.item_id
    assert errors[0].task_id == task.id


def test_create_packfile_w_root_subdir(test_data_dir):
    walker = create_walker(test_data_dir)
    context = s.ItemContext(
        group={"_id": "grp"}, project={"label": "prj"}, packfile={"type": "zip"}
    )

    tmpfile, metadata, deid_log_payload = upload.create_packfile(
        walker,
        "test.dicom.zip",
        [
            "DICOM/16844_1_1_dicoms/MR.1.2.840.113619.2.408.5282380.5220731.23348.1516669692.164.dcm",
            "DICOM/16844_1_1_dicoms/MR.1.2.840.113619.2.408.5282380.5220731.23348.1516669692.165.dcm",
        ],
        "/",
        context,
    )

    zip_file = zipfile.ZipFile(tmpfile)
    assert set(zip_file.namelist()) == {
        "DICOM/",
        "DICOM/16844_1_1_dicoms/",
        "DICOM/16844_1_1_dicoms/MR.1.2.840.113619.2.408.5282380.5220731.23348.1516669692.164.dcm",
        "DICOM/16844_1_1_dicoms/MR.1.2.840.113619.2.408.5282380.5220731.23348.1516669692.165.dcm",
    }
    assert metadata == {"name": "test.dicom.zip", "zip_member_count": 2, "type": "zip"}
    assert deid_log_payload is None


def test_create_packfile_w_non_root_subdir(test_data_dir):
    walker = create_walker(test_data_dir)
    context = s.ItemContext(
        group={"_id": "grp"}, project={"label": "prj"}, packfile={"type": "zip"}
    )

    tmpfile, metadata, deid_log_payload = upload.create_packfile(
        walker,
        "test.dicom.zip",
        [
            "MR.1.2.840.113619.2.408.5282380.5220731.23348.1516669692.164.dcm",
            "MR.1.2.840.113619.2.408.5282380.5220731.23348.1516669692.165.dcm",
        ],
        "/DICOM/16844_1_1_dicoms",
        context,
    )

    zip_file = zipfile.ZipFile(tmpfile)
    assert set(zip_file.namelist()) == {
        "MR.1.2.840.113619.2.408.5282380.5220731.23348.1516669692.164.dcm",
        "MR.1.2.840.113619.2.408.5282380.5220731.23348.1516669692.165.dcm",
    }
    assert metadata == {"name": "test.dicom.zip", "zip_member_count": 2, "type": "zip"}
    assert deid_log_payload is None


def test_create_packfile_w_flatten(test_data_dir):
    walker = create_walker(test_data_dir)
    context = s.ItemContext(
        group={"_id": "grp"},
        project={"label": "prj"},
        packfile={"type": "zip", "flatten": True},
    )

    tmpfile, metadata, deid_log_payload = upload.create_packfile(
        walker,
        "test.dicom.zip",
        [
            "DICOM/16844_1_1_dicoms/MR.1.2.840.113619.2.408.5282380.5220731.23348.1516669692.164.dcm",
            "DICOM/16844_1_1_dicoms/MR.1.2.840.113619.2.408.5282380.5220731.23348.1516669692.165.dcm",
        ],
        "/",
        context,
    )

    zip_file = zipfile.ZipFile(tmpfile)
    assert set(zip_file.namelist()) == {
        "MR.1.2.840.113619.2.408.5282380.5220731.23348.1516669692.164.dcm",
        "MR.1.2.840.113619.2.408.5282380.5220731.23348.1516669692.165.dcm",
    }
    assert metadata == {"name": "test.dicom.zip", "zip_member_count": 2, "type": "zip"}
    assert deid_log_payload is None
