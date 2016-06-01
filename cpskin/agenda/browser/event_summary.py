# -*- coding: utf-8 -*-
from plone.app.event.browser.event_summary import EventSummaryView


class EventContactSummaryView(EventSummaryView):

    def get_organizer(self):
        if self.context.organizer is None:
            return None
        else:
            return self.context.organizer.to_object

    def get_contact(self):
        if self.context.contact is None:
            return None
        else:
            return self.context.contact.to_object

    def get_location(self):
        if self.context.location is None:
            return None
        else:
            return self.context.location.to_object

    def get_partners(self):
        if not self.context.partners:
            return None
        else:
            partners = [p.to_object for p in self.context.partners]
            return partners
