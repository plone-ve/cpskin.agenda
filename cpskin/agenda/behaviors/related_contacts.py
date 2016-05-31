# -*- coding: utf-8 -*-
from collective.contact.widget.schema import ContactList, ContactChoice
from collective.contact.widget.source import ContactSourceBinder
from cpskin.core.utils import add_behavior
from cpskin.core.utils import remove_behavior
from cpskin.locales import CPSkinMessageFactory as _
from plone.autoform.interfaces import IFormFieldProvider
# from plone.supermodel import directives
from plone.supermodel import model
from zope.interface import provider


@provider(IFormFieldProvider)
class IRelatedContacts(model.Schema):

    location = ContactChoice(
        title=_(u"Location"),
        source=ContactSourceBinder(
            portal_type=('organization',),
        ),
        required=False,
    )

    organizer = ContactChoice(
        title=_(u"Organizer"),
        source=ContactSourceBinder(
            portal_type=('person', 'organization'),
        ),
        required=False,
    )

    contact = ContactChoice(
        title=_(u"Contact"),
        source=ContactSourceBinder(
            portal_type=('person', 'organization'),
        ),
        required=False,
    )

    partner = ContactList(
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
        if 'cpskin.agenda.behaviors.related_contacts.IRelatedContacts' in obj.behaviors:
            remove_behavior(
                type_name, 'plone.app.event.dx.behaviors.IEventAttendees')
        else:
            add_behavior(
                type_name, 'plone.app.event.dx.behaviors.IEventAttendees')
