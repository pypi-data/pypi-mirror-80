import requests


def get_request(url, payload, source=''):
    status_code, msg, resp_data = 500, '', {}
    try:
        resp = requests.get(url, params=payload)
    except Exception as ex:
        msg = f'{source} ConnectionError: {ex}.'
        return status_code, resp_data, msg

    if resp.status_code >= 500:
        msg = '%s ExceptionError: Request Get API failed.' % source
        return status_code, resp_data, msg

    if resp.status_code == 200:
        try:
            resp_data = resp.json()
            status_code = 200
        except ValueError:
            msg = '%s JSONDecodedError: Response JSON Decoded Error.' % source
    return status_code, resp_data, msg


def post_request(url, payload, source='', **kwargs):
    status_code, msg, resp_data = 500, '', {}
    try:
        resp = requests.post(url, data=payload, **kwargs)
    except Exception as ex:
        msg = f'{source} ConnectionError: {ex}.'
        return status_code, resp_data, msg

    status_code = resp.status_code
    if resp.status_code == 200:
        try:
            resp_data = resp.json()
        except ValueError:
            msg = '%s JSONDecodedError: Response JSON Decoded Error.' % source
    else:
        msg = f'{source} ExceptionError: {resp.content}.'
    return status_code, resp_data, msg
