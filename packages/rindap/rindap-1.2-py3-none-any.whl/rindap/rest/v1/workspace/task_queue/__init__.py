# coding=utf-8

from rindap.base import deserialize
from rindap.base import values
from rindap.base.instance_context import InstanceContext
from rindap.base.instance_resource import InstanceResource
from rindap.base.list_resource import ListResource
from rindap.base.page import Page


class TaskQueueList(ListResource):
    """  """

    def __init__(self, version, workspace_sid):
        """
        Initialize the TaskQueueList

        :param Version version: Version that contains the resource
        :param workspace_sid: The SID of the Workspace that contains the TaskQueue

        :returns: rindap.rest.v1.workspace.task_queue.TaskQueueList
        :rtype: rindap.rest.v1.workspace.task_queue.TaskQueueList
        """
        super(TaskQueueList, self).__init__(version)

        # Path Solution
        self._solution = {'workspace_sid': workspace_sid, }
        self._uri = '/Workspaces/{workspace_sid}/TaskQueues'.format(**self._solution)

    def stream(self, friendly_name=values.unset,
               evaluate_worker_attributes=values.unset, worker_sid=values.unset,
               limit=None, page_size=None):
        """
        Streams TaskQueueInstance records from the API as a generator stream.
        This operation lazily loads records as efficiently as possible until the limit
        is reached.
        The results are returned as a generator, so this operation is memory efficient.

        :param unicode friendly_name: The friendly_name of the TaskQueue resources to read
        :param unicode evaluate_worker_attributes: The attributes of the Workers to read
        :param unicode worker_sid: The SID of the Worker with the TaskQueue resources to read
        :param int limit: Upper limit for the number of records to return. stream()
                          guarantees to never return more than limit.  Default is no limit
        :param int page_size: Number of records to fetch per request, when not set will use
                              the default value of 50 records.  If no page_size is defined
                              but a limit is defined, stream() will attempt to read the
                              limit with the most efficient page size, i.e. min(limit, 1000)

        :returns: Generator that will yield up to limit results
        :rtype: list[rindap.rest.v1.workspace.task_queue.TaskQueueInstance]
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
        Lists TaskQueueInstance records from the API as a list.
        Unlike stream(), this operation is eager and will load `limit` records into
        memory before returning.

        :param unicode friendly_name: The friendly_name of the TaskQueue resources to read
        :param unicode evaluate_worker_attributes: The attributes of the Workers to read
        :param unicode worker_sid: The SID of the Worker with the TaskQueue resources to read
        :param int limit: Upper limit for the number of records to return. list() guarantees
                          never to return more than limit.  Default is no limit
        :param int page_size: Number of records to fetch per request, when not set will use
                              the default value of 50 records.  If no page_size is defined
                              but a limit is defined, list() will attempt to read the limit
                              with the most efficient page size, i.e. min(limit, 1000)

        :returns: Generator that will yield up to limit results
        :rtype: list[rindap.rest.v1.workspace.task_queue.TaskQueueInstance]
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
        Retrieve a single page of TaskQueueInstance records from the API.
        Request is executed immediately

        :param unicode friendly_name: The friendly_name of the TaskQueue resources to read
        :param unicode evaluate_worker_attributes: The attributes of the Workers to read
        :param unicode worker_sid: The SID of the Worker with the TaskQueue resources to read
        :param str page_token: PageToken provided by the API
        :param int page_number: Page Number, this value is simply for client state
        :param int page_size: Number of records to return, defaults to 50

        :returns: Page of TaskQueueInstance
        :rtype: rindap.rest.v1.workspace.task_queue.TaskQueuePage
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

        return TaskQueuePage(self._version, response, self._solution)

    def get_page(self, target_url):
        """
        Retrieve a specific page of TaskQueueInstance records from the API.
        Request is executed immediately

        :param str target_url: API-generated URL for the requested results page

        :returns: Page of TaskQueueInstance
        :rtype: rindap.rest.v1.workspace.task_queue.TaskQueuePage
        """
        response = self._version.domain.rindap.request(
            'GET',
            target_url,
        )

        return TaskQueuePage(self._version, response, self._solution)

    def create(self, friendly_name):
        """
        Create the TaskQueueInstance

        :param unicode friendly_name: A string to describe the resource

        :returns: The created TaskQueueInstance
        :rtype: rindap.rest.v1.workspace.task_queue.TaskQueueInstance
        """
        data = values.of({
            'FriendlyName': friendly_name
        })

        payload = self._version.create(method='POST', uri=self._uri, data=data, )

        return TaskQueueInstance(self._version, payload, workspace_sid=self._solution['workspace_sid'], )

    def get(self, sid):
        """
        Constructs a TaskQueueContext

        :param sid: The SID of the resource to

        :returns: rindap.rest.v1.workspace.task_queue.TaskQueueContext
        :rtype: rindap.rest.v1.workspace.task_queue.TaskQueueContext
        """
        return TaskQueueContext(self._version, workspace_sid=self._solution['workspace_sid'], sid=sid, )

    def __call__(self, sid):
        """
        Constructs a TaskQueueContext

        :param sid: The SID of the resource to

        :returns: rindap.rest.v1.workspace.task_queue.TaskQueueContext
        :rtype: rindap.rest.v1.workspace.task_queue.TaskQueueContext
        """
        return TaskQueueContext(self._version, workspace_sid=self._solution['workspace_sid'], sid=sid, )

    def __repr__(self):
        """
        Provide a friendly representation

        :returns: Machine friendly representation
        :rtype: str
        """
        return '<Rindap.V1.TaskQueueList>'


class TaskQueuePage(Page):
    """  """

    def __init__(self, version, response, solution):
        """
        Initialize the TaskQueuePage

        :param Version version: Version that contains the resource
        :param Response response: Response from the API
        :param workspace_sid: The SID of the Workspace that contains the TaskQueue

        :returns: rindap.rest.v1.workspace.task_queue.TaskQueuePage
        :rtype: rindap.rest.v1.workspace.task_queue.TaskQueuePage
        """
        super(TaskQueuePage, self).__init__(version, response)

        # Path Solution
        self._solution = solution

    def get_instance(self, payload):
        """
        Build an instance of TaskQueueInstance

        :param dict payload: Payload response from the API

        :returns: rindap.rest.v1.workspace.task_queue.TaskQueueInstance
        :rtype: rindap.rest.v1.workspace.task_queue.TaskQueueInstance
        """
        return TaskQueueInstance(self._version, payload, workspace_sid=self._solution['workspace_sid'], )

    def __repr__(self):
        """
        Provide a friendly representation

        :returns: Machine friendly representation
        :rtype: str
        """
        return '<Rindap.V1.TaskQueuePage>'


class TaskQueueContext(InstanceContext):
    """  """

    def __init__(self, version, workspace_sid, sid):
        """
        Initialize the TaskQueueContext

        :param Version version: Version that contains the resource
        :param workspace_sid: The SID of the Workspace with the TaskQueue to fetch
        :param sid: The SID of the resource to

        :returns: rindap.rest.v1.workspace.task_queue.TaskQueueContext
        :rtype: rindap.rest.v1.workspace.task_queue.TaskQueueContext
        """
        super(TaskQueueContext, self).__init__(version)

        # Path Solution
        self._solution = {'workspace_sid': workspace_sid, 'sid': sid, }
        self._uri = '/Workspaces/{workspace_sid}/TaskQueues/{sid}'.format(**self._solution)

    def fetch(self):
        """
        Fetch the TaskQueueInstance

        :returns: The fetched TaskQueueInstance
        :rtype: rindap.rest.v1.workspace.task_queue.TaskQueueInstance
        """
        payload = self._version.fetch(method='GET', uri=self._uri, )

        return TaskQueueInstance(
            self._version,
            payload,
            workspace_sid=self._solution['workspace_sid'],
            sid=self._solution['sid'],
        )

    def update(self, friendly_name=values.unset):
        """
        Update the TaskQueueInstance

        :param unicode friendly_name: A string to describe the resource

        :returns: The updated TaskQueueInstance
        :rtype: rindap.rest.v1.workspace.task_queue.TaskQueueInstance
        """
        data = values.of({
            'FriendlyName': friendly_name
        })

        payload = self._version.update(method='PUT', uri=self._uri, data=data, )

        return TaskQueueInstance(
            self._version,
            payload,
            workspace_sid=self._solution['workspace_sid'],
            sid=self._solution['sid'],
        )

    def delete(self):
        """
        Deletes the TaskQueueInstance

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
        return '<Rindap.V1.TaskQueueContext {}>'.format(context)


class TaskQueueInstance(InstanceResource):
    """  """

    def __init__(self, version, payload, workspace_sid, sid=None):
        """
        Initialize the TaskQueueInstance

        :returns: rindap.rest.v1.workspace.task_queue.TaskQueueInstance
        :rtype: rindap.rest.v1.workspace.task_queue.TaskQueueInstance
        """
        super(TaskQueueInstance, self).__init__(version)

        # Marshaled Properties
        self._properties = {
            'account_sid': payload.get('account_sid'),
            'date_created': deserialize.iso8601_datetime(payload.get('date_created')),
            'date_updated': deserialize.iso8601_datetime(payload.get('date_updated')),
            'friendly_name': payload.get('friendly_name'),
            'sid': payload.get('sid'),
            'url': payload.get('url'),
            'workspace_sid': payload.get('workspace_sid'),
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

        :returns: TaskQueueContext for this TaskQueueInstance
        :rtype: rindap.rest.v1.workspace.task_queue.TaskQueueContext
        """
        if self._context is None:
            self._context = TaskQueueContext(
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
    def url(self):
        """
        :returns: The absolute URL of the TaskQueue resource
        :rtype: unicode
        """
        return self._properties['url']

    @property
    def workspace_sid(self):
        """
        :returns: The SID of the Workspace that contains the TaskQueue
        :rtype: unicode
        """
        return self._properties['workspace_sid']

    @property
    def links(self):
        """
        :returns: The URLs of related resources
        :rtype: unicode
        """
        return self._properties['links']

    def fetch(self):
        """
        Fetch the TaskQueueInstance

        :returns: The fetched TaskQueueInstance
        :rtype: rindap.rest.v1.workspace.task_queue.TaskQueueInstance
        """
        return self._proxy.fetch()

    def update(self, friendly_name=values.unset):
        """
        Update the TaskQueueInstance

        :param unicode friendly_name: A string to describe the resource

        :returns: The updated TaskQueueInstance
        :rtype: rindap.rest.v1.workspace.task_queue.TaskQueueInstance
        """
        return self._proxy.update(
            friendly_name=friendly_name,
        )

    def delete(self):
        """
        Deletes the TaskQueueInstance

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
        return '<Rindap.V1.TaskQueueInstance {}>'.format(context)
