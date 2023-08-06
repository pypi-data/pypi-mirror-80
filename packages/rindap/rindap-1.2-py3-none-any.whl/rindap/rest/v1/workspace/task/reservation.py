# coding=utf-8

from rindap.base import deserialize
from rindap.base import serialize
from rindap.base import values
from rindap.base.instance_context import InstanceContext
from rindap.base.instance_resource import InstanceResource
from rindap.base.list_resource import ListResource
from rindap.base.page import Page


class ReservationList(ListResource):
    """  """

    def __init__(self, version, workspace_sid, task_sid):
        """
        Initialize the ReservationList

        :param Version version: Version that contains the resource
        :param workspace_sid: The SID of the Workspace that this task is contained within.
        :param task_sid: The SID of the reserved Task resource

        :returns: rindap.rest.v1.workspace.task.reservation.ReservationList
        :rtype: rindap.rest.v1.workspace.task.reservation.ReservationList
        """
        super(ReservationList, self).__init__(version)

        # Path Solution
        self._solution = {'workspace_sid': workspace_sid, 'task_sid': task_sid, }
        self._uri = '/Workspaces/{workspace_sid}/Tasks/{task_sid}/Reservations'.format(**self._solution)

    def stream(self, reservation_status=values.unset, limit=None, page_size=None):
        """
        Streams ReservationInstance records from the API as a generator stream.
        This operation lazily loads records as efficiently as possible until the limit
        is reached.
        The results are returned as a generator, so this operation is memory efficient.

        :param ReservationInstance.Status reservation_status: Returns the list of reservations for a task with a specified ReservationStatus
        :param int limit: Upper limit for the number of records to return. stream()
                          guarantees to never return more than limit.  Default is no limit
        :param int page_size: Number of records to fetch per request, when not set will use
                              the default value of 50 records.  If no page_size is defined
                              but a limit is defined, stream() will attempt to read the
                              limit with the most efficient page size, i.e. min(limit, 1000)

        :returns: Generator that will yield up to limit results
        :rtype: list[rindap.rest.v1.workspace.task.reservation.ReservationInstance]
        """
        limits = self._version.read_limits(limit, page_size)

        page = self.page(reservation_status=reservation_status, page_size=limits['page_size'], )

        return self._version.stream(page, limits['limit'], limits['page_limit'])

    def list(self, reservation_status=values.unset, limit=None, page_size=None):
        """
        Lists ReservationInstance records from the API as a list.
        Unlike stream(), this operation is eager and will load `limit` records into
        memory before returning.

        :param ReservationInstance.Status reservation_status: Returns the list of reservations for a task with a specified ReservationStatus
        :param int limit: Upper limit for the number of records to return. list() guarantees
                          never to return more than limit.  Default is no limit
        :param int page_size: Number of records to fetch per request, when not set will use
                              the default value of 50 records.  If no page_size is defined
                              but a limit is defined, list() will attempt to read the limit
                              with the most efficient page size, i.e. min(limit, 1000)

        :returns: Generator that will yield up to limit results
        :rtype: list[rindap.rest.v1.workspace.task.reservation.ReservationInstance]
        """
        return list(self.stream(reservation_status=reservation_status, limit=limit, page_size=page_size, ))

    def page(self, reservation_status=values.unset, page_token=values.unset,
             page_number=values.unset, page_size=values.unset):
        """
        Retrieve a single page of ReservationInstance records from the API.
        Request is executed immediately

        :param ReservationInstance.Status reservation_status: Returns the list of reservations for a task with a specified ReservationStatus
        :param str page_token: PageToken provided by the API
        :param int page_number: Page Number, this value is simply for client state
        :param int page_size: Number of records to return, defaults to 50

        :returns: Page of ReservationInstance
        :rtype: rindap.rest.v1.workspace.task.reservation.ReservationPage
        """
        data = values.of({
            'ReservationStatus': reservation_status,
            'PageToken': page_token,
            'Page': page_number,
            'PageSize': page_size,
        })

        response = self._version.page(method='GET', uri=self._uri, params=data, )

        return ReservationPage(self._version, response, self._solution)

    def get_page(self, target_url):
        """
        Retrieve a specific page of ReservationInstance records from the API.
        Request is executed immediately

        :param str target_url: API-generated URL for the requested results page

        :returns: Page of ReservationInstance
        :rtype: rindap.rest.v1.workspace.task.reservation.ReservationPage
        """
        response = self._version.domain.rindap.request(
            'GET',
            target_url,
        )

        return ReservationPage(self._version, response, self._solution)

    def get(self, sid):
        """
        Constructs a ReservationContext

        :param sid: The SID of the TaskReservation resource to fetch

        :returns: rindap.rest.v1.workspace.task.reservation.ReservationContext
        :rtype: rindap.rest.v1.workspace.task.reservation.ReservationContext
        """
        return ReservationContext(
            self._version,
            workspace_sid=self._solution['workspace_sid'],
            task_sid=self._solution['task_sid'],
            sid=sid,
        )

    def __call__(self, sid):
        """
        Constructs a ReservationContext

        :param sid: The SID of the TaskReservation resource to fetch

        :returns: rindap.rest.v1.workspace.task.reservation.ReservationContext
        :rtype: rindap.rest.v1.workspace.task.reservation.ReservationContext
        """
        return ReservationContext(
            self._version,
            workspace_sid=self._solution['workspace_sid'],
            task_sid=self._solution['task_sid'],
            sid=sid,
        )

    def __repr__(self):
        """
        Provide a friendly representation

        :returns: Machine friendly representation
        :rtype: str
        """
        return '<Rindap.Taskrouter.V1.ReservationList>'


class ReservationPage(Page):
    """  """

    def __init__(self, version, response, solution):
        """
        Initialize the ReservationPage

        :param Version version: Version that contains the resource
        :param Response response: Response from the API
        :param workspace_sid: The SID of the Workspace that this task is contained within.
        :param task_sid: The SID of the reserved Task resource

        :returns: rindap.rest.v1.workspace.task.reservation.ReservationPage
        :rtype: rindap.rest.v1.workspace.task.reservation.ReservationPage
        """
        super(ReservationPage, self).__init__(version, response)

        # Path Solution
        self._solution = solution

    def get_instance(self, payload):
        """
        Build an instance of ReservationInstance

        :param dict payload: Payload response from the API

        :returns: rindap.rest.v1.workspace.task.reservation.ReservationInstance
        :rtype: rindap.rest.v1.workspace.task.reservation.ReservationInstance
        """
        return ReservationInstance(
            self._version,
            payload,
            workspace_sid=self._solution['workspace_sid'],
            task_sid=self._solution['task_sid'],
        )

    def __repr__(self):
        """
        Provide a friendly representation

        :returns: Machine friendly representation
        :rtype: str
        """
        return '<Rindap.Taskrouter.V1.ReservationPage>'


class ReservationContext(InstanceContext):
    """  """

    def __init__(self, version, workspace_sid, task_sid, sid):
        """
        Initialize the ReservationContext

        :param Version version: Version that contains the resource
        :param workspace_sid: The SID of the Workspace with the TaskReservation resource to fetch
        :param task_sid: The SID of the reserved Task resource with the TaskReservation resource to fetch
        :param sid: The SID of the TaskReservation resource to fetch

        :returns: rindap.rest.v1.workspace.task.reservation.ReservationContext
        :rtype: rindap.rest.v1.workspace.task.reservation.ReservationContext
        """
        super(ReservationContext, self).__init__(version)

        # Path Solution
        self._solution = {'workspace_sid': workspace_sid, 'task_sid': task_sid, 'sid': sid, }
        self._uri = '/Workspaces/{workspace_sid}/Tasks/{task_sid}/Reservations/{sid}'.format(**self._solution)

    def fetch(self):
        """
        Fetch the ReservationInstance

        :returns: The fetched ReservationInstance
        :rtype: rindap.rest.v1.workspace.task.reservation.ReservationInstance
        """
        payload = self._version.fetch(method='GET', uri=self._uri, )

        return ReservationInstance(
            self._version,
            payload,
            workspace_sid=self._solution['workspace_sid'],
            task_sid=self._solution['task_sid'],
            sid=self._solution['sid'],
        )

    def update(self, reservation_status=values.unset):
        """
        Update the ReservationInstance

        :param ReservationInstance.Status reservation_status: The new status of the reservation
        :param unicode status_callback: The URL we should call to send status information to your application
        :param unicode status_callback_method: The HTTP method we should use to call status_callback
        :param unicode timeout: Timeout for call when executing a Conference instruction
        :param unicode region: The region where we should mix the conference audio

        :returns: The updated ReservationInstance
        :rtype: rindap.rest.v1.workspace.task.reservation.ReservationInstance
        """
        data = values.of({
            'ReservationStatus': reservation_status,
        })

        payload = self._version.update(method='PUT', uri=self._uri, data=data, )

        return ReservationInstance(
            self._version,
            payload,
            workspace_sid=self._solution['workspace_sid'],
            task_sid=self._solution['task_sid'],
            sid=self._solution['sid'],
        )

    def __repr__(self):
        """
        Provide a friendly representation

        :returns: Machine friendly representation
        :rtype: str
        """
        context = ' '.join('{}={}'.format(k, v) for k, v in self._solution.items())
        return '<Rindap.Taskrouter.V1.ReservationContext {}>'.format(context)


class ReservationInstance(InstanceResource):
    """  """

    class Status(object):
        PENDING = "pending"
        ACCEPTED = "accepted"
        REJECTED = "rejected"
        COMPLETED = "completed"

    def __init__(self, version, payload, workspace_sid, task_sid, sid=None):
        """
        Initialize the ReservationInstance

        :returns: rindap.rest.v1.workspace.task.reservation.ReservationInstance
        :rtype: rindap.rest.v1.workspace.task.reservation.ReservationInstance
        """
        super(ReservationInstance, self).__init__(version)

        # Marshaled Properties
        self._properties = {
            'account_sid': payload.get('account_sid'),
            'date_created': deserialize.iso8601_datetime(payload.get('date_created')),
            'date_updated': deserialize.iso8601_datetime(payload.get('date_updated')),
            'reservation_status': payload.get('reservation_status'),
            'sid': payload.get('sid'),
            'task_sid': payload.get('task_sid'),
            'worker_name': payload.get('worker_name'),
            'worker_sid': payload.get('worker_sid'),
            'workspace_sid': payload.get('workspace_sid'),
            'url': payload.get('url'),
            'links': payload.get('links'),
        }

        # Context
        self._context = None
        self._solution = {
            'workspace_sid': workspace_sid,
            'task_sid': task_sid,
            'sid': sid or self._properties['sid'],
        }

    @property
    def _proxy(self):
        """
        Generate an instance context for the instance, the context is capable of
        performing various actions.  All instance actions are proxied to the context

        :returns: ReservationContext for this ReservationInstance
        :rtype: rindap.rest.v1.workspace.task.reservation.ReservationContext
        """
        if self._context is None:
            self._context = ReservationContext(
                self._version,
                workspace_sid=self._solution['workspace_sid'],
                task_sid=self._solution['task_sid'],
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
        :returns: The ISO 8601 date and time in GMT when the resource was created
        :rtype: datetime
        """
        return self._properties['date_created']

    @property
    def date_updated(self):
        """
        :returns: The ISO 8601 date and time in GMT when the resource was last updated
        :rtype: datetime
        """
        return self._properties['date_updated']

    @property
    def reservation_status(self):
        """
        :returns: The current status of the reservation
        :rtype: ReservationInstance.Status
        """
        return self._properties['reservation_status']

    @property
    def sid(self):
        """
        :returns: The unique string that identifies the resource
        :rtype: unicode
        """
        return self._properties['sid']

    @property
    def task_sid(self):
        """
        :returns: The SID of the reserved Task resource
        :rtype: unicode
        """
        return self._properties['task_sid']

    @property
    def worker_name(self):
        """
        :returns: The friendly_name of the Worker that is reserved
        :rtype: unicode
        """
        return self._properties['worker_name']

    @property
    def worker_sid(self):
        """
        :returns: The SID of the reserved Worker resource
        :rtype: unicode
        """
        return self._properties['worker_sid']

    @property
    def workspace_sid(self):
        """
        :returns: The SID of the Workspace that this task is contained within.
        :rtype: unicode
        """
        return self._properties['workspace_sid']

    @property
    def url(self):
        """
        :returns: The absolute URL of the TaskReservation reservation
        :rtype: unicode
        """
        return self._properties['url']

    @property
    def links(self):
        """
        :returns: The URLs of related resources
        :rtype: unicode
        """
        return self._properties['links']

    def fetch(self):
        """
        Fetch the ReservationInstance

        :returns: The fetched ReservationInstance
        :rtype: rindap.rest.v1.workspace.task.reservation.ReservationInstance
        """
        return self._proxy.fetch()

    def update(self, reservation_status=values.unset):
        """
        Update the ReservationInstance

        :param ReservationInstance.Status reservation_status: The new status of the reservation

        :returns: The updated ReservationInstance
        :rtype: rindap.rest.v1.workspace.task.reservation.ReservationInstance
        """
        return self._proxy.update(
            reservation_status=reservation_status,
        )

    def __repr__(self):
        """
        Provide a friendly representation

        :returns: Machine friendly representation
        :rtype: str
        """
        context = ' '.join('{}={}'.format(k, v) for k, v in self._solution.items())
        return '<Rindap.V1.ReservationInstance {}>'.format(context)
