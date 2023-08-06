import unittest
import responses
import jwt
import json

import publisher
from publisher import _encode_payload, _generate_token, SWITCH_JWT_SECRET, publish


class TestUtils(unittest.TestCase):
    def test_encoding(self):
        """
        encoder should take a dict and transofrm it
        into its correspoding base64 string
        """
        encoded_payload = _encode_payload({'some_payload': 'to_encode'})

        expected_encode = 'eyJzb21lX3BheWxvYWQiOiAidG9fZW5jb2RlIn0='
        self.assertEqual(encoded_payload, expected_encode)

    def test_jwt_token_generation(self):
        """
        jwt should generate valid token with correct signatures
        """
        jwt_token = _generate_token('me')
        decoded = jwt.decode(jwt_token, SWITCH_JWT_SECRET, algorithms='HS256')

        self.assertEqual(decoded, {'Author': 'me'})

    @responses.activate
    def test_publish_happy(self):
        """
        should be able to publish message with all params passed
        """
        expected_payload = {
            'Payload': 'eyJib2R5IjogeyJoZWxsbyI6ICJ3b3JsZCJ9fQ==',
            'Topic': 'test'
        }
        publisher.SWITCH_BASE_URL = 'http://test.com'
        responses.add(responses.POST,
                      f'{publisher.SWITCH_BASE_URL}/publish',
                      json={'sucess': 'thank you'},
                      status=200)

        publish(topic='test',
                author='test_author',
                options={'body': {
                    'hello': 'world'
                }})

        self.assertEqual(len(responses.calls), 1)
        self.assertEqual(json.loads(responses.calls[0].request.body),
                         expected_payload)
        decoded = jwt.decode(
            responses.calls[0].request.headers['Authorization'].split(
                'bearer ')[1],
            SWITCH_JWT_SECRET,
            algorithms='HS256')


if __name__ == '__main__':
    unittest.main()
