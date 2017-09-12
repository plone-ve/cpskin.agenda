# -*- coding: utf-8 -*-
from collective.js.jqueryui.utils import get_datepicker_date_format
from collective.js.jqueryui.utils import get_python_date_format
from collective.js.jqueryui.viewlet import L10nDatepicker
from cpskin.locales import CPSkinMessageFactory as _
from DateTime import DateTime
from datetime import datetime
from eea.facetednavigation.widgets import ViewPageTemplateFile
from eea.facetednavigation.widgets.widget import Widget as AbstractWidget

import logging


logger = logging.getLogger('cpskin.agenda')


class Widget(AbstractWidget, L10nDatepicker):
    """
    Simple date Widget specific to events
    """
    widget_type = 'simpledate'
    widget_label = _('Simple date for events')
    view_js = '++resource++cpskin.agenda.widgets.simpledate.view.js'
    edit_js = '++resource++cpskin.agenda.widgets.simpledate.edit.js'
    view_css = '++resource++cpskin.agenda.widgets.simpledate.view.css'
    edit_css = '++resource++cpskin.agenda.widgets.simpledate.edit.css'

    index = ViewPageTemplateFile('widget.pt')
    edit_schema = AbstractWidget.edit_schema.copy()

    @property
    def default(self):
        """Return default value"""
        default = self.data.get('default', '')
        if not default:
            return ''
        default = default.strip()
        try:
            default = DateTime(datetime.strptime(default,
                                                 self.python_date_format))
            default = default.strftime(self.python_date_format)
        except Exception, err:
            logger.exception('%s => Date: %s', err, default)
            default = ''
        return default

    def query(self, form):
        """Get value from form and return a catalog dict query"""
        query = {}
        if self.hidden:
            date = self.default
        else:
            value = form.get(self.data.getId(), ())
            if not value:
                return query
            date = value
        try:
            date = DateTime(datetime.strptime(date,
                                              self.python_date_format))
        except Exception, err:
            logger.exception(err)
            return query
        start = end = date
        start = start - 1
        start = start.latestTime()
        end = end.latestTime()
        query['end'] = {'query': start, 'range': 'min'}
        query['start'] = {'query': end, 'range': 'max'}
        return query

    @property
    def js_date_format(self):
        """Return the date format to use with JS datepicker"""
        return get_datepicker_date_format(self.request)

    @property
    def python_date_format(self):
        """Return the date format to use in python"""
        return get_python_date_format(self.request)

    @property
    def js_language(self):
        """Return the language to use with JS code"""
        return self.jq_language()
