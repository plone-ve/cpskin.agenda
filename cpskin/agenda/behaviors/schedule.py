# -*- coding: utf-8 -*-
from plone.app.contenttypes.interfaces import IEvent
from plone.autoform import directives as form
from plone.autoform.interfaces import IFormFieldProvider
from zope import schema
from zope.component import adapter
from zope.interface import implementer
from zope.interface import Interface
from zope.interface import provider


@provider(IFormFieldProvider)
class ISchedule(Interface):

    form.order_after(schedule='IEventRecurrence.recurrence')
    schedule = schema.Text(
        title=u'Schedule',
        required=False,
    )


@implementer(ISchedule)
@adapter(IEvent)
class Schedule(object):

    def __init__(self, context):
        self.context = context

    @property
    def schedule(self):
        return getattr(self.context, 'schedule', None)

    @schedule.setter
    def schedule(self, value):
        self.context.schedule = value
