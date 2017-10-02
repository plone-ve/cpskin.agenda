# -*- coding: utf-8 -*-
from cpskin.agenda.behaviors.related_contacts import IRelatedContacts
from cpskin.core.utils import format_phone
from cpskin.locales import CPSkinMessageFactory as _
from plone import api
from plone.app.event.browser.event_summary import EventSummaryView
from plone.app.event.browser.event_view import get_location
from plone.dexterity.interfaces import IDexterityFTI
from zope.component import getUtility
from zope.component import queryUtility
from zope.schema import getFieldsInOrder
from zope.schema.interfaces import IVocabularyFactory


class EventContactSummaryView(EventSummaryView):

    def get_organizer(self):
        if not getattr(self.context, 'organizer', None):
            return None
        else:
            return self.context.organizer.to_object

    def get_contact(self):
        if not getattr(self.context, 'contact', None):
            return None
        else:
            return self.context.contact.to_object

    def get_phone_or_cellphone(self, contact):
        phones = getattr(contact, 'phone', [])
        if not isinstance(phones, list):
            phones = [phones]
        if len(phones) == 0:
            phones = getattr(contact, 'cell_phone', [])
        if not phones:
            return []
        return [format_phone(phone) for phone in phones]

    def get_location(self):
        if not getattr(self.context, 'location', None):
            return None
        else:
            if isinstance(self.context.location, unicode):
                return get_location(self.context)
            else:
                return self.context.location.to_object

    def get_partners(self):
        if not getattr(self.context, 'partners', None):
            return None
        else:
            partners = [p.to_object for p in self.context.partners]
            return partners

    def enabled(self):
        """Check if IRelatedContacts behavior is enabled"""
        fti = queryUtility(IDexterityFTI, name='Event')
        behaviors = list(fti.behaviors)
        if IRelatedContacts.__identifier__ in behaviors:
            return True
        else:
            return False

    @property
    def more_occurrences_text(self):
        msgid = _(
            u'msg_num_more_occurrences',
            default=u'Il y a ${results} occurrence(s) en plus.',
            mapping={u'results': self.num_more_occurrences}
        )
        return self.context.translate(msgid)

    def get_taxonomies(self):
        """Return all field added by taxonomies"""
        portal_type = 'Event'
        schema = getUtility(IDexterityFTI, name=portal_type).lookupSchema()
        fields = getFieldsInOrder(schema)
        taxonomies = []
        for name, field in fields:
            # categories check is a hack for Namur, do not remove it.
            if (name.startswith('taxonomy_') or 'categories' in name) \
                    and field:
                if getattr(field, 'value_type', None):
                    vocabulary_name = field.value_type.vocabularyName
                else:
                    vocabulary_name = field.vocabularyName
                factory = getUtility(IVocabularyFactory, vocabulary_name)
                vocabulary = factory(api.portal.get())
                tokens = getattr(self.context, name, '')
                if not tokens:
                    continue
                if isinstance(tokens, basestring):
                    tokens = [tokens]
                categories = []
                for token in tokens:
                    if token in vocabulary.inv_data.keys():
                        cat = vocabulary.inv_data.get(token)
                        categories.append(cat[1:])
                categories.sort()
                tax = {}
                tax['name'] = field.title
                tax['id'] = name
                tax['value'] = ', '.join(categories)
                taxonomies.append(tax)
        return sort_taxonomies(taxonomies)


def sort_taxonomies(taxonomies):
    prefered_order = (
        'categories',
        'gratuite',
        'publiccible',
        'danslecadrede'
    )
    prefered_order_ids = []
    indexes = [tax['id'] for tax in taxonomies]
    for order in prefered_order:
        for ind in indexes:
            if order in ind:
                prefered_order_ids.append(ind)
    rest = list(set(indexes).difference(prefered_order_ids))
    prefered_order_ids.extend(rest)
    sorted_tax = []
    for prefered_order_id in prefered_order_ids:
        tax = [tax for tax in taxonomies if tax['id'] == prefered_order_id][0]
        sorted_tax.append(tax)
    return sorted_tax
