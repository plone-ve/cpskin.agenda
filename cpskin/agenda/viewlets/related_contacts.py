# -*- coding: utf-8 -*-

from plone.app.layout.viewlets import common


class RelatedContactsViewlet(common.ViewletBase):

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
        if not self.context.partner:
            return None
        else:
            partners = [p.to_object for p in self.context.partner]
            return partners

    def available(self):
        #Si au moins un des fields a été complété ==> return True
        if self.get_organizer() is not None or \
           self.get_contact() is not None or \
           self.get_location() is not None or \
           self.get_partner() is not None:
            return True
        else:
            return False
