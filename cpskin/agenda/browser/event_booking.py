from cpskin.agenda.browser.event_summary import EventContactSummaryView
from zope.annotation.interfaces import IAnnotations
from plone.app.imagecropping import PAI_STORAGE_KEY


class EventBooking(EventContactSummaryView):
    """
    """

    def get_good_banner(self):
        img = None
        if self.context.image_header and self.has_crop(
            self.context, "image_header", "banner_event"
        ):
            img = "@@images/image_header/banner_event"
        if (
            img is None
            and self.context.image_header
            and self.has_crop(self.context, "image_header", "banner")
        ):
            img = "@@images/image_header/banner"
        if img is None and self.context.image_header:
            img = "@@images/image_header"
        if (
            img is None
            and self.context.image
            and self.has_crop(self.context, "image", "banner_event")
        ):
            img = "@@images/image/banner_event"
        if (
            img is None
            and self.context.image
            and self.has_crop(self.context, "image", "banner")
        ):
            img = "@@images/image/banner"
        if img is None and self.context.image:
            img = "@@images/image"
        if img is None:
            return img
        else:
            return "{}/{}".format(self.data.url, img)

    def has_crop(self, obj, fieldname, scale):
        crops = IAnnotations(obj).get(PAI_STORAGE_KEY)
        if not crops:
            return False
        return "{0:s}_{1:s}".format(fieldname, scale) in crops

    def get_str_location(self):
        location = super(EventBooking, self).get_location()
        number = ": {}".format(location.number) if location.number else u""
        street = location.street.encode("utf-8") if location.street else u""
        zip_code = location.zip_code or u""
        city = location.city.encode("utf-8") if location.city else u""
        return "{} {} {}, {} {}".format(
            location.Title(), number, street, zip_code, city
        )
