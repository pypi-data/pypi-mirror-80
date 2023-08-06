# coding=utf-8

from rindap.base.version import Version
from rindap.rest.v1.workspace import WorkspaceList


class V1(Version):

    def __init__(self, domain):
        """
        Initialize the V1 version of Rindap

        :returns: V1 version of Rindap
        :rtype: rindap.rest.v1.V1.V1
        """
        super(V1, self).__init__(domain)
        self.version = 'v1'
        self._workspaces = None

    @property
    def workspaces(self):
        """
        :rtype: rindap.rest.v1.workspace.WorkspaceList
        """
        if self._workspaces is None:
            self._workspaces = WorkspaceList(self)
        return self._workspaces

    def __repr__(self):
        """
        Provide a friendly representation

        :returns: Machine friendly representation
        :rtype: str
        """
        return '<Rindap.V1>'
