# -*- coding: utf-8 -*-

from plone import api
from plone.app.robotframework.testing import AUTOLOGIN_LIBRARY_FIXTURE
from plone.app.testing import FunctionalTesting
from plone.app.testing import IntegrationTesting
from plone.app.testing import PloneWithPackageLayer
from plone.app.testing import TEST_USER_ID
from plone.app.testing import applyProfile
from plone.app.testing import login
from plone.app.testing import setRoles
from plone.testing import z2

import cpskin.agenda


class CPSkinAgendaPloneWithPackageLayer(PloneWithPackageLayer):

    def setUpZope(self, app, configurationContext):
        self.loadZCML('testing.zcml', package=cpskin.agenda)
        z2.installProduct(app, 'Products.DateRecurringIndex')

    def tearDownZope(self, app):
        z2.uninstallProduct(app, 'Products.DateRecurringIndex')

    def setUpPloneSite(self, portal):
        portal.acl_users.userFolderAddUser('admin',
                                           'secret',
                                           ['Manager'],
                                           [])
        setRoles(portal, TEST_USER_ID, ['Manager'])
        login(portal, 'admin')
        portal.portal_workflow.setDefaultChain('one_state_workflow')
        applyProfile(portal, 'cpskin.agenda:testing')
        applyProfile(portal, 'plone.app.contenttypes:plone-content')
        api.content.create(
            type='Folder',
            id='folder',
            title='folder',
            container=portal)


CPSKIN_AGENDA_FIXTURE = CPSkinAgendaPloneWithPackageLayer(
    name='CPSKIN_AGENDA_FIXTURE',
    zcml_filename='testing.zcml',
    zcml_package=cpskin.agenda,
    gs_profile_id='cpskin.agenda:testing')

CPSKIN_AGENDA_INTEGRATION_TESTING = IntegrationTesting(
    bases=(CPSKIN_AGENDA_FIXTURE,),
    name='cpskin.agenda:Integration')

CPSKIN_AGENDA_ROBOT_TESTING = FunctionalTesting(
    bases=(CPSKIN_AGENDA_FIXTURE, AUTOLOGIN_LIBRARY_FIXTURE,
           z2.ZSERVER_FIXTURE),
    name='cpskin.agenda:Robot')
