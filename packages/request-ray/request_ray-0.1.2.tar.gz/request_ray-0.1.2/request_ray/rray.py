import grequests


def extract_retry(request):
    """extracts the value of the key retry from the dict or returns 0 if Not found
    Args:
        request(dict): required to have
            - method(string): http method to use
            - url(string): url of the requested resource
            - kwargs(dict): defines more specs for the request
                - data(dict): if request has json body
                - headers(dict): if you want to attach any headers to the request
    Returns:
        int: how many times this request was retried
    """
    if not request.get('retries'):
        return 0
    else:
        return request.get('retries')


def index_requests(reqs):
    """adds an index key for each dict entry in the array
    Args:
        requests_set (list): Array of requests to send:
            request(dict): required to have
                - method(string): http method to use
                - url(string): url of the requested resource
                - kwargs(dict): defines more specs for the request
                    - data(dict): if request has json body
                    - headers(dict): if you want to attach any headers to the request
    Returns:
        Array: Array of all requests with indexed key in each request dict {'index': index}.
    """
    for idx, req in enumerate(reqs):
        req['index'] = idx

    return reqs


def send_requests(requests_set, aperature, max_retry):
    """
    Args:
        requests_set (list): Array of requests to send:
            request(dict): required to have
                - method(string): http method to use
                - url(string): url of the requested resource
                - kwargs(dict): defines more specs for the request
                    - data(dict): if request has json body
                    - headers(dict): if you want to attach any headers to the request
        aperature (int): Max number of concurrent requests to be sent.
        max_retry (int): Max number of retries for failed requests
    Returns:
        tuple:
            list: Array of all request responses handled.
    Raises:
        AttributeError:
        ValueError: If `param2` is equal to `param1`.
    """
    responses = []
    requests_set = index_requests(requests_set)

    while len(requests_set):
        staged_set = requests_set[:aperature]  # slice current window
        requests_set = requests_set[aperature:]  # slice out executed requests from requests_set

        active_set = (grequests.request(r.get('method'), r.get('url'), **r.get('kwargs'))
                      for r in staged_set)  # requests' objects formation
        response_set = grequests.map(active_set)  # concurrent execution

        for idx, response in enumerate(response_set):
            request = staged_set[idx]

            if response and response.status_code < 400:
                responses.append({'response': response, 'index': request.get('index')})

            else:
                retry = extract_retry(request)
                if retry < max_retry:
                    request['retries'] = retry + 1
                    requests_set.append(request)
                else:
                    responses.append({'response': response, 'index': request.get('index')})

    return sorted(responses, key=lambda r: r.get('index'))
