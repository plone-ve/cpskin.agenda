# -*- coding: utf-8 -*-
from cpskin.agenda.dates import event_dates
from cpskin.agenda.faceted.views.view import is_in_range
from cpskin.agenda.faceted.views.view import sort_and_group
from cpskin.agenda.testing import CPSKIN_AGENDA_INTEGRATION_TESTING
from datetime import date
from datetime import datetime
from plone import api
from plone.app.event.dx.behaviors import IEventRecurrence

import pytz
import unittest2 as unittest


def createEvent(folder, id, start, end, whole_day=False):
    event = api.content.create(
        type='Event',
        id=id,
        title=id,
        container=folder,
        start=start,
        end=end,
        timezone='UTC',
        whole_day=whole_day)
    return event


def same(tuple1, tuple2):
    return sorted(tuple1) == sorted(tuple2)


class TestEventSearch(unittest.TestCase):

    layer = CPSKIN_AGENDA_INTEGRATION_TESTING

    def setUp(self):
        self.portal = self.layer['portal']
        self.app = self.layer['app']
        self.request = self.app.REQUEST
        self.folder = getattr(self.portal, 'folder')

    def test_get_dates(self):
        utc = pytz.utc
        start = datetime(2001, 1, 1, 10, 0, tzinfo=utc)
        end = datetime(2001, 1, 1, 11, 0, tzinfo=utc)

        event = createEvent(self.folder, '1', start, end)
        index = event_dates(event)()
        self.assertEqual(len(index), 1)
        self.assertEqual(index[0], date(2001, 1, 1))

        event = createEvent(self.folder, '2', start, end)
        event_rec = IEventRecurrence(event)
        event_rec.recurrence = 'RRULE:FREQ=DAILY;COUNT=4'
        event.reindexObject()
        index = event_dates(event)()
        self.assertEqual(len(index), 4)
        self.assertTrue(same(index, (date(2001, 1, 1), date(2001, 1, 2),
                                     date(2001, 1, 3), date(2001, 1, 4))))

    def test_is_in_range(self):
        start = date(2001, 1, 5)
        end = date(2001, 1, 7)
        self.assertFalse(is_in_range(date(2001, 1, 4), start, end))
        self.assertTrue(is_in_range(date(2001, 1, 5), start, end))
        self.assertTrue(is_in_range(date(2001, 1, 6), start, end))
        self.assertTrue(is_in_range(date(2001, 1, 7), start, end))
        self.assertFalse(is_in_range(date(2001, 1, 8), start, end))
        self.assertFalse(is_in_range(date(2001, 1, 4), start, None))
        self.assertTrue(is_in_range(date(2001, 1, 5), start, None))
        self.assertTrue(is_in_range(date(2001, 1, 8), start, None))
        self.assertTrue(is_in_range(date(2001, 1, 4), None, end))
        self.assertTrue(is_in_range(date(2001, 1, 7), None, end))
        self.assertFalse(is_in_range(date(2001, 1, 8), None, end))
        self.assertTrue(is_in_range(date(2001, 1, 8), None, None))

    def test_sort_and_group_simple(self):
        utc = pytz.utc
        start = datetime(2001, 1, 2, 10, 0, tzinfo=utc)
        end = datetime(2001, 1, 5, 9, 0, tzinfo=utc)
        createEvent(self.folder, '1', start, end)
        brains = api.content.find(portal_type='Event')
        self.assertEqual(len(brains), 1)
        result = sort_and_group(self.folder, brains, None, None)
        self.assertTrue(len(result), 4)
        self.assertTrue(same(
            result.keys(),
            [date(2001, 1, 2), date(2001, 1, 3),
             date(2001, 1, 4), date(2001, 1, 5)]))
        self.assertEqual(len(result.values()[0]['single']), 0)
        self.assertEqual(len(result.values()[0]['multi']), 1)

    def test_sort_and_group_multi(self):
        utc = pytz.utc
        start = datetime(2001, 1, 2, 10, 0, tzinfo=utc)
        end = datetime(2001, 1, 2, 11, 0, tzinfo=utc)
        createEvent(self.folder, '1', start, end)
        brains = api.content.find(portal_type='Event')
        self.assertEqual(len(brains), 1)
        result1 = sort_and_group(self.folder, brains,
                                 date(2001, 1, 2), date(2001, 1, 2))
        result2 = sort_and_group(self.folder, brains,
                                 date(2001, 1, 1), date(2001, 1, 2))
        result3 = sort_and_group(self.folder, brains,
                                 date(2001, 1, 2), date(2001, 1, 3))
        result4 = sort_and_group(self.folder, brains,
                                 date(2001, 1, 1), date(2001, 1, 3))
        self.assertTrue(len(result1), 1)
        self.assertTrue(result1 == result2 == result3 == result4)
        self.assertEqual(result1.keys()[0], date(2001, 1, 2))
        self.assertEqual(len(result1.values()[0]['single']), 1)
        self.assertEqual(len(result1.values()[0]['multi']), 0)
