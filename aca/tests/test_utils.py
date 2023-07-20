from aca.utils import encode_base64, decode_base64


class TestUtils:
    payload = {"some": "payload"}
    b64 = "eyJzb21lIjogInBheWxvYWQifQ=="

    def test_encode_base64(self):
        assert encode_base64(self.payload) == self.b64

    def test_decode_base64(self):
        assert decode_base64(self.b64) == self.payload
