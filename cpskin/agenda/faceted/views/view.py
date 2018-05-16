# -*- coding: utf-8 -*-
from datetime import date
from datetime import timedelta
from eea.facetednavigation.interfaces import ICriteria
from plone import api
from plone.app.contenttypes.behaviors.collection import ICollection
from Products.CMFPlone.PloneBatch import Batch
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
    We need to sort events with this order :
      1. on start date : one-day event
      2. on start date : multi days events starting on the searched start date
         (first end first)
      3. on searched start date : multi days events starting before and ending
         after searched start date (first end first)
      4. on end date : multi days events starting before and ending before
         searched start date (first start first)
      5. on start date : multi days events starting after and ending after
         searched start date (first end first)
    """
    catalog = api.portal.get_tool('portal_catalog')
    rid = brain.getRID()
    idx = catalog.getIndexDataForRID(rid)
    allDates = sorted(idx['event_dates'])
    startDate = allDates[0]
    endDate = allDates[-1]
    if len(allDates) == 1:
        return startDate, 0, 0
    elif startDate == searchedStartDate:
        return startDate, 1, (endDate - searchedStartDate).days
    elif startDate < searchedStartDate < endDate:
        return searchedStartDate, 2, (endDate - searchedStartDate).days
    elif startDate < searchedStartDate:
        return endDate, 3, (startDate - searchedStartDate).days
    elif startDate > searchedStartDate:
        return startDate, 4, (endDate - searchedStartDate).days


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

        if isinstance(results, Batch):  # Unbatch if needed
            results = results._sequence
        results = sorted(
            results,
            key=lambda brain: sort_ungrouped(brain, startDate, endDate)
        )
        return results[:self.limit]

    def organize(self, results):
        if not results:
            return {}
        if isinstance(results, Batch):  # Unbatch if needed
            results = results._sequence
        startDate, endDate = self.get_criteria_dates()
        results = sort_and_group(self.context, results, startDate, endDate)
        resultsByDaysList = [{d: l} for d, l in results.items()]
        resultsByDaysList = sorted(resultsByDaysList)
        return resultsByDaysList[:self.limit]

    def perPage(self):
        num_per_page = 20
        criteria = ICriteria(self.context)
        for cid, criterion in criteria.items():
            widgetclass = criteria.widget(cid=cid)
            widget = widgetclass(self.context, self.request, criterion)
            if widget.widget_type == 'resultsperpage':
                kwargs = dict((key.replace('[]', ''), val)
                              for key, val in self.request.form.items())
                num_per_page = widget.results_per_page(kwargs)
        return num_per_page

    def render_event_preview(self, obj):
        context = self.context
        request = self.request
        scale = getattr(context, 'collection_image_scale', 'thumb')
        request['scale'] = scale
        request['collection'] = context
        render_view = u'faceted-agenda-view-item'
        if self.__name__ == 'faceted-events-preview-items':
            # This will be removed when aceted-agenda-view-items will totally
            # replace faceted-events-preview-items
            render_view = u'faceted-event-preview-item'
        elif self.__name__ == 'faceted-agenda-ungrouped-view-items':
            render_view = u'faceted-agenda-ungrouped-view-item'
        view = getMultiAdapter((obj, request), name=render_view)
        return view and view() or ''
