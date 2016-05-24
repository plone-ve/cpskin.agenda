# -*- coding: utf-8 -*-

from plone import api
from plone.app.testing import applyProfile
import unittest2 as unittest

from cpskin.agenda.testing import CPSKIN_AGENDA_INTEGRATION_TESTING


class TestProfiles(unittest.TestCase):

    layer = CPSKIN_AGENDA_INTEGRATION_TESTING

    def setUp(self):
        self.portal = self.layer['portal']

    def test_reinstall(self):
        applyProfile(self.portal, 'cpskin.agenda:default')

    def test_product_is_installed(self):
        pid = 'cpskin.agenda'
        qi_tool = api.portal.get_tool('portal_quickinstaller')
        installed = [p['id'] for p in qi_tool.listInstalledProducts()]
        self.assertTrue(pid in installed)
