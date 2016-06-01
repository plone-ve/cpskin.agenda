# -*- coding: utf-8 -*-
from cpskin.agenda.behaviors.related_contacts import IRelatedContacts
from cpskin.agenda.interfaces import ICPSkinAgendaLayer
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
        alsoProvides(self.request, ICPSkinAgendaLayer)
        setRoles(self.portal, TEST_USER_ID, ['Manager'])

    def test_only_one_attendees_field(self):
        fti = queryUtility(IDexterityFTI, name='Event')
        event_behaviors = ['plone.app.event.dx.behaviors.IEventAttendees',
                           'plone.app.event.dx.behaviors.IEventLocation',
                           'plone.app.event.dx.behaviors.IEventContact'
                           ]

        behaviors = list(fti.behaviors)

        for event_behavior in event_behaviors:
            self.assertIn(event_behavior, behaviors)

        add_behavior('Event', IRelatedContacts.__identifier__)

        behaviors = list(fti.behaviors)
        for event_behavior in event_behaviors:
            self.assertNotIn(event_behavior, behaviors)

        remove_behavior('Event', IRelatedContacts.__identifier__)

        behaviors = list(fti.behaviors)
        for event_behavior in event_behaviors:
            self.assertIn(event_behavior, behaviors)
