# -*- coding: utf-8 -*-
from cpskin.agenda.behaviors.related_contacts import IRelatedContacts
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
            if name.startswith('taxonomy_') and field:
                if getattr(field, 'value_type', None):
                    vocabulary_name = field.value_type.vocabularyName
                else:
                    vocabulary_name = field.vocabularyName
                factory = getUtility(IVocabularyFactory, vocabulary_name)
                vocabulary = factory(api.portal.get())
                tokens = getattr(self.context, name, '')
                if not tokens:
                    continue
                if not isinstance(tokens, basestring):
                    tokens = [tokens]
                categories = []
                for token in tokens:
                    if token in vocabulary.inv_data.keys():
                        cat = vocabulary.inv_data.get(token)
                        categories.append(cat[1:])
                categories.sort()
                tax = {}
                tax['name'] = field.title
                tax['value'] = ', '.join(categories)
                taxonomies.append(tax)
        return taxonomies
