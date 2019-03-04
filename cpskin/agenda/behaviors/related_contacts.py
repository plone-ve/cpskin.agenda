# -*- coding: utf-8 -*-
from collective.contact.core.browser.address import get_address
from collective.contact.widget.interfaces import IContactChoice
from collective.contact.widget.schema import ContactChoice
from collective.contact.widget.schema import ContactList
from collective.contact.widget.source import ContactSourceBinder
from collective.geo.geographer.geo import GeoreferencingAnnotator
from collective.geo.geographer.interfaces import IGeoreferenceable
from collective.taxonomy.interfaces import ITaxonomy
from cpskin.agenda.interfaces import ICPSkinAgendaLayer
from cpskin.core.utils import add_behavior
from cpskin.core.utils import remove_behavior
from cpskin.core.utils import safe_utf8
from cpskin.locales import CPSkinMessageFactory as _
from persistent.dict import PersistentDict
from plone.app.contenttypes.interfaces import ICollection
from plone.app.contenttypes.interfaces import IEvent
from plone.app.event.base import expand_events
from plone.autoform import directives as form
from plone.autoform.interfaces import IFormFieldProvider
from plone.dexterity.interfaces import IDexterityContent
from plone.event.interfaces import IOccurrence
from plone.restapi.interfaces import IFieldSerializer
from plone.restapi.interfaces import ISerializeToJson
from plone.restapi.serializer.collection import SerializeCollectionToJson
from plone.restapi.serializer.converters import json_compatible
from plone.restapi.serializer.dxcontent import SerializeToJson
from plone.restapi.serializer.dxfields import DefaultFieldSerializer
from plone.supermodel import model
from z3c.relationfield.relation import RelationValue
from zope.annotation.interfaces import IAnnotations
from zope.component import adapter
from zope.component import getMultiAdapter
from zope.component import getSiteManager
from zope.interface import implementer
from zope.interface import Interface
from zope.interface import provider
from zope.schema.interfaces import IField


KEY = 'collective.geo.geographer.georeference'


@provider(IFormFieldProvider)
class IRelatedContacts(model.Schema):

    form.order_before(location='IRichText.text')
    location = ContactChoice(
        title=_(u'Location'),
        source=ContactSourceBinder(
            portal_type=('organization',),
        ),
        required=False,
    )

    form.order_after(organizer='IRelatedContacts.location')
    organizer = ContactChoice(
        title=_(u'Organizer'),
        source=ContactSourceBinder(
            portal_type=('person', 'organization'),
        ),
        required=False,
    )

    form.order_after(contact='IRelatedContacts.organizer')
    contact = ContactChoice(
        title=_(u'Contact'),
        source=ContactSourceBinder(
            portal_type=('person', 'organization'),
        ),
        required=False,
    )

    form.order_after(partners='IRelatedContacts.contact')
    partners = ContactList(
        title=_(u'Partners'),
        value_type=ContactChoice(
            title=_(u'Partner'),
            source=ContactSourceBinder(
                portal_type=('person', 'organization'),
            )
        ),
        required=False,
    )


class LocationRelatedContactsGeoreferencingAnnotator(GeoreferencingAnnotator):

    def __init__(self, context):
        if isinstance(getattr(context, 'location', None), RelationValue):
            contact_obj = context.location.to_object
            context = contact_obj
        self.context = context
        annotations = IAnnotations(self.context)
        self.geo = annotations.get(KEY, None)
        if not self.geo:
            annotations[KEY] = PersistentDict()
            self.geo = annotations[KEY]
            self.geo['type'] = None
            self.geo['coordinates'] = None
            self.geo['crs'] = None


class ILocationRelatedContactsGeoreferenceable(IGeoreferenceable):
    pass


@implementer(IRelatedContacts)
@adapter(IEvent)
class RelatedContacts(object):

    def __init__(self, context):
        self.context = context

    @property
    def location(self):
        return getattr(self.context, 'location', None)

    @location.setter
    def location(self, value):
        self.context.location = value

    @property
    def organizer(self):
        return getattr(self.context, 'organizer', None)

    @organizer.setter
    def organizer(self, value):
        self.context.organizer = value

    @property
    def contact(self):
        return getattr(self.context, 'contact', None)

    @contact.setter
    def contact(self, value):
        self.context.contact = value

    @property
    def partners(self):
        return getattr(self.context, 'partners', None)

    @partners.setter
    def partners(self, value):
        self.context.partners = value


def modified_event(obj, event):
    type_name = obj.id
    if type_name == 'Event':
        pae_behaviors = [
            'plone.app.event.dx.behaviors.IEventAttendees',
            'plone.app.event.dx.behaviors.IEventLocation',
            'plone.app.event.dx.behaviors.IEventContact'
        ]
        if 'cpskin.agenda.behaviors.related_contacts.IRelatedContacts' in obj.behaviors:  # noqa
            for pae_behavior in pae_behaviors:
                remove_behavior(type_name, pae_behavior)
        else:
            for pae_behavior in pae_behaviors:
                add_behavior(type_name, pae_behavior)


@adapter(IContactChoice, IDexterityContent, Interface)
class ContactFieldSerializer(DefaultFieldSerializer):
    def __call__(self):
        value = self.get_value()
        if getattr(value, 'to_object', False):
            obj = value.to_object
            result = {
                'title': obj.title,
                'path': '/'.join(obj.getPhysicalPath()),
                'phone': obj.phone,
                'cell_phone': obj.cell_phone,
            }
            result.update(get_address(obj))
            return json_compatible(result)
        return json_compatible(value, self.context)


@implementer(ISerializeToJson)
@adapter(IOccurrence, ICPSkinAgendaLayer)
class SerializeOccurenceToJson(SerializeToJson):
    def __call__(self):
        obj = self.context
        parent = obj.aq_parent
        summary = getMultiAdapter((parent, self.request), ISerializeToJson)()
        summary['@type'] = obj.portal_type
        summary['@id'] = obj.absolute_url(),
        summary['start'] = obj.start
        summary['end'] = obj.end
        summary['recurrence'] = ''
        return json_compatible(summary)


@implementer(ISerializeToJson)
@adapter(ICollection, ICPSkinAgendaLayer)
class SerializeEventCollectionToJson(SerializeCollectionToJson):

    def __call__(self, version=None, include_items=True):
        if 'allevents' in self.request.form.keys():
            results = super(SerializeCollectionToJson, self).__call__(
                version=version,
            )
            events = expand_events(
                self.context.results(batch=False),
                2
            )
            # items = []
            # i = 0
            # for brain in events:
            #     items.append(getMultiAdapter((brain, self.request),
            #          ISerializeToJson)())
            #     i += 1
            #     print '{0} / {1}'.format(str(i), len(events))
            # results['items'] = items
            results['items'] = [
                getMultiAdapter((brain, self.request), ISerializeToJson)()
                for brain in events
            ]
            results['items_total'] = len(events)
            return results
        else:
            return super(SerializeEventCollectionToJson, self).__call__(
                version, include_items)


@adapter(IField, IDexterityContent, ICPSkinAgendaLayer)
@implementer(IFieldSerializer)
class TaxonomyFieldSerializer(object):

    def __init__(self, field, context, request):
        self.context = context
        self.request = request
        self.field = field

    def __call__(self):
        field_name = self.field.__name__
        if (field_name == 'categories_evenements' or
           field_name.startswith('taxonomy_')) and \
           field_name != 'taxonomy_category':
            lang = self.context.language
            taxonomy_ids = self.get_value()
            if not taxonomy_ids:
                return []
            if isinstance(taxonomy_ids, basestring):
                taxonomy_ids = [taxonomy_ids]
            domain = 'collective.taxonomy.{0}'.format(
                field_name.replace('taxonomy_', '').replace('_', ''))
            sm = getSiteManager()
            utility = sm.queryUtility(ITaxonomy, name=domain)
            taxonomy_list = [taxonomy_id for taxonomy_id in taxonomy_ids]
            text = []
            if len(taxonomy_list) > 0:
                for taxonomy_id in taxonomy_list:
                    text.append(
                        safe_utf8(
                            utility.translate(
                                taxonomy_id,
                                context=self.context,
                                target_language=lang
                            )
                        )
                    )
                return json_compatible(text)
        else:
            return json_compatible(self.get_value())

    def get_value(self, default=None):
        return getattr(self.field.interface(self.context),
                       self.field.__name__,
                       default)
