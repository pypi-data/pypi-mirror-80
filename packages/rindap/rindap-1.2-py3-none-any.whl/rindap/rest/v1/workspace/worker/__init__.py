# coding=utf-8

from rindap.base import deserialize
from rindap.base import values
from rindap.base.instance_context import InstanceContext
from rindap.base.instance_resource import InstanceResource
from rindap.base.list_resource import ListResource
from rindap.base.page import Page
from rindap.rest.v1.workspace.worker.reservation import ReservationList


class WorkerList(ListResource):
    """  """

    def __init__(self, version, workspace_sid):
        """
        Initialize the WorkerList

        :param Version version: Version that contains the resource
        :param workspace_sid: The SID of the Workspace that contains the Worker

        :returns: rindap.rest.v1.workspace.worker.WorkerList
        :rtype: rindap.rest.v1.workspace.worker.WorkerList
        """
        super(WorkerList, self).__init__(version)

        # Path Solution
        self._solution = {'workspace_sid': workspace_sid, }
        self._uri = '/Workspaces/{workspace_sid}/Workers'.format(**self._solution)

    def stream(self, activity_name=values.unset, activity_sid=values.unset,
               available=values.unset, friendly_name=values.unset,
               target_workers_expression=values.unset, task_queue_name=values.unset,
               limit=None, page_size=None):
        """
        Streams WorkerInstance records from the API as a generator stream.
        This operation lazily loads records as efficiently as possible until the limit
        is reached.
        The results are returned as a generator, so this operation is memory efficient.

        :param unicode activity_name: The activity_name of the Worker resources to read
        :param unicode activity_sid: The activity_sid of the Worker resources to read
        :param unicode available: Whether to return Worker resources that are available or unavailable
        :param unicode friendly_name: The friendly_name of the Worker resources to read
        :param unicode target_workers_expression: Filter by Workers that would match an expression on a TaskQueue
        :param unicode task_queue_name: The friendly_name of the TaskQueue that the Workers to read are eligible for
        :param int limit: Upper limit for the number of records to return. stream()
                          guarantees to never return more than limit.  Default is no limit
        :param int page_size: Number of records to fetch per request, when not set will use
                              the default value of 50 records.  If no page_size is defined
                              but a limit is defined, stream() will attempt to read the
                              limit with the most efficient page size, i.e. min(limit, 1000)

        :returns: Generator that will yield up to limit results
        :rtype: list[rindap.rest.v1.workspace.worker.WorkerInstance]
        """
        limits = self._version.read_limits(limit, page_size)

        page = self.page(
            activity_name=activity_name,
            activity_sid=activity_sid,
            available=available,
            friendly_name=friendly_name,
            target_workers_expression=target_workers_expression,
            task_queue_name=task_queue_name,
            page_size=limits['page_size'],
        )

        return self._version.stream(page, limits['limit'], limits['page_limit'])

    def list(self, activity_name=values.unset, activity_sid=values.unset,
             available=values.unset, friendly_name=values.unset,
             target_workers_expression=values.unset, task_queue_name=values.unset,
             limit=None, page_size=None):
        """
        Lists WorkerInstance records from the API as a list.
        Unlike stream(), this operation is eager and will load `limit` records into
        memory before returning.

        :param unicode activity_name: The activity_name of the Worker resources to read
        :param unicode activity_sid: The activity_sid of the Worker resources to read
        :param unicode available: Whether to return Worker resources that are available or unavailable
        :param unicode friendly_name: The friendly_name of the Worker resources to read
        :param unicode target_workers_expression: Filter by Workers that would match an expression on a TaskQueue
        :param unicode task_queue_name: The friendly_name of the TaskQueue that the Workers to read are eligible for
        :param int limit: Upper limit for the number of records to return. list() guarantees
                          never to return more than limit.  Default is no limit
        :param int page_size: Number of records to fetch per request, when not set will use
                              the default value of 50 records.  If no page_size is defined
                              but a limit is defined, list() will attempt to read the limit
                              with the most efficient page size, i.e. min(limit, 1000)

        :returns: Generator that will yield up to limit results
        :rtype: list[rindap.rest.v1.workspace.worker.WorkerInstance]
        """
        return list(self.stream(
            activity_name=activity_name,
            activity_sid=activity_sid,
            available=available,
            friendly_name=friendly_name,
            target_workers_expression=target_workers_expression,
            task_queue_name=task_queue_name,
            limit=limit,
            page_size=page_size,
        ))

    def page(self, activity_name=values.unset, activity_sid=values.unset,
             available=values.unset, friendly_name=values.unset,
             target_workers_expression=values.unset, task_queue_name=values.unset,
             task_queue_sid=values.unset, page_token=values.unset,
             page_number=values.unset, page_size=values.unset):
        """
        Retrieve a single page of WorkerInstance records from the API.
        Request is executed immediately

        :param unicode activity_name: The activity_name of the Worker resources to read
        :param unicode activity_sid: The activity_sid of the Worker resources to read
        :param unicode available: Whether to return Worker resources that are available or unavailable
        :param unicode friendly_name: The friendly_name of the Worker resources to read
        :param unicode target_workers_expression: Filter by Workers that would match an expression on a TaskQueue
        :param unicode task_queue_name: The friendly_name of the TaskQueue that the Workers to read are eligible for
        :param unicode task_queue_sid: The SID of the TaskQueue that the Workers to read are eligible for
        :param str page_token: PageToken provided by the API
        :param int page_number: Page Number, this value is simply for client state
        :param int page_size: Number of records to return, defaults to 50

        :returns: Page of WorkerInstance
        :rtype: rindap.rest.v1.workspace.worker.WorkerPage
        """
        data = values.of({
            'ActivityName': activity_name,
            'ActivitySid': activity_sid,
            'Available': available,
            'FriendlyName': friendly_name,
            'TargetWorkersExpression': target_workers_expression,
            'TaskQueueName': task_queue_name,
            'TaskQueueSid': task_queue_sid,
            'PageToken': page_token,
            'Page': page_number,
            'PageSize': page_size,
        })

        response = self._version.page(method='GET', uri=self._uri, params=data, )

        return WorkerPage(self._version, response, self._solution)

    def get_page(self, target_url):
        """
        Retrieve a specific page of WorkerInstance records from the API.
        Request is executed immediately

        :param str target_url: API-generated URL for the requested results page

        :returns: Page of WorkerInstance
        :rtype: rindap.rest.v1.workspace.worker.WorkerPage
        """
        response = self._version.domain.rindap.request(
            'GET',
            target_url,
        )

        return WorkerPage(self._version, response, self._solution)

    def create(self, friendly_name, activity=values.unset, task_queues=[], rate_limit_profile_sid=values.unset):
        """
        Create the WorkerInstance

        :param unicode friendly_name: A string to describe the resource
        :param unicode activity_sid: The SID of a valid Activity that describes the new Worker's initial state
        :param unicode attributes: A valid JSON string that describes the new Worker
        :param unicode task_queues: The SID array of the TaskQueue that the Workers to read are eligible for
        :param univode rate_limit_profile_sid: The SID of the RateLimitProfile for overseeing the maximum rate of reservations this Worker can have hourly.

        :returns: The created WorkerInstance
        :rtype: rindap.rest.v1.workspace.worker.WorkerInstance
        """
        data = values.of({
            'FriendlyName': friendly_name,
            'Activity': activity,
            'TaskQueues': ",".join(task_queues),
            'RateLimitProfileSid': rate_limit_profile_sid
        })

        payload = self._version.create(method='POST', uri=self._uri, data=data, )

        return WorkerInstance(self._version, payload, workspace_sid=self._solution['workspace_sid'], )

    def get(self, sid):
        """
        Constructs a WorkerContext

        :param sid: The SID of the resource to fetch

        :returns: rindap.rest.v1.workspace.worker.WorkerContext
        :rtype: rindap.rest.v1.workspace.worker.WorkerContext
        """
        return WorkerContext(self._version, workspace_sid=self._solution['workspace_sid'], sid=sid, )

    def __call__(self, sid):
        """
        Constructs a WorkerContext

        :param sid: The SID of the resource to fetch

        :returns: rindap.rest.v1.workspace.worker.WorkerContext
        :rtype: rindap.rest.v1.workspace.worker.WorkerContext
        """
        return WorkerContext(self._version, workspace_sid=self._solution['workspace_sid'], sid=sid, )

    def __repr__(self):
        """
        Provide a friendly representation

        :returns: Machine friendly representation
        :rtype: str
        """
        return '<Rindap.V1.WorkerList>'


class WorkerPage(Page):
    """  """

    def __init__(self, version, response, solution):
        """
        Initialize the WorkerPage

        :param Version version: Version that contains the resource
        :param Response response: Response from the API
        :param workspace_sid: The SID of the Workspace that contains the Worker

        :returns: rindap.rest.v1.workspace.worker.WorkerPage
        :rtype: rindap.rest.v1.workspace.worker.WorkerPage
        """
        super(WorkerPage, self).__init__(version, response)

        # Path Solution
        self._solution = solution

    def get_instance(self, payload):
        """
        Build an instance of WorkerInstance

        :param dict payload: Payload response from the API

        :returns: rindap.rest.v1.workspace.worker.WorkerInstance
        :rtype: rindap.rest.v1.workspace.worker.WorkerInstance
        """
        return WorkerInstance(self._version, payload, workspace_sid=self._solution['workspace_sid'], )

    def __repr__(self):
        """
        Provide a friendly representation

        :returns: Machine friendly representation
        :rtype: str
        """
        return '<Rindap.V1.WorkerPage>'


class WorkerContext(InstanceContext):
    """  """

    def __init__(self, version, workspace_sid, sid):
        """
        Initialize the WorkerContext

        :param Version version: Version that contains the resource
        :param workspace_sid: The SID of the Workspace with the Worker to fetch
        :param sid: The SID of the resource to fetch

        :returns: rindap.rest.v1.workspace.worker.WorkerContext
        :rtype: rindap.rest.v1.workspace.worker.WorkerContext
        """
        super(WorkerContext, self).__init__(version)

        # Path Solution
        self._solution = {'workspace_sid': workspace_sid, 'sid': sid, }
        self._uri = '/Workspaces/{workspace_sid}/Workers/{sid}'.format(**self._solution)

        # Dependents
        self._reservations = None

    def fetch(self):
        """
        Fetch the WorkerInstance

        :returns: The fetched WorkerInstance
        :rtype: rindap.rest.v1.workspace.worker.WorkerInstance
        """
        payload = self._version.fetch(method='GET', uri=self._uri, )

        return WorkerInstance(
            self._version,
            payload,
            workspace_sid=self._solution['workspace_sid'],
            sid=self._solution['sid'],
        )

    def update(self, activity=values.unset, attributes=values.unset,
               friendly_name=values.unset,
               reject_pending_reservations=values.unset, task_queues=values.unset,
               rate_limit_profile_sid=values.unset):
        """
        Update the WorkerInstance

        :param unicode activity_sid: The SID of the Activity that describes the Worker's initial state
        :param unicode attributes: The JSON string that describes the Worker
        :param unicode friendly_name: A string to describe the Worker
        :param bool reject_pending_reservations: Whether to reject pending reservations
        :param unicode task_queues: The SID array of the TaskQueue that the Workers to read are eligible for
        :param univode rate_limit_profile_sid: The SID of the RateLimitProfile for overseeing the maximum rate of reservations this Worker can have hourly.

        :returns: The updated WorkerInstance
        :rtype: rindap.rest.v1.workspace.worker.WorkerInstance
        """

        if task_queues != values.unset:
            task_queues_param = ",".join(task_queues)
        else:
            task_queues_param = values.unset

        data = values.of({
            'Activity': activity,
            'Attributes': attributes,
            'FriendlyName': friendly_name,
            'RejectPendingReservations': reject_pending_reservations,
            'TaskQueues': task_queues_param,
            'RateLimitProfileSid': rate_limit_profile_sid

        })

        payload = self._version.update(method='PUT', uri=self._uri, data=data, )

        return WorkerInstance(
            self._version,
            payload,
            workspace_sid=self._solution['workspace_sid'],
            sid=self._solution['sid'],
        )

    def delete(self):
        """
        Deletes the WorkerInstance

        :returns: True if delete succeeds, False otherwise
        :rtype: bool
        """
        return self._version.delete(method='DELETE', uri=self._uri, )

    @property
    def reservations(self):
        """
        Access the reservations

        :returns: rindap.rest.v1.workspace.worker.reservation.ReservationList
        :rtype: rindap.rest.v1.workspace.worker.reservation.ReservationList
        """
        if self._reservations is None:
            self._reservations = ReservationList(
                self._version,
                workspace_sid=self._solution['workspace_sid'],
                worker_sid=self._solution['sid'],
            )
        return self._reservations

    def __repr__(self):
        """
        Provide a friendly representation

        :returns: Machine friendly representation
        :rtype: str
        """
        context = ' '.join('{}={}'.format(k, v) for k, v in self._solution.items())
        return '<Rindap.V1.WorkerContext {}>'.format(context)


class WorkerInstance(InstanceResource):
    """  """

    def __init__(self, version, payload, workspace_sid, sid=None):
        """
        Initialize the WorkerInstance

        :returns: rindap.rest.v1.workspace.worker.WorkerInstance
        :rtype: rindap.rest.v1.workspace.worker.WorkerInstance
        """
        super(WorkerInstance, self).__init__(version)

        # Marshaled Properties
        self._properties = {
            'account_sid': payload.get('account_sid'),
            'activity_name': payload.get('activity_name'),
            'activity': payload.get('activity'),
            'attributes': payload.get('attributes'),
            'available': payload.get('available'),
            'date_created': deserialize.iso8601_datetime(payload.get('date_created')),
            'date_status_changed': deserialize.iso8601_datetime(payload.get('date_status_changed')),
            'date_updated': deserialize.iso8601_datetime(payload.get('date_updated')),
            'friendly_name': payload.get('friendly_name'),
            'sid': payload.get('sid'),
            'workspace_sid': payload.get('workspace_sid'),
            'rate_limit_profile_sid': payload.get('rate_limit_profile_sid'),
            'task_queue_sids': payload.get('queues'),
            'url': payload.get('url'),
            'links': payload.get('links'),
        }

        # Context
        self._context = None
        self._solution = {'workspace_sid': workspace_sid, 'sid': sid or self._properties['sid'], }

    @property
    def _proxy(self):
        """
        Generate an instance context for the instance, the context is capable of
        performing various actions.  All instance actions are proxied to the context

        :returns: WorkerContext for this WorkerInstance
        :rtype: rindap.rest.v1.workspace.worker.WorkerContext
        """
        if self._context is None:
            self._context = WorkerContext(
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
    def activity_name(self):
        """
        :returns: The friendly_name of the Worker's current Activity
        :rtype: unicode
        """
        return self._properties['activity_name']

    @property
    def activity(self):
        """
        :returns: The Name of the Worker's current Activity
        :rtype: unicode
        """
        return self._properties['activity']

    @property
    def attributes(self):
        """
        :returns: The JSON string that describes the Worker
        :rtype: unicode
        """
        return self._properties['attributes']

    @property
    def available(self):
        """
        :returns: Whether the Worker is available to perform tasks
        :rtype: bool
        """
        return self._properties['available']

    @property
    def date_created(self):
        """
        :returns: The ISO 8601 date and time in GMT when the resource was created
        :rtype: datetime
        """
        return self._properties['date_created']

    @property
    def date_status_changed(self):
        """
        :returns: The date and time in GMT of the last change to the Worker's activity
        :rtype: datetime
        """
        return self._properties['date_status_changed']

    @property
    def date_updated(self):
        """
        :returns: The ISO 8601 date and time in GMT when the resource was last updated
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
        :returns: The SID of the Workspace that contains the Worker
        :rtype: unicode
        """
        return self._properties['workspace_sid']

    @property
    def rate_limit_profile_sid(self):
        """
        :returns: The SID of the RateLimitProfile that contains the Worker
        :rtype: unicode
        """
        return self._properties['rate_limit_profile_sid']

    @property
    def task_queue_sids(self):
        """
        :returns: The SIDs of the TaskQueue that contains the Worker
        :rtype: unicode
        """
        return self._properties['task_queue_sids']

    @property
    def url(self):
        """
        :returns: The absolute URL of the Worker resource
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
        Fetch the WorkerInstance

        :returns: The fetched WorkerInstance
        :rtype: rindap.rest.v1.workspace.worker.WorkerInstance
        """
        return self._proxy.fetch()

    def update(self, activity=values.unset, attributes=values.unset,
               friendly_name=values.unset,
               reject_pending_reservations=values.unset):
        """
        Update the WorkerInstance

        :param unicode activity: The Name of the Activity that describes the Worker's initial state
        :param unicode attributes: The JSON string that describes the Worker
        :param unicode friendly_name: A string to describe the Worker
        :param bool reject_pending_reservations: Whether to reject pending reservations

        :returns: The updated WorkerInstance
        :rtype: rindap.rest.v1.workspace.worker.WorkerInstance
        """
        return self._proxy.update(
            activity=activity,
            attributes=attributes,
            friendly_name=friendly_name,
            reject_pending_reservations=reject_pending_reservations,
        )

    def delete(self):
        """
        Deletes the WorkerInstance

        :returns: True if delete succeeds, False otherwise
        :rtype: bool
        """
        return self._proxy.delete()

    @property
    def reservations(self):
        """
        Access the reservations

        :returns: rindap.rest.v1.workspace.worker.reservation.ReservationList
        :rtype: rindap.rest.v1.workspace.worker.reservation.ReservationList
        """
        return self._proxy.reservations

    def __repr__(self):
        """
        Provide a friendly representation

        :returns: Machine friendly representation
        :rtype: str
        """
        context = ' '.join('{}={}'.format(k, v) for k, v in self._solution.items())
        return '<Rindap.V1.WorkerInstance {}>'.format(context)
