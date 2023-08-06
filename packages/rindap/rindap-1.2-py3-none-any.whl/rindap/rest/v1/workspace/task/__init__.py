# coding=utf-8

from rindap.base import deserialize
from rindap.base import serialize
from rindap.base import values
from rindap.base.instance_context import InstanceContext
from rindap.base.instance_resource import InstanceResource
from rindap.base.list_resource import ListResource
from rindap.base.page import Page
from rindap.rest.v1.workspace.task.reservation import ReservationList


class TaskList(ListResource):
    """  """

    def __init__(self, version, workspace_sid):
        """
        Initialize the TaskList

        :param Version version: Version that contains the resource
        :param workspace_sid: The SID of the Workspace that contains the Task

        :returns: rindap.rest.v1.workspace.task.TaskList
        :rtype: rindap.rest.v1.workspace.task.TaskList
        """
        super(TaskList, self).__init__(version)

        # Path Solution
        self._solution = {'workspace_sid': workspace_sid, }
        self._uri = '/Workspaces/{workspace_sid}/Tasks'.format(**self._solution)

    def stream(self, priority=values.unset, assignment_status=values.unset,
               workflow_sid=values.unset, workflow_name=values.unset,
               evaluate_task_attributes=values.unset, ordering=values.unset,
               has_addons=values.unset, limit=None, page_size=None):
        """
        Streams TaskInstance records from the API as a generator stream.
        This operation lazily loads records as efficiently as possible until the limit
        is reached.
        The results are returned as a generator, so this operation is memory efficient.

        :param unicode priority: The priority value of the Tasks to read
        :param unicode assignment_status: Returns the list of all Tasks in the Workspace with the specified assignment_status
        :param unicode workflow_sid: The SID of the Workflow with the Tasks to read
        :param unicode workflow_name: The friendly name of the Workflow with the Tasks to read
        :param unicode evaluate_task_attributes: The task attributes of the Tasks to read
        :param unicode ordering: Controls the order of the Tasks returned
        :param bool has_addons: Whether to read Tasks with addons
        :param int limit: Upper limit for the number of records to return. stream()
                          guarantees to never return more than limit.  Default is no limit
        :param int page_size: Number of records to fetch per request, when not set will use
                              the default value of 50 records.  If no page_size is defined
                              but a limit is defined, stream() will attempt to read the
                              limit with the most efficient page size, i.e. min(limit, 1000)

        :returns: Generator that will yield up to limit results
        :rtype: list[rindap.rest.v1.workspace.task.TaskInstance]
        """
        limits = self._version.read_limits(limit, page_size)

        page = self.page(
            priority=priority,
            assignment_status=assignment_status,
            workflow_sid=workflow_sid,
            workflow_name=workflow_name,
            evaluate_task_attributes=evaluate_task_attributes,
            ordering=ordering,
            has_addons=has_addons,
            page_size=limits['page_size'],
        )

        return self._version.stream(page, limits['limit'], limits['page_limit'])

    def list(self, priority=values.unset, assignment_status=values.unset,
             workflow_sid=values.unset, workflow_name=values.unset,
             evaluate_task_attributes=values.unset, ordering=values.unset,
             has_addons=values.unset, limit=None, page_size=None):
        """
        Lists TaskInstance records from the API as a list.
        Unlike stream(), this operation is eager and will load `limit` records into
        memory before returning.

        :param unicode priority: The priority value of the Tasks to read
        :param unicode assignment_status: Returns the list of all Tasks in the Workspace with the specified assignment_status
        :param unicode workflow_sid: The SID of the Workflow with the Tasks to read
        :param unicode workflow_name: The friendly name of the Workflow with the Tasks to read
        :param unicode evaluate_task_attributes: The task attributes of the Tasks to read
        :param unicode ordering: Controls the order of the Tasks returned
        :param bool has_addons: Whether to read Tasks with addons
        :param int limit: Upper limit for the number of records to return. list() guarantees
                          never to return more than limit.  Default is no limit
        :param int page_size: Number of records to fetch per request, when not set will use
                              the default value of 50 records.  If no page_size is defined
                              but a limit is defined, list() will attempt to read the limit
                              with the most efficient page size, i.e. min(limit, 1000)

        :returns: Generator that will yield up to limit results
        :rtype: list[rindap.rest.v1.workspace.task.TaskInstance]
        """
        return list(self.stream(
            priority=priority,
            assignment_status=assignment_status,
            workflow_sid=workflow_sid,
            workflow_name=workflow_name,
            evaluate_task_attributes=evaluate_task_attributes,
            ordering=ordering,
            has_addons=has_addons,
            limit=limit,
            page_size=page_size,
        ))

    def page(self, priority=values.unset, assignment_status=values.unset,
             workflow_sid=values.unset, workflow_name=values.unset,
             evaluate_task_attributes=values.unset, ordering=values.unset,
             has_addons=values.unset, page_token=values.unset,
             page_number=values.unset, page_size=values.unset):
        """
        Retrieve a single page of TaskInstance records from the API.
        Request is executed immediately

        :param unicode priority: The priority value of the Tasks to read
        :param unicode assignment_status: Returns the list of all Tasks in the Workspace with the specified assignment_status
        :param unicode workflow_sid: The SID of the Workflow with the Tasks to read
        :param unicode workflow_name: The friendly name of the Workflow with the Tasks to read
        :param unicode evaluate_task_attributes: The task attributes of the Tasks to read
        :param unicode ordering: Controls the order of the Tasks returned
        :param bool has_addons: Whether to read Tasks with addons
        :param str page_token: PageToken provided by the API
        :param int page_number: Page Number, this value is simply for client state
        :param int page_size: Number of records to return, defaults to 50

        :returns: Page of TaskInstance
        :rtype: rindap.rest.v1.workspace.task.TaskPage
        """
        data = values.of({
            'Priority': priority,
            'AssignmentStatus': serialize.map(assignment_status, lambda e: e),
            'WorkflowSid': workflow_sid,
            'WorkflowName': workflow_name,
            'EvaluateTaskAttributes': evaluate_task_attributes,
            'Ordering': ordering,
            'HasAddons': has_addons,
            'PageToken': page_token,
            'Page': page_number,
            'PageSize': page_size,
        })

        response = self._version.page(method='GET', uri=self._uri, params=data, )

        return TaskPage(self._version, response, self._solution)

    def get_page(self, target_url):
        """
        Retrieve a specific page of TaskInstance records from the API.
        Request is executed immediately

        :param str target_url: API-generated URL for the requested results page

        :returns: Page of TaskInstance
        :rtype: rindap.rest.v1.workspace.task.TaskPage
        """
        response = self._version.domain.rindap.request(
            'GET',
            target_url,
        )

        return TaskPage(self._version, response, self._solution)

    def create(self, timeout=values.unset, priority=values.unset, workflow_sid=values.unset,
               attributes=values.unset):
        """
        Create the TaskInstance

        :param unicode timeout: The amount of time in seconds the task is allowed to live
        :param unicode priority: The priority to assign the new task and override the default
        :param unicode workflow_sid: The SID of the Workflow that you would like to handle routing for the new Task
        :param unicode attributes: A URL-encoded JSON string describing the attributes of the task

        :returns: The created TaskInstance
        :rtype: rindap.rest.v1.workspace.task.TaskInstance
        """
        data = values.of({
            'Timeout': timeout,
            'Priority': priority,
            'WorkflowSid': workflow_sid,
            'Attributes': attributes,
        })

        payload = self._version.create(method='POST', uri=self._uri, data=data, )

        return TaskInstance(self._version, payload, workspace_sid=self._solution['workspace_sid'], )

    def get(self, sid):
        """
        Constructs a TaskContext

        :param sid: The SID of the resource to fetch

        :returns: rindap.rest.v1.workspace.task.TaskContext
        :rtype: rindap.rest.v1.workspace.task.TaskContext
        """
        return TaskContext(self._version, workspace_sid=self._solution['workspace_sid'], sid=sid, )

    def __call__(self, sid):
        """
        Constructs a TaskContext

        :param sid: The SID of the resource to fetch

        :returns: rindap.rest.v1.workspace.task.TaskContext
        :rtype: rindap.rest.v1.workspace.task.TaskContext
        """
        return TaskContext(self._version, workspace_sid=self._solution['workspace_sid'], sid=sid, )

    def __repr__(self):
        """
        Provide a friendly representation

        :returns: Machine friendly representation
        :rtype: str
        """
        return '<Rindap.V1.TaskList>'


class TaskPage(Page):
    """  """

    def __init__(self, version, response, solution):
        """
        Initialize the TaskPage

        :param Version version: Version that contains the resource
        :param Response response: Response from the API
        :param workspace_sid: The SID of the Workspace that contains the Task

        :returns: rindap.rest.v1.workspace.task.TaskPage
        :rtype: rindap.rest.v1.workspace.task.TaskPage
        """
        super(TaskPage, self).__init__(version, response)

        # Path Solution
        self._solution = solution

    def get_instance(self, payload):
        """
        Build an instance of TaskInstance

        :param dict payload: Payload response from the API

        :returns: rindap.rest.v1.workspace.task.TaskInstance
        :rtype: rindap.rest.v1.workspace.task.TaskInstance
        """
        return TaskInstance(self._version, payload, workspace_sid=self._solution['workspace_sid'], )

    def __repr__(self):
        """
        Provide a friendly representation

        :returns: Machine friendly representation
        :rtype: str
        """
        return '<Rindap.V1.TaskPage>'


class TaskContext(InstanceContext):
    """  """

    def __init__(self, version, workspace_sid, sid):
        """
        Initialize the TaskContext

        :param Version version: Version that contains the resource
        :param workspace_sid: The SID of the Workspace with the Task to fetch
        :param sid: The SID of the resource to fetch

        :returns: rindap.rest.v1.workspace.task.TaskContext
        :rtype: rindap.rest.v1.workspace.task.TaskContext
        """
        super(TaskContext, self).__init__(version)

        # Path Solution
        self._solution = {'workspace_sid': workspace_sid, 'sid': sid, }
        self._uri = '/Workspaces/{workspace_sid}/Tasks/{sid}'.format(**self._solution)

        # Dependents
        self._reservations = None

    def fetch(self):
        """
        Fetch the TaskInstance

        :returns: The fetched TaskInstance
        :rtype: rindap.rest.v1.workspace.task.TaskInstance
        """
        payload = self._version.fetch(method='GET', uri=self._uri, )

        return TaskInstance(
            self._version,
            payload,
            workspace_sid=self._solution['workspace_sid'],
            sid=self._solution['sid'],
        )

    def update(self, attributes=values.unset, assignment_status=values.unset,
               reason=values.unset, priority=values.unset):
        """
        Update the TaskInstance

        :param unicode attributes: The JSON string that describes the custom attributes of the task
        :param TaskInstance.Status assignment_status: The new status of the task
        :param unicode reason: The reason that the Task was canceled or complete
        :param unicode priority: The Task's new priority value

        :returns: The updated TaskInstance
        :rtype: rindap.rest.v1.workspace.task.TaskInstance
        """
        data = values.of({
            'Attributes': attributes,
            'AssignmentStatus': assignment_status,
            'Reason': reason,
            'Priority': priority,
        })

        payload = self._version.update(method='PUT', uri=self._uri, data=data, )

        return TaskInstance(
            self._version,
            payload,
            workspace_sid=self._solution['workspace_sid'],
            sid=self._solution['sid'],
        )

    def delete(self):
        """
        Deletes the TaskInstance

        :returns: True if delete succeeds, False otherwise
        :rtype: bool
        """
        return self._version.delete(method='DELETE', uri=self._uri, )

    @property
    def reservations(self):
        """
        Access the reservations

        :returns: rindap.rest.v1.workspace.task.reservation.ReservationList
        :rtype: rindap.rest.v1.workspace.task.reservation.ReservationList
        """
        if self._reservations is None:
            self._reservations = ReservationList(
                self._version,
                workspace_sid=self._solution['workspace_sid'],
                task_sid=self._solution['sid'],
            )
        return self._reservations

    def __repr__(self):
        """
        Provide a friendly representation

        :returns: Machine friendly representation
        :rtype: str
        """
        context = ' '.join('{}={}'.format(k, v) for k, v in self._solution.items())
        return '<Rindap.V1.TaskContext {}>'.format(context)


class TaskInstance(InstanceResource):
    """  """

    class Status(object):
        PENDING = "pending"
        AWAITING_RESERVATION = "awaiting_reservation"
        RESERVED = "reserved"
        ASSIGNED = "assigned"
        CANCELED = "canceled"
        POSTPONED = "postponed"
        COMPLETED = "completed"

    def __init__(self, version, payload, workspace_sid, sid=None):
        """
        Initialize the TaskInstance

        :returns: rindap.rest.v1.workspace.task.TaskInstance
        :rtype: rindap.rest.v1.workspace.task.TaskInstance
        """
        super(TaskInstance, self).__init__(version)

        # Marshaled Properties
        self._properties = {
            'account_sid': payload.get('account_sid'),
            'age': deserialize.integer(payload.get('age')),
            'assignment_status': payload.get('assignment_status'),
            'attributes': payload.get('attributes'),
            'addons': payload.get('addons'),
            'date_created': deserialize.iso8601_datetime(payload.get('date_created')),
            'date_updated': deserialize.iso8601_datetime(payload.get('date_updated')),
            'priority': deserialize.integer(payload.get('priority')),
            'reason': payload.get('reason'),
            'sid': payload.get('sid'),
            'timeout': deserialize.integer(payload.get('timeout')),
            'workflow_sid': payload.get('workflow_sid'),
            'workflow_friendly_name': payload.get('workflow_friendly_name'),
            'workspace_sid': payload.get('workspace_sid'),
            'url': payload.get('url'),
            'links': payload.get('links'),
            'forked_from': payload.get('forked_from'),
            'postponed_till': deserialize.iso8601_datetime(payload.get('postponed_till')),
            'postponing_reason': payload.get('postponing_reason'),
            'loop_retries_left': deserialize.integer(payload.get('loop_retries_left')),
        }

        # Context
        self._context = None
        self._solution = {'workspace_sid': workspace_sid, 'sid': sid or self._properties['sid'], }

    @property
    def _proxy(self):
        """
        Generate an instance context for the instance, the context is capable of
        performing various actions.  All instance actions are proxied to the context

        :returns: TaskContext for this TaskInstance
        :rtype: rindap.rest.v1.workspace.task.TaskContext
        """
        if self._context is None:
            self._context = TaskContext(
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
    def age(self):
        """
        :returns: The number of seconds since the Task was created
        :rtype: unicode
        """
        return self._properties['age']

    @property
    def assignment_status(self):
        """
        :returns: The current status of the Task's assignment
        :rtype: TaskInstance.Status
        """
        return self._properties['assignment_status']

    @property
    def attributes(self):
        """
        :returns: The JSON string with custom attributes of the work
        :rtype: unicode
        """
        return self._properties['attributes']

    @property
    def addons(self):
        """
        :returns: An object that contains the addon data for all installed addons
        :rtype: unicode
        """
        return self._properties['addons']

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
    def priority(self):
        """
        :returns: Retrieve the list of all Tasks in the Workspace with the specified priority
        :rtype: unicode
        """
        return self._properties['priority']

    @property
    def reason(self):
        """
        :returns: The reason the Task was canceled or completed
        :rtype: unicode
        """
        return self._properties['reason']

    @property
    def sid(self):
        """
        :returns: The unique string that identifies the resource
        :rtype: unicode
        """
        return self._properties['sid']

    @property
    def timeout(self):
        """
        :returns: The amount of time in seconds that the Task is allowed to live
        :rtype: unicode
        """
        return self._properties['timeout']

    @property
    def workflow_sid(self):
        """
        :returns: The SID of the Workflow that is controlling the Task
        :rtype: unicode
        """
        return self._properties['workflow_sid']

    @property
    def workflow_friendly_name(self):
        """
        :returns: The friendly name of the Workflow that is controlling the Task
        :rtype: unicode
        """
        return self._properties['workflow_friendly_name']

    @property
    def workspace_sid(self):
        """
        :returns: The SID of the Workspace that contains the Task
        :rtype: unicode
        """
        return self._properties['workspace_sid']

    @property
    def url(self):
        """
        :returns: The absolute URL of the Task resource
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

    @property
    def forked_from(self):
        """
        :returns: The SID of the Parent Task
        :rtype: unicode
        """
        return self._properties['forked_from']

    @property
    def postponed_till(self):
        """
        :returns: The date and time in GMT, till the task is postponed
        :rtype: datetime
        """
        return self._properties['postponed_till']

    @property
    def postponing_reason(self):
        """
        :returns: The explanation of the reason for postponing
        :rtype: unicode
        """
        return self._properties['postponing_reason']

    @property
    def loop_retries_left(self):
        """
        :returns: The number of retries left for the current Loop Filter in the Workflow
        :rtype: number
        """
        return self._properties['loop_retries_left']

    def fetch(self):
        """
        Fetch the TaskInstance

        :returns: The fetched TaskInstance
        :rtype: rindap.rest.v1.workspace.task.TaskInstance
        """
        return self._proxy.fetch()

    def update(self, attributes=values.unset, assignment_status=values.unset,
               reason=values.unset, priority=values.unset):
        """
        Update the TaskInstance

        :param unicode attributes: The JSON string that describes the custom attributes of the task
        :param TaskInstance.Status assignment_status: The new status of the task
        :param unicode reason: The reason that the Task was canceled or complete
        :param unicode priority: The Task's new priority value

        :returns: The updated TaskInstance
        :rtype: rindap.rest.v1.workspace.task.TaskInstance
        """
        return self._proxy.update(
            attributes=attributes,
            assignment_status=assignment_status,
            reason=reason,
            priority=priority,
        )

    def delete(self):
        """
        Deletes the TaskInstance

        :returns: True if delete succeeds, False otherwise
        :rtype: bool
        """
        return self._proxy.delete()

    @property
    def reservations(self):
        """
        Access the reservations

        :returns: rindap.rest.v1.workspace.task.reservation.ReservationList
        :rtype: rindap.rest.v1.workspace.task.reservation.ReservationList
        """
        return self._proxy.reservations

    def __repr__(self):
        """
        Provide a friendly representation

        :returns: Machine friendly representation
        :rtype: str
        """
        context = ' '.join('{}={}'.format(k, v) for k, v in self._solution.items())
        return '<Rindap.V1.TaskInstance {}>'.format(context)
