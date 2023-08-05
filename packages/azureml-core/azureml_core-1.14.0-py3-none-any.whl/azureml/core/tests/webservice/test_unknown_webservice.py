import json
import pytest
from unittest import mock

from azureml.core import Workspace
from azureml.core.webservice import Webservice, UnknownWebservice
from azureml.core.image import Image
from azureml.core.model import Model
from azureml._model_management._constants import UNKNOWN_IMAGE_TYPE, UNKNOWN_WEBSERVICE_TYPE


def get_model_mock():
    modelMock = mock.MagicMock(spec=Model)
    modelMock.id = "modelId"
    return modelMock


def get_workspace_mock():
    ws = mock.MagicMock(spec=Workspace)
    ws._auth = mock.MagicMock()
    ws._auth.get_authentication_header.return_value = {"Authentication": "Bearer AAA"}
    return ws


@pytest.mark.parametrize("mock_webservices_resp", [
    {
        "imageId": "blah-resnet50:2",
        "imageDetails": {
            "id": "blah-resnet50:2",
            "name": "blah-resnet50",
            "version": '2',
            "description": "",
            "tags": "",
            "kvTags": "",
            "properties": "",
            "createdTime": "2018-11-05T19:12:17.0180845Z",
            "imageType": UNKNOWN_IMAGE_TYPE,
            "imageFlavor": "BrainwavePackage",
            "creationState": "NotStarted",
            "modelIds": [
                "resnet-50-rtai:11"
            ],
            "imageLocation": "aml://artifact/LocalUpload/fpga/blah-resnet50:2"
        },
        "numReplicas": '1',
        "ipAddress": "40.76.76.187",
        "port": '80',
        "sslEnabled": False,
        "id": "blah",
        "name": "blah",
        "description": "",
        "tags": "",
        "kvTags": {},
        "properties": {},
        "state": "Healthy",
        "createdTime": "2018-11-06T00:44:43.6122342Z",
        "updatedTime": "2018-11-06T00:44:43.6122342Z",
        "computeType": UNKNOWN_WEBSERVICE_TYPE
    }
])

@pytest.mark.skip
def test_unknown_webservice_init(mock_webservices_resp):
    mock_image = mock.Mock(spec=Image)
    with mock.patch('azureml.core.webservice.webservice.Webservice._get',
                    return_value=mock_webservices_resp), \
        mock.patch('azureml.core.webservice.webservice._get_mms_url'), \
            mock.patch('azureml.core.image.image.Image.deserialize', return_value=mock_image):
            mock_ws = get_workspace_mock()
            webservice = Webservice(mock_ws, "blah")
            assert isinstance(webservice, UnknownWebservice)


@pytest.mark.parametrize("mock_webservices_resp", [
    {
        "imageId": "blah-resnet50:2",
        "imageDetails": {
            "id": "blah-resnet50:2",
            "name": "blah-resnet50",
            "version": '2',
            "description": "",
            "tags": "",
            "kvTags": "",
            "properties": "",
            "createdTime": "2018-11-05T19:12:17.0180845Z",
            "imageType":  UNKNOWN_IMAGE_TYPE,
            "imageFlavor": "BrainwavePackage",
            "creationState": "NotStarted",
            "modelIds": [
                "resnet-50-rtai:11"
            ],
            "imageLocation": "aml://artifact/LocalUpload/fpga/blah-resnet50:2"
        },
        "numReplicas": '1',
        "ipAddress": "40.76.76.187",
        "port": '80',
        "sslEnabled": False,
        "id": "blah",
        "name": "blah",
        "description": "",
        "tags": "",
        "kvTags": {},
        "properties": {},
        "state": "Healthy",
        "createdTime": "2018-11-06T00:44:43.6122342Z",
        "updatedTime": "2018-11-06T00:44:43.6122342Z",
        "computeType": UNKNOWN_WEBSERVICE_TYPE
    }
])

@pytest.mark.skip
def test_unknown_webservice_list(mock_webservices_resp):
    mock_image = mock.Mock(spec=Image)
    mock_webservice_response = mock.Mock()
    mock_webservice_response.content = json.dumps({"value": [mock_webservices_resp]})
    mock_webservice_response.raise_for_status = mock.Mock()
    with mock.patch('azureml.core.webservice.webservice._get_mms_url'), \
        mock.patch('azureml.core.webservice.webservice.requests.get', return_value=mock_webservice_response), \
            mock.patch('azureml.core.image.image.Image.deserialize', return_value=mock_image):
            mock_ws = get_workspace_mock()
            webservices = Webservice.list(mock_ws)
            assert len(webservices) == 1
            assert isinstance(webservices[0], UnknownWebservice)

