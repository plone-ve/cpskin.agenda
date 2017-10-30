# -*- coding: utf-8 -*-
from collective.taxonomy.interfaces import ITaxonomy
from cpskin.agenda.behaviors.related_contacts import IRelatedContacts
from cpskin.agenda.browser.event_summary import sort_taxonomies
from cpskin.agenda.interfaces import ICPSkinAgendaLayer
from cpskin.agenda.testing import CPSKIN_AGENDA_INTEGRATION_TESTING
from cpskin.core.utils import add_behavior
from plone import api
from plone.app.event.dx.behaviors import IEventBasic
from plone.app.testing import applyProfile
from plone.app.testing import setRoles
from plone.app.testing import TEST_USER_ID
from plone.schemaeditor.utils import FieldAddedEvent
from plone.schemaeditor.utils import IEditableSchema
from z3c.relationfield.relation import RelationValue
from zope import schema
from zope.component import getMultiAdapter
from zope.component import getUtility
from zope.component import queryUtility
from zope.event import notify
from zope.interface import directlyProvides
from zope.intid.interfaces import IIntIds
from zope.lifecycleevent import ObjectAddedEvent

import datetime
import unittest


def add_test_contents(portal):
    # add some contacts
    applyProfile(portal, 'collective.contact.core:default')
    directory_person = api.content.create(
        container=portal, type='directory', id='directory-person')
    person = api.content.create(
        container=directory_person, type='person', id='person')
    person.firstname = u'Foo'
    person.lastname = u'Bar'
    person.gender = u'F'
    person.street = u'Zoning Industriel'
    person.number = u'34'
    person.zip_code = u'5190'
    person.city = u'Mornimont'

    position_types = [{'name': u'Position', 'token': u'pos'}]
    organization_types = [{'name': u'Organization', 'token': u'orga'}]
    organization_levels = [{'name': u'Levels', 'token': u'lev'}]

    params = {'position_types': position_types,
              'organization_types': organization_types,
              'organization_levels': organization_levels}
    directory_organization = api.content.create(
        container=portal,
        type='directory',
        id='directory-organization',
        **params)

    params = {'title': u'Organisation1',
              'organization_type': u'orga',
              'use_parent_address': True,
              }
    organization1 = api.content.create(
        container=directory_organization,
        type='organization',
        id='organization1',
        **params)
    params['use_parent_address'] = True
    organization2 = api.content.create(
        container=directory_organization,
        type='organization',
        id='organization2',
        **params)
    return person, organization1, organization2


class TestViews(unittest.TestCase):

    layer = CPSKIN_AGENDA_INTEGRATION_TESTING

    def setUp(self):
        self.portal = self.layer['portal']
        self.request = self.layer['request']
        setRoles(self.portal, TEST_USER_ID, ['Manager'])
        directlyProvides(self.request, ICPSkinAgendaLayer)  # noqa

    def test_event_view_without_behavior(self):
        timezone = 'Europe/Brussels'
        now = datetime.datetime.now()
        self.event = api.content.create(
            container=self.portal,
            type='Event',
            id='event')
        self.event.timezone = timezone
        self.event.location = u'Mon adresse'
        eventbasic = IEventBasic(self.event)
        eventbasic.start = datetime.datetime(now.year, now.month, now.day, 18)
        eventbasic.end = datetime.datetime(now.year, now.month, now.day, 21)
        self.event.reindexObject()
        view = getMultiAdapter(
            (self.event, self.request), name='event_summary')
        self.assertNotIn('partners', view())

    def test_related_contacts_behavior_view_for_partners(self):
        add_behavior('Event', IRelatedContacts.__identifier__)
        timezone = 'Europe/Brussels'
        now = datetime.datetime.now()
        self.event = api.content.create(
            container=self.portal,
            type='Event',
            id='event')
        self.event.timezone = timezone
        eventbasic = IEventBasic(self.event)
        eventbasic.start = datetime.datetime(now.year, now.month, now.day, 18)
        eventbasic.end = datetime.datetime(now.year, now.month, now.day, 21)
        self.event.reindexObject()
        view = getMultiAdapter(
            (self.event, self.request), name='event_summary')
        self.assertNotIn('partners', view())

        person, organization1, organization2 = add_test_contents(self.portal)

        # set related contact
        intids = getUtility(IIntIds)
        to_id1 = intids.getId(person)
        to_id2 = intids.getId(organization2)
        rv1 = RelationValue(to_id1)
        rv2 = RelationValue(to_id2)
        self.event.partners = [rv1, rv2]
        self.assertIn('partners', view())

    def test_related_contacts_behavior_view_for_location(self):
        add_behavior('Event', IRelatedContacts.__identifier__)
        timezone = 'Europe/Brussels'
        now = datetime.datetime.now()
        self.event = api.content.create(
            container=self.portal,
            type='Event',
            id='event')
        self.event.timezone = timezone
        eventbasic = IEventBasic(self.event)
        eventbasic.start = datetime.datetime(now.year, now.month, now.day, 18)
        eventbasic.end = datetime.datetime(now.year, now.month, now.day, 21)
        self.event.reindexObject()
        view = getMultiAdapter(
            (self.event, self.request), name='event_summary')
        person, organization1, organization2 = add_test_contents(self.portal)

        # set related contact
        intids = getUtility(IIntIds)
        to_id = intids.getId(organization1)
        rv = RelationValue(to_id)
        self.event.location = rv
        self.assertIn('Location', view())

    def test_related_contacts_behavior_view_for_contact(self):
        add_behavior('Event', IRelatedContacts.__identifier__)
        timezone = 'Europe/Brussels'
        now = datetime.datetime.now()
        self.event = api.content.create(
            container=self.portal,
            type='Event',
            id='event')
        self.event.timezone = timezone
        eventbasic = IEventBasic(self.event)
        eventbasic.start = datetime.datetime(now.year, now.month, now.day, 18)
        eventbasic.end = datetime.datetime(now.year, now.month, now.day, 21)
        self.event.reindexObject()
        view = getMultiAdapter(
            (self.event, self.request), name='event_summary')
        person, organization1, organization2 = add_test_contents(self.portal)

        # set related contact
        intids = getUtility(IIntIds)
        to_id = intids.getId(organization1)
        rv = RelationValue(to_id)
        self.event.contact = rv
        self.assertEqual(
            view.get_website(organization1),
            None
        )
        organization1.website = 'www.foo.bar'
        self.assertEqual(
            view.get_website(organization1),
            '<a class="event_website" href="http://www.foo.bar" target="_blank">www.foo.bar</a>'  # noqa
        )

    def test_taxonmies_field_visible(self):
        applyProfile(self.portal, 'collective.taxonomy:default')

        utility = queryUtility(ITaxonomy, name='collective.taxonomy.test')
        taxonomy_test = schema.Set(
            title=u'taxonomy_test',
            description=u'taxonomy description schema',
            required=False,
            value_type=schema.Choice(
                vocabulary=u'collective.taxonomy.test'),
        )
        portal_types = api.portal.get_tool('portal_types')
        fti = portal_types.get('Event')
        event_schema = fti.lookupSchema()
        schemaeditor = IEditableSchema(event_schema)
        schemaeditor.addField(taxonomy_test, name='taxonomy_test')
        notify(ObjectAddedEvent(taxonomy_test, event_schema))
        notify(FieldAddedEvent(fti, taxonomy_test))
        event = api.content.create(self.portal, 'Event', 'testevent')
        simple_tax = [val for val in utility.data['en'].values()]
        event.taxonomy_test = set(simple_tax[0])

        view = getMultiAdapter(
            (event, self.portal.REQUEST), name='event_summary')

        taxonomies = view.get_taxonomies()
        self.assertEqual(taxonomies[0]['value'], 'Information Science')

        event.taxonomy_test = set(simple_tax[0:2])
        taxonomies = view.get_taxonomies()
        self.assertEqual(
            taxonomies[0]['value'],
            'Information Science, Information Science/Book Collecting')

        event.taxonomy_test = set()
        taxonomies = view.get_taxonomies()
        self.assertEqual(len(taxonomies), 0)

    def test_sort_of_taxonomies(self):
        # applyProfile(self.portal, 'collective.taxonomy:default')
        taxonomies = [
            {'name': u'Soutenu par la Ville de Namur',
             'value': u'Sports',
             'id': 'taxonomy_soutenuparlavilledenamur_'},
            {'name': u'Dans le cadre de',
             'value': u'Challenge des joggings de la Ville de Namur',
             'id': 'taxonomy_danslecadrede'},
            {'name': u'Co\xfbt',
             'value': 'Payant',
             'id': 'taxonomy_gratuite'},
            {'name': u'Public cible',
             'value': u'Tout public',
             'id': 'taxonomy_publiccible'},
            {'id': 'categories_evenements',
             'name': u'Cat\xe9gories \xe9v\xe9nements',
             'value': u'Sport'},
        ]
        sorted_tax = sort_taxonomies(taxonomies)
        self.assertEqual(sorted_tax[0]['id'], 'categories_evenements')
        self.assertEqual(sorted_tax[2]['id'], 'taxonomy_publiccible')
        self.assertEqual(sorted_tax[4]['id'],
                         'taxonomy_soutenuparlavilledenamur_')

    def test_phone_or_cellphone(self):
        add_behavior('Event', IRelatedContacts.__identifier__)
        timezone = 'Europe/Brussels'
        now = datetime.datetime.now()
        self.event = api.content.create(
            container=self.portal,
            type='Event',
            id='event')
        self.event.timezone = timezone
        eventbasic = IEventBasic(self.event)
        eventbasic.start = datetime.datetime(now.year, now.month, now.day, 18)
        eventbasic.end = datetime.datetime(now.year, now.month, now.day, 21)
        self.event.reindexObject()
        view = getMultiAdapter(
            (self.event, self.request), name='event_summary')
        person, organization1, organization2 = add_test_contents(self.portal)
        organization1.phone = ['081/586.100']
        phone_or_cellphone = view.get_phone_or_cellphone(organization1)
        self.assertEqual(phone_or_cellphone[0].get('formated'),
                         '+32 (0) 81 58 61 00')
        organization1.phone = []
        phone_or_cellphone = view.get_phone_or_cellphone(organization1)
        self.assertEqual(len(phone_or_cellphone), 0)
        organization1.cell_phone = ['081/586.101']
        phone_or_cellphone = view.get_phone_or_cellphone(organization1)
        self.assertEqual(phone_or_cellphone[0].get('formated'),
                         '+32 (0) 81 58 61 01')
