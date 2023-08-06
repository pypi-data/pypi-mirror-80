# coding=utf-8

from rindap.base import deserialize
from rindap.base import values
from rindap.base.instance_context import InstanceContext
from rindap.base.instance_resource import InstanceResource
from rindap.base.list_resource import ListResource
from rindap.base.page import Page


class RateLimitProfileList(ListResource):
    """  """

    def __init__(self, version, workspace_sid):
        """
        Initialize the RateLimitProfileList

        :param Version version: Version that contains the resource
        :param workspace_sid: The SID of the Workspace that contains the RateLimitProfile

        :returns: rindap.rest.v1.workspace.task_queue.RateLimitProfileList
        :rtype: rindap.rest.v1.workspace.task_queue.RateLimitProfileList
        """
        super(RateLimitProfileList, self).__init__(version)

        # Path Solution
        self._solution = {'workspace_sid': workspace_sid, }
        self._uri = '/Workspaces/{workspace_sid}/RateLimitProfiles'.format(**self._solution)

    def stream(self, friendly_name=values.unset,
               evaluate_worker_attributes=values.unset, worker_sid=values.unset,
               limit=None, page_size=None):
        """
        Streams RateLimitProfileInstance records from the API as a generator stream.
        This operation lazily loads records as efficiently as possible until the limit
        is reached.
        The results are returned as a generator, so this operation is memory efficient.

        :param unicode friendly_name: The friendly_name of the RateLimitProfile resources to read
        :param unicode evaluate_worker_attributes: The attributes of the Workers to read
        :param unicode worker_sid: The SID of the Worker with the RateLimitProfile resources to read
        :param int limit: Upper limit for the number of records to return. stream()
                          guarantees to never return more than limit.  Default is no limit
        :param int page_size: Number of records to fetch per request, when not set will use
                              the default value of 50 records.  If no page_size is defined
                              but a limit is defined, stream() will attempt to read the
                              limit with the most efficient page size, i.e. min(limit, 1000)

        :returns: Generator that will yield up to limit results
        :rtype: list[rindap.rest.v1.workspace.task_queue.RateLimitProfileInstance]
        """
        limits = self._version.read_limits(limit, page_size)

        page = self.page(
            friendly_name=friendly_name,
            evaluate_worker_attributes=evaluate_worker_attributes,
            worker_sid=worker_sid,
            page_size=limits['page_size'],
        )

        return self._version.stream(page, limits['limit'], limits['page_limit'])

    def list(self, friendly_name=values.unset,
             evaluate_worker_attributes=values.unset, worker_sid=values.unset,
             limit=None, page_size=None):
        """
        Lists RateLimitProfileInstance records from the API as a list.
        Unlike stream(), this operation is eager and will load `limit` records into
        memory before returning.

        :param unicode friendly_name: The friendly_name of the RateLimitProfile resources to read
        :param unicode evaluate_worker_attributes: The attributes of the Workers to read
        :param unicode worker_sid: The SID of the Worker with the RateLimitProfile resources to read
        :param int limit: Upper limit for the number of records to return. list() guarantees
                          never to return more than limit.  Default is no limit
        :param int page_size: Number of records to fetch per request, when not set will use
                              the default value of 50 records.  If no page_size is defined
                              but a limit is defined, list() will attempt to read the limit
                              with the most efficient page size, i.e. min(limit, 1000)

        :returns: Generator that will yield up to limit results
        :rtype: list[rindap.rest.v1.workspace.task_queue.RateLimitProfileInstance]
        """
        return list(self.stream(
            friendly_name=friendly_name,
            evaluate_worker_attributes=evaluate_worker_attributes,
            worker_sid=worker_sid,
            limit=limit,
            page_size=page_size,
        ))

    def page(self, friendly_name=values.unset,
             evaluate_worker_attributes=values.unset, worker_sid=values.unset,
             page_token=values.unset, page_number=values.unset,
             page_size=values.unset):
        """
        Retrieve a single page of RateLimitProfileInstance records from the API.
        Request is executed immediately

        :param unicode friendly_name: The friendly_name of the RateLimitProfile resources to read
        :param unicode evaluate_worker_attributes: The attributes of the Workers to read
        :param unicode worker_sid: The SID of the Worker with the RateLimitProfile resources to read
        :param str page_token: PageToken provided by the API
        :param int page_number: Page Number, this value is simply for client state
        :param int page_size: Number of records to return, defaults to 50

        :returns: Page of RateLimitProfileInstance
        :rtype: rindap.rest.v1.workspace.task_queue.RateLimitProfilePage
        """
        data = values.of({
            'FriendlyName': friendly_name,
            'EvaluateWorkerAttributes': evaluate_worker_attributes,
            'WorkerSid': worker_sid,
            'PageToken': page_token,
            'Page': page_number,
            'PageSize': page_size,
        })

        response = self._version.page(method='GET', uri=self._uri, params=data, )

        return RateLimitProfilePage(self._version, response, self._solution)

    def get_page(self, target_url):
        """
        Retrieve a specific page of RateLimitProfileInstance records from the API.
        Request is executed immediately

        :param str target_url: API-generated URL for the requested results page

        :returns: Page of RateLimitProfileInstance
        :rtype: rindap.rest.v1.workspace.task_queue.RateLimitProfilePage
        """
        response = self._version.domain.rindap.request(
            'GET',
            target_url,
        )

        return RateLimitProfilePage(self._version, response, self._solution)

    def create(self, friendly_name, reservation_per_hour=10):
        """
        Create the RateLimitProfileInstance

        :param unicode friendly_name: A string to describe the resource
        :param integer reservation_per_hour: The maximum number of Reservations that can be created hourly, for a Worker with this RateLimitProfile

        :returns: The created RateLimitProfileInstance
        :rtype: rindap.rest.v1.workspace.task_queue.RateLimitProfileInstance
        """
        data = values.of({
            'FriendlyName': friendly_name,
            'ReservationsPerHour': reservation_per_hour
        })

        payload = self._version.create(method='POST', uri=self._uri, data=data, )

        return RateLimitProfileInstance(self._version, payload, workspace_sid=self._solution['workspace_sid'], )

    def get(self, sid):
        """
        Constructs a RateLimitProfileContext

        :param sid: The SID of the resource to

        :returns: rindap.rest.v1.workspace.task_queue.RateLimitProfileContext
        :rtype: rindap.rest.v1.workspace.task_queue.RateLimitProfileContext
        """
        return RateLimitProfileContext(self._version, workspace_sid=self._solution['workspace_sid'], sid=sid, )

    def __call__(self, sid):
        """
        Constructs a RateLimitProfileContext

        :param sid: The SID of the resource to

        :returns: rindap.rest.v1.workspace.task_queue.RateLimitProfileContext
        :rtype: rindap.rest.v1.workspace.task_queue.RateLimitProfileContext
        """
        return RateLimitProfileContext(self._version, workspace_sid=self._solution['workspace_sid'], sid=sid, )

    def __repr__(self):
        """
        Provide a friendly representation

        :returns: Machine friendly representation
        :rtype: str
        """
        return '<Rindap.V1.RateLimitProfileList>'


class RateLimitProfilePage(Page):
    """  """

    def __init__(self, version, response, solution):
        """
        Initialize the RateLimitProfilePage

        :param Version version: Version that contains the resource
        :param Response response: Response from the API
        :param workspace_sid: The SID of the Workspace that contains the RateLimitProfile

        :returns: rindap.rest.v1.workspace.task_queue.RateLimitProfilePage
        :rtype: rindap.rest.v1.workspace.task_queue.RateLimitProfilePage
        """
        super(RateLimitProfilePage, self).__init__(version, response)

        # Path Solution
        self._solution = solution

    def get_instance(self, payload):
        """
        Build an instance of RateLimitProfileInstance

        :param dict payload: Payload response from the API

        :returns: rindap.rest.v1.workspace.task_queue.RateLimitProfileInstance
        :rtype: rindap.rest.v1.workspace.task_queue.RateLimitProfileInstance
        """
        return RateLimitProfileInstance(self._version, payload, workspace_sid=self._solution['workspace_sid'], )

    def __repr__(self):
        """
        Provide a friendly representation

        :returns: Machine friendly representation
        :rtype: str
        """
        return '<Rindap.V1.RateLimitProfilePage>'


class RateLimitProfileContext(InstanceContext):
    """  """

    def __init__(self, version, workspace_sid, sid):
        """
        Initialize the RateLimitProfileContext

        :param Version version: Version that contains the resource
        :param workspace_sid: The SID of the Workspace with the RateLimitProfile to fetch
        :param sid: The SID of the resource to

        :returns: rindap.rest.v1.workspace.task_queue.RateLimitProfileContext
        :rtype: rindap.rest.v1.workspace.task_queue.RateLimitProfileContext
        """
        super(RateLimitProfileContext, self).__init__(version)

        # Path Solution
        self._solution = {'workspace_sid': workspace_sid, 'sid': sid, }
        self._uri = '/Workspaces/{workspace_sid}/RateLimitProfiles/{sid}'.format(**self._solution)

    def fetch(self):
        """
        Fetch the RateLimitProfileInstance

        :returns: The fetched RateLimitProfileInstance
        :rtype: rindap.rest.v1.workspace.task_queue.RateLimitProfileInstance
        """
        payload = self._version.fetch(method='GET', uri=self._uri, )

        return RateLimitProfileInstance(
            self._version,
            payload,
            workspace_sid=self._solution['workspace_sid'],
            sid=self._solution['sid'],
        )

    def update(self, friendly_name=values.unset, reservation_per_hour=values.unset):
        """
        Update the RateLimitProfileInstance

        :param unicode friendly_name: A string to describe the resource
        :param integer reservation_per_hour: The maximum number of Reservations that can be created hourly, for a Worker with this RateLimitProfile

        :returns: The updated RateLimitProfileInstance
        :rtype: rindap.rest.v1.workspace.task_queue.RateLimitProfileInstance
        """
        data = values.of({
            'FriendlyName': friendly_name,
            'ReservationsPerHour': reservation_per_hour
            
        })

        payload = self._version.update(method='PUT', uri=self._uri, data=data, )

        return RateLimitProfileInstance(
            self._version,
            payload,
            workspace_sid=self._solution['workspace_sid'],
            sid=self._solution['sid'],
        )

    def delete(self):
        """
        Deletes the RateLimitProfileInstance

        :returns: True if delete succeeds, False otherwise
        :rtype: bool
        """
        return self._version.delete(method='DELETE', uri=self._uri, )

    def __repr__(self):
        """
        Provide a friendly representation

        :returns: Machine friendly representation
        :rtype: str
        """
        context = ' '.join('{}={}'.format(k, v) for k, v in self._solution.items())
        return '<Rindap.V1.RateLimitProfileContext {}>'.format(context)


class RateLimitProfileInstance(InstanceResource):
    """  """

    def __init__(self, version, payload, workspace_sid, sid=None):
        """
        Initialize the RateLimitProfileInstance

        :returns: rindap.rest.v1.workspace.task_queue.RateLimitProfileInstance
        :rtype: rindap.rest.v1.workspace.task_queue.RateLimitProfileInstance
        """
        super(RateLimitProfileInstance, self).__init__(version)

        # Marshaled Properties
        self._properties = {
            'account_sid': payload.get('account_sid'),
            'date_created': deserialize.iso8601_datetime(payload.get('date_created')),
            'date_updated': deserialize.iso8601_datetime(payload.get('date_updated')),
            'friendly_name': payload.get('friendly_name'),
            'sid': payload.get('sid'),
            'workspace_sid': payload.get('workspace_sid')
        }

        # Context
        self._context = None
        self._solution = {'workspace_sid': workspace_sid, 'sid': sid or self._properties['sid'], }

    @property
    def _proxy(self):
        """
        Generate an instance context for the instance, the context is capable of
        performing various actions.  All instance actions are proxied to the context

        :returns: RateLimitProfileContext for this RateLimitProfileInstance
        :rtype: rindap.rest.v1.workspace.task_queue.RateLimitProfileContext
        """
        if self._context is None:
            self._context = RateLimitProfileContext(
                self._version,
                workspace_sid=self._solution['workspace_sid'],
                sid=self._solution['sid'],
            )
        return self._context

    @property
    def account_sid(self):
        """
        :returns: The SID of the Account that created the resource
        :rtype: unicode
        """
        return self._properties['account_sid']

    @property
    def date_created(self):
        """
        :returns: The RFC 2822 date and time in GMT when the resource was created
        :rtype: datetime
        """
        return self._properties['date_created']

    @property
    def date_updated(self):
        """
        :returns: The RFC 2822 date and time in GMT when the resource was last updated
        :rtype: datetime
        """
        return self._properties['date_updated']

    @property
    def friendly_name(self):
        """
        :returns: The string that you assigned to describe the resource
        :rtype: unicode
        """
        return self._properties['friendly_name']

    @property
    def sid(self):
        """
        :returns: The unique string that identifies the resource
        :rtype: unicode
        """
        return self._properties['sid']

    @property
    def workspace_sid(self):
        """
        :returns: The SID of the Workspace that contains the RateLimitProfile
        :rtype: unicode
        """
        return self._properties['workspace_sid']

    def fetch(self):
        """
        Fetch the RateLimitProfileInstance

        :returns: The fetched RateLimitProfileInstance
        :rtype: rindap.rest.v1.workspace.task_queue.RateLimitProfileInstance
        """
        return self._proxy.fetch()

    def update(self, friendly_name=values.unset, reservation_per_hour=values.unset):
        """
        Update the RateLimitProfileInstance

        :param unicode friendly_name: A string to describe the resource
        :param integer reservation_per_hour: The maximum number of Reservations that can be created hourly, for a Worker with this RateLimitProfile

        :returns: The updated RateLimitProfileInstance
        :rtype: rindap.rest.v1.workspace.task_queue.RateLimitProfileInstance
        """
        return self._proxy.update(
            friendly_name=friendly_name,
            reservation_per_hour=reservation_per_hour
        )

    def delete(self):
        """
        Deletes the RateLimitProfileInstance

        :returns: True if delete succeeds, False otherwise
        :rtype: bool
        """
        return self._proxy.delete()

    def __repr__(self):
        """
        Provide a friendly representation

        :returns: Machine friendly representation
        :rtype: str
        """
        context = ' '.join('{}={}'.format(k, v) for k, v in self._solution.items())
        return '<Rindap.V1.RateLimitProfileInstance {}>'.format(context)
