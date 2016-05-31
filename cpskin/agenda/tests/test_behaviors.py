# -*- coding: utf-8 -*-
from cpskin.agenda.behaviors.related_contacts import IRelatedContacts
from cpskin.core.interfaces import ICPSkinCoreLayer
from cpskin.agenda.testing import CPSKIN_AGENDA_INTEGRATION_TESTING
from cpskin.core.utils import add_behavior
from cpskin.core.utils import remove_behavior
from plone.app.testing import TEST_USER_ID
from plone.app.testing import setRoles
from zope.interface import alsoProvides
from plone.dexterity.interfaces import IDexterityFTI
from zope.component import queryUtility

import unittest


class TestBehaviors(unittest.TestCase):

    layer = CPSKIN_AGENDA_INTEGRATION_TESTING

    def setUp(self):
        self.portal = self.layer['portal']
        self.request = self.layer['request']
        alsoProvides(self.request, ICPSkinCoreLayer)
        setRoles(self.portal, TEST_USER_ID, ['Manager'])

    def test_only_one_attendees_field(self):
        fti = queryUtility(IDexterityFTI, name='Event')
        behaviors = list(fti.behaviors)
        self.assertIn(
            'plone.app.event.dx.behaviors.IEventAttendees', behaviors)

        add_behavior('Event', IRelatedContacts.__identifier__)

        behaviors = list(fti.behaviors)
        self.assertNotIn(
            'plone.app.event.dx.behaviors.IEventAttendees', behaviors)

        remove_behavior('Event', IRelatedContacts.__identifier__)

        behaviors = list(fti.behaviors)
        self.assertIn(
            'plone.app.event.dx.behaviors.IEventAttendees', behaviors)
