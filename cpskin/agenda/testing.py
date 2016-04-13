# -*- coding: utf-8 -*-

from plone.testing import z2
from plone.app.testing import applyProfile
from plone.app.testing import FunctionalTesting
from plone.app.testing import IntegrationTesting
from plone.app.testing import PloneWithPackageLayer
from plone.app.robotframework.testing import AUTOLOGIN_LIBRARY_FIXTURE

import cpskin.agenda


class CPSkinAgendaPloneWithPackageLayer(PloneWithPackageLayer):
    """
    """

    def setUpPloneSite(self, portal):
        applyProfile(portal, 'cpskin.agenda:testing')


CPSKIN_AGENDA_FIXTURE = CPSkinAgendaPloneWithPackageLayer(
    name="CPSKIN_AGENDA_FIXTURE",
    zcml_filename="testing.zcml",
    zcml_package=cpskin.agenda,
    gs_profile_id="cpskin.agenda:testing")

CPSKIN_AGENDA_INTEGRATION_TESTING = IntegrationTesting(
    bases=(CPSKIN_AGENDA_FIXTURE,),
    name="cpskin.agenda:Integration")

CPSKIN_AGENDA_ROBOT_TESTING = FunctionalTesting(
    bases=(CPSKIN_AGENDA_FIXTURE, AUTOLOGIN_LIBRARY_FIXTURE,
           z2.ZSERVER_FIXTURE),
    name="cpskin.agenda:Robot")
