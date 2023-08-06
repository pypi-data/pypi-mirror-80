# Request Ray

[![PyPI version](https://badge.fury.io/py/request-ray.svg)](https://badge.fury.io/py/request-ray)
[![Build Status:](https://github.com/Kareem-Emad/request-ray/workflows/build/badge.svg)](https://github.com/Kareem-Emad/request-ray/actions)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)


a batch based request package with retry stratgy that enables you to send X requests concurrently at rate of Y requests/execution with max retries for each N

## Setup

```shell
pip install request-ray
```

## How to use

```python
from request_ray import rray

requests = [{
    'method': 'POST',
    'url': 'https://google.com',
    'kwargs': {'data': json.dumps({'hello': 'world'}), 'headers': {'alpha': 'beta'}}
}, {
    'method': 'GET',
    'url': 'https://facebook.com',
    'kwargs': {}
}]

batch_size = 2 # max no of requests to send at a time
retry_policy = 3 # how many times to retry failed requests

responses rray.send_requests(requests, batch_size, retry_policy)
print(responses) # array of expected responses with structure in each element: {'index': 0, 'response': standard_response_object}
```

## How it works

As shown below:

- 6 requests are queued
- first 3 are started
- 1,3 get 200 ok and 2 get 500 so it's enqueued again
- 2 is retried with next requests till it's statisfied or retry max reached

![Diagram](./assets/diagram.png)
