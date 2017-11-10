# -*- coding: utf-8 -*-
from collective.geo.behaviour.interfaces import ICoordinates
from collective.geo.geographer.interfaces import IGeoreferenced
from cpskin.agenda.behaviors.related_contacts import IRelatedContacts
from cpskin.agenda.interfaces import ICPSkinAgendaLayer
from cpskin.agenda.testing import CPSKIN_AGENDA_INTEGRATION_TESTING
from cpskin.core.utils import add_behavior
from cpskin.core.utils import remove_behavior
from plone import api
from plone.app.testing import applyProfile
from plone.app.testing import setRoles
from plone.app.testing import TEST_USER_ID
from plone.dexterity.interfaces import IDexterityFTI
from z3c.relationfield.relation import RelationValue
from zope.component import getMultiAdapter
from zope.component import getUtility
from zope.component import queryUtility
from zope.event import notify
from zope.interface import alsoProvides
from zope.intid.interfaces import IIntIds
from zope.lifecycleevent import ObjectModifiedEvent

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

    def test_override_geo_with_related_contact(self):
        add_behavior(
            'Event', 'cpskin.agenda.behaviors.related_contacts.IRelatedContacts')  # noqa
        add_behavior('Event', ICoordinates.__identifier__)
        event = api.content.create(
            container=self.portal,
            type='Event',
            id='myevent'
        )

        # add some contacts
        applyProfile(self.portal, 'collective.contact.core:default')
        add_behavior('organization', ICoordinates.__identifier__)
        directory = api.content.create(
            container=self.portal, type='directory', id='directory')
        organization = api.content.create(
            container=directory, type='organization', id='organization')
        organization.title = u'IMIO'
        organization.street = u'Rue Léon Morel'
        organization.number = u'1'
        organization.zip_code = u'5032'
        organization.city = u'Isnes'

        # set related contact
        intids = getUtility(IIntIds)
        to_id = intids.getId(organization)
        rv = RelationValue(to_id)
        event.location = rv
        notify(ObjectModifiedEvent(event))

        # coord = ICoordinates(event)
        view = getMultiAdapter((event, event.REQUEST), name='geoview')
        coord = view.getCoordinates()
        self.assertEqual(coord, (None, None))
        coordinates = ICoordinates(event).coordinates

        self.assertEqual(coordinates, u'')

        # check if event georeferenced is correct
        orga_geo = IGeoreferenced(organization)
        orga_geo.setGeoInterface('Point', (4.711178, 50.504827))
        notify(ObjectModifiedEvent(event))
        view = getMultiAdapter((event, event.REQUEST), name='geoview')
        coord = view.getCoordinates()
        self.assertEqual(coord, ('Point', (4.711178, 50.504827)))
        coordinates = ICoordinates(event).coordinates
        self.assertEqual(coordinates, 'POINT (4.711178 50.504827)')
