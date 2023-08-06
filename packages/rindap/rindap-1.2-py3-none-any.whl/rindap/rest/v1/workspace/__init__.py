# coding=utf-8

from rindap.base import deserialize
from rindap.base import values
from rindap.base.instance_context import InstanceContext
from rindap.base.instance_resource import InstanceResource
from rindap.base.list_resource import ListResource
from rindap.base.page import Page
from rindap.rest.v1.workspace.task import TaskList
from rindap.rest.v1.workspace.task_queue import TaskQueueList
from rindap.rest.v1.workspace.worker import WorkerList
from rindap.rest.v1.workspace.workflow import WorkflowList
from rindap.rest.v1.workspace.rate_limit_profile import RateLimitProfileList


class WorkspaceList(ListResource):
    """  """

    def __init__(self, version):
        """
        Initialize the WorkspaceList

        :param Version version: Version that contains the resource

        :returns: rindap.rest.v1.workspace.WorkspaceList
        :rtype: rindap.rest.v1.workspace.WorkspaceList
        """
        super(WorkspaceList, self).__init__(version)

        # Path Solution
        self._solution = {}
        self._uri = '/Workspaces'.format(**self._solution)

    def stream(self, friendly_name=values.unset, limit=None, page_size=None):
        """
        Streams WorkspaceInstance records from the API as a generator stream.
        This operation lazily loads records as efficiently as possible until the limit
        is reached.
        The results are returned as a generator, so this operation is memory efficient.

        :param unicode friendly_name: The friendly_name of the Workspace resources to read
        :param int limit: Upper limit for the number of records to return. stream()
                          guarantees to never return more than limit.  Default is no limit
        :param int page_size: Number of records to fetch per request, when not set will use
                              the default value of 50 records.  If no page_size is defined
                              but a limit is defined, stream() will attempt to read the
                              limit with the most efficient page size, i.e. min(limit, 1000)

        :returns: Generator that will yield up to limit results
        :rtype: list[rindap.rest.v1.workspace.WorkspaceInstance]
        """
        limits = self._version.read_limits(limit, page_size)

        page = self.page(friendly_name=friendly_name, page_size=limits['page_size'], )

        return self._version.stream(page, limits['limit'], limits['page_limit'])

    def list(self, friendly_name=values.unset, limit=None, page_size=None):
        """
        Lists WorkspaceInstance records from the API as a list.
        Unlike stream(), this operation is eager and will load `limit` records into
        memory before returning.

        :param unicode friendly_name: The friendly_name of the Workspace resources to read
        :param int limit: Upper limit for the number of records to return. list() guarantees
                          never to return more than limit.  Default is no limit
        :param int page_size: Number of records to fetch per request, when not set will use
                              the default value of 50 records.  If no page_size is defined
                              but a limit is defined, list() will attempt to read the limit
                              with the most efficient page size, i.e. min(limit, 1000)

        :returns: Generator that will yield up to limit results
        :rtype: list[rindap.rest.v1.workspace.WorkspaceInstance]
        """
        return list(self.stream(friendly_name=friendly_name, limit=limit, page_size=page_size, ))

    def page(self, friendly_name=values.unset, page_token=values.unset,
             page_number=values.unset, page_size=values.unset):
        """
        Retrieve a single page of WorkspaceInstance records from the API.
        Request is executed immediately

        :param unicode friendly_name: The friendly_name of the Workspace resources to read
        :param str page_token: PageToken provided by the API
        :param int page_number: Page Number, this value is simply for client state
        :param int page_size: Number of records to return, defaults to 50

        :returns: Page of WorkspaceInstance
        :rtype: rindap.rest.v1.workspace.WorkspacePage
        """
        data = values.of({
            'FriendlyName': friendly_name,
            'PageToken': page_token,
            'Page': page_number,
            'PageSize': page_size,
        })

        response = self._version.page(method='GET', uri=self._uri, params=data, )

        return WorkspacePage(self._version, response, self._solution)

    def get_page(self, target_url):
        """
        Retrieve a specific page of WorkspaceInstance records from the API.
        Request is executed immediately

        :param str target_url: API-generated URL for the requested results page

        :returns: Page of WorkspaceInstance
        :rtype: rindap.rest.v1.workspace.WorkspacePage
        """
        response = self._version.domain.rindap.request(
            'GET',
            target_url,
        )

        return WorkspacePage(self._version, response, self._solution)

    def create(self, friendly_name, event_callback_url=values.unset, event_callback_method='POST',
               default_activity='offline', timeout_activity='offline'):
        """
        Create the WorkspaceInstance

        :param unicode friendly_name: A string to describe the Workspace resource
        :param unicode event_callback_url: The URL we should call when an event occurs
        :param unicode event_callback_method:  The HTTP Request Method for calling the EventCallbackUrl
        :param unicode default_activity: The Activity that will be used when new Workers are created in the Workspace.
        :param timeout_activity: The Activity that will be assigned to a Worker when a Task reservation times out without a response

        :returns: The created WorkspaceInstance
        :rtype: rindap.rest.v1.workspace.WorkspaceInstance
        """
        data = values.of({
            'FriendlyName': friendly_name,
            'EventCallbackUrl': event_callback_url,
            'EventCallbackMethod': event_callback_method,
            'DefaultActivity': default_activity,
            'TimeoutActivity': timeout_activity
        })

        payload = self._version.create(method='POST', uri=self._uri, data=data, )

        return WorkspaceInstance(self._version, payload, )

    def get(self, sid):
        """
        Constructs a WorkspaceContext

        :param sid: The SID of the resource to fetch

        :returns: rindap.rest.v1.workspace.WorkspaceContext
        :rtype: rindap.rest.v1.workspace.WorkspaceContext
        """
        return WorkspaceContext(self._version, sid=sid, )

    def __call__(self, sid):
        """
        Constructs a WorkspaceContext

        :param sid: The SID of the resource to fetch

        :returns: rindap.rest.v1.workspace.WorkspaceContext
        :rtype: rindap.rest.v1.workspace.WorkspaceContext
        """
        return WorkspaceContext(self._version, sid=sid, )

    def __repr__(self):
        """
        Provide a friendly representation

        :returns: Machine friendly representation
        :rtype: str
        """
        return '<Rindap.Taskrouter.V1.WorkspaceList>'


class WorkspacePage(Page):
    """  """

    def __init__(self, version, response, solution):
        """
        Initialize the WorkspacePage

        :param Version version: Version that contains the resource
        :param Response response: Response from the API

        :returns: rindap.rest.v1.workspace.WorkspacePage
        :rtype: rindap.rest.v1.workspace.WorkspacePage
        """
        super(WorkspacePage, self).__init__(version, response)

        # Path Solution
        self._solution = solution

    def get_instance(self, payload):
        """
        Build an instance of WorkspaceInstance

        :param dict payload: Payload response from the API

        :returns: rindap.rest.v1.workspace.WorkspaceInstance
        :rtype: rindap.rest.v1.workspace.WorkspaceInstance
        """
        return WorkspaceInstance(self._version, payload, )

    def __repr__(self):
        """
        Provide a friendly representation

        :returns: Machine friendly representation
        :rtype: str
        """
        return '<Rindap.Taskrouter.V1.WorkspacePage>'


class WorkspaceContext(InstanceContext):
    """  """

    def __init__(self, version, sid):
        """
        Initialize the WorkspaceContext

        :param Version version: Version that contains the resource
        :param sid: The SID of the resource to fetch

        :returns: rindap.rest.v1.workspace.WorkspaceContext
        :rtype: rindap.rest.v1.workspace.WorkspaceContext
        """
        super(WorkspaceContext, self).__init__(version)

        # Path Solution
        self._solution = {'sid': sid, }
        self._uri = '/Workspaces/{sid}'.format(**self._solution)

        # Dependents
        self._tasks = None
        self._task_queues = None
        self._workers = None
        self._workflows = None
        self._rate_limit_profiles = None

    def fetch(self):
        """
        Fetch the WorkspaceInstance

        :returns: The fetched WorkspaceInstance
        :rtype: rindap.rest.v1.workspace.WorkspaceInstance
        """
        payload = self._version.fetch(method='GET', uri=self._uri, )

        return WorkspaceInstance(self._version, payload, sid=self._solution['sid'], )

    def update(self, default_activity=values.unset,
               event_callback_url=values.unset, event_callback_method=values.unset,
               friendly_name=values.unset,
               timeout_activity=values.unset):
        """
        Update the WorkspaceInstance

        :param unicode default_activity: The Name of the Activity that will be used when new Workers are created in the Workspace
        :param unicode event_callback_url: The URL we should call when an event occurs
        :param unicode events_filter: The list of Workspace events for which to call event_callback_url
        :param unicode friendly_name: A string to describe the Workspace resource
        :param bool multi_task_enabled: Whether multi-tasking is enabled
        :param unicode timeout_activity: The Name of the Activity that will be assigned to a Worker when a Task reservation times out without a response
        :param WorkspaceInstance.QueueOrder prioritize_queue_order: The type of TaskQueue to prioritize when Workers are receiving Tasks from both types of TaskQueues

        :returns: The updated WorkspaceInstance
        :rtype: rindap.rest.v1.workspace.WorkspaceInstance
        """
        data = values.of({
            'DefaultActivity': default_activity,
            'EventCallbackUrl': event_callback_url,
            'EventCallbackMethod': event_callback_method,
            'FriendlyName': friendly_name,
            'TimeoutActivity': timeout_activity,
        })

        payload = self._version.update(method='PUT', uri=self._uri, data=data, )

        return WorkspaceInstance(self._version, payload, sid=self._solution['sid'], )

    def delete(self):
        """
        Deletes the WorkspaceInstance

        :returns: True if delete succeeds, False otherwise
        :rtype: bool
        """
        return self._version.delete(method='DELETE', uri=self._uri, )

    @property
    def tasks(self):
        """
        Access the tasks

        :returns: rindap.rest.v1.workspace.task.TaskList
        :rtype: rindap.rest.v1.workspace.task.TaskList
        """
        if self._tasks is None:
            self._tasks = TaskList(self._version, workspace_sid=self._solution['sid'], )
        return self._tasks

    @property
    def task_queues(self):
        """
        Access the task_queues

        :returns: rindap.rest.v1.workspace.task_queue.TaskQueueList
        :rtype: rindap.rest.v1.workspace.task_queue.TaskQueueList
        """
        if self._task_queues is None:
            self._task_queues = TaskQueueList(self._version, workspace_sid=self._solution['sid'], )
        return self._task_queues

    @property
    def workers(self):
        """
        Access the workers

        :returns: rindap.rest.v1.workspace.worker.WorkerList
        :rtype: rindap.rest.v1.workspace.worker.WorkerList
        """
        if self._workers is None:
            self._workers = WorkerList(self._version, workspace_sid=self._solution['sid'], )
        return self._workers

    @property
    def workflows(self):
        """
        Access the workflows

        :returns: rindap.rest.v1.workspace.workflow.WorkflowList
        :rtype: rindap.rest.v1.workspace.workflow.WorkflowList
        """
        if self._workflows is None:
            self._workflows = WorkflowList(self._version, workspace_sid=self._solution['sid'], )
        return self._workflows

    @property
    def rate_limit_profiles(self):
        """
        Access the rate_limit_profiles

        :returns: rindap.rest.v1.workspace.workflow.RateLimitProfileList
        :rtype: rindap.rest.v1.workspace.workflow.RateLimitProfileList
        """

        if self._rate_limit_profiles is None:
            self._rate_limit_profiles = RateLimitProfileList(self._version, workspace_sid=self._solution['sid'], )
        return self._rate_limit_profiles

    def __repr__(self):
        """
        Provide a friendly representation

        :returns: Machine friendly representation
        :rtype: str
        """
        context = ' '.join('{}={}'.format(k, v) for k, v in self._solution.items())
        return '<Rindap.Taskrouter.V1.WorkspaceContext {}>'.format(context)


class WorkspaceInstance(InstanceResource):
    """  """

    class QueueOrder(object):
        FIFO = "FIFO"
        LIFO = "LIFO"

    def __init__(self, version, payload, sid=None):
        """
        Initialize the WorkspaceInstance

        :returns: rindap.rest.v1.workspace.WorkspaceInstance
        :rtype: rindap.rest.v1.workspace.WorkspaceInstance
        """
        super(WorkspaceInstance, self).__init__(version)

        # Marshaled Properties
        self._properties = {
            'account_sid': payload.get('account_sid'),
            'date_created': deserialize.iso8601_datetime(payload.get('date_created')),
            'date_updated': deserialize.iso8601_datetime(payload.get('date_updated')),
            'default_activity': payload.get('default_activity'),
            'event_callback_url': payload.get('event_callback_url'),
            'friendly_name': payload.get('friendly_name'),
            'sid': payload.get('sid'),
            'timeout_activity': payload.get('timeout_activity'),
            'url': payload.get('url'),
            'links': payload.get('links'),
        }

        # Context
        self._context = None
        self._solution = {'sid': sid or self._properties['sid'], }

    @property
    def _proxy(self):
        """
        Generate an instance context for the instance, the context is capable of
        performing various actions.  All instance actions are proxied to the context

        :returns: WorkspaceContext for this WorkspaceInstance
        :rtype: rindap.rest.v1.workspace.WorkspaceContext
        """
        if self._context is None:
            self._context = WorkspaceContext(self._version, sid=self._solution['sid'], )
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
    def default_activity(self):
        """
        :returns: The name of the default activity
        :rtype: unicode
        """
        return self._properties['default_activity']

    @property
    def event_callback_url(self):
        """
        :returns: The URL we call when an event occurs
        :rtype: unicode
        """
        return self._properties['event_callback_url']

    @property
    def friendly_name(self):
        """
        :returns: The string that you assigned to describe the Workspace resource
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
    def timeout_activity(self):
        """
        :returns: The name of the timeout activity
        :rtype: unicode
        """
        return self._properties['timeout_activity']

    @property
    def url(self):
        """
        :returns: The absolute URL of the Workspace resource
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
        Fetch the WorkspaceInstance

        :returns: The fetched WorkspaceInstance
        :rtype: rindap.rest.v1.workspace.WorkspaceInstance
        """
        return self._proxy.fetch()

    def update(self, default_activity=values.unset,
               event_callback_url=values.unset, events_filter=values.unset,
               friendly_name=values.unset, multi_task_enabled=values.unset,
               timeout_activity=values.unset,
               prioritize_queue_order=values.unset):
        """
        Update the WorkspaceInstance

        :param unicode default_activity: The Name of the Activity that will be used when new Workers are created in the Workspace
        :param unicode event_callback_url: The URL we should call when an event occurs
        :param unicode events_filter: The list of Workspace events for which to call event_callback_url
        :param unicode friendly_name: A string to describe the Workspace resource
        :param bool multi_task_enabled: Whether multi-tasking is enabled
        :param unicode timeout_activity: The Name of the Activity that will be assigned to a Worker when a Task reservation times out without a response
        :param WorkspaceInstance.QueueOrder prioritize_queue_order: The type of TaskQueue to prioritize when Workers are receiving Tasks from both types of TaskQueues

        :returns: The updated WorkspaceInstance
        :rtype: rindap.rest.v1.workspace.WorkspaceInstance
        """
        return self._proxy.update(
            default_activity=default_activity,
            event_callback_url=event_callback_url,
            events_filter=events_filter,
            friendly_name=friendly_name,
            multi_task_enabled=multi_task_enabled,
            timeout_activity=timeout_activity,
            prioritize_queue_order=prioritize_queue_order,
        )

    def delete(self):
        """
        Deletes the WorkspaceInstance

        :returns: True if delete succeeds, False otherwise
        :rtype: bool
        """
        return self._proxy.delete()

    @property
    def events(self):
        """
        Access the events

        :returns: rindap.rest.v1.workspace.event.EventList
        :rtype: rindap.rest.v1.workspace.event.EventList
        """
        return self._proxy.events

    @property
    def tasks(self):
        """
        Access the tasks

        :returns: rindap.rest.v1.workspace.task.TaskList
        :rtype: rindap.rest.v1.workspace.task.TaskList
        """
        return self._proxy.tasks

    @property
    def task_queues(self):
        """
        Access the task_queues

        :returns: rindap.rest.v1.workspace.task_queue.TaskQueueList
        :rtype: rindap.rest.v1.workspace.task_queue.TaskQueueList
        """
        return self._proxy.task_queues

    @property
    def workers(self):
        """
        Access the workers

        :returns: rindap.rest.v1.workspace.worker.WorkerList
        :rtype: rindap.rest.v1.workspace.worker.WorkerList
        """
        return self._proxy.workers

    @property
    def workflows(self):
        """
        Access the workflows

        :returns: rindap.rest.v1.workspace.workflow.WorkflowList
        :rtype: rindap.rest.v1.workspace.workflow.WorkflowList
        """
        return self._proxy.workflows

    def __repr__(self):
        """
        Provide a friendly representation

        :returns: Machine friendly representation
        :rtype: str
        """
        context = ' '.join('{}={}'.format(k, v) for k, v in self._solution.items())
        return '<Rindap.Taskrouter.V1.WorkspaceInstance {}>'.format(context)
