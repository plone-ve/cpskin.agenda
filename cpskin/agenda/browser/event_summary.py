# -*- coding: utf-8 -*-
from datetime import datetime

import pytz
from cpskin.agenda.behaviors.related_contacts import IRelatedContacts
from cpskin.locales import CPSkinMessageFactory as _

from cpskin.core.utils import format_phone
from plone import api
from plone.app.event.browser.event_summary import EventSummaryView
from plone.app.event.browser.event_view import get_location
from plone.dexterity.interfaces import IDexterityFTI
from plone.event.interfaces import IRecurrenceSupport
from zope.component import getUtility
from zope.component import queryUtility
from zope.schema import getFieldsInOrder
from zope.schema.interfaces import IVocabularyFactory


class EventContactSummaryView(EventSummaryView):

    def has_booking(self):
        booking_type = getattr(self.context, 'booking_type', None)
        if booking_type is None:
            return False
        return (booking_type != 'no_booking')

    def get_booking_type(self):
        booking_type = getattr(self.context, 'booking_type')
        vocab = getUtility(
            IVocabularyFactory,
            name='cpskin.core.vocabularies.booking_types',
        )(self.context)
        return vocab.getTerm(booking_type).title

    def get_organizer(self):
        organizer = getattr(self.context.aq_base, 'organizer', None)
        if not organizer:
            return None
        else:
            return organizer.to_object

    def get_contact(self):
        contact = getattr(self.context.aq_base, 'contact', None)
        if not contact:
            return None
        else:
            return contact.to_object

    def get_formatted_phone(self, phone):
        return format_phone(phone)

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
        location = getattr(self.context.aq_base, 'location', None)
        if not location:
            return None
        else:
            if isinstance(location, unicode):
                return get_location(self.context)
            else:
                return location.to_object

    def get_website(self, contact):
        website = getattr(contact, 'website')
        if not website:
            return None
        if website.startswith('http'):
            url = website
            website_name = website.replace('http://', '')
        elif website.startswith('https'):
            url = website
            website_name = website.replace('https://', '')
        else:
            url = 'http://{0}'.format(website)
            website_name = website
        html = ''
        html += '<a class="event_website" href="{0}" target="_blank">{1}</a>'.format(  # noqa
            url, website_name)
        return html

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
        portal_type = self.context.portal_type
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

    @property
    def next_occurrences(self):
        """Returns occurrences for this context, except the start
        occurrence, limited to self.max_occurrence occurrences.

        :returns: List with next occurrences.
        :rtype: list
        """
        occurrences = []
        adapter = IRecurrenceSupport(self.event_context, None)
        if adapter:
            cnt_future_occ = 0
            for occ in adapter.occurrences():
                if cnt_future_occ == self.max_occurrences:
                    break
                if occ.end >= datetime.utcnow().replace(tzinfo=pytz.utc):
                    cnt_future_occ += 1
                    occurrences.append(occ)
        return occurrences


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
