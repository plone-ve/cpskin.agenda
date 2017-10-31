# -*- coding: utf-8 -*-
from collective.geo.geographer.interfaces import IGeoreferenceable
from collective.geo.geographer.interfaces import IGeoreferenced
from plone.app.contenttypes.interfaces import IEvent
from plone.indexer.decorator import indexer
from z3c.relationfield.relation import RelationValue


@indexer(IEvent)
def zgeo_geometry_value(obj):
    if isinstance(obj.contact, RelationValue):
        if obj.contact.isBroken():
            obj.contact = None
            raise AttributeError
        contact_obj = obj.contact.to_object
        # import ipdb; ipdb.set_trace()
        if IGeoreferenceable.providedBy(contact_obj):
            old_geo = IGeoreferenced(obj)
            old_geo.removeGeoInterface()
            geo = IGeoreferenced(contact_obj)
            if geo.type and geo.coordinates:
                return {
                    'type': geo.type,
                    'coordinates': geo.coordinates
                }
    # The catalog expects AttributeErrors when a value can't be found
    raise AttributeError
