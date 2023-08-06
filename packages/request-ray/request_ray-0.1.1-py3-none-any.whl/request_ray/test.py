import unittest
import responses
import json

from rray import extract_retry, index_requests, send_requests


class TestUtils(unittest.TestCase):
    def test_retry_extract(self):
        self.assertEqual(extract_retry({'retries': 123}), 123)
        self.assertEqual(extract_retry({}), 0)

    def test_index_requests(self):
        data_array = [{'k': 'v'}, {'ke': 'va'}, {'key': 'val'}]

        expected_array = [{'k': 'v', 'index': 0}, {'ke': 'va', 'index': 1}, {'key': 'val', 'index': 2}]

        self.assertEqual(index_requests(data_array), expected_array)

    @responses.activate
    def test_send_requests_happy(self):
        """
        happy scenario
        should be able to send requests successfully with 200 feedback
        """
        requests = [{
            'method': 'get',
            'url': 'https://google.com',
            'kwargs': {}
        }, {
            'method': 'get',
            'url': 'https://facebook.com',
            'kwargs': {}
        }]

        for req in requests:
            responses.add(responses.GET, req['url'], json={'sucess': 'thank you'}, status=200)

        rs = send_requests(requests, 2, 14)

        self.assertEqual(len(rs), 2)
        for idx, r in enumerate(rs):
            self.assertEqual(r['index'], idx)
            self.assertEqual(r['response'].status_code, 200)

        self.assertEqual(len(responses.calls), 2)

    @responses.activate
    def test_send_requests_happy_respect_kwargs(self):
        """
        happy scenario
        should be able to send requests successfully with 200 feedback
        """
        requests = [{
            'method': 'POST',
            'url': 'https://google.com',
            'kwargs': {'data': json.dumps({'hello': 'world'})}
        }, {
            'method': 'GET',
            'url': 'https://facebook.com',
            'kwargs': {}
        }]

        for req in requests:
            responses.add(req['method'], req['url'], json={'sucess': 'thank you'}, status=200)

        rs = send_requests(requests, 2, 14)

        self.assertEqual(len(rs), 2)
        for idx, r in enumerate(rs):
            self.assertEqual(r['index'], idx)
            self.assertEqual(r['response'].status_code, 200)

        self.assertEqual(len(responses.calls), 2)
        self.assertEqual(responses.calls[0].request.body, requests[0]['kwargs']['data'])

    @responses.activate
    def test_send_requests_happy_respect_handle_batches(self):
        """
        happy scenario
        should be able to send requests in batches successfully with 200 feedback
        """
        requests = [{
            'method': 'POST',
            'url': 'https://google.com',
            'kwargs': {'data': json.dumps({'hello': 'world'})}
        }, {
            'method': 'GET',
            'url': 'https://facebook.com',
            'kwargs': {}
        }, {
            'method': 'GET',
            'url': 'https://test.com',
            'kwargs': {}
        }, {
            'method': 'GET',
            'url': 'https://testat.com',
            'kwargs': {}
        }]

        for req in requests:
            responses.add(req['method'], req['url'], json={'sucess': 'thank you'}, status=200)

        rs = send_requests(requests, 3, 14)

        self.assertEqual(len(rs), 4)
        for idx, r in enumerate(rs):
            self.assertEqual(r['index'], idx)
            self.assertEqual(r['response'].status_code, 200)

        self.assertEqual(len(responses.calls), 4)
        self.assertEqual(responses.calls[0].request.body, requests[0]['kwargs']['data'])

    @responses.activate
    def test_send_requests_fail_retry(self):
        """
        happy scenario
        should retry failed request till sucess or retry max reached
        """
        requests = [{
            'method': 'POST',
            'url': 'https://google.com',
            'kwargs': {'data': json.dumps({'hello': 'world'})},
            'status': 200
        }, {
            'method': 'GET',
            'url': 'https://facebook.com',
            'kwargs': {},
            'status': 200
        }, {
            'method': 'GET',
            'url': 'https://unkown.com',
            'kwargs': {},
            'status': 500
        }]

        for req in requests:
            responses.add(req['method'], req['url'], json={}, status=req['status'])

        rs = send_requests(requests, 3, 2)

        self.assertEqual(len(rs), 3)
        for idx, r in enumerate(rs):
            self.assertEqual(r['index'], idx)
            self.assertEqual(r['response'].status_code, requests[idx]['status'])

        self.assertEqual(len(responses.calls), 3 + 2)  # 3 requests + 2 retries for last request


if __name__ == '__main__':
    unittest.main()
