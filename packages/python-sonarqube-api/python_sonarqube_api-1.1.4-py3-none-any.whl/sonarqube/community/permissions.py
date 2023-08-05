#!/usr/bin/env python
# -*- coding:utf-8 -*-
# @Author: Jialiang Shi
from sonarqube.utils.rest_client import RestClient
from sonarqube.utils.config import (
    API_PERMISSIONS_ADD_GROUP_ENDPOINT,
    API_PERMISSIONS_REMOVE_GROUP_ENDPOINT,
    API_PERMISSIONS_ADD_USER_ENDPOINT,
    API_PERMISSIONS_REMOVE_USER_ENDPOINT,
    API_PERMISSIONS_APPLY_TEMPLATE_ENDPOINT,
    API_PERMISSIONS_ADD_GROUP_TO_TEMPLATE_ENDPOINT,
    API_PERMISSIONS_REMOVE_GROUP_FROM_TEMPLATE_ENDPOINT,
    API_PERMISSIONS_ADD_PROJECT_CREATOR_TO_TEMPLATE_ENDPOINT,
    API_PERMISSIONS_REMOVE_PROJECT_CREATOR_FROM_TEMPLATE_ENDPOINT,
    API_PERMISSIONS_ADD_USER_TO_TEMPLATE_ENDPOINT,
    API_PERMISSIONS_REMOVE_USER_FROM_TEMPLATE_ENDPOINT,
    API_PERMISSIONS_BULK_APPLY_TEMPLATE_ENDPOINT,
    API_PERMISSIONS_CREATE_TEMPLATE_ENDPOINT,
    API_PERMISSIONS_DELETE_TEMPLATE_ENDPOINT,
    API_PERMISSIONS_SEARCH_TEMPLATES_ENDPOINT,
    API_PERMISSIONS_SET_DEFAULT_TEMPLATE_ENDPOINT,
    API_PERMISSIONS_UPDATE_TEMPLATE_ENDPOINT
)


class SonarQubePermissions(RestClient):
    """
    SonarQube permissions Operations
    """
    def __init__(self, **kwargs):
        """

        :param kwargs:
        """
        super(SonarQubePermissions, self).__init__(**kwargs)

    def add_permission_to_group(self, group_name, permission, project_key=None):
        """
        Add permission to a group.
        This service defaults to global permissions, but can be limited to project permissions by providing project key.
        The group name must be provided.

        :param group_name: Group name or 'anyone' (case insensitive)
        :param permission: Permission.
          Possible values are for:
            * Possible values for global permissions: admin, profileadmin, gateadmin, scan, provisioning
            * Possible values for project permissions admin, codeviewer, issueadmin, securityhotspotadmin, scan, user
        :param project_key: Project key
        :return:
        """
        params = {
            'groupName': group_name,
            'permission': permission
        }
        if project_key:
            params.update({"projectKey": project_key})

        self.post(API_PERMISSIONS_ADD_GROUP_ENDPOINT, params=params)

    def remove_permission_from_group(self, group_name, permission, project_key=None):
        """
        Remove a permission from a group.
        This service defaults to global permissions, but can be limited to project permissions by providing project key.
        The group name must be provided.

        :param group_name: Group name or 'anyone' (case insensitive)
        :param permission: Permission
          Possible values are for:
            * Possible values for global permissions: admin, profileadmin, gateadmin, scan, provisioning
            * Possible values for project permissions admin, codeviewer, issueadmin, securityhotspotadmin, scan, user
        :param project_key: Project key
        :return:
        """
        params = {
            'groupName': group_name,
            'permission': permission
        }
        if project_key:
            params.update({"projectKey": project_key})

        self.post(API_PERMISSIONS_REMOVE_GROUP_ENDPOINT, params=params)

    def add_permission_to_user(self, login, permission, project_key=None):
        """
        Add permission to a user.
        This service defaults to global permissions, but can be limited to project permissions by providing project key.

        :param login: User login
        :param permission: Permission
          Possible values are for:
            * Possible values for global permissions: admin, profileadmin, gateadmin, scan, provisioning
            * Possible values for project permissions admin, codeviewer, issueadmin, securityhotspotadmin, scan, user
        :param project_key: Project key
        :return:
        """
        params = {
            'login': login,
            'permission': permission
        }
        if project_key:
            params.update({"projectKey": project_key})

        self.post(API_PERMISSIONS_ADD_USER_ENDPOINT, params=params)

    def remove_permission_from_user(self, login, permission, project_key=None):
        """
        Remove permission from a user.
        This service defaults to global permissions, but can be limited to project permissions by providing project key.

        :param login: User login
        :param permission: Permission
          Possible values are for:
            * Possible values for global permissions: admin, profileadmin, gateadmin, scan, provisioning
            * Possible values for project permissions admin, codeviewer, issueadmin, securityhotspotadmin, scan, user
        :param project_key: Project key
        :return:
        """
        params = {
            'login': login,
            'permission': permission
        }
        if project_key:
            params.update({"projectKey": project_key})

        self.post(API_PERMISSIONS_REMOVE_USER_ENDPOINT, params=params)

    def apply_template_to_project(self, template_name, project_key):
        """
        Apply a permission template to one project.

        :param template_name: Template name
        :param project_key: Project key
        :return:
        """
        params = {
            'projectKey': project_key,
            'templateName': template_name
        }

        self.post(API_PERMISSIONS_APPLY_TEMPLATE_ENDPOINT, params=params)

    def apply_template_to_projects(self, template_name, projects=None, analyzedBefore=None, onProvisionedOnly=False,
                                   q=None, qualifiers="TRK"):
        """
        Apply a permission template to several projects.

        :param template_name: Template name
        :param projects: Comma-separated list of project keys
        :param analyzedBefore: Filter the projects for which last analysis is older than the given date (exclusive).
        :param onProvisionedOnly: Filter the projects that are provisioned.
          Possible values are for: True or False. default value is False.
        :param q: Limit search to:
          Possible values are for:
            * project names that contain the supplied string
            * project keys that are exactly the same as the supplied string
        :param qualifiers: Comma-separated list of component qualifiers. Filter the results with the specified
          qualifiers. Possible values are:
            * TRK - Projects
          default value is TRK.
        :return:
        """
        params = {
            'templateName': template_name,
            'qualifiers': qualifiers,
            'onProvisionedOnly': onProvisionedOnly and 'true' or 'false'
        }

        if projects:
            params.update({"projects": projects})

        if analyzedBefore:
            params.update({"analyzedBefore": analyzedBefore})

        if q:
            params.update({"q": q})

        self.post(API_PERMISSIONS_BULK_APPLY_TEMPLATE_ENDPOINT, params=params)

    def add_group_to_template(self, group_name, template_name, permission):
        """
        Add a group to a permission template.

        :param group_name: Group name or 'anyone' (case insensitive)
        :param template_name: Template name
        :param permission: Permission
          Possible values are for:
            * Possible values for project permissions admin, codeviewer, issueadmin, securityhotspotadmin, scan, user
        :return:
        """
        params = {
            'groupName': group_name,
            'templateName': template_name,
            'permission': permission
        }

        self.post(API_PERMISSIONS_ADD_GROUP_TO_TEMPLATE_ENDPOINT, params=params)

    def remove_group_from_template(self, group_name, template_name, permission):
        """
        Remove a group from a permission template.

        :param group_name: Group name or 'anyone' (case insensitive)
        :param template_name: Template name
        :param permission: Permission
          Possible values are for:
            * Possible values for project permissions admin, codeviewer, issueadmin, securityhotspotadmin, scan, user
        :return:
        """
        params = {
            'groupName': group_name,
            'templateName': template_name,
            'permission': permission
        }

        self.post(API_PERMISSIONS_REMOVE_GROUP_FROM_TEMPLATE_ENDPOINT, params=params)

    def add_project_creator_to_template(self, template_name, permission):
        """
        Add a project creator to a permission template.

        :param template_name: Template name
        :param permission: Permission
          Possible values are for:
            * Possible values for project permissions admin, codeviewer, issueadmin, securityhotspotadmin, scan, user
        :return:
        """
        params = {
            'templateName': template_name,
            'permission': permission
        }

        self.post(API_PERMISSIONS_ADD_PROJECT_CREATOR_TO_TEMPLATE_ENDPOINT, params=params)

    def remove_project_creator_from_template(self, template_name, permission):
        """
        Remove a project creator from a permission template.

        :param template_name: Template name
        :param permission: Permission
          Possible values are for:
            * Possible values for project permissions admin, codeviewer, issueadmin, securityhotspotadmin, scan, user
        :return:
        """
        params = {
            'templateName': template_name,
            'permission': permission
        }

        self.post(API_PERMISSIONS_REMOVE_PROJECT_CREATOR_FROM_TEMPLATE_ENDPOINT, params=params)

    def add_user_to_template(self, user_login, template_name, permission):
        """
        Add a user to a permission template.

        :param user_login: User login
        :param template_name: Template name
        :param permission: Permission
          Possible values are for:
            * Possible values for project permissions admin, codeviewer, issueadmin, securityhotspotadmin, scan, user
        :return:
        """
        params = {
            'login': user_login,
            'templateName': template_name,
            'permission': permission
        }

        self.post(API_PERMISSIONS_ADD_USER_TO_TEMPLATE_ENDPOINT, params=params)

    def remove_user_from_template(self, user_login, template_name, permission):
        """
        Remove a user from a permission template.

        :param user_login: User login
        :param template_name: Template name
        :param permission: Permission
          Possible values are for:
            * Possible values for project permissions admin, codeviewer, issueadmin, securityhotspotadmin, scan, user
        :return:
        """
        params = {
            'login': user_login,
            'templateName': template_name,
            'permission': permission
        }

        self.post(API_PERMISSIONS_REMOVE_USER_FROM_TEMPLATE_ENDPOINT, params=params)

    def create_template(self, template_name, description=None, pattern=None):
        """
        Create a permission template.

        :param template_name: Template name
        :param description: Template description
        :param pattern: Project key pattern. Must be a valid Java regular expression
        :return: request response.
        """
        params = {
            'name': template_name
        }

        if description:
            params.update({"description": description})

        if pattern:
            params.update({"projectKeyPattern": pattern})

        self.post(API_PERMISSIONS_CREATE_TEMPLATE_ENDPOINT, params=params)

    def delete_template(self, template_name):
        """
        Delete a permission template.

        :param template_name: Template name
        :return:
        """
        params = {
            'templateName': template_name
        }

        self.post(API_PERMISSIONS_DELETE_TEMPLATE_ENDPOINT, params=params)

    def search_templates(self, q=None):
        """
        List permission templates.

        :param q: Limit search to permission template names that contain the supplied string.
        :return: defaultTemplates, permissionTemplates, permissions
        """
        params = {}

        if q:
            params.update({"q": q})

        resp = self.get(API_PERMISSIONS_SEARCH_TEMPLATES_ENDPOINT, params=params)
        response = resp.json()
        return response

    def set_default_template(self, template_name, qualifier="TRK"):
        """
        Set a permission template as default.

        :param template_name: Template name
        :param qualifier: Project qualifier. Filter the results with the specified qualifier.
          Possible values are:
            * TRK - Projects
          default value is TRK.
        :return:
        """
        params = {
            'templateName': template_name,
            'qualifier': qualifier
        }

        self.post(API_PERMISSIONS_SET_DEFAULT_TEMPLATE_ENDPOINT, params=params)

    def update_template(self, template_id, template_name=None, description=None, pattern=None):
        """
        Update a permission template.

        :param template_id: Template id
        :param template_name: Template name
        :param description: Template description
        :param pattern: Project key pattern. Must be a valid Java regular expression
        :return: request response
        """
        params = {
            'id': template_id
        }

        if template_name:
            params.update({"name": template_name})

        if description:
            params.update({"description": description})

        if pattern:
            params.update({"projectKeyPattern": pattern})

        return self.post(API_PERMISSIONS_UPDATE_TEMPLATE_ENDPOINT, params=params)
