# -*- coding: utf-8 -*-

from collective.js.jqueryui.viewlet import L10nDatepicker
from eea.facetednavigation.widgets.daterange.widget import Widget as BaseWidget

from cpskin.locales import CPSkinMessageFactory as _


class Widget(BaseWidget, L10nDatepicker):
    """
    Date range Widget specific to events
    """
    widget_type = 'daterange'
    widget_label = _('Date range for events')

    def query(self, form):
        """
        Execute special treatment on basic widget query() result to handle
        search based on 2 indexes
        """
        query = super(Widget, self).query(form)
        if not query:
            return query
        index, params = query.popitem()
        start = params['query'][0]
        end = params['query'][1]
        query = {}
        # All events from start date ongoing:
        # The minimum end date of events is the date from which we search.
        query['end'] = {'query': start, 'range': 'min'}
        # All events until end date:
        # The maximum start date must be the date until we search.
        query['start'] = {'query': end, 'range': 'max'}
        return query
