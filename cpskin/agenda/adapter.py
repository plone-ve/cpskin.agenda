# -*- coding: utf-8 -*-
from collective.geo.geographer.interfaces import IGeoreferenceable
from collective.geo.geographer.interfaces import IGeoreferenced
from plone.app.contenttypes.interfaces import IEvent
from plone.indexer.decorator import indexer
from z3c.relationfield.relation import RelationValue


@indexer(IEvent)
def zgeo_geometry_value(obj):
    if isinstance(obj.location, RelationValue):
        if obj.location.isBroken():
            obj.location = None
            raise AttributeError
        contact_obj = obj.location.to_object
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
