import unittest2 as unittest

from cpskin.agenda.testing import CPSKIN_AGENDA_INTEGRATION_TESTING


class TestProfiles(unittest.TestCase):

    layer = CPSKIN_AGENDA_INTEGRATION_TESTING

    def setUp(self):
        self.portal = self.layer['portal']
