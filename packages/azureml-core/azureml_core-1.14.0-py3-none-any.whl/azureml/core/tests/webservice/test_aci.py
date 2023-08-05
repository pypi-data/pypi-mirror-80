# ---------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# ---------------------------------------------------------
import copy
import json
import pytest

from azureml.core.webservice import AciWebservice
from azureml.exceptions import WebserviceException
from unittest.mock import patch, Mock, PropertyMock


@pytest.fixture(scope='function')
def mock_webservice():
    webservice = AciWebservice(None, None)

    return webservice


class TestAciWebservice(object):
    @patch('azureml.core.webservice.aci.Model.deserialize')
    @patch('azureml.core.webservice.aci.Environment._deserialize_and_add_to_object')
    @patch('azureml.core.webservice.aci.VnetConfiguration.deserialize')
    @patch('azureml.core.webservice.aci.EncryptionProperties.deserialize')
    @patch('azureml.core.webservice.aci.ContainerResourceRequirements.deserialize')
    @patch('azureml.core.webservice.aci.Webservice._initialize')
    @patch('azureml.core.webservice.aci.AciWebservice._validate_get_payload')
    def test__initialize(self, mock_validate_payload, mock_super_init, mock_crr_deserialize, mock_ep_deserialize,
                         mock_vc_deserialize, mock_env_deserialize, mock_model_deserialize, mock_webservice,
                         mock_workspace):
        app_insights_enabled = True
        cname = 'cname'
        container_resource_requirements = 'container_resource_requirements'
        encryption_properties = 'encryption_properties'
        vnet_configuration = 'vnet_configuration'
        location = 'location'
        public_ip = 'public_ip'
        scoring_uri = 'scoring/uri'
        ssl_certificate = 'ssl_certificate'
        ssl_enabled = 'ssl_enabled'
        ssl_key = 'ssl_key'
        public_fqdn = 'public_fqdn'
        environment_image_request = {'environment': 'env_object'}
        models = ['model']
        model_config_map = 'model_config_map'

        payload = {'appInsightsEnabled': app_insights_enabled, 'cname': cname,
                   'containerResourceRequirements': container_resource_requirements,
                   'encryptionProperties': encryption_properties, 'vnetConfiguration': vnet_configuration,
                   'location': location, 'publicIp': public_ip, 'scoringUri': scoring_uri,
                   'sslCertificate': ssl_certificate, 'sslEnabled': ssl_enabled, 'sslKey': ssl_key,
                   'publicFqdn': public_fqdn, 'environmentImageRequest': environment_image_request, 'models': models,
                   'modelConfigMap': model_config_map}

        mock_webservice._initialize(mock_workspace, payload)

        mock_validate_payload.assert_called_once_with(payload)
        mock_super_init.assert_called_once_with(mock_workspace, payload)
        mock_crr_deserialize.assert_called_once_with(container_resource_requirements)
        mock_ep_deserialize.assert_called_once_with(encryption_properties)
        mock_vc_deserialize.assert_called_once_with(vnet_configuration)
        mock_env_deserialize.assert_called_once_with('env_object')
        mock_model_deserialize.assert_called_once_with(mock_workspace, 'model')

    @patch('azureml.core.webservice.aci.AciServiceDeploymentConfiguration')
    def test_deploy_configuration(self, mock_deploy_config):
        cpu_cores = 'cpu_cores'
        memory_gb = 'memory_gb'
        tags = 'tags'
        properties = 'properties'
        description = 'description'
        location = 'location'
        auth_enabled = 'auth_enabled'
        ssl_enabled = 'ssl_enabled'
        enable_app_insights = 'enable_app_insights'
        ssl_cert_pem_file = 'ssl_cert_pem_file'
        ssl_key_pem_file = 'ssl_key_pem_file'
        ssl_cname = 'ssl_cname'
        dns_name_label = 'dns_name_label'
        primary_key = 'primary_key'
        secondary_key = 'secondary_key'
        collect_model_data = 'collect_model_data'
        cmk_vault_base_url = 'cmk_vault_base_url'
        cmk_key_name = 'cmk_key_name'
        cmk_key_version = 'cmk_key_version'
        vnet_name = 'vnet_name'
        subnet_name = 'subnet_name'
        deploy_config = Mock()
        mock_deploy_config.return_value = deploy_config

        result = AciWebservice.deploy_configuration(cpu_cores, memory_gb, tags, properties, description, location,
                                                    auth_enabled, ssl_enabled, enable_app_insights, ssl_cert_pem_file,
                                                    ssl_key_pem_file, ssl_cname, dns_name_label, primary_key,
                                                    secondary_key, collect_model_data, cmk_vault_base_url,
                                                    cmk_key_name, cmk_key_version, vnet_name, subnet_name)
        mock_deploy_config.assert_called_once_with(cpu_cores=cpu_cores, memory_gb=memory_gb, tags=tags,
                                                   properties=properties, description=description,
                                                   location=location, auth_enabled=auth_enabled,
                                                   ssl_enabled=ssl_enabled, enable_app_insights=enable_app_insights,
                                                   ssl_cert_pem_file=ssl_cert_pem_file,
                                                   ssl_key_pem_file=ssl_key_pem_file,
                                                   ssl_cname=ssl_cname, dns_name_label=dns_name_label,
                                                   primary_key=primary_key, secondary_key=secondary_key,
                                                   collect_model_data=collect_model_data,
                                                   cmk_vault_base_url=cmk_vault_base_url,
                                                   cmk_key_name=cmk_key_name,
                                                   cmk_key_version=cmk_key_version,
                                                   vnet_name=vnet_name, subnet_name=subnet_name)
        assert deploy_config == result

    @patch('azureml.core.webservice.aci.Webservice._webservice_session', new_callable=PropertyMock)
    @patch('azureml.core.webservice.aci.AciWebservice.get_keys')
    @patch('azureml.core.webservice.aci.ClientBase')
    def test_run(self, mock_client_base, mock_get_keys, mock_webservice_session, mock_webservice, mock_http_response):
        mock_webservice.scoring_uri = None
        mock_webservice.state = 'Failed'
        mock_webservice.error = 'error'

        with pytest.raises(WebserviceException):
            mock_webservice.run('data')

        mock_webservice.scoring_uri = 'scoring_uri'
        mock_client_base._execute_func.return_value = mock_http_response(500, None)

        with pytest.raises(WebserviceException):
            mock_webservice.run('data')

        mock_client_base._execute_func.return_value = mock_http_response(200, {'content_key': 'content_val'})
        expected = {'status_code': 200, 'content': {'content_key': 'content_val'}, 'headers': None}
        result = mock_webservice.run('data')
        assert expected == result

        mock_client_base._execute_func.side_effect = [mock_http_response(401, None),
                                                      mock_http_response(200, {'content_key': 'content_val'})]
        mock_webservice.auth_enabled = True
        mock_webservice._session = Mock()
        mock_webservice._session.headers = {}
        mock_get_keys.return_value = ['key1', 'key2']
        result = mock_webservice.run('data')
        assert expected == result

    @patch('azureml.core.webservice.aci.AciWebservice.update_deployment_state')
    @patch('azureml.core.webservice.aci.get_requests_session')
    @patch('azureml.core.webservice.aci.ClientBase')
    @patch('azureml.core.webservice.aci.global_tracking_info_registry')
    @patch('azureml.core.webservice.aci.build_and_validate_no_code_environment_image_request')
    @patch('azureml.core.webservice.aci.convert_parts_to_environment')
    @patch('azureml.core.webservice.aci.AciWebservice._validate_update')
    def test_update(self, mock_validate_update, mock_convert_to_env, mock_validate_no_code, mock_global_tracking,
                    mock_client_base, mock_get_session, mock_update_deployment_state, mock_webservice, mock_workspace,
                    mock_http_response):
        with pytest.raises(WebserviceException):
            mock_webservice.update()

        tags = {'tag_key': 'tag_val'}
        properties = {'prop_key': 'prop_val'}
        description = 'description'
        auth_enabled = 'auth_enabled'
        ssl_enabled = 'ssl_enabled'
        ssl_cname = 'ssl_cname'
        enable_app_insights = 'enable_app_insights'
        inference_config = Mock()
        environment_image_request = 'environment_image_request'
        inference_config._build_environment_image_request.return_value = environment_image_request
        mock_convert_to_env.return_value = inference_config, None
        mock_webservice.environment = Mock()
        mock_webservice._mms_endpoint = '/mms/base/endpoint'
        mock_webservice.image = None
        model = Mock()
        model.id = 'foo:1'
        mock_webservice.models = [model]
        mock_webservice.workspace = mock_workspace
        mock_webservice._auth = mock_workspace._auth_object
        mock_webservice.name = 'webservice_name'
        mock_global_tracking.gather_all.return_value = {'global_key': 'global_val'}
        mock_client_base._execute_func.return_value = mock_http_response(200, json.dumps({'operationId': 'op_id'}))

        mock_webservice.update(tags=tags, properties=properties, description=description, auth_enabled=auth_enabled,
                               ssl_enabled=ssl_enabled, ssl_cname=ssl_cname, enable_app_insights=enable_app_insights,
                               inference_config=inference_config)
        mock_validate_update.assert_called_once_with(None, tags, properties, description, auth_enabled, ssl_enabled,
                                                     None, None, ssl_cname, enable_app_insights, None,
                                                     inference_config)
        inference_config._build_environment_image_request.assert_called_once_with(mock_workspace, [model.id])
        mock_global_tracking.gather_all.assert_called_once()
        mock_update_deployment_state.assert_called_once()
        assert '/mms/operations/op_id' == mock_webservice._operation_endpoint

        models = [model]
        mock_client_base._execute_func.return_value = mock_http_response(202, None, {'Operation-Location': 'op_id'})
        mock_webservice.update(tags=tags, properties=properties, description=description, auth_enabled=auth_enabled,
                               ssl_enabled=ssl_enabled, ssl_cname=ssl_cname, enable_app_insights=enable_app_insights,
                               models=models)
        mock_validate_no_code.assert_called_once_with(models)

        mock_client_base._execute_func.return_value = mock_http_response(500, None)
        with pytest.raises(WebserviceException):
            mock_webservice.update(tags=tags, properties=properties, description=description,
                                   auth_enabled=auth_enabled, ssl_enabled=ssl_enabled, ssl_cname=ssl_cname,
                                   enable_app_insights=enable_app_insights, models=models)

    def test__validate_update(self, mock_webservice):
        ssl_cert_pem_file = 'cert_file'
        ssl_key_pem_file = 'key_file'
        ssl_enabled = False
        mock_webservice.ssl_enabled = False

        try:
            mock_webservice._validate_update(None, None, None, None, None, ssl_enabled, ssl_cert_pem_file,
                                             ssl_key_pem_file, None, None, None, None)
            pytest.fail('This should throw')
        except WebserviceException as e:
            assert 'SSL must be enabled in order to update SSL cert/key' in e.message
            assert 'unable to find ssl_cert_pem_file at provided path' in e.message
            assert 'unable to find ssl_key_pem_file at provided path' in e.message

    @patch('azureml.core.webservice.aci.AciWebservice.update')
    @patch('azureml.core.webservice.aci.AciWebservice._add_tags')
    def test_add_tags(self, mock_add_tags, mock_update, mock_webservice):
        tags = {'new_tag': 'new_val'}
        old_tags = {'old_tag': 'old_val'}
        merged = copy.deepcopy(tags)
        merged.update(old_tags)
        mock_webservice.tags = old_tags
        mock_add_tags.return_value = merged

        mock_webservice.add_tags(tags)
        mock_add_tags.assert_called_once_with(tags)
        mock_update.assert_called_once_with(tags=merged)
        assert merged == mock_webservice.tags

    @patch('azureml.core.webservice.aci.AciWebservice.update')
    @patch('azureml.core.webservice.aci.AciWebservice._remove_tags')
    def test_remove_tags(self, mock_remove_tags, mock_update, mock_webservice):
        old_tags = {'old_tag': 'old_val'}
        mock_remove_tags.return_value = {}
        mock_webservice.tags = old_tags
        tags_to_remove = ['old_tag']

        mock_webservice.remove_tags(tags_to_remove)
        mock_remove_tags.assert_called_once_with(tags_to_remove)
        mock_update.assert_called_once_with(tags={})
        assert {} == mock_webservice.tags

    @patch('azureml.core.webservice.aci.AciWebservice.update')
    @patch('azureml.core.webservice.aci.AciWebservice._add_properties')
    def test_add_properties(self, mock_add_properties, mock_update, mock_webservice):
        properties = {'new_prop': 'new_val'}
        old_properties = {'old_prop': 'old_val'}
        merged = copy.deepcopy(properties)
        merged.update(old_properties)
        mock_webservice.properties = old_properties
        mock_add_properties.return_value = merged

        mock_webservice.add_properties(properties)
        mock_add_properties.assert_called_once_with(properties)
        mock_update.assert_called_once_with(properties=merged)
        assert merged == mock_webservice.properties

    @patch('azureml.core.webservice.aci.Environment._serialize_to_dict')
    @patch('azureml.core.webservice.aci.Webservice.serialize')
    def test_serialize(self, mock_super_serialize, mock_env_serialize, mock_webservice):
        mock_super_serialize.return_value = {'parent_key': 'parent_val'}
        container_resource_requirements = Mock()
        encryption_properties = Mock()
        vnet_configuration = Mock()
        env_details = {'env_key': 'env_val'}
        mock_env_serialize.return_value = env_details
        model = Mock()
        mock_webservice.container_resource_requirements = container_resource_requirements
        mock_webservice.encryption_properties = encryption_properties
        mock_webservice.vnet_configuration = vnet_configuration
        mock_webservice.image_id = None
        mock_webservice.scoring_uri = 'scoring_uri'
        mock_webservice.location = 'location'
        mock_webservice.auth_enabled = 'auth_enabled'
        mock_webservice.ssl_enabled = 'ssl_enabled'
        mock_webservice.enable_app_insights = 'enable_app_insights'
        mock_webservice.ssl_certificate = 'ssl_certificate'
        mock_webservice.ssl_key = 'ssl_key'
        mock_webservice.cname = 'cname'
        mock_webservice.public_ip = 'public_ip'
        mock_webservice.public_fqdn = 'public_fqdn'
        mock_webservice.environment = 'environment'
        mock_webservice.models = [model]
        expected = {'parent_key': 'parent_val',
                    'containerResourceRequirements': container_resource_requirements.serialize.return_value,
                    'imageId': mock_webservice.image_id, 'scoringUri': mock_webservice.scoring_uri,
                    'location': mock_webservice.location, 'authEnabled': mock_webservice.auth_enabled,
                    'sslEnabled': mock_webservice.ssl_enabled,
                    'appInsightsEnabled': mock_webservice.enable_app_insights,
                    'sslCertificate': mock_webservice.ssl_certificate, 'sslKey': mock_webservice.ssl_key,
                    'cname': mock_webservice.cname, 'publicIp': mock_webservice.public_ip,
                    'publicFqdn': mock_webservice.public_fqdn, 'environmentDetails': env_details,
                    'modelDetails': [model.serialize.return_value],
                    'encryptionProperties': encryption_properties.serialize.return_value,
                    'vnetConfiguration': vnet_configuration.serialize.return_value}

        result = mock_webservice.serialize()
        assert expected == result

    def test_get_token(self, mock_webservice):
        with pytest.raises(NotImplementedError):
            mock_webservice.get_token()

