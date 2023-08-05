import unittest
from azureml.core.compute import ComputeTarget, KustoCompute
from unittest.mock import Mock, MagicMock, patch
from azureml.core.workspace import Workspace
from azureml._restclient.clientbase import ClientBase


class KustoComputeTests(unittest.TestCase):
    def setUp(self):
        self.workspace = MagicMock(Workspace)
        self.resource_id = "/subscriptions/mock-subscription-id/resourceGroups/mock-rg/providers" \
                           "/Microsoft.Kusto/clusters/mockcluster"
        self.kusto_connection_string = "mock-connection-string"
        self.application_id = "mock-application-id"
        self.application_key = "mock-application-key"
        self.tenant_id = "mock-tenant-id"
        self.compute = "mockcompute"

    @patch.object(ComputeTarget, '_attach')
    def test_attach_kusto_compute(self, mock__attach):
        ws = self.workspace
        config = KustoCompute.attach_configuration(resource_group=ws.resource_group, workspace_name=ws.name,
                                                   resource_id=self.resource_id, tenant_id=self.tenant_id,
                                                   kusto_connection_string=self.kusto_connection_string,
                                                   application_id=self.application_id,
                                                   application_key=self.application_key)
        kusto_compute = KustoCompute(None, None)
        mock__attach.return_value = kusto_compute
        kusto_compute._attach(workspace=ws, name=self.compute, config=config)

        mock__attach.assert_called_once()

    def test_kusto_compute_build_payload(self):
        payload = KustoCompute._build_attach_payload(location=self.workspace.location,
                                                     resource_id=self.resource_id,
                                                     kusto_connection_string=self.kusto_connection_string,
                                                     client_id=self.application_id,
                                                     secret=self.application_key,
                                                     tenant_id=self.tenant_id)
        assert payload['location'] == self.workspace.location
        assert payload['properties']['resourceId'] == self.resource_id
        assert payload['properties']['properties']['kustoConnectionString'] == self.kusto_connection_string

    def test_validate_get_payload(self):
        payload_dict = self.build_valid_payload()
        KustoCompute._validate_get_payload(payload_dict)

    @patch.object(ComputeTarget, '_get_resource_manager_endpoint')
    @patch.object(ComputeTarget, '_initialize')
    def test__initialize(self, mock__get_resource_manager_endpoint, mock__initialize):
        kusto_compute = KustoCompute(None, None)
        kusto_compute._initialize(Mock(), MagicMock())

        mock__get_resource_manager_endpoint.assert_called_once()
        mock__initialize.assert_called_once()

    @patch.object(KustoCompute, '_initialize')
    def test_deserialize(self, mock__initialize):
        payload_dict = self.build_valid_payload()
        KustoCompute.deserialize(Mock(), payload_dict)
        mock__initialize.assert_called_once()

    @patch.object(ClientBase, '_execute_func')
    def test_get_credentials(self, mock__execute_func):
        kusto_compute = KustoCompute(None, None)
        mock_credentials_dict = """{"servicePrincipalCredentials":{"clientId":"mock-application-id", 
        "secret":"mock-application-key", "tenantId":"mock-tenant-id"}} """
        return_val = Mock()
        return_val.content = mock_credentials_dict
        mock__execute_func.return_value = return_val

        kusto_compute._mlc_endpoint = 'mock-endpoint'
        kusto_compute._auth = Mock()

        cred = kusto_compute.get_credentials()
        sp = cred['servicePrincipalCredentials']
        assert sp['clientId'] == self.application_id
        assert sp['secret'] == self.application_key
        assert sp['tenantId'] == self.tenant_id

    def build_valid_payload(self):
        payload_dict = dict()
        payload_dict['id'] = 'mock-id'
        payload_dict['location'] = 'mock-location'
        payload_dict['tags'] = 'mock-tags'
        payload_dict['name'] = self.compute
        properties_dict = dict()
        properties_dict['computeType'] = 'Kusto'
        properties_dict['provisioningErrors'] = None
        properties_dict['description'] = None
        properties_dict['provisioningState'] = None
        properties_dict['resourceId'] = self.resource_id
        properties_dict['properties'] = None
        payload_dict['properties'] = properties_dict

        return payload_dict
