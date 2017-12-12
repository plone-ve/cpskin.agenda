# -*- coding: utf-8 -*-d
from collective.atomrss.interfaces import ICollectiveAtomrssLayer
from collective.geo.behaviour.interfaces import ICoordinates
from collective.geo.geographer.interfaces import IGeoreferenced
from cpskin.agenda.behaviors.related_contacts import IRelatedContacts
from cpskin.agenda.testing import CPSKIN_AGENDA_INTEGRATION_TESTING
from cpskin.core.utils import add_behavior
from persistent.dict import PersistentDict
from plone import api
from plone.app.testing import applyProfile
from plone.app.testing import setRoles
from plone.app.testing import TEST_USER_ID
from Products.CMFPlone.browser.syndication.settings import FEED_SETTINGS_KEY
from z3c.relationfield.relation import RelationValue
from zope.annotation.interfaces import IAnnotations
from zope.component import getUtility
from zope.event import notify
from zope.interface import alsoProvides
from zope.intid.interfaces import IIntIds
from zope.lifecycleevent import ObjectModifiedEvent

import unittest


class TestAdapters(unittest.TestCase):
    layer = CPSKIN_AGENDA_INTEGRATION_TESTING

    def setUp(self):
        self.portal = self.layer['portal']
        self.request = self.layer['request']
        setRoles(self.portal, TEST_USER_ID, ['Manager'])

    def test_save_zgeo_catalog_from_contact(self):
        applyProfile(self.portal, 'collective.geo.leaflet:default')
        add_behavior('Event', IRelatedContacts.__identifier__)
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
        event.reindexObject()
        # geo = IGeoreferenced(event)
        brain = api.content.find(UID=event.UID())[0]
        # brain.zgeo_geometry
        import Missing
        self.assertTrue(brain.zgeo_geometry == Missing.Value)
        orga_geo = IGeoreferenced(organization)
        orga_geo.setGeoInterface('Point', (4.711178, 50.504827))
        notify(ObjectModifiedEvent(event))
        brain = api.content.find(UID=event.UID())[0]
        self.assertEqual(brain.zgeo_geometry['type'], 'Point')
        # check if event georeferenced is correct

    def test_cpskin_event_feed_item(self):
        folder = event = api.content.create(self.portal, 'Folder', 'myfolder')
        add_behavior('Event', IRelatedContacts.__identifier__)
        event = api.content.create(
            container=folder,
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
        organization.use_parent_address = False
        # set related contact
        intids = getUtility(IIntIds)
        to_id = intids.getId(organization)
        rv = RelationValue(to_id)
        event.location = rv
        notify(ObjectModifiedEvent(event))
        event.reindexObject()
        # set syndication
        applyProfile(self.portal, 'collective.atomrss:default')
        default_enabled_key = 'Products.CMFPlone.interfaces.syndication.ISiteSyndicationSettings.default_enabled'  # noqa
        api.portal.set_registry_record(default_enabled_key, True)
        request = folder.REQUEST

        alsoProvides(request, ICollectiveAtomrssLayer)

        _metadata = PersistentDict()
        _metadata['render_body'] = True
        annotations = IAnnotations(folder)
        annotations[FEED_SETTINGS_KEY] = _metadata
        view = api.content.get_view(
            name='atom.xml',
            context=folder,
            request=request)
        self.assertTrue(u'IMIO<br />Rue L\xe9on Morel, 1<br />5032 Isnes' in view.index())  # noqa
