# ---------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# ---------------------------------------------------------
import pytest

from azureml.core.model import InferenceConfig, Model
from azureml.core.webservice import LocalWebservice
from azureml.core.webservice.local import LocalWebserviceDeploymentConfiguration
from azureml.exceptions import WebserviceException
from azureml._model_management import _constants
from datetime import datetime
from unittest.mock import patch, Mock


@pytest.fixture(scope='function')
@patch('azureml.core.webservice.local.LocalWebservice.update_deployment_state', Mock(return_value=None))
@patch('azureml.core.webservice.local.get_docker_host_container', Mock(return_value=None))
@patch('azureml.core.webservice.local.get_docker_client', Mock(return_value=None))
def mock_webservice(mock_workspace):
    webservice = LocalWebservice(mock_workspace, 'foo')

    return webservice


class TestLocalWebservice(object):
    @patch('azureml.core.webservice.local.cleanup_docker_image')
    @patch('azureml.core.webservice.local.cleanup_container')
    def test_delete(self, mock_cleanup_container, mock_cleanup_docker_image, mock_webservice):
        mock_webservice.state = LocalWebservice.STATE_RUNNING
        mock_image = Mock()
        mock_image.id = 'id'
        mock_container = Mock()
        mock_container.image = mock_image
        mock_webservice._container = mock_container
        mock_webservice._docker_client = 'docker_client'

        mock_webservice.delete(delete_image=True)
        mock_cleanup_container.assert_called_once_with(mock_webservice._container)
        assert not mock_webservice._context_dir
        assert not mock_webservice._models_dir
        mock_cleanup_docker_image.assert_called_once_with(mock_webservice._docker_client,
                                                          mock_webservice._container.image.id)
        assert LocalWebservice.STATE_DELETED == mock_webservice.state

    @patch('azureml.core.webservice.local.LocalWebserviceDeploymentConfiguration')
    def test_deploy_configuration(self, mock_deploy_config):
        port = 'port'

        result = LocalWebservice.deploy_configuration(port)
        mock_deploy_config.assert_called_once_with(port)
        assert mock_deploy_config.return_value == result

    @patch('azureml.core.webservice.local.Model')
    def test_deploy_to_cloud(self, mock_model, mock_webservice, mock_workspace):
        mock_webservice._deployable = False

        with pytest.raises(WebserviceException):
            mock_webservice.deploy_to_cloud()

        mock_webservice.name = 'foo'
        mock_webservice.workspace = mock_workspace
        mock_webservice._inference_config = 'inference_config'
        mock_webservice._models_remote = ['remote_model']
        mock_webservice._models_local = [{'local_path': 'path_to_model'}]
        mock_webservice._deployable = True

        result = mock_webservice.deploy_to_cloud(deployment_config='deploy_config', deployment_target='target')
        mock_model.deploy.assert_called_once_with(workspace=mock_webservice.workspace, name=mock_webservice.name,
                                                  models=['path_to_model', 'remote_model'],
                                                  inference_config=mock_webservice._inference_config,
                                                  deployment_config='deploy_config', deployment_target='target')
        assert mock_model.deploy.return_value == result

    def test_deserialize(self):
        with pytest.raises(NotImplementedError):
            LocalWebservice.deserialize('workspace', 'payload')

    def test_get_keys(self, mock_webservice):
        with pytest.raises(NotImplementedError):
            mock_webservice.get_keys()

    @patch('azureml.core.webservice.local.get_docker_logs')
    def test_get_logs(self, mock_get_docker_logs, mock_webservice):
        mock_webservice.state = LocalWebservice.STATE_RUNNING
        mock_webservice._container = 'container'

        result = mock_webservice.get_logs(1000)
        mock_get_docker_logs.assert_called_once_with(mock_webservice._container, num_lines=1000)
        assert mock_get_docker_logs.return_value == result

    def test_get_token(self, mock_webservice):
        with pytest.raises(NotImplementedError):
            mock_webservice.get_token()

    @patch('azureml.core.webservice.local.get_docker_client')
    @patch('azureml.core.webservice.local.get_docker_containers')
    def test_list(self, mock_get_docker_containers, mock_get_docker_client, mock_workspace):
        container = Mock()
        container.labels = {LocalWebservice._CONTAINER_LABEL_SERVICE_NAME: 'webservice_name'}
        mock_get_docker_containers.return_value = [container]

        list_func = LocalWebservice.list

        with patch('azureml.core.webservice.local.LocalWebservice') as mock_local_init:
            list_func(mock_workspace)
            mock_get_docker_containers.assert_called_once()
            mock_get_docker_client.assert_called_once()

    def test_regen_key(self, mock_webservice):
        with pytest.raises(NotImplementedError):
            mock_webservice.regen_key('key')

    @patch('azureml.core.webservice.local.LocalWebservice._run_container')
    def test_reload(self, mock_run_container, mock_webservice):
        mock_webservice.state = LocalWebservice.STATE_RUNNING

        mock_webservice.reload(True)
        mock_run_container.assert_called_once_with(wait=True)

    @patch('azureml.core.webservice.local.container_scoring_call')
    @patch('azureml.core.webservice.local.LocalWebservice.wait_for_deployment')
    def test_run(self, mock_wait_for_deploy, mock_container_scoring_call, mock_webservice):
        mock_webservice.state = LocalWebservice.STATE_DEPLOYING
        mock_webservice._port = 'port'
        mock_webservice._container = 'container'
        mock_webservice._internal_base_url = 'base_url'

        result = mock_webservice.run('input_data')
        mock_wait_for_deploy.assert_called_once()
        mock_container_scoring_call.assert_called_once_with(mock_webservice._port, 'input_data',
                                                            mock_webservice._container,
                                                            mock_webservice._internal_base_url,
                                                            cleanup_on_failure=False)
        assert mock_container_scoring_call.return_value == result

    def test_serialize(self, mock_webservice, mock_workspace):
        mock_webservice.created_time = datetime.now()
        mock_webservice.updated_time = datetime.now()
        mock_webservice.name = 'name'
        mock_webservice.tags = 'tags'
        mock_webservice.properties = 'properties'
        mock_webservice.state = 'state'
        mock_webservice.error = 'error'
        mock_webservice.compute_type = 'compute_type'
        mock_webservice.workspace = mock_workspace
        mock_webservice.image_id = 'image_id'
        mock_webservice._base_uri = 'base_uri'
        mock_webservice._port = 'port'

        expected = {'name': mock_webservice.name, 'tags': mock_webservice.tags,
                    'properties': mock_webservice.properties, 'state': mock_webservice.state,
                    'createdTime': mock_webservice.created_time.isoformat(),
                    'updatedTime': mock_webservice.updated_time.isoformat(), 'error': mock_webservice.error,
                    'computeType': mock_webservice.compute_type, 'workspaceName': mock_webservice.workspace.name,
                    'imageId': mock_webservice.image_id, 'scoringUri': mock_webservice.scoring_uri,
                    'swaggerUri': mock_webservice.swagger_uri, 'port': mock_webservice.port}
        result = mock_webservice.serialize()
        assert expected == result

    @patch('azureml.core.webservice.local.LocalWebservice._run_container')
    @patch('azureml.core.webservice.local.LocalWebservice._build_image')
    @patch('azureml.core.webservice.local.LocalWebservice._generate_docker_context')
    @patch('azureml.core.webservice.local.LocalWebservice._collect_models')
    @patch('azureml.core.webservice.local.convert_parts_to_environment')
    @patch('azureml.core.webservice.local.LocalWebservice._identify_models')
    def test_update(self, mock_identify_models, mock_convert_to_env, mock_collect_models, mock_generate_docker_context,
                    mock_build_image, mock_run_container, mock_webservice, mock_workspace):
        mock_webservice.state = LocalWebservice.STATE_RUNNING
        deployment_config = Mock()

        with pytest.raises(WebserviceException):
            mock_webservice.update(deployment_config=deployment_config)

        inference_config = Mock()

        with pytest.raises(WebserviceException):
            mock_webservice.update(inference_config=inference_config)

        models = 'models'
        mock_identify_models.return_value = 'models_local', 'models_remote'
        deployment_config = Mock(spec=LocalWebserviceDeploymentConfiguration)
        inference_config = Mock(spec=InferenceConfig)
        inference_config.environment = Mock()
        mock_convert_to_env.return_value = inference_config, None
        mock_webservice.workspace = mock_workspace
        mock_webservice.name = 'foo'
        mock_webservice._deployable = True

        mock_webservice.update(models, None, deployment_config, True, inference_config)
        mock_identify_models.assert_called_once_with(mock_workspace, models)
        mock_convert_to_env.assert_called_once_with('foo', inference_config)
        mock_collect_models.assert_called_once()
        mock_generate_docker_context.assert_called_once()
        mock_build_image.assert_called_once()
        mock_run_container.assert_called_once_with(wait=True)

    @patch('azureml.core.webservice.local.LocalWebservice._get_container_models_remote')
    @patch('azureml.core.webservice.local.LocalWebservice._get_container_models_local')
    @patch('azureml.core.webservice.local.LocalWebservice._get_container_model_path_dir')
    @patch('azureml.core.webservice.local.LocalWebservice._get_container_inference_config')
    @patch('azureml.core.webservice.local.LocalWebservice._get_container_image_config')
    @patch('azureml.core.webservice.local.LocalWebservice._get_container_deployment_config')
    @patch('azureml.core.webservice.local.LocalWebservice._generate_base_urls')
    @patch('azureml.core.webservice.local.LocalWebservice._get_container')
    def test_update_deployment_state(self, mock_get_container, mock_generate_base_urls, mock_get_deploy_config,
                                     mock_get_image_config, mock_get_inference_config, mock_get_model_path_dir,
                                     mock_get_models_local, mock_get_models_remote, mock_webservice, mock_workspace):
        mock_webservice._docker_client = 'docker_client'
        mock_webservice.workspace = mock_workspace
        mock_webservice.name = 'foo'
        container = Mock()
        container.image = Mock()
        mock_get_container.return_value = container
        mock_generate_base_urls.return_value = 'base_url', 'internal_base_url', 'port'

        mock_webservice.update_deployment_state(True)
        mock_get_container.assert_called_once_with('docker_client', mock_workspace, 'foo', must_exist=True)
        mock_generate_base_urls.assert_called_once()
        mock_get_deploy_config.assert_called_once_with(container)
        mock_get_image_config.assert_called_once_with(container)
        mock_get_inference_config.assert_called_once_with(container)
        mock_get_model_path_dir.assert_called_once_with(container)
        mock_get_models_local.assert_called_once_with(container)
        mock_get_models_remote.assert_called_once_with(mock_workspace, container)

    @patch('azureml.core.webservice.local.container_health_check')
    def test_wait_for_deployment(self, mock_health_check, mock_webservice):
        mock_webservice.state = LocalWebservice.STATE_DEPLOYING
        mock_webservice._port = 'port'
        mock_webservice._container = 'container'
        mock_webservice._internal_base_url = 'internal_base_url'
        mock_webservice._base_url = 'base_url'

        mock_webservice.wait_for_deployment()
        mock_health_check.assert_called_once_with('port', 'container', health_url='internal_base_url',
                                                  cleanup_if_failed=False)
        assert LocalWebservice.STATE_RUNNING == mock_webservice.state

        mock_health_check.side_effect = WebserviceException('Exception')
        with pytest.raises(WebserviceException):
            mock_webservice.wait_for_deployment()
            assert LocalWebservice.STATE_FAILED == mock_webservice.state

    @patch('azureml.core.webservice.local.build_docker_image')
    @patch('azureml.core.webservice.local.LocalWebservice._login_to_registry')
    def test__build_image(self, mock_login, mock_build_image, mock_webservice):
        mock_webservice._docker_client = 'docker_client'
        mock_webservice._context_dir = Mock()
        mock_webservice._context_dir.name = 'dir_name'
        mock_webservice.name = 'foo'

        mock_webservice._build_image()
        mock_login.assert_called_once()
        mock_build_image.assert_called_once_with('docker_client', 'dir_name', 'foo', pull=True)
        assert mock_build_image.return_value == mock_webservice._image

    def test__collect_models(self):
        pytest.skip('Unimplimented')

    def test__construct_base_url(self):
        port = 'port'
        expected = 'http://localhost:{}'.format(port)

        result = LocalWebservice._construct_base_url(port)
        assert expected == result

    def test__construct_container_name(self):
        service_name = 'foo'
        result = LocalWebservice._construct_container_name(service_name)
        assert service_name == result

    def test__construct_internal_base_url(self):
        alias = 'alias'
        expected = 'http://{}:{}'.format(alias, _constants.DOCKER_IMAGE_HTTP_PORT)
        result = LocalWebservice._construct_internal_base_url(alias)
        assert expected == result

    def test__copy_files_with_overwrite(self):
        pytest.skip('Unimplimented')

    def test__copy_local_asset(self):
        pytest.skip('Unimplimented')

    @patch('azureml.core.webservice.local.LocalWebservice')
    def test__deploy(self, mock_local, mock_workspace):
        name = 'foo'
        models = ['model']
        deployment_config = Mock()
        wait = True
        inference_config = Mock()

        with pytest.raises(WebserviceException):
            LocalWebservice._deploy(mock_workspace, name, models, deployment_config=deployment_config)

        with pytest.raises(WebserviceException):
            LocalWebservice._deploy(mock_workspace, name, models, inference_config=inference_config)

        inference_config = Mock(InferenceConfig)
        mock_local.deploy_configuration.reset_mock()

        result = LocalWebservice._deploy(mock_workspace, name, models, wait=wait, inference_config=inference_config)
        mock_local.deploy_configuration.assert_called_once()
        mock_local.assert_called_once_with(mock_workspace, name, must_exist=False)
        mock_local.return_value.update.assert_called_once_with(models=models, image_config=None,
                                                               inference_config=inference_config,
                                                               deployment_config=
                                                               mock_local.deploy_configuration.return_value, wait=wait)

    @patch('azureml.core.webservice.local.LocalWebservice._construct_internal_base_url')
    @patch('azureml.core.webservice.local.LocalWebservice._construct_base_url')
    @patch('azureml.core.webservice.local.get_docker_port')
    @patch('azureml.core.webservice.local.connect_docker_network')
    def test__generate_base_urls(self, mock_connect_docker_network, mock_get_docker_port, mock_construct_base_url,
                                 mock_construct_internal_base_url, mock_webservice):
        mock_webservice._host_container = 'host_container'
        mock_webservice._host_network = 'host_network'
        mock_webservice._container = Mock()
        mock_webservice._container.short_id = 'short_id'
        mock_webservice._docker_client = 'docker_client'
        mock_webservice.name = 'foo'

        base_url, internal_base_url, port = mock_webservice._generate_base_urls()
        assert mock_construct_base_url.return_value == base_url
        assert mock_construct_internal_base_url.return_value == internal_base_url
        assert mock_get_docker_port.return_value == port

    @patch('azureml.core.webservice.local.LocalWebservice._copy_files_with_overwrite')
    @patch('azureml.core.webservice.local.Model.package')
    def test__generate_docker_context(self, mock_model_package, mock_copy_files, mock_webservice, mock_workspace):
        mock_webservice._image_config = None
        mock_webservice._models_remote = ['model_remote']
        mock_webservice._models_local = ['model_local']
        mock_webservice._inference_config = Mock()
        mock_webservice._models_dir = Mock()
        mock_webservice._models_dir.name = 'model_dir_name'
        mock_webservice.workspace = mock_workspace
        mock_package = mock_model_package.return_value

        mock_webservice._generate_docker_context()
        mock_model_package.assert_called_once_with(mock_workspace, [], mock_webservice._inference_config,
                                                   generate_dockerfile=True)
        mock_package.wait_for_creation.assert_called_once()
        mock_package.save.assert_called_once()
        mock_package.get_container_registry.assert_called_once()
        assert mock_package.get_container_registry.return_value == mock_webservice._registry
        mock_copy_files.assert_called_once()

    @patch('azureml.core.webservice.local.get_docker_container')
    @patch('azureml.core.webservice.local.LocalWebservice._construct_container_name')
    def test__get_container(self, mock_construct_name, mock_get_container, mock_workspace):
        result = LocalWebservice._get_container('docker_client', None, None)
        assert not result

        result = LocalWebservice._get_container('docker_client', mock_workspace, 'name')
        mock_construct_name.assert_called_once_with('name')
        mock_get_container.assert_called_once_with('docker_client', mock_construct_name.return_value, all=True,
                                                   limit=1)
        assert mock_get_container.return_value == result

    @patch('azureml.core.webservice.local.pickle.loads')
    @patch('azureml.core.webservice.local.b64decode')
    def test__get_container_deployment_config(self, mock_decode, mock_pickle_loads):
        container = Mock()
        container.labels = {LocalWebservice._CONTAINER_LABEL_DEPLOYMENT_CONFIG: 'deploy_config'}

        result = LocalWebservice._get_container_deployment_config(container)
        mock_decode.assert_called_once_with('deploy_config')
        mock_pickle_loads.assert_called_once_with(mock_decode.return_value)
        mock_pickle_loads.return_value.validate_configuration.assert_called_once()
        assert mock_pickle_loads.return_value == result

    @patch('azureml.core.webservice.local.pickle.loads')
    @patch('azureml.core.webservice.local.b64decode')
    def test__get_container_image_config(self, mock_decode, mock_pickle_loads):
        container = Mock()
        container.labels = {LocalWebservice._CONTAINER_LABEL_IMAGE_CONFIG: 'deploy_config'}

        result = LocalWebservice._get_container_image_config(container)
        mock_decode.assert_called_once_with('deploy_config')
        mock_pickle_loads.assert_called_once_with(mock_decode.return_value)
        mock_pickle_loads.return_value.validate_configuration.assert_called_once()
        assert mock_pickle_loads.return_value == result

    @patch('azureml.core.webservice.local.pickle.loads')
    @patch('azureml.core.webservice.local.b64decode')
    def test__get_container_inference_config(self, mock_decode, mock_pickle_loads):
        container = Mock()
        container.labels = {LocalWebservice._CONTAINER_LABEL_INFERENCE_CONFIG: 'deploy_config'}

        result = LocalWebservice._get_container_inference_config(container)
        mock_decode.assert_called_once_with('deploy_config')
        mock_pickle_loads.assert_called_once_with(mock_decode.return_value)
        mock_pickle_loads.return_value.validate_configuration.assert_called_once()
        assert mock_pickle_loads.return_value == result

    def test__get_container_model_path_dir(self):
        mock_container = Mock()
        mock_container.labels = {LocalWebservice._CONTAINER_LABEL_MODEL_PATH_DIR: 'model_path'}

        result = LocalWebservice._get_container_model_path_dir(mock_container)
        assert 'model_path' == result

    @patch('azureml.core.webservice.local.pickle.loads')
    @patch('azureml.core.webservice.local.b64decode')
    def test__get_container_models_local(self, mock_decode, mock_pickle_loads):
        mock_container = Mock()
        mock_container.labels = {LocalWebservice._CONTAINER_LABEL_MODELS_LOCAL: 'local_model'}

        result = LocalWebservice._get_container_models_local(mock_container)
        mock_decode.assert_called_once_with('local_model')
        mock_pickle_loads.assert_called_once_with(mock_decode.return_value)
        assert mock_pickle_loads.return_value == result

    @patch('azureml.core.webservice.local.Model')
    @patch('azureml.core.webservice.local.pickle.loads')
    @patch('azureml.core.webservice.local.b64decode')
    def test__get_container_models_remote(self, mock_decode, mock_pickle_loads, mock_model, mock_workspace):
        mock_container = Mock()
        mock_container.labels = {LocalWebservice._CONTAINER_LABEL_MODELS_REMOTE: ['model_id']}
        mock_pickle_loads.return_value = ['model_id']

        result = LocalWebservice._get_container_models_remote(mock_workspace, mock_container)
        mock_decode.assert_called_once_with(['model_id'])
        mock_pickle_loads.assert_called_once_with(mock_decode.return_value)
        mock_model.assert_called_once_with(mock_workspace, id='model_id')
        assert [mock_model.return_value] == result

    def test__get_image_aml_app_root(self):
        pytest.skip('Unimplimented')

    @patch('azureml.core.webservice.local.Model.__new__')
    def test__identify_models(self, mock_model_class, mock_workspace):
        local_model = '/path/to/model'
        remote_model = 'foo:1'
        in_mem_model = Mock(spec=Model)
        models = [local_model, remote_model, in_mem_model]
        returned_remote_model = Mock(spec=Model)
        mock_model_class.side_effect = [WebserviceException('ModelNotFound'), returned_remote_model]

        local, remote = LocalWebservice._identify_models(mock_workspace, models)
        assert [{'name': 'model', 'image_path': 'model', 'local_path': local_model}] == local
        assert [returned_remote_model, in_mem_model] == remote

        with pytest.raises(NotImplementedError):
            LocalWebservice._identify_models(mock_workspace, [1])

    @patch('azureml.core.webservice.local.login_to_docker_registry')
    def test__login_to_registry(self, mock_login, mock_webservice):
        mock_webservice._registry = None
        mock_webservice._login_to_registry()
        mock_login.assert_not_called()

        mock_webservice._registry = Mock()
        mock_webservice._registry.address = None
        mock_webservice._registry.username = None
        mock_webservice._registry.password = None
        mock_webservice._login_to_registry()
        mock_login.assert_not_called()

        mock_webservice._docker_client = 'docker_client'
        mock_webservice._registry.address = 'address'
        mock_webservice._registry.username = 'username'
        mock_webservice._registry.password = 'password'
        mock_webservice._login_to_registry()
        mock_login.assert_called_once_with('docker_client', 'username', 'password', 'address')

    @patch('azureml.core.webservice.local.LocalWebservice.wait_for_deployment')
    @patch('azureml.core.webservice.local.LocalWebservice._generate_base_urls')
    @patch('azureml.core.webservice.local.start_docker_container')
    @patch('azureml.core.webservice.local.LocalWebservice._copy_local_asset')
    @patch('azureml.core.webservice.local.create_docker_container')
    @patch('azureml.core.webservice.local.pickle.dumps')
    @patch('azureml.core.webservice.local.b64encode')
    @patch('azureml.core.webservice.local.LocalWebservice._construct_container_name')
    @patch('azureml.core.webservice.local.LocalWebservice.delete')
    def test__run_container(self, mock_delete, mock_construct_container_name, mock_encode, mock_pickle_dumps,
                            mock_create_docker_container, mock_copy_local_asset, mock_start_docker_container,
                            mock_generate_base_urls, mock_wait_for_deployment, mock_webservice):
        mock_webservice._container = Mock()
        mock_webservice._container.image.tags = []
        mock_construct_container_name.return_value = 'container_name'
        mock_webservice.name = 'name'
        mock_webservice._deployment_config = Mock()
        mock_webservice._deployment_config.port = 'port'
        mock_webservice._image_config = None
        mock_webservice._inference_config = Mock()
        mock_webservice._inference_config.environment = Mock()
        mock_webservice._inference_config.environment.environment_variables = {'env_key': 'env_val'}
        mock_webservice._inference_config.source_directory = None
        mock_webservice._inference_config.entry_script = 'entry_script'
        mock_webservice._models_local = 'models_local'
        mock_remote_model = Mock()
        mock_remote_model.id = 'remote_model'
        mock_webservice._models_remote = [mock_remote_model]
        mock_webservice._model_path_dir = 'model_path_dir'
        mock_webservice._docker_client = 'docker_client'
        new_container = Mock()
        mock_create_docker_container.return_value = new_container
        mock_generate_base_urls.return_value = 'base_url', 'internal_base_url', 'port'

        mock_webservice._run_container(True)
        mock_delete.assert_called_once_with(delete_cache=False, delete_image=True)
        mock_construct_container_name.assert_called_once_with('name')
        mock_create_docker_container.assert_called_once()
        mock_copy_local_asset.assert_called_once_with(new_container, 'entry_script', container_rel_path='main.py')
        mock_start_docker_container.assert_called_once_with(new_container)
        assert new_container == mock_webservice._container
        assert 'base_url' == mock_webservice._base_url
        assert 'internal_base_url' == mock_webservice._internal_base_url
        assert 'port' == mock_webservice._port
        mock_wait_for_deployment.assert_called_once()
