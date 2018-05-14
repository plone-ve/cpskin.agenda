# -*- coding: utf-8 -*-
from Acquisition import aq_base
from collective.atomrss.adapters import EventFeedItem
from collective.contact.core.browser.address import get_address
from collective.documentgenerator.content.condition import ConfigurablePODTemplateCondition  # noqa
from collective.geo.geographer.interfaces import IGeoreferenceable
from collective.geo.geographer.interfaces import IGeoreferenced
from cpskin.core.utils import format_phone
from cpskin.core.utils import safe_utf8
from imio.dashboard.content.pod_template import DashboardPODTemplateCondition as DPTC  # noqa
from plone.app.contenttypes.interfaces import IEvent
from plone.indexer.decorator import indexer
from Products.CMFPlone.interfaces.syndication import IFeed
from z3c.relationfield.relation import RelationValue
from zope.component import adapts


@indexer(IEvent)
def zgeo_geometry_value(obj):
    if isinstance(obj.location, RelationValue):
        if obj.location.isBroken():
            obj.location = None
            raise AttributeError
        contact_obj = obj.location.to_object
    else:
        contact_obj = obj
    if IGeoreferenceable.providedBy(contact_obj):
        # old_geo = IGeoreferenced(obj)
        # old_geo.removeGeoInterface()
        geo = IGeoreferenced(contact_obj)
        if geo.type and geo.coordinates:
            return {
                'type': geo.type,
                'coordinates': geo.coordinates
            }
    # The catalog expects AttributeErrors when a value can't be found
    raise AttributeError


class CpskinEventFeedItem(EventFeedItem):
    adapts(IEvent, IFeed)

    def get_field(self, field_name):
        if field_name in ['contact_email', 'contact_name', 'contact_phone']:
            sub = field_name.replace('contact_', '')
            field = getattr(aq_base(self.context), 'contact', '')
        else:
            field = getattr(aq_base(self.context), field_name, '')
        if not field:
            return ''
        if isinstance(field, RelationValue):
            if field.isBroken():
                return ''
            obj = field.to_object
            if field_name == 'location':
                address = get_address(obj)
                if not address:
                    return '{0}'.format(safe_utf8(obj.title))
                number = ''
                if address.get('number', None):
                    number = ', {0}'.format(address['number'])
                return '{0}<br />{1}{2}<br />{3} {4}'.format(
                    safe_utf8(obj.title),
                    safe_utf8(address.get('street') or ''),
                    number,
                    address.get('zip_code') or '',
                    safe_utf8(address.get('city') or '')
                )
            else:
                if sub == 'name':
                    return getattr(obj, 'title', '')
                if sub == 'phone':
                    phones = getattr(obj, 'phone', '')
                    if not phones:
                        return ''
                    if not isinstance(phones, list):
                        phones = [phones]
                    return ', '.join([format_phone(phone)['formated'] for phone in phones])  # noqa

                return getattr(obj, sub, '')
        else:
            return field

    @property
    def contactname(self):
        return self.get_field('contact_name')

    @property
    def contactemail(self):
        return self.get_field('contact_email')

    @property
    def contactphone(self):
        return self.get_field('contact_phone')

    @property
    def location(self):
        return self.get_field('location')
