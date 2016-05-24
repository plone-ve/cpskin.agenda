# -*- coding: utf-8 -*-

from datetime import timedelta
from plone.app.contenttypes.interfaces import IEvent
from plone.app.event.base import RET_MODE_ACCESSORS
from plone.app.event.base import expand_events
from plone.indexer import indexer


@indexer(IEvent)
def event_dates(obj):
    """
    Return all days in which the event occurs
    """
    if obj.start is None or obj.end is None:
        return None

    event_days = set()
    occurences = expand_events([obj], RET_MODE_ACCESSORS)
    for occurence in occurences:
        start = occurence.start
        event_days.add(start.date())
        end = occurence.end
        duration = (end.date() - start.date()).days
        for idx in range(1, duration + 1):
            day = start + timedelta(days=idx)
            event_days.add(day.date())

    return tuple(event_days)
