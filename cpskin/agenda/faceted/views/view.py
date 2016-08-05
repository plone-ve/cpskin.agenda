# -*- coding: utf-8 -*-

from Products.Five.browser import BrowserView
from zope.component import getMultiAdapter


class EventsView(BrowserView):
    """
    """

    def render_event_preview(self, obj):
        context = self.context
        request = self.request
        scale = getattr(context, 'collection_image_scale', 'thumb')
        request['scale'] = scale
        view = getMultiAdapter((obj, request),
                                name=u'faceted-event-preview-item')
        return view and view() or ''
