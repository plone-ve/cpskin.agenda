# -*- coding: utf-8 -*-

from Products.Five.browser import BrowserView
from plone import api
from zope.component import getMultiAdapter


def is_in_range(date, start, end):
    if start and date < start:
        return False
    if end and date > end:
        return False
    return True


def sort_and_group(context, brains, start, end):
    """
    We need to group by day and separate one-day and multi-days events
    """
    catalog = api.portal.get_tool('portal_catalog')
    days = {}
    for brain in brains:
        rid = brain.getRID()
        idx = catalog.getIndexDataForRID(rid)
        allDates = idx['event_dates']
        multiDays = len(allDates) > 1 and 'multi' or 'single'
        for date in allDates:
            if not is_in_range(date, start, end):
                continue
            if date in days:
                days[date][multiDays].append(brain)
            else:
                days[date] = {'single': [],
                              'multi': []}
                days[date][multiDays].append(brain)
    return days


class EventsView(BrowserView):
    """
    """

    def organize(self, results):
        if not results:
            return {}
        startDate = None
        endDate = None
        handler = getMultiAdapter((self.context, self.request),
                                  name=u'faceted_query')
        criteria = handler.criteria()
        if 'start' in criteria and 'end' in criteria:
            endDate = criteria['start']['query'].asdatetime().date()
            startDate = criteria['end']['query'].asdatetime().date()
        results = sort_and_group(self.context, results, startDate, endDate)
        return results
