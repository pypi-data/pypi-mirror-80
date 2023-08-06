import hashlib
import logging
import time

import requests
import urllib3


logger = logging.getLogger(__name__)

app_key = None
app_secret = None
proxy_ip = "s1.proxy.mayidaili.com"
proxy_port = "8123"

proxies = {
    'http' : 'http://' + proxy_ip + ':' + proxy_port,
    'https': 'https://' + proxy_ip + ':' + proxy_port
}

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


def set_auth(app_key, app_secret, proxy_ip=None, proxy_port=None):
    globals()['app_key'] = app_key
    globals()['app_secret'] = app_secret
    if proxy_ip:
        globals()['proxy_ip'] = proxy_ip
    if proxy_port:
        globals()['proxy_port'] = proxy_port


class NoAuthException(Exception):
    pass


def get_proxy_auth_header(retry_post: bool = None,
                          start_transaction: bool = None,
                          hold_transaction: bool = None):
    if not (app_key and app_secret):
        raise NoAuthException('Please set app key and app secret use set_auth().')

    params = {
        'app_key'  : app_key,
        'timestamp': time.strftime(r'%Y-%m-%d %H:%M:%S'),
    }

    if retry_post:
        params['retrypost'] = 'true'

    if start_transaction:
        # A transaction max hold 30s
        print('start_transaction')
        params['release-transaction'] = '1'
        params['with-transaction'] = '1'

    if hold_transaction:
        print('hold_transaction')
        params['with-transaction'] = '1'

    codes = app_secret
    for k, v in sorted(params.items(), key=lambda x: x[0]):
        codes += k + v
    codes += app_secret
    sign = hashlib.md5(codes.encode('utf-8')).hexdigest().upper()

    proxy_auth_header = 'MYH-AUTH-MD5 sign=' + sign
    for k, v in params.items():
        proxy_auth_header += '&' + k + '=' + v

    return proxy_auth_header


def proxy_get(url, extra_headers: dict = {}, timeout=None, stream=None, allow_redirects=True) -> requests.Response:
    headers = {
        'User-Agent'         : 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.121 Safari/537.36',  # noqa
        'Proxy-Authorization': get_proxy_auth_header(),
    }
    headers.update(extra_headers)
    resp = requests.get(url, headers=headers, proxies=proxies, verify=False, timeout=timeout,
                        stream=stream, allow_redirects=allow_redirects)
    return resp


def proxy_post(url, data, params=None, extra_headers: dict = {}, timeout=None, stream=None, allow_redirects=True, retry_post=None) -> requests.Response:
    headers = {
        'User-Agent'         : 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.121 Safari/537.36',  # noqa
        'Proxy-Authorization': get_proxy_auth_header(retry_post=retry_post),
    }
    headers.update(extra_headers)
    resp = requests.post(url, data=data, params=params, headers=headers, proxies=proxies, verify=False, timeout=timeout,
                         stream=stream, allow_redirects=allow_redirects)
    return resp


def proxy_head(url, extra_headers: dict = {}, timeout=None, allow_redirects=True) -> requests.Response:
    headers = {
        'User-Agent'         : 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.121 Safari/537.36',  # noqa
        'Proxy-Authorization': get_proxy_auth_header(),
    }
    headers.update(extra_headers)
    resp = requests.head(url, headers=headers, proxies=proxies, verify=False, timeout=timeout,
                         allow_redirects=allow_redirects)
    return resp
