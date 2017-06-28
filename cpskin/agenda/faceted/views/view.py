# -*- coding: utf-8 -*-
from datetime import date
from datetime import timedelta
from plone import api
from plone.app.contenttypes.behaviors.collection import ICollection
from Products.Five.browser import BrowserView
from zope.component import getMultiAdapter


def is_in_range(date, start, end):
    if start and date < start:
        return False
    if end and date > end:
        return False
    return True


def sort_ungrouped(brain, searchedStartDate, searchedEndDate):
    """
    We need to sort events by start date with this order :
      1. one-day event
      2. multi days events starting on the searched start date
         (first end first)
      3. multi days events starting before the searched start date
         (first end first)
    """
    catalog = api.portal.get_tool('portal_catalog')
    rid = brain.getRID()
    idx = catalog.getIndexDataForRID(rid)
    allDates = idx['event_dates']
    if len(allDates) == 1:
        return allDates[0], 0, 0
    elif allDates[0] == searchedStartDate:
        return searchedStartDate, 1, 0
    else:
        return searchedStartDate, 1, searchedEndDate - searchedStartDate


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
        for evendDate in allDates:
            if not is_in_range(evendDate, start, end):
                continue
            if evendDate in days:
                days[evendDate][multiDays].append(brain)
            else:
                days[evendDate] = {'single': [],
                                   'multi': []}
                days[evendDate][multiDays].append(brain)
    return days


class EventsView(BrowserView):
    """
    """

    @property
    def limit(self):
        limit = ICollection(self.context).limit
        return limit

    def get_criteria_dates(self):
        startDate = None
        endDate = None
        handler = getMultiAdapter((self.context, self.request),
                                  name=u'faceted_query')
        criteria = handler.criteria()
        if 'start' in criteria and 'end' in criteria:
            endDate = criteria['start']['query'].asdatetime().date()
            startDate = criteria['end']['query'].asdatetime().date()
            # Faceted use previous day at 23:59:59 for its query
            startDate = startDate + timedelta(days=1)
        else:
            # By default we show only future events
            startDate = date.today()
        return startDate, endDate

    def organize_ungrouped(self, results):
        if not results:
            return {}
        startDate, endDate = self.get_criteria_dates()

        results = [r for r in results]  # Unbatch if needed
        sorted(
            results,
            key=lambda brain: sort_ungrouped(brain, startDate, endDate)
        )
        return results[:self.limit]

    def organize(self, results):
        if not results:
            return {}
        startDate, endDate = self.get_criteria_dates()
        results = sort_and_group(self.context, results, startDate, endDate)
        resultsByDaysList = [{d: l} for d, l in results.items()]
        resultsByDaysList = sorted(resultsByDaysList)
        return resultsByDaysList[:self.limit]

    def render_event_preview(self, obj):
        context = self.context
        request = self.request
        scale = getattr(context, 'collection_image_scale', 'thumb')
        request['scale'] = scale
        render_view = u'faceted-agenda-view-item'
        if self.__name__ == 'faceted-events-preview-items':
            # This will be removed when aceted-agenda-view-items will totally
            # replace faceted-events-preview-items
            render_view = u'faceted-event-preview-item'
        elif self.__name__ == 'faceted-agenda-ungrouped-view-items':
            render_view = u'faceted-agenda-ungrouped-view-item'
        view = getMultiAdapter((obj, request), name=render_view)
        return view and view() or ''
