# -*- coding: utf-8 -*-
from collective.contact.widget.schema import ContactList, ContactChoice
from collective.contact.widget.source import ContactSourceBinder
from cpskin.locales import CPSkinMessageFactory as _
from plone.autoform.interfaces import IFormFieldProvider
from plone.supermodel import directives
from plone.supermodel import model
from zope.interface import provider


@provider(IFormFieldProvider)
class IRelatedContacts(model.Schema):
    directives.fieldset(
        'categorization',
        label=_(u'label_schema_categorization', default=u'Categorization'),
        fields=('location', 'organizer', 'contact', 'partner'),
    )

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
