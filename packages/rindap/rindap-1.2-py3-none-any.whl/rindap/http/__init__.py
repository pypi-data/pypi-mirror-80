from rindap.base.exceptions import RindapException


class HttpClient(object):
    """
    An abstract class representing an HTTP client.
    """
    def request(self, method, url, params=None, data=None, headers=None, auth=None,
                timeout=None, allow_redirects=False):
        """
        Make an HTTP request.
        """
        raise RindapException('HttpClient is an abstract class')
