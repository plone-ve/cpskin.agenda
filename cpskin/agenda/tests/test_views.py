# -*- coding: utf-8 -*-
from cpskin.agenda.behaviors.related_contacts import IRelatedContacts
from cpskin.agenda.interfaces import ICPSkinAgendaLayer
from cpskin.agenda.testing import CPSKIN_AGENDA_INTEGRATION_TESTING
from cpskin.core.utils import add_behavior
from plone import api
from plone.app.event.dx.behaviors import IEventBasic
from plone.app.testing import TEST_USER_ID, setRoles
from zope.component import getMultiAdapter
from zope.interface import directlyProvides

import datetime
import unittest


class TestViews(unittest.TestCase):

    layer = CPSKIN_AGENDA_INTEGRATION_TESTING

    def setUp(self):
        self.portal = self.layer['portal']
        self.request = self.layer['request']
        setRoles(self.portal, TEST_USER_ID, ['Manager'])
        directlyProvides(self.request, ICPSkinAgendaLayer)

    def test_event_with_related_contacts_behavior_view(self):
        timezone = 'Europe/Brussels'
        now = datetime.datetime.now()
        add_behavior('Event', IRelatedContacts.__identifier__)
        event = api.content.create(
            container=self.portal,
            type='Event',
            id='event')
        event.timezone = timezone
        eventbasic = IEventBasic(event)
        eventbasic.start = datetime.datetime(now.year, now.month, now.day, 18)
        eventbasic.end = datetime.datetime(now.year, now.month, now.day, 21)
        event.reindexObject()

        view = getMultiAdapter(
            (event, self.request), name='event_summary')
