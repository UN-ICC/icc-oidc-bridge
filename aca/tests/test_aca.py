from aca.client import ACAClient


class TestAcaClient:
    url = "http://127.0.0.1"
    client = ACAClient(url, url, "token")

    def test_create_proof_request(self, requests_mock):
        mock_result = {"result": 0}
        requests_mock.post(f"{self.url}/present-proof/create-request", json=mock_result)
        result = self.client.create_proof_request({})
        assert result == mock_result

    def test_get_public_did(self, requests_mock):
        mock_result = {"result": 0}
        requests_mock.get(f"{self.url}/wallet/did/public", json=mock_result)
        result = self.client.get_public_did()
        assert result == 0

    def test_get_credential_definition(self, requests_mock):
        mock_result = {"definition": 0}
        requests_mock.get(
            f"{self.url}/credential-definitions/some_def_id",
            json={"credential_definition": mock_result},
        )
        result = self.client.get_credential_definition("some_def_id")
        assert result == mock_result

    def test_get_schema(self, requests_mock):
        mock_result = {"schema": 0}
        requests_mock.get(
            f"{self.url}/schemas/some_schema_id", json={"schema_json": mock_result}
        )
        result = self.client.get_schema("some_schema_id")
        assert result == mock_result

    def test_get_endpoint_url(self):
        result = self.client.get_endpoint_url()
        assert result == self.url
