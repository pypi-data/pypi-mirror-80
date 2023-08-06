# coding=utf-8
import os
import platform
from rindap import __version__
from rindap.base.exceptions import RindapException
from rindap.base.obsolete import obsolete_client
from rindap.http.http_client import RindapHttpClient

from rindap.base.domain import Domain
from rindap.rest.v1 import V1


class Client(object):
    """ A client for accessing the Rindap API. """

    def __init__(self, username=None, password=None, account_sid=None, region=None,
                 http_client=None, environment=None):
        """
        Initializes the Rindap Client

        :param str username: Username to authenticate with
        :param str password: Password to authenticate with
        :param str account_sid: Account Sid, defaults to Username
        :param str region: Rindap Region to make requests to
        :param HttpClient http_client: HttpClient, defaults to RindapHttpClient
        :param dict environment: Environment to look for auth details, defaults to os.environ

        :returns: Rindap Client
        :rtype: rindap.rest.Client
        """
        environment = environment or os.environ

        self.username = username or environment.get('ACCOUNT_SID')
        """ :type : str """
        self.password = password or environment.get('AUTH_TOKEN')
        """ :type : str """
        self.account_sid = account_sid or self.username
        """ :type : str """
        self.region = region
        """ :type : str """

        if not self.username or not self.password:
            raise RindapException("Credentials are required to create a RindapClient")

        self.auth = (self.username, self.password)
        """ :type : tuple(str, str) """
        self.http_client = http_client or RindapHttpClient()
        """ :type : HttpClient """

        # Domains
        self._rindap = None

    def request(self, method, uri, params=None, data=None, headers=None, auth=None,
                timeout=None, allow_redirects=False):
        """
        Makes a request to the Rindap API using the configured http client
        Authentication information is automatically added if none is provided

        :param str method: HTTP Method
        :param str uri: Fully qualified url
        :param dict[str, str] params: Query string parameters
        :param dict[str, str] data: POST body data
        :param dict[str, str] headers: HTTP Headers
        :param tuple(str, str) auth: Authentication
        :param int timeout: Timeout in seconds
        :param bool allow_redirects: Should the client follow redirects

        :returns: Response from the Rindap API
        :rtype: rindap.http.response.Response
        """
        auth = auth or self.auth
        headers = headers or {}

        headers['User-Agent'] = 'rindap-python/{} (Python {})'.format(
            __version__,
            platform.python_version(),
        )
        headers['X-Rindap-Client'] = 'python-{}'.format(__version__)
        headers['Accept-Charset'] = 'utf-8'

        if method == 'POST' and 'Content-Type' not in headers:
            headers['Content-Type'] = 'application/x-www-form-urlencoded'

        if 'Accept' not in headers:
            headers['Accept'] = 'application/json'

        if self.region:
            head, tail = uri.split('.', 1)

            if not tail.startswith(self.region):
                uri = '.'.join([head, self.region, tail])

        return self.http_client.request(
            method,
            uri,
            params=params,
            data=data,
            headers=headers,
            auth=auth,
            timeout=timeout,
            allow_redirects=allow_redirects
        )

    @property
    def rindap(self):
        """
        Access the Rindap Domain

        :returns: Rindap Domain
        :rtype: rindap.rest.Rindap
        """
        if self._rindap is None:
            from rindap.rest import Rindap
            self._rindap = Rindap(self)
        return self._rindap

    def __repr__(self):
        """
        Provide a friendly representation

        :returns: Machine friendly representation
        :rtype: str
        """
        return '<Rindap {}>'.format(self.account_sid)


@obsolete_client
class RindapClient(object):
    """ Dummy client which provides no functionality. Please use
    rindap.rest.Client instead. """

    def __init__(self, *args):
        pass


@obsolete_client
class RindapRestClient(object):
    """ Dummy client which provides no functionality. Please use
    rindap.rest.Client instead. """

    def __init__(self, *args):
        pass


# @obsolete_client
# class RindapTaskRouterClient(object):
#     """ Dummy client which provides no functionality. Please use
#     rindap.rest.Client instead. """

#     def __init__(self, *args):
#         pass

class Rindap(Domain):

    def __init__(self, rindap):
        """
        Initialize the Rindap Domain

        :returns: Domain for Rindap
        :rtype: rindap.rest.Rindap
        """
        super(Rindap, self).__init__(rindap)

        self.base_url = 'https://api.rindap.com'

        # Versions
        self._v1 = None

    @property
    def v1(self):
        """
        :returns: Version v1 of Rindap
        :rtype: rindap.rest.v1.V1
        """
        if self._v1 is None:
            self._v1 = V1(self)
        return self._v1

    @property
    def workspaces(self):
        """
        :rtype: rindap.rest.v1.workspace.WorkspaceList
        """
        return self.v1.workspaces

    def __repr__(self):
        """
        Provide a friendly representation

        :returns: Machine friendly representation
        :rtype: str
        """
        return '<Rindap>'
