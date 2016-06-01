# -*- coding: utf-8 -*-
from cpskin.agenda.behaviors.related_contacts import IRelatedContacts
from cpskin.agenda.interfaces import ICPSkinAgendaLayer
from cpskin.agenda.testing import CPSKIN_AGENDA_INTEGRATION_TESTING
from cpskin.core.utils import add_behavior
from plone import api
from plone.app.event.dx.behaviors import IEventBasic
from plone.app.testing import applyProfile
from plone.app.testing import TEST_USER_ID, setRoles
from zope.component import getMultiAdapter
from zope.component import getUtility
from zope.interface import directlyProvides
from zope.intid.interfaces import IIntIds
from z3c.relationfield.relation import RelationValue

import datetime
import unittest


class TestViews(unittest.TestCase):

    layer = CPSKIN_AGENDA_INTEGRATION_TESTING

    def setUp(self):
        self.portal = self.layer['portal']
        self.request = self.layer['request']
        setRoles(self.portal, TEST_USER_ID, ['Manager'])
        directlyProvides(self.request, ICPSkinAgendaLayer)
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
        self.assertNotIn("partners", view())

        # add some contacts
        applyProfile(self.portal, 'collective.contact.core:default')
        directory_person = api.content.create(
            container=self.portal, type='directory', id='directory-person')
        person = api.content.create(
            container=directory_person, type='person', id='person')
        person.firstname = u'Foo'
        person.lastname = u'Bar'
        person.gender = u'F'
        person.street = u'Zoning Industriel'
        person.number = u'34'
        person.zip_code = u'5190'
        person.city = u'Mornimont'

        # set related contact
        intids = getUtility(IIntIds)
        to_id = intids.getId(person)
        rv = RelationValue(to_id)
        event.partners = [rv]
        self.assertIn("partners", view())

        directory_organization = api.content.create(
            container=self.portal, type='directory', id='directory-organization')
        import ipdb;ipdb.set_trace()
        organization = api.content.create(
            container=directory_organization, type='organization', id='organization')
        organization.Title = u'Foo'
