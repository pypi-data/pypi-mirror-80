# ---------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# ---------------------------------------------------------
import copy
import json
import pytest
import types

from azureml.core.webservice import Webservice
from azureml.exceptions import WebserviceException
from datetime import datetime
from unittest.mock import patch, Mock


@pytest.fixture(scope='function')
def mock_webservice():
    webservice = Mock(spec=Webservice)

    return webservice


class TestWebservice(object):

    def test_new(self):
        pytest.skip('Unimplimented')

    def test_repr(self, mock_webservice):
        mock_webservice.__repr__ = Webservice.__repr__

        returned = mock_webservice.__repr__()
        assert 'workspace=' in returned
        assert 'name=' in returned
        assert 'image_id=' in returned
        assert 'compute_type=' in returned
        assert 'state=' in returned
        assert 'scoring_uri=' in returned
        assert 'tags=' in returned
        assert 'properties=' in returned
        assert 'created_by=' in returned

    def test__all_subclasses(self):
        pytest.skip('Unimplimented')

    def test__webservice_session(self):
        pytest.skip('Unimplimented')

    @patch('azureml.core.webservice.webservice._get_mms_url')
    @patch('azureml.core.webservice.webservice.Image.deserialize')
    def test__initialize(self, mock_image_deserialize, mock_get_mms_url, mock_webservice, mock_workspace):
        mock_webservice._initialize = types.MethodType(Webservice._initialize, mock_webservice)
        mock_image = Mock()
        mock_image_deserialize.return_value = mock_image
        mock_get_mms_url.return_value = 'mock/root/url'
        obj_dict = {'authEnabled': True, 'computeType': 'AKS', 'createdTime': datetime.now().strftime('%y%m%dT%H%M%S'),
                    'description': 'webservice description', 'imageId': 'foo:1', 'imageDigest': 'image digest',
                    'kvTags': {'key': 'value'}, 'name': 'webservice_name', 'properties': {'key': 'value'},
                    'createdBy': 'created_by_obj', 'error': None, 'imageDetails': 'image_details_obj',
                    'state': 'succeeded', 'updatedTime': datetime.now().strftime('%y%m%dT%H%M%S')}

        mock_webservice._initialize(mock_workspace, obj_dict)
        mock_image_deserialize.assert_called_once_with(mock_workspace, 'image_details_obj')
        mock_get_mms_url.assert_called_once_with(mock_workspace)

    @patch('azureml.core.webservice.webservice.get_requests_session')
    @patch('azureml.core.webservice.webservice.ClientBase')
    @patch('azureml.core.webservice.webservice._get_mms_url')
    def test__get(self, mock_get_mms_url, mock_client_base, mock_get_session, mock_workspace, mock_http_response):
        with pytest.raises(WebserviceException):
            Webservice._get(mock_workspace)

        name = 'foo'
        base_url = 'mock/base/url'
        mock_get_mms_url.return_value = base_url
        mock_client_base._execute_func.return_value = mock_http_response(200,
                                                                         json.dumps({'service_key': 'service_val'}))

        result = Webservice._get(mock_workspace, name)
        mock_get_mms_url.assert_called_once_with(mock_workspace)
        mock_get_session.assert_called_once()
        assert result == {'service_key': 'service_val'}

        mock_client_base._execute_func.return_value = mock_http_response(404, None)
        result = Webservice._get(mock_workspace, name)
        assert not result

        mock_client_base._execute_func.return_value = mock_http_response(500, None)
        with pytest.raises(WebserviceException):
            Webservice._get(mock_workspace, name)

    def test_check_webservice_exists(self, mock_workspace):
        try:
            Webservice.check_for_existing_webservice(mock_workspace, "mj-aci-model-test03", False, lambda: '''
            {
              "id": null,
              "name": "mj-aci-model-test03",
              "description": null,
              "tags": null,
              "kvTags": null,
              "properties": null,
              "operationId": null,
              "state": "Transitioning",
              "createdTime": "2020-08-24T07:20:29.7806277",
              "error": {
                "message": "Service mj-aci-model-test03 with the same name already exists, please use a different service name or delete the existing service."
              },
              "computeType": "UNKNOWN",
              "createdBy": null
            }
            ''')
        except WebserviceException as e:
            assert "Service mj-aci-model-test03 with the same name already exists, please use a different service " \
                   "name or delete the existing service." == e.message
            return

        pytest.fail("should throw WebserviceException")

    def test_check_webservice_not_exists(self, mock_workspace):
        Webservice.check_for_existing_webservice(mock_workspace, "mj-aci-model-test03", False, lambda: '''
        {
          "id": null,
          "name": "mj-aci-model-test03",
          "description": null,
          "tags": null,
          "kvTags": null,
          "properties": null,
          "operationId": null,
          "state": "Transitioning",
          "createdTime": "2020-08-24T07:20:29.7806277",
          "computeType": "UNKNOWN",
          "createdBy": null
        }
        ''')

    def test_check_webservice_overwrite(self, mock_workspace):
        Webservice.check_for_existing_webservice(mock_workspace, "mj-aci-model-test03", True, lambda: '''
        {
          "id": null,
          "name": "mj-aci-model-test03",
          "description": null,
          "tags": null,
          "kvTags": null,
          "properties": null,
          "operationId": null,
          "state": "Transitioning",
          "createdTime": "2020-08-24T07:20:29.7806277",
          "error": {
            "message": "Service mj-aci-model-test03 with the same name already exists, please use a different service name or delete the existing service."
          },
          "computeType": "UNKNOWN",
          "createdBy": null
        }
        ''')

    def test_check_webservice_url_no_response_content(self, mock_workspace):
        Webservice.check_for_existing_webservice(mock_workspace, "mj-aci-model-test03", False, lambda: None)

    @patch('azureml.core.webservice.webservice.ClientBase')
    @patch('azureml.core.webservice.webservice._get_mms_url')
    def test__deploy_webservice(self, mock_get_mms_url, mock_client_base, mock_workspace, mock_http_response):
        mock_get_mms_url.return_value = 'mock/base/url'
        mock_client_base._execute_func.return_value = mock_http_response(202, None, {'Operation-Location':
                                                                                     'operation/url/operation/id'})
        name = "foo"
        payload = {'payload_key': 'payload_value'}
        webservice_class = Mock()
        expected = webservice_class.return_value

        result = Webservice._deploy_webservice(mock_workspace, name, payload, False, webservice_class)
        webservice_class.assert_called_once_with(mock_workspace, name=name)
        assert result == expected

        mock_client_base._execute_func.return_value = mock_http_response(500, None)
        with pytest.raises(WebserviceException):
            Webservice._deploy_webservice(mock_workspace, name, payload, False, webservice_class)

        mock_client_base._execute_func.return_value = mock_http_response(400, None)
        with pytest.raises(WebserviceException):
            Webservice._deploy_webservice(mock_workspace, name, payload, False, webservice_class)

    def test_wait_for_deployment(self, mock_webservice):
        mock_webservice.wait_for_deployment = types.MethodType(Webservice.wait_for_deployment, mock_webservice)
        mock_webservice._wait_for_operation_to_complete = Mock()
        mock_webservice.update_deployment_state = Mock()
        mock_webservice._wait_for_operation_to_complete.return_value = 'Succeeded', None, None
        mock_webservice.state = 'Failed'
        mock_webservice._operation_endpoint = 'operation/endpoint'

        mock_webservice.wait_for_deployment()
        mock_webservice.update_deployment_state.assert_called_once()

        mock_webservice._wait_for_operation_to_complete.return_value = ('Failed', {'error_key': 'error_val'},
                                         {'operationDetails': {'subOperationType': 'BuildEnvironment'}})
        with pytest.raises(WebserviceException):  # TODO add check for exception string
            mock_webservice.wait_for_deployment()

        mock_webservice._wait_for_operation_to_complete.return_value = ('Failed', {'error_key': 'error_val'},
                                         {'operationDetails': {'subOperationType': 'DeployService'}})
        with pytest.raises(WebserviceException):  # TODO add check for exception string
            mock_webservice.wait_for_deployment()

        mock_webservice._wait_for_operation_to_complete.return_value = 'Failed', None, {}
        mock_webservice.error = None

        with pytest.raises(WebserviceException):  # TODO add check for exception string
            mock_webservice.wait_for_deployment()

        mock_webservice.error = {'error_key': 'error_val'}

        with pytest.raises(WebserviceException):  # TODO add check for exception string
            mock_webservice.wait_for_deployment()

        mock_webservice._wait_for_operation_to_complete.side_effect = WebserviceException('No operation endpoint')
        mock_webservice.update_deployment_state.reset_mock()
        with pytest.raises(WebserviceException):  # TODO add check for exception string
            mock_webservice.wait_for_deployment()
            mock_webservice.update_deployment_state.assert_called_once()

    @patch('azureml.core.webservice.webservice.time.sleep')
    def test__wait_for_operation_to_complete(self, mock_sleep, mock_webservice):
        mock_webservice._wait_for_operation_to_complete = types.MethodType(Webservice._wait_for_operation_to_complete,
                                                                           mock_webservice)
        mock_webservice._operation_endpoint = None
        show_output = False

        with pytest.raises(WebserviceException):
            mock_webservice._wait_for_operation_to_complete(show_output)

        mock_webservice._operation_endpoint = 'operation/endpoint'
        mock_webservice._get_operation_state.side_effect = [('Running', None, None), ('Failed', 'error', 'operation')]

        result = mock_webservice._wait_for_operation_to_complete(show_output)
        mock_sleep.assert_called_once()
        assert ('Failed', 'error', 'operation') == result
        assert 2 == mock_webservice._get_operation_state.call_count

    @patch('azureml.core.webservice.webservice.get_requests_session')
    @patch('azureml.core.webservice.webservice.ClientBase')
    def test__get_operation_state(self, mock_client_base, mock_get_session, mock_webservice, mock_workspace,
                                  mock_http_response):
        mock_webservice._get_operation_state = types.MethodType(Webservice._get_operation_state, mock_webservice)
        mock_webservice._auth = mock_workspace._auth_object
        mock_webservice._operation_endpoint = 'operation/endpoint'
        mock_client_base._execute_func.return_value = mock_http_response(200, json.dumps({'state': 'Failed',
                                                                                          'error': 'error'}))

        result = mock_webservice._get_operation_state()
        mock_get_session.assert_called_once()
        mock_client_base._execute_func.assert_called_once()
        assert result == ('Failed', 'error', {'state': 'Failed', 'error': 'error'})

        mock_client_base._execute_func.return_value = mock_http_response(500, None)
        with pytest.raises(WebserviceException):
            mock_webservice._get_operation_state()

    def test_update_deployment_state(self):
        mock_webservice.update_deployment_state = types.MethodType(Webservice.update_deployment_state, mock_webservice)
        mock_webservice.workspace = "workspace"
        mock_webservice.name = "name"

        with patch('azureml.core.webservice.webservice.Webservice') as mock_webservice_class:
            mock_instance = mock_webservice_class.return_value
            mock_instance.__dict__ = mock_webservice.__dict__
            mock_webservice.update_deployment_state()
            mock_webservice_class.assert_called_once_with(mock_webservice.workspace, name=mock_webservice.name)

    @patch('azureml.core.webservice.webservice.Webservice._all_subclasses')
    @patch('azureml.core.webservice.webservice.get_requests_session')
    @patch('azureml.core.webservice.webservice.get_paginated_results')
    @patch('azureml.core.webservice.webservice.ClientBase')
    @patch('azureml.core.webservice.webservice._get_mms_url')
    def test_list(self, mock_get_mms_url, mock_client_base, mock_get_paginated_results, mock_get_session,
                  mock_all_subclasses, mock_workspace, mock_http_response):
        compute_type = 'bad'

        with pytest.raises(WebserviceException):
            Webservice.list(mock_workspace, compute_type)

        compute_type = 'ACI'
        model_name = 'foo'
        model_id = 'foo:1'
        tags = ['tag', ['tag2', 'value2']]
        properties = ['prop', ['prop2', 'propvalue2']]
        image_digest = 'image_digest'
        service_payload = {'payload_key': 'payload_val', 'computeType': 'ACI'}
        mock_client_base._execute_func.return_value = mock_http_response(200, json.dumps(service_payload))
        paginated_results = [service_payload]
        mock_get_paginated_results.return_value = paginated_results
        mock_child_class = Mock()
        mock_child_class._webservice_type = 'ACI'
        mock_child_instance = mock_child_class.deserialize.return_value
        mock_all_subclasses.return_value = [mock_child_class]

        result = Webservice.list(mock_workspace, compute_type, model_name=model_name, model_id=model_id, tags=tags,
                                 properties=properties, image_digest=image_digest)
        mock_client_base._execute_func.assert_called_once()
        mock_get_session.assert_called_once()
        mock_get_paginated_results.assert_called_once()
        mock_child_class.deserialize.assert_called_once_with(mock_workspace, service_payload)
        assert [mock_child_instance] == result

    def test__add_tags(self, mock_webservice):
        mock_webservice._add_tags = types.MethodType(Webservice._add_tags, mock_webservice)
        tags = {'new_tag': 'new_val'}
        mock_webservice.tags = None

        result = mock_webservice._add_tags(tags)
        assert tags == result

        old_tags = {'old_tag': 'old_val'}
        expected = copy.deepcopy(old_tags)
        expected.update(tags)
        mock_webservice.tags = old_tags

        result = mock_webservice._add_tags(tags)
        assert expected == result

    def test__remove_tags(self, mock_webservice):
        mock_webservice._remove_tags = types.MethodType(Webservice._remove_tags, mock_webservice)
        mock_webservice.tags = None
        tags = {'existing_key': 'existing_val', 'key_2': 'val_2'}
        tag_to_remove = 'existing_key'

        result = mock_webservice._remove_tags(tag_to_remove)
        assert not result

        mock_webservice.tags = tags
        result = mock_webservice._remove_tags(tag_to_remove)
        assert {'key_2': 'val_2'} == result

    def test__add_properties(self, mock_webservice):
        mock_webservice._add_properties = types.MethodType(Webservice._add_properties, mock_webservice)
        props = {'new_prop': 'new_val'}
        mock_webservice.properties = None

        result = mock_webservice._add_properties(props)
        assert props == result

        old_props = {'old_prop': 'old_val'}
        expected = copy.deepcopy(old_props)
        expected.update(props)
        mock_webservice.properties = old_props

        result = mock_webservice._add_properties(props)
        assert expected == result

    @patch('azureml.core.webservice.webservice.get_requests_session')
    @patch('azureml.core.webservice.webservice.ClientBase')
    def test_get_logs(self, mock_client_base, mock_get_session, mock_webservice, mock_workspace, mock_http_response):
        mock_webservice.get_logs = types.MethodType(Webservice.get_logs, mock_webservice)
        mock_webservice.workspace = mock_workspace
        mock_webservice._mms_endpoint = 'mms/endpoint'
        session_get = mock_get_session.return_value
        headers = {'Content-Type': 'application/json', 'Bearer': 'key'}
        mock_workspace._auth_object.get_authentication_header = Mock()
        mock_workspace._auth_object.get_authentication_header.return_value = {'Bearer': 'key'}

        num_lines = 1000
        init = True
        mock_client_base._execute_func.return_value = mock_http_response(404, None)

        with pytest.raises(WebserviceException):
            mock_webservice.get_logs()

        mock_client_base._execute_func.return_value = mock_http_response(200, json.dumps({'invalid': 'payload'}))

        with pytest.raises(WebserviceException):
            mock_webservice.get_logs()

        response_payload = {'content': 'logs'}
        mock_client_base._execute_func.reset_mock()
        mock_client_base._execute_func.return_value = mock_http_response(200, json.dumps(response_payload))
        expected_params = {'tail': 5000, 'init': False}

        result = mock_webservice.get_logs()
        assert response_payload['content'] == result
        mock_client_base._execute_func.assert_called_once_with(session_get.get, 'mms/endpoint/logs', headers=headers,
                                                               params=expected_params)

        mock_client_base._execute_func.reset_mock()
        expected_params = {'tail': num_lines, 'init': init}

        result = mock_webservice.get_logs(num_lines, init)
        assert response_payload['content'] == result
        mock_client_base._execute_func.assert_called_once_with(session_get.get, 'mms/endpoint/logs', headers=headers,
                                                               params=expected_params)

    @patch('azureml.core.webservice.webservice.get_requests_session')
    @patch('azureml.core.webservice.webservice.ClientBase')
    def test_get_keys(self, mock_client_base, mock_get_session, mock_webservice, mock_workspace, mock_http_response):
        mock_webservice.get_keys = types.MethodType(Webservice.get_keys, mock_webservice)
        mock_webservice._auth = mock_workspace._auth_object
        mock_webservice._mms_endpoint = 'mms/endpoint'
        response_payload = {}
        mock_client_base._execute_func.return_value = mock_http_response(500, json.dumps(response_payload))

        with pytest.raises(WebserviceException):
            mock_webservice.get_keys()

        mock_client_base._execute_func.return_value = mock_http_response(200, json.dumps(response_payload))

        with pytest.raises(WebserviceException):
            mock_webservice.get_keys()

        response_payload = {'primaryKey': 'primary_key'}
        mock_client_base._execute_func.return_value = mock_http_response(200, json.dumps(response_payload))

        with pytest.raises(WebserviceException):
            mock_webservice.get_keys()

        response_payload = {'primaryKey': 'primary_key', 'secondaryKey': 'secondary_key'}
        mock_client_base._execute_func.return_value = mock_http_response(200, json.dumps(response_payload))

        primary_key, secondary_key = mock_webservice.get_keys()
        assert primary_key == 'primary_key'
        assert secondary_key == 'secondary_key'

    @patch('azureml.core.webservice.webservice.time.sleep', Mock(return_value=None))
    @patch('azureml.core.webservice.webservice._get_mms_url')
    @patch('azureml.core.webservice.webservice.get_requests_session')
    @patch('azureml.core.webservice.webservice.ClientBase')
    def test_regen_key(self, mock_client_base, mock_get_session, mock_get_mms_url, mock_webservice, mock_workspace,
                       mock_http_response):
        mock_webservice.regen_key = types.MethodType(Webservice.regen_key, mock_webservice)
        mock_webservice.workspace = mock_workspace
        mock_webservice._auth = mock_workspace._auth_object
        mock_webservice._mms_endpoint = 'mms/endpoint'

        with pytest.raises(WebserviceException):
            mock_webservice.regen_key(None)

        with pytest.raises(WebserviceException):
            mock_webservice.regen_key('badkey')

        mock_client_base._execute_func.return_value = mock_http_response(500, None)

        with pytest.raises(WebserviceException):
            mock_webservice.regen_key('Primary')

        mock_client_base._execute_func.return_value = mock_http_response(200, None, {})

        with pytest.raises(WebserviceException):
            mock_webservice.regen_key('Primary')

        mock_client_base._execute_func.side_effect = [mock_http_response(200, None, {'Operation-Location': 'op/loc'}),
                                                      mock_http_response(500, None)]

        with pytest.raises(WebserviceException):
            mock_webservice.regen_key('Primary')

        mock_client_base._execute_func.side_effect = [mock_http_response(200, None, {'Operation-Location': 'op/loc'}),
                                                      mock_http_response(200, json.dumps({'invalid': 'payload'}))]

        with pytest.raises(WebserviceException):
            mock_webservice.regen_key('Primary')

        mock_client_base._execute_func.side_effect = [mock_http_response(200, None, {'Operation-Location': 'op/loc'}),
                                                      mock_http_response(200, json.dumps({'state': 'Failed'}))]

        with pytest.raises(WebserviceException):
            mock_webservice.regen_key('Primary')

        mock_client_base._execute_func.side_effect = [mock_http_response(200, None, {'Operation-Location': 'op/loc'}),
                                                      mock_http_response(200, json.dumps({'state': 'Succeeded'}))]
        mock_webservice.regen_key('Primary')


    @patch('azureml.core.webservice.webservice._get_mms_url')
    @patch('azureml.core.webservice.webservice.get_requests_session')
    @patch('azureml.core.webservice.webservice.ClientBase')
    def test_delete(self, mock_client_base, mock_get_session, mock_get_mms_url, mock_webservice, mock_workspace,
                    mock_http_response):
        mock_webservice.delete = types.MethodType(Webservice.delete, mock_webservice)
        mock_webservice.name = 'foo'
        mock_webservice.workspace = mock_workspace
        mock_webservice._auth = mock_workspace._auth_object
        mock_webservice._mms_endpoint = 'mms/endpoint'
        mock_client_base._execute_func.return_value = mock_http_response(500, None)

        with pytest.raises(WebserviceException):
            mock_webservice.delete()

        mock_client_base._execute_func.return_value = mock_http_response(200, None)
        mock_webservice.delete()
        assert 'Deleting' == mock_webservice.state

        mock_client_base._execute_func.return_value = mock_http_response(202, None, {})
        with pytest.raises(WebserviceException):
            mock_webservice.delete()

        mock_client_base._execute_func.return_value = mock_http_response(202, None, {'Operation-Location': 'op/loc'})
        mock_webservice.delete()
        assert 'Deleting' == mock_webservice.state
        mock_webservice._wait_for_operation_to_complete.assert_called_once()

        mock_client_base._execute_func.return_value = mock_http_response(204, None)
        mock_webservice.delete()

    def test_serialize(self, mock_webservice, mock_workspace):
        mock_webservice.serialize = types.MethodType(Webservice.serialize, mock_webservice)
        mock_webservice.created_time = datetime.now()
        mock_webservice.updated_time = datetime.now()
        mock_webservice.scoring_uri = 'scoring_uri'
        mock_webservice.name = 'name'
        mock_webservice.description = 'description'
        mock_webservice.tags = 'tags'
        mock_webservice.properties = 'properties'
        mock_webservice.state = 'state'
        mock_webservice.error = 'error'
        mock_webservice.compute_type = 'compute_type'
        mock_webservice.workspace = mock_workspace
        mock_webservice.image = None
        mock_webservice.image_id = None
        mock_webservice.image_digest = 'image_digest'
        mock_webservice.created_by = 'created_by'

        expected = {'name': mock_webservice.name, 'description': mock_webservice.description,
                    'tags': mock_webservice.tags, 'properties': mock_webservice.properties,
                    'state': mock_webservice.state, 'createdTime': mock_webservice.created_time.isoformat(),
                    'updatedTime': mock_webservice.updated_time.isoformat(), 'error': mock_webservice.error,
                    'computeType': mock_webservice.compute_type, 'workspaceName': mock_webservice.workspace.name,
                    'imageId': mock_webservice.image_id, 'imageDigest': mock_webservice.image_digest,
                    'imageDetails': None, 'scoringUri': mock_webservice.scoring_uri,
                    'createdBy': mock_webservice.created_by}

        result = mock_webservice.serialize()
        assert expected == result

    def test_deserialize(self):
        pytest.skip('Unimplimented')

    def test__validate_get_payload(self):
        pytest.skip('Unimplimented')


class TestContainerResourceRequirements(object):
    def test_serialize(self):
        pytest.skip('Unimplimented')

    def test_deserialize(self):
        pytest.skip('Unimplimented')


class LivenessProbeRequirements(object):
    def test_serialize(self):
        pytest.skip('Unimplimented')

    def test_deserialize(self):
        pytest.skip('Unimplimented')


class AutoScaler(object):
    def test_serialize(self):
        pytest.skip('Unimplimented')

    def test_deserialize(self):
        pytest.skip('Unimplimented')


class DataCollection(object):
    def test_serialize(self):
        pytest.skip('Unimplimented')

    def test_deserialize(self):
        pytest.skip('Unimplimented')


class WebserviceDeploymentConfiguration(object):
    def test_validate_configuration(self):
        pytest.skip('Unimplimented')

    def test_validate_image(self):
        pytest.skip('Unimplimented')

    def test__build_base_create_payload(self):
        pytest.skip('Unimplimented')


class WebServiceAccessToken(object):
    def test_serialize(self):
        pytest.skip('Unimplimented')

    def test_deserialize(self):
        pytest.skip('Unimplimented')

