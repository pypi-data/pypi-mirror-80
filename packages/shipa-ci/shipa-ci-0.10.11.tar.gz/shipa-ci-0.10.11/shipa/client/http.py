import os
import tempfile
import requests


class HttpClient(object):
    def __init__(self, ca_cert=None, ca=None, insecure=False):
        self.cert_file = None
        self.ca_cert = ca_cert
        self.ca = ca
        self.verify = not insecure

    def __enter__(self):
        self.cert_file = None
        if self.ca_cert is not None:
            self.verify = self.ca_cert
        elif self.ca is not None:
            self.cert_file = tempfile.NamedTemporaryFile(delete=False)
            self.cert_file.write(self.ca.encode('utf-8'))
            self.cert_file.close()
            self.verify = self.cert_file.name
        return self

    def __exit__(self, *exc):
        if self.cert_file is not None:
            os.unlink(self.cert_file.name)
            self.cert_file = None
        return False

    def make_request(self, method, url, **kwargs):
        kwargs = dict(kwargs, verify=self.verify)
        return requests.request(method, url, **kwargs)

    def post(self, url, **kwargs):
        return self.make_request('post', url, **kwargs)

    def delete(self, url, **kwargs):
        return self.make_request('delete', url, **kwargs)

    def get(self, url, **kwargs):
        return self.make_request('get', url, **kwargs)

    def put(self, url, **kwargs):
        return self.make_request('put', url, **kwargs)


class MockClient(object):

    def __init__(self, response=None):
        self.response = response

    def post(self, url, **kwargs):
        return self.response

    def delete(self, url, **kwargs):
        return self.response

    def get(self, url, **kwargs):
        return self.response

    def put(self, url, **kwargs):
        return self.response


class MockResponse(object):

    def __init__(self, code=200, text=None):
        self.status_code = code
        self.text = text
