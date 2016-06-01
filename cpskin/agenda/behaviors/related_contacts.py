# -*- coding: utf-8 -*-
from collective.contact.widget.schema import ContactList, ContactChoice
from collective.contact.widget.source import ContactSourceBinder
from cpskin.core.utils import add_behavior
from cpskin.core.utils import remove_behavior
from cpskin.locales import CPSkinMessageFactory as _
from plone.autoform.interfaces import IFormFieldProvider
from plone.autoform import directives as form
from plone.supermodel import model
from zope.interface import provider


@provider(IFormFieldProvider)
class IRelatedContacts(model.Schema):

    form.order_before(location='IRichText.text')
    location = ContactChoice(
        title=_(u"Location"),
        source=ContactSourceBinder(
            portal_type=('organization',),
        ),
        required=False,
    )

    form.order_after(organizer='IRelatedContacts.location')
    organizer = ContactChoice(
        title=_(u"Organizer"),
        source=ContactSourceBinder(
            portal_type=('person', 'organization'),
        ),
        required=False,
    )

    form.order_after(contact='IRelatedContacts.organizer')
    contact = ContactChoice(
        title=_(u"Contact"),
        source=ContactSourceBinder(
            portal_type=('person', 'organization'),
        ),
        required=False,
    )

    form.order_after(partners='IRelatedContacts.contact')
    partners = ContactList(
        title=_(u"Partners"),
        value_type=ContactChoice(
            title=_(u"Partner"),
            source=ContactSourceBinder(
                portal_type=('person', 'organization'),
            )
        ),
        required=False,
    )


def modified_event(obj, event):
    type_name = obj.id
    if type_name == "Event":
        pae_behaviors = [
            'plone.app.event.dx.behaviors.IEventAttendees',
            'plone.app.event.dx.behaviors.IEventLocation',
            'plone.app.event.dx.behaviors.IEventContact'
        ]
        if 'cpskin.agenda.behaviors.related_contacts.IRelatedContacts' in obj.behaviors:
            for pae_behavior in pae_behaviors:
                remove_behavior(type_name, pae_behavior)
        else:
            for pae_behavior in pae_behaviors:
                add_behavior(type_name, pae_behavior)
