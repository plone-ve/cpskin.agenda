# -*- coding: utf-8 -*-

from Products.CMFPlone.PloneBatch import Batch
from Products.CMFPlone.utils import safeToInt
from collective.contact.facetednav.browser.view import ContactsFacetedQueryHandler
from datetime import timedelta
from eea.facetednavigation.config import ANNO_FACETED_LAYOUT
from eea.facetednavigation.interfaces import ICriteria
from eea.facetednavigation.interfaces import IFacetedCatalog
from eea.facetednavigation.interfaces import IWidgetFilterBrains
from plone import api
from types import GeneratorType
from zope.annotation.interfaces import IAnnotations
from zope.component import getMultiAdapter
from zope.component import getUtility
from zope.component import queryAdapter
import logging

logger = logging.getLogger('eea.facetednavigation.browser.app.query')


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


class QueryHandler(ContactsFacetedQueryHandler):

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
            # Faceted use previous day at 23:59:59 for its query
            startDate = startDate + timedelta(days=1)
        results = sort_and_group(self.context, results, startDate, endDate)
        return results

    def query(self, batch=True, sort=False, **kwargs):
        """ Search using given criteria
        """
        annotation = IAnnotations(self.context)
        layout = annotation.get(ANNO_FACETED_LAYOUT, 'faceted-preview-items')
        if layout != 'faceted-events-preview-items':
            return super(QueryHandler, self).query(batch, sort, **kwargs)

        if self.request:
            kwargs.update(self.request.form)
            kwargs.pop('sort[]', None)
            kwargs.pop('sort', None)

        # jQuery >= 1.4 adds type to params keys
        # $.param({ a: [2,3,4] }) // "a[]=2&a[]=3&a[]=4"
        # Let's fix this
        kwargs = dict((key.replace('[]', ''), val)
                      for key, val in kwargs.items())

        query = self.criteria(sort=sort, **kwargs)
        catalog = getUtility(IFacetedCatalog)
        try:
            brains = catalog(self.context, **query)
        except Exception, err:
            logger.exception(err)
            return Batch([], 20, 0)
        if not brains:
            return Batch([], 20, 0)

        # Apply after query (filter) on brains
        num_per_page = 20
        criteria = ICriteria(self.context)
        for cid, criterion in criteria.items():
            widgetclass = criteria.widget(cid=cid)
            widget = widgetclass(self.context, self.request, criterion)

            if widget.widget_type == 'resultsperpage':
                num_per_page = widget.results_per_page(kwargs)

            brains_filter = queryAdapter(widget, IWidgetFilterBrains)
            if brains_filter:
                brains = brains_filter(brains, kwargs)

        # Specific to cpskin.agenda faceted-events-preview-items view

        resultsByDays = self.organize(brains)
        resultsByDaysList = [{d: l} for d, l in resultsByDays.items()]
        resultsByDaysList = sorted(resultsByDaysList)

        if not batch:
            return resultsByDaysList

        b_start = safeToInt(kwargs.get('b_start', 0))
        orphans = num_per_page * 20 / 100  # orphans = 20% of items per page

        if isinstance(resultsByDaysList, GeneratorType):
            resultsByDaysList = [r for r in resultsByDaysList]

        return Batch(resultsByDaysList, num_per_page, b_start, orphan=orphans)
