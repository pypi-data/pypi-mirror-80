# ---------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# ---------------------------------------------------------
import copy
import json
import pytest

from azureml.core.webservice import AksWebservice, AksEndpoint
from azureml.exceptions import WebserviceException
from datetime import datetime
from unittest.mock import patch, Mock, PropertyMock


@pytest.fixture(scope='function')
def mock_webservice():
    webservice = AksWebservice(None, None)

    return webservice


@pytest.fixture(scope='function')
def mock_endpoint():
    endpoint = AksEndpoint(None, None)

    return endpoint


class TestAksWebservice(object):
    @patch('azureml.core.webservice.aks.Model.deserialize')
    @patch('azureml.core.webservice.aks.Environment._deserialize_and_add_to_object')
    @patch('azureml.core.webservice.aks.DataCollection.deserialize')
    @patch('azureml.core.webservice.aks.LivenessProbeRequirements.deserialize')
    @patch('azureml.core.webservice.aks.ContainerResourceRequirements.deserialize')
    @patch('azureml.core.webservice.aks.AutoScaler.deserialize')
    @patch('azureml.core.webservice.aks.Webservice._initialize')
    @patch('azureml.core.webservice.aks.AksWebservice._validate_get_payload')
    def test__initialize(self, mock_validate_payload, mock_super_initialize, mock_as_deserialize, mock_crr_deserialize,
                        mock_lpr_deserialize, mock_dc_deserialize, mock_env_deserialize, mock_model_deserialize,
                        mock_webservice, mock_workspace):
        app_insights_enabled = 'app_insights_enabled'
        auto_scaler = 'auto_scaler'
        compute_name = 'compute_name'
        container_resource_requirements = 'container_resource_requirements'
        liveness_probe_requirements = 'liveness_probe_requirements'
        data_collection = 'data_collection'
        max_concurrent_requests_per_container = 'max_concurrent_requests_per_container'
        max_queue_wait_ms = 'max_queue_wait_ms'
        num_replicas = 'num_replicas'
        scoring_timeout_ms = 'scoring_timeout_ms'
        scoring_uri = 'scoring/uri'
        is_default = 'is_default'
        traffic_percentile = 'traffic_percentile'
        version_type = 'version_type'
        aad_auth_enabled = 'aad_auth_enabled'
        environment = 'environment_details'
        environment_image_request = {'environment': environment}
        model = {'model': 'payload'}
        models = [model]
        deployment_status = 'deployment_status'
        namespace = 'namespace'
        model_config_map = 'model_config_map'

        webservice_payload = {'appInsightsEnabled': app_insights_enabled, 'autoScaler': auto_scaler,
                              'computeName': compute_name,
                              'containerResourceRequirements': container_resource_requirements,
                              'livenessProbeRequirements': liveness_probe_requirements,
                              'dataCollection': data_collection,
                              'maxConcurrentRequestsPerContainer': max_concurrent_requests_per_container,
                              'maxQueueWaitMs': max_queue_wait_ms, 'numReplicas': num_replicas,
                              'scoringTimeoutMs': scoring_timeout_ms, 'scoringUri': scoring_uri,
                              'isDefault': is_default, 'trafficPercentile': traffic_percentile, 'type': version_type,
                              'aadAuthEnabled': aad_auth_enabled, 'environmentImageRequest': environment_image_request,
                              'models': models, 'deploymentStatus': deployment_status, 'namespace': namespace,
                              'modelConfigMap': model_config_map}

        mock_webservice._initialize(mock_workspace, webservice_payload)
        mock_validate_payload.assert_called_once_with(webservice_payload)
        mock_super_initialize.assert_called_once_with(mock_workspace, webservice_payload)
        mock_as_deserialize.assert_called_once_with(auto_scaler)
        mock_crr_deserialize.assert_called_once_with(container_resource_requirements)
        mock_lpr_deserialize.assert_called_once_with(liveness_probe_requirements)
        mock_dc_deserialize.assert_called_once_with(data_collection)
        mock_env_deserialize.assert_called_once_with(environment)
        mock_model_deserialize.assert_called_once_with(mock_workspace, model)

    @patch('azureml.core.webservice.aks.AksServiceDeploymentConfiguration')
    def test_deploy_configuration(self, mock_deploy_config):
        autoscale_enabled = 'autoscale_enabled'
        autoscale_min_replicas = 'autoscale_min_replicas'
        autoscale_max_replicas = 'autoscale_max_replicas'
        autoscale_refresh_seconds = 'autoscale_refresh_seconds'
        autoscale_target_utilization = 'autoscale_target_utilization'
        collect_model_data = 'collect_model_data'
        auth_enabled = 'auth_enabled'
        cpu_cores = 'cpu_cores'
        memory_gb = 'memory_gb'
        enable_app_insights = 'enable_app_insights'
        scoring_timeout_ms = 'scoring_timeout_ms'
        replica_max_concurrent_requests = 'replica_max_concurrent_requests'
        max_request_wait_time = 'max_request_wait_time'
        num_replicas = 'num_replicas'
        primary_key = 'primary_key'
        secondary_key = 'secondary_key'
        tags = 'tags'
        properties = 'properties'
        description = 'description'
        gpu_cores = 'gpu_cores'
        period_seconds = 'period_seconds'
        initial_delay_seconds = 'initial_delay_seconds'
        timeout_seconds = 'timeout_seconds'
        success_threshold = 'success_threshold'
        failure_threshold = 'failure_threshold'
        namespace = 'namespace'
        token_auth_enabled = 'token_auth_enabled'
        compute_target_name = 'compute_target_name'

        result = AksWebservice.deploy_configuration(autoscale_enabled, autoscale_min_replicas, autoscale_max_replicas,
                                                    autoscale_refresh_seconds, autoscale_target_utilization,
                                                    collect_model_data, auth_enabled, cpu_cores, memory_gb,
                                                    enable_app_insights, scoring_timeout_ms,
                                                    replica_max_concurrent_requests, max_request_wait_time,
                                                    num_replicas, primary_key, secondary_key, tags, properties,
                                                    description, gpu_cores, period_seconds, initial_delay_seconds,
                                                    timeout_seconds, success_threshold, failure_threshold, namespace,
                                                    token_auth_enabled, compute_target_name)
        mock_deploy_config.assert_called_once_with(autoscale_enabled, autoscale_min_replicas, autoscale_max_replicas,
                                                   autoscale_refresh_seconds, autoscale_target_utilization,
                                                   collect_model_data, auth_enabled, cpu_cores, memory_gb,
                                                   enable_app_insights, scoring_timeout_ms,
                                                   replica_max_concurrent_requests, max_request_wait_time,
                                                   num_replicas, primary_key, secondary_key, tags, properties,
                                                   description, gpu_cores, period_seconds, initial_delay_seconds,
                                                   timeout_seconds, success_threshold, failure_threshold, namespace,
                                                   token_auth_enabled, compute_target_name)
        assert mock_deploy_config.return_value == result

    @patch('azureml.core.webservice.aks.Webservice._webservice_session', new_callable=PropertyMock)
    @patch('azureml.core.webservice.aks.AksWebservice.get_token')
    @patch('azureml.core.webservice.aks.AksWebservice.get_keys')
    @patch('azureml.core.webservice.aks.ClientBase')
    def test_run(self, mock_client_base, mock_get_keys, mock_get_token, mock_webservice_session, mock_webservice,
                 mock_http_response):
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

        mock_client_base._execute_func.side_effect = [mock_http_response(401, None),
                                                      mock_http_response(200, {'content_key': 'content_val'})]
        mock_webservice.auth_enabled = False
        mock_webservice.token_auth_enabled = True
        mock_get_token.return_value = 'token', 'refresh_time'
        result = mock_webservice.run('data')
        assert expected == result

    def test_update(self):
        pytest.skip('Unimplimented')

    def test__validate_update(self):
        pytest.skip('Unimplimented')

    @patch('azureml.core.webservice.aks.AksWebservice.update')
    @patch('azureml.core.webservice.aks.AksWebservice._add_tags')
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

    @patch('azureml.core.webservice.aks.AksWebservice.update')
    @patch('azureml.core.webservice.aks.AksWebservice._remove_tags')
    def test_remove_tags(self, mock_remove_tags, mock_update, mock_webservice):
        old_tags = {'old_tag': 'old_val'}
        mock_remove_tags.return_value = {}
        mock_webservice.tags = old_tags
        tags_to_remove = ['old_tag']

        mock_webservice.remove_tags(tags_to_remove)
        mock_remove_tags.assert_called_once_with(tags_to_remove)
        mock_update.assert_called_once_with(tags={})
        assert {} == mock_webservice.tags

    @patch('azureml.core.webservice.aks.AksWebservice.update')
    @patch('azureml.core.webservice.aks.AksWebservice._add_properties')
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

    @patch('azureml.core.webservice.aks.Environment._serialize_to_dict')
    @patch('azureml.core.webservice.aks.Webservice.serialize')
    def test_serialize(self, mock_super_serialize, mock_env_serialize, mock_webservice):
        parent_serialize = {'parent_key': 'parent_val'}
        mock_super_serialize.return_value = parent_serialize
        mock_autoscaler = Mock()
        mock_autoscaler.serialize.return_value = 'autoscaler'
        mock_container_resource_requirements = Mock()
        mock_container_resource_requirements.serialize.return_value = 'container_resource_requirements'
        mock_liveness_probe_requirements = Mock()
        mock_liveness_probe_requirements.serialize.return_value = 'liveness_probe_requirements'
        mock_data_collection = Mock()
        mock_data_collection.serialize.return_value = 'data_collection'
        mock_env_serialize.return_value = 'env_details'
        mock_model = Mock()
        mock_model.serialize.return_value = 'model'
        mock_webservice.enable_app_insights = 'app_insights_enabled'
        mock_webservice.autoscaler = mock_autoscaler
        mock_webservice.compute_name = 'compute_name'
        mock_webservice.container_resource_requirements = mock_container_resource_requirements
        mock_webservice.liveness_probe_requirements = mock_liveness_probe_requirements
        mock_webservice.data_collection = mock_data_collection
        mock_webservice.max_concurrent_requests_per_container = 'max_concurrent_requests_per_container'
        mock_webservice.max_request_wait_time = 'max_queue_wait_ms'
        mock_webservice.num_replicas = 'num_replicas'
        mock_webservice.scoring_timeout_ms = 'scoring_timeout_ms'
        mock_webservice.scoring_uri = 'scoring/uri'
        mock_webservice.is_default = 'is_default'
        mock_webservice.traffic_percentile = 'traffic_percentile'
        mock_webservice.version_type = 'version_type'
        mock_webservice.auth_enabled = 'auth_enabled'
        mock_webservice.token_auth_enabled = 'aad_auth_enabled'
        mock_webservice.environment = 'environment'
        mock_webservice.models = [mock_model]
        mock_webservice.deployment_status = 'deployment_status'
        mock_webservice.namespace = 'namespace'
        mock_webservice.model_config_map = 'model_config_map'
        mock_webservice.image_id = 'image_id'

        aks_properties = {'appInsightsEnabled': mock_webservice.enable_app_insights,
                          'authEnabled': mock_webservice.auth_enabled, 'autoScaler': 'autoscaler',
                          'computeName': mock_webservice.compute_name,
                          'containerResourceRequirements': 'container_resource_requirements',
                          'dataCollection': 'data_collection', 'imageId': mock_webservice.image_id,
                          'maxConcurrentRequestsPerContainer': mock_webservice.max_concurrent_requests_per_container,
                          'maxQueueWaitMs': mock_webservice.max_request_wait_time,
                          'livenessProbeRequirements': 'liveness_probe_requirements',
                          'numReplicas': mock_webservice.num_replicas,
                          'deploymentStatus': mock_webservice.deployment_status,
                          'scoringTimeoutMs': mock_webservice.scoring_timeout_ms,
                          'scoringUri': mock_webservice.scoring_uri,
                          'aadAuthEnabled': mock_webservice.token_auth_enabled, 'environmentDetails': 'env_details',
                          'modelDetails': ['model'], 'isDefault': mock_webservice.is_default,
                          'trafficPercentile': mock_webservice.traffic_percentile,
                          'versionType': mock_webservice.version_type}
        expected = parent_serialize
        expected.update(aks_properties)

        result = mock_webservice.serialize()
        assert expected == result

    @patch('azureml.core.webservice.aks.AksWebservice._internal_get_access_token')
    def test_get_access_token(self, mock_get_access_token, mock_webservice):
        expected = mock_get_access_token.return_value

        token = mock_webservice.get_access_token()
        mock_get_access_token.assert_called_once()
        assert expected == token

    @patch('azureml.core.webservice.aks.AksServiceAccessToken')
    @patch('azureml.core.webservice.aks.get_requests_session')
    @patch('azureml.core.webservice.aks.ClientBase')
    def test__internal_get_access_token(self, mock_client_base, mock_get_session, mock_service_access_token,
                                        mock_webservice, mock_workspace, mock_http_response):
        mock_webservice._auth = mock_workspace._auth_object
        mock_webservice._mms_endpoint = 'mms/endpoint'
        auth_token_json = {'auth': 'token'}
        mock_client_base._execute_func.return_value = mock_http_response(200, json.dumps(auth_token_json))

        result = mock_webservice._internal_get_access_token()
        mock_service_access_token.deserialize.assert_called_once_with(auth_token_json)
        assert mock_service_access_token.deserialize.return_value == result


class TestAksEndpoint(object):
    @patch('azureml.core.webservice.aks.AksWebservice._initialize')
    @patch('azureml.core.webservice.aks._get_mms_url')
    @patch('azureml.core.webservice.aks.AksEndpoint._validate_get_payload')
    def test__initialize(self, mock_validate_payload, mock_get_mms_url, mock_webservice_initialize, mock_endpoint,
                         mock_workspace):
        mock_get_mms_url.return_value = 'mms/endpoint'
        auth_enabled = 'auth_enabled'
        compute_type = 'compute_type'
        created_time = datetime.now()
        description = 'description'
        kv_tags = {'tag_key': 'tag_val'}
        name = 'name'
        properties = {'prop_tag': 'prop_val'}
        error = 'error'
        state = 'state'
        updated_time = datetime.now()
        enable_app_insights = 'enable_app_insights'
        compute_name = 'compute_name'
        scoring_uri = 'scoring_uri'
        token_auth_enabled = 'token_auth_enabled'
        deployment_status = 'deployment_status'
        namespace = 'namespace'

        payload = {'authEnabled': auth_enabled, 'computeType': compute_type,
                   'createdTime': created_time.strftime('%y%m%dT%H%M%S'), 'description': description,
                   'kvTags': kv_tags, 'name': name, 'properties': properties, 'error': error, 'state': state,
                   'updatedTime': updated_time.strftime('%y%m%dT%H%M%S'), 'appInsightsEnabled': enable_app_insights,
                   'computeName': compute_name, 'scoringUri': scoring_uri, 'aadAuthEnabled': token_auth_enabled,
                   'versions': {'version_name': 'version_payload'}, 'deploymentStatus': deployment_status,
                   'namespace': namespace}

        mock_endpoint._initialize(mock_workspace, payload)
        mock_validate_payload.assert_called_once_with(payload)
        mock_get_mms_url.assert_called_once_with(mock_workspace)
        mock_webservice_initialize.assert_called_once_with(mock_workspace, 'version_payload')

    @patch('azureml.core.webservice.aks.AksEndpointDeploymentConfiguration')
    def test_deploy_configuration(self, mock_deploy_config):
        autoscale_enabled = 'autoscale_enabled'
        autoscale_min_replicas = 'autoscale_min_replicas'
        autoscale_max_replicas = 'autoscale_max_replicas'
        autoscale_refresh_seconds = 'autoscale_refresh_seconds'
        autoscale_target_utilization = 'autoscale_target_utilization'
        collect_model_data = 'collect_model_data'
        auth_enabled = 'auth_enabled'
        cpu_cores = 'cpu_cores'
        memory_gb = 'memory_gb'
        enable_app_insights = 'enable_app_insights'
        scoring_timeout_ms = 'scoring_timeout_ms'
        replica_max_concurrent_requests = 'replica_max_concurrent_requests'
        max_request_wait_time = 'max_request_wait_time'
        num_replicas = 'num_replicas'
        primary_key = 'primary_key'
        secondary_key = 'secondary_key'
        tags = 'tags'
        properties = 'properties'
        description = 'description'
        gpu_cores = 'gpu_cores'
        period_seconds = 'period_seconds'
        initial_delay_seconds = 'initial_delay_seconds'
        timeout_seconds = 'timeout_seconds'
        success_threshold = 'success_threshold'
        failure_threshold = 'failure_threshold'
        namespace = 'namespace'
        token_auth_enabled = 'token_auth_enabled'
        version_name = 'version_name'
        traffic_percentile = 'traffic_percentile'
        compute_target_name = 'compute_target_name'

        result = AksEndpoint.deploy_configuration(autoscale_enabled, autoscale_min_replicas, autoscale_max_replicas,
                                                  autoscale_refresh_seconds, autoscale_target_utilization,
                                                  collect_model_data, auth_enabled, cpu_cores, memory_gb,
                                                  enable_app_insights, scoring_timeout_ms,
                                                  replica_max_concurrent_requests, max_request_wait_time, num_replicas,
                                                  primary_key, secondary_key, tags, properties, description, gpu_cores,
                                                  period_seconds, initial_delay_seconds, timeout_seconds,
                                                  success_threshold, failure_threshold, namespace, token_auth_enabled,
                                                  version_name, traffic_percentile, compute_target_name)
        mock_deploy_config.assert_called_once_with(autoscale_enabled, autoscale_min_replicas, autoscale_max_replicas,
                                                   autoscale_refresh_seconds, autoscale_target_utilization,
                                                   collect_model_data, auth_enabled, cpu_cores, memory_gb,
                                                   enable_app_insights, scoring_timeout_ms,
                                                   replica_max_concurrent_requests, max_request_wait_time,
                                                   num_replicas, primary_key, secondary_key, tags, properties,
                                                   description, gpu_cores, period_seconds, initial_delay_seconds,
                                                   timeout_seconds, success_threshold, failure_threshold, namespace,
                                                   token_auth_enabled, version_name, traffic_percentile,
                                                   compute_target_name)
        assert mock_deploy_config.return_value == result

    def test_update(self):
        pytest.skip('Unimplimented')

    @patch('azureml.core.webservice.aks.AksEndpoint._patch_endpoint_call')
    def test_delete_version(self, mock_patch_endpoint_call, mock_endpoint, mock_workspace):
        mock_endpoint.name = 'endpoint_name'
        with pytest.raises(WebserviceException):
            mock_endpoint.delete_version(None)

        mock_endpoint._auth = mock_workspace._auth_object
        mock_endpoint.delete_version('version_name')
        mock_patch_endpoint_call.assert_called_once()

    @patch('azureml.core.webservice.aks.AksEndpoint._patch_endpoint_call')
    @patch('azureml.core.webservice.aks.ComputeTarget')
    @patch('azureml.core.webservice.aks.AksServiceDeploymentConfiguration')
    @patch('azureml.core.webservice.aks.global_tracking_info_registry')
    @patch('azureml.core.webservice.aks.convert_parts_to_environment')
    @patch('azureml.core.webservice.aks.build_and_validate_no_code_environment_image_request')
    @patch('azureml.core.webservice.aks.AksEndpoint._validate_update')
    def test_create_version(self, mock_validate_update, mock_build_no_code, mock_convert_to_env, mock_global_tracking,
                            mock_service_deploy_config, mock_compute_target, mock_patch_endpoint_call,
                            mock_endpoint, mock_workspace):
        mock_endpoint.name = 'webservice_name'
        with pytest.raises(WebserviceException):
            mock_endpoint.create_version(None)

        version_name = 'version_name'
        autoscale_enabled = 'autoscale_enabled'
        autoscale_min_replicas = 'autoscale_min_replicas'
        autoscale_max_replicas = 'autoscale_max_replicas'
        autoscale_refresh_seconds = 'autoscale_refresh_seconds'
        autoscale_target_utilization = 'autoscale_target_utilization'
        collect_model_data = 'collect_model_data'
        cpu_cores = 'cpu_cores'
        memory_gb = 'memory_gb'
        scoring_timeout_ms = 'scoring_timeout_ms'
        replica_max_concurrent_requests = 'replica_max_concurrent_requests'
        max_request_wait_time = 'max_request_wait_time'
        num_replicas = 'num_replicas'
        tags = {'tag_key': 'tag_val'}
        properties = {'prop_key': 'prop_val'}
        description = 'description'
        models = None
        gpu_cores = 'gpu_cores'
        period_seconds = 'period_seconds'
        initial_delay_seconds = 'initial_delay_seconds'
        timeout_seconds = 'timeout_seconds'
        success_threshold = 'success_threshold'
        failure_threshold = 'failure_threshold'
        traffic_percentile = 'traffic_percentile'
        is_default = True
        is_control_version_type = True
        inference_config = Mock()

        mock_convert_to_env.return_value = inference_config, True
        mock_global_tracking.gather_all.return_value = {}
        mock_endpoint._auth = mock_workspace._auth_object
        mock_endpoint.versions = {'existing_version_name': 'existing_version_obj'}
        mock_endpoint.workspace = mock_workspace
        mock_endpoint.compute_name = 'compute_name'
        mock_deploy_config = Mock()
        mock_deploy_config._build_create_payload.return_value = {'version_create_payload_key': 'payload_val'}
        mock_service_deploy_config.return_value = mock_deploy_config

        mock_endpoint.create_version(version_name, autoscale_enabled, autoscale_min_replicas, autoscale_max_replicas,
                                     autoscale_refresh_seconds, autoscale_target_utilization, collect_model_data,
                                     cpu_cores, memory_gb, scoring_timeout_ms, replica_max_concurrent_requests,
                                     max_request_wait_time, num_replicas, tags, properties, description, models, None,
                                     gpu_cores, period_seconds, initial_delay_seconds, timeout_seconds,
                                     success_threshold, failure_threshold, traffic_percentile, is_default,
                                     is_control_version_type)
        mock_validate_update.assert_called_once_with(autoscale_enabled, autoscale_min_replicas, autoscale_max_replicas,
                                                     autoscale_refresh_seconds, autoscale_target_utilization,
                                                     collect_model_data, cpu_cores, memory_gb, None,
                                                     scoring_timeout_ms, replica_max_concurrent_requests,
                                                     max_request_wait_time, num_replicas, tags, properties,
                                                     description, models, None, gpu_cores, period_seconds,
                                                     initial_delay_seconds, timeout_seconds, success_threshold,
                                                     failure_threshold, None, None, None, version_name,
                                                     traffic_percentile)
        mock_build_no_code.assert_called_once()
        mock_global_tracking.gather_all.assert_called_once()
        mock_service_deploy_config.assert_called_once_with(autoscale_enabled, autoscale_min_replicas,
                                                           autoscale_max_replicas, autoscale_refresh_seconds,
                                                           autoscale_target_utilization, collect_model_data, None,
                                                           cpu_cores, memory_gb, None, scoring_timeout_ms,
                                                           replica_max_concurrent_requests, max_request_wait_time,
                                                           num_replicas, None, None, tags, properties, description,
                                                           gpu_cores, period_seconds, initial_delay_seconds,
                                                           timeout_seconds, success_threshold, failure_threshold, None,
                                                           None, None)
        mock_compute_target.assert_called_once_with(mock_endpoint.workspace, mock_endpoint.compute_name)
        mock_deploy_config._build_create_payload.assert_called_once_with(version_name, mock_build_no_code.return_value,
                                                                         mock_compute_target.return_value)
        mock_patch_endpoint_call.assert_called_once()

        mock_endpoint.create_version(version_name, autoscale_enabled, autoscale_min_replicas, autoscale_max_replicas,
                                     autoscale_refresh_seconds, autoscale_target_utilization, collect_model_data,
                                     cpu_cores, memory_gb, scoring_timeout_ms, replica_max_concurrent_requests,
                                     max_request_wait_time, num_replicas, tags, properties, description, models,
                                     inference_config, gpu_cores, period_seconds, initial_delay_seconds,
                                     timeout_seconds, success_threshold, failure_threshold, traffic_percentile,
                                     is_default, is_control_version_type)
        mock_convert_to_env.assert_called_once_with(version_name, inference_config)
        inference_config._build_environment_image_request.assert_called_once()

    @patch('azureml.core.webservice.aks.AksEndpoint._patch_endpoint_call')
    @patch('azureml.core.webservice.aks.build_and_validate_no_code_environment_image_request')
    @patch('azureml.core.webservice.aks.convert_parts_to_environment')
    @patch('azureml.core.webservice.aks.global_tracking_info_registry')
    def test_update_version(self, mock_global_tracking, mock_convert_to_env, mock_build_no_code,
                            mock_patch_endpoint_call, mock_endpoint, mock_workspace):
        mock_endpoint.workspace = mock_workspace
        mock_endpoint._auth = mock_workspace._auth_object
        with pytest.raises(WebserviceException):
            mock_endpoint.update_version(None)

        version_name = 'version_name'
        with pytest.raises(WebserviceException):
            mock_endpoint.update_version(version_name)

        autoscale_enabled = 'autoscale_enabled'
        autoscale_min_replicas = 'autoscale_min_replicas'
        autoscale_max_replicas = 'autoscale_max_replicas'
        autoscale_refresh_seconds = 'autoscale_refresh_seconds'
        autoscale_target_utilization = 'autoscale_target_utilization'
        collect_model_data = 'collect_model_data'
        cpu_cores = 'cpu_cores'
        memory_gb = 'memory_gb'
        scoring_timeout_ms = 'scoring_timeout_ms'
        replica_max_concurrent_requests = 'replica_max_concurrent_requests'
        max_request_wait_time = 'max_request_wait_time'
        num_replicas = 'num_replicas'
        tags = {'tag_key': 'tag_val'}
        properties = {'prop_key': 'prop_val'}
        description = 'description'
        models = None
        gpu_cores = 'gpu_cores'
        period_seconds = 'period_seconds'
        initial_delay_seconds = 'initial_delay_seconds'
        timeout_seconds = 'timeout_seconds'
        success_threshold = 'success_threshold'
        failure_threshold = 'failure_threshold'
        traffic_percentile = 'traffic_percentile'
        is_default = True
        is_control_version_type = True
        inference_config = Mock()

        mock_global_tracking.gather_all.return_value = {'gloabl_key': 'global_val'}
        mock_version = Mock()
        mock_version.models = []
        mock_endpoint.versions = {'version_name': mock_version}
        mock_convert_to_env.return_value = inference_config, True

        mock_endpoint.update_version(version_name, autoscale_enabled, autoscale_min_replicas, autoscale_max_replicas,
                                     autoscale_refresh_seconds, autoscale_target_utilization, collect_model_data,
                                     cpu_cores, memory_gb, scoring_timeout_ms, replica_max_concurrent_requests,
                                     max_request_wait_time, num_replicas, tags, properties, description, models,
                                     inference_config, gpu_cores, period_seconds, initial_delay_seconds,
                                     timeout_seconds, success_threshold, failure_threshold, traffic_percentile,
                                     is_default, is_control_version_type)
        mock_global_tracking.gather_all.assert_called_once()
        mock_convert_to_env.assert_called_once_with(version_name, inference_config)
        inference_config._build_environment_image_request.assert_called_once()
        mock_patch_endpoint_call.assert_called_once()

        models = ['model']
        mock_endpoint.update_version(version_name, autoscale_enabled, autoscale_min_replicas, autoscale_max_replicas,
                                     autoscale_refresh_seconds, autoscale_target_utilization, collect_model_data,
                                     cpu_cores, memory_gb, scoring_timeout_ms, replica_max_concurrent_requests,
                                     max_request_wait_time, num_replicas, tags, properties, description, models, None,
                                     gpu_cores, period_seconds, initial_delay_seconds, timeout_seconds,
                                     success_threshold, failure_threshold, traffic_percentile, is_default,
                                     is_control_version_type)
        mock_build_no_code.assert_called_once_with(models)

    @patch('azureml.core.webservice.aks.AksEndpoint.update_deployment_state')
    @patch('azureml.core.webservice.aks.get_requests_session')
    @patch('azureml.core.webservice.aks.ClientBase')
    def test__patch_endpoint_call(self, mock_client_base, mock_get_session, mock_update_deployment_state,
                                  mock_endpoint, mock_http_response):
        mock_client_base._execute_func.return_value = mock_http_response(200, None)
        mock_endpoint._mms_endpoint = '/mms/mock/endpoint'
        headers = 'headers'
        params = 'params'
        patch_list = 'patch_list'

        mock_endpoint._patch_endpoint_call(headers, params, patch_list)
        mock_client_base._execute_func.assert_called_once_with(mock_get_session.return_value.patch,
                                                               mock_endpoint._mms_endpoint, headers=headers,
                                                               params=params, json=patch_list)
        mock_update_deployment_state.assert_called_once()

        mock_client_base._execute_func.return_value = mock_http_response(202, None, {'Operation-Location': 'op_loc'})
        mock_endpoint._patch_endpoint_call(headers, params, patch_list)
        assert '/mms/operations/op_loc' == mock_endpoint._operation_endpoint

        mock_client_base._execute_func.return_value = mock_http_response(500, None)
        with pytest.raises(WebserviceException):
            mock_endpoint._patch_endpoint_call(headers, params, patch_list)

    @patch('azureml.core.webservice.aks.webservice_name_validation')
    @patch('azureml.core.webservice.aks.AksWebservice._validate_update')
    def test__validate_update(self, mock_super_validate_update, mock_name_validation, mock_endpoint):
        version_name = 'version_name'
        autoscale_enabled = 'autoscale_enabled'
        autoscale_min_replicas = 'autoscale_min_replicas'
        autoscale_max_replicas = 'autoscale_max_replicas'
        autoscale_refresh_seconds = 'autoscale_refresh_seconds'
        autoscale_target_utilization = 'autoscale_target_utilization'
        collect_model_data = 'collect_model_data'
        cpu_cores = 'cpu_cores'
        memory_gb = 'memory_gb'
        scoring_timeout_ms = 'scoring_timeout_ms'
        replica_max_concurrent_requests = 'replica_max_concurrent_requests'
        max_request_wait_time = 'max_request_wait_time'
        num_replicas = 'num_replicas'
        tags = {'tag_key': 'tag_val'}
        properties = {'prop_key': 'prop_val'}
        description = 'description'
        models = None
        gpu_cores = 'gpu_cores'
        period_seconds = 'period_seconds'
        initial_delay_seconds = 'initial_delay_seconds'
        timeout_seconds = 'timeout_seconds'
        success_threshold = 'success_threshold'
        failure_threshold = 'failure_threshold'
        traffic_percentile = 102
        inference_config = Mock()

        with pytest.raises(WebserviceException):
            mock_endpoint._validate_update(autoscale_enabled, autoscale_min_replicas, autoscale_max_replicas,
                                           autoscale_refresh_seconds, autoscale_target_utilization, collect_model_data,
                                           cpu_cores, memory_gb, None, scoring_timeout_ms,
                                           replica_max_concurrent_requests, max_request_wait_time, num_replicas, tags,
                                           properties, description, models, inference_config, gpu_cores,
                                           period_seconds, initial_delay_seconds, timeout_seconds, success_threshold,
                                           failure_threshold, None, None, None, version_name, traffic_percentile)

            mock_super_validate_update.assert_called_once_with(None, autoscale_enabled, autoscale_min_replicas,
                                                               autoscale_max_replicas, autoscale_refresh_seconds,
                                                               autoscale_target_utilization, collect_model_data,
                                                               cpu_cores, memory_gb, None, scoring_timeout_ms,
                                                               replica_max_concurrent_requests, max_request_wait_time,
                                                               num_replicas, tags, properties, description, models,
                                                               inference_config, gpu_cores, period_seconds,
                                                               initial_delay_seconds, timeout_seconds,
                                                               success_threshold, failure_threshold, None, None, None)
            mock_name_validation.assert_called_once_with(version_name)

    def test_serialize(self, mock_endpoint, mock_workspace):
        mock_endpoint.created_time = datetime.now()
        mock_endpoint.updated_time = datetime.now()
        mock_version = Mock()
        mock_version.serialize.return_value = 'version_obj'
        mock_endpoint.versions = {'version_name': mock_version}
        mock_endpoint.name = 'endpoint_name'
        mock_endpoint.description = 'description'
        mock_endpoint.tags = 'tags'
        mock_endpoint.properties = 'properties'
        mock_endpoint.state = 'state'
        mock_endpoint.error = 'error'
        mock_endpoint.compute_name = 'compute_name'
        mock_endpoint.compute_type = 'compute_type'
        mock_endpoint.workspace = mock_workspace
        mock_endpoint.deployment_status = 'deployment_status'
        mock_endpoint.scoring_uri = 'scoring_uri'
        mock_endpoint.auth_enabled = 'auth_enabled'
        mock_endpoint.token_auth_enabled = 'token_auth_enabled'
        mock_endpoint.enable_app_insights = 'enable_app_insights'
        expected = {'name': mock_endpoint.name, 'description': mock_endpoint.description, 'tags': mock_endpoint.tags,
                    'properties': mock_endpoint.properties, 'state': mock_endpoint.state,
                    'createdTime': mock_endpoint.created_time.isoformat(),
                    'updatedTime': mock_endpoint.updated_time.isoformat(), 'error': mock_endpoint.error,
                    'computeName': mock_endpoint.compute_name, 'computeType': mock_endpoint.compute_type,
                    'workspaceName': mock_endpoint.workspace.name, 'deploymentStatus': mock_endpoint.deployment_status,
                    'scoringUri': mock_endpoint.scoring_uri, 'authEnabled': mock_endpoint.auth_enabled,
                    'aadAuthEnabled': mock_endpoint.token_auth_enabled,
                    'appInsightsEnabled': mock_endpoint.enable_app_insights,
                    'versions': {'version_name': 'version_obj'}}

        result = mock_endpoint.serialize()
        assert expected == result
