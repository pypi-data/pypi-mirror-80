"""Test Sdk implemetation"""
import io
from unittest.mock import call, Mock, patch

import pytest

from flywheel_cli import sdk_impl


def test_retry():
    # pylint: disable=protected-access, expression-not-assigned, bad-continuation
    """Test retry on server error response"""
    fw = Mock(
        **{
            "api_client.call_api.return_value": {
                "ticket": "ticket",
                "urls": {"name": "url"},
            }
        }
    )
    upload_wrapper = sdk_impl.SdkUploadWrapper(fw)
    container = Mock(container_type="type", id="id")
    fileobj = io.BytesIO(b"test")

    upload_wrapper._upload_session = Mock(
        **{
            "put.return_value": Mock(status_code=503),
        }
    )
    with patch("flywheel_cli.sdk_impl.time") as time:
        upload_wrapper.signed_url_upload(container, "name", fileobj)
        assert time.sleep.mock_calls == [call(2 ** 0), call(2 ** 1), call(2 ** 2)]
        assert upload_wrapper._upload_session.put.mock_calls == [
            call("url", data=fileobj, headers=None),
            call("url", data=fileobj, headers=None),
            call("url", data=fileobj, headers=None),
            call("url", data=fileobj, headers=None),
            call().raise_for_status(),
            call().close(),
        ]

    upload_wrapper._upload_session = Mock(
        **{
            "put.return_value": Mock(status_code=429),
        }
    )
    with patch("flywheel_cli.sdk_impl.time") as time:
        upload_wrapper.signed_url_upload(container, "name", fileobj)
        assert time.sleep.mock_calls == [call(2 ** 0), call(2 ** 1), call(2 ** 2)]
        assert upload_wrapper._upload_session.put.mock_calls == [
            call("url", data=fileobj, headers=None),
            call("url", data=fileobj, headers=None),
            call("url", data=fileobj, headers=None),
            call("url", data=fileobj, headers=None),
            call().raise_for_status(),
            call().close(),
        ]

    upload_wrapper._upload_session = Mock(
        **{
            "put.return_value": Mock(status_code=200),
        }
    )
    with patch("flywheel_cli.sdk_impl.time") as time:
        upload_wrapper.signed_url_upload(container, "name", fileobj)
        assert time.sleep.mock_calls == []
        upload_wrapper._upload_session.put.assert_called_once()


def test_create_container(sdk_mock, attr_dict):
    upload_wrapper = sdk_impl.SdkUploadWrapper(sdk_mock)

    sdk_mock.reset_mock()
    upload_wrapper.create_container(
        attr_dict({"container_type": "session", "id": 123}),
        attr_dict(
            {
                "container_type": "acquisition",
                "context": {
                    "label": "abc",
                },
            }
        ),
    )

    assert sdk_mock.mock_calls == [
        call.add_acquisition({"label": "abc", "session": 123})
    ]
