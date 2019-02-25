Changelog
=========

1.2.14 (2019-02-25)
-------------------

- Fix weird bug with some events.
  [bsuttor]

- Limit categories to first element on agenda view : WEB-2866
  [laulaz]


1.2.13 (2018-09-11)
-------------------

- Hide past occurrences in events : #21524
  [daggelpop]


1.2.12 (2018-09-10)
-------------------

- Display booking fields in event summary : #20989
  [laulaz]


1.2.11 (2018-09-03)
-------------------

- Fix hard code type (#22092).
  [seb]


1.2.10 (2018-07-16)
-------------------

- Add Taxonomy field serializer.
  [bsuttor]


1.2.9 (2018-07-13)
------------------

- Add restapi serializer for occurence.
  [bsuttor]

- Improve agenda to show only date in the future
  [oxydedefer]


1.2.8 (2018-05-16)
------------------

- Improve / fix agenda sort order
  [laulaz]


1.2.7 (2018-05-14)
------------------

- Do not use acquisition to get contact into rss feed.
  [bsuttor]


1.2.6 (2018-05-14)
------------------

- Show description on ungrouped agenda view if needed : #21067
  [laulaz]

- Fix sort order on ungrouped agenda view
  [laulaz]

- Format phone for event summary view without related contacts.
  [bsuttor]

- Add target="_blank" to event_url in summary view.
  [bsuttor]


1.2.5 (2018-02-13)
------------------

- Also catalog zgeo_geometry for event without IRelatedContacts behavior.
  [bsuttor]


1.2.4 (2017-12-12)
------------------

- Include overrides.zcml into cpskin.policy.
  [bsuttor]


1.2.3 (2017-12-12)
------------------

- Override atomrss adapter to get related contact for event.
  [bsuttor]


1.2.2 (2017-11-22)
------------------

- Add setter and getter in new factory behavior.
  [bsuttor]


1.2.1 (2017-11-22)
------------------

- Do not use acquisition to get contact on event_view.
  [bsuttor]


1.2.0 (2017-11-22)
------------------

- Related Contact location is now used to get coordinates from event with a location.
zgeo_geometry_value is now in catalog with location related_contact value.
  [bsuttor]


1.1.18 (2017-10-30)
-------------------

- Improve website from related contacts.
  [bsuttor]


1.1.17 (2017-10-25)
-------------------

- Add categories on agenda ungrouped view : #18471
  [laulaz]

- Change events dates display to reflect index view
  [laulaz]


1.1.16 (2017-10-02)
-------------------

- Fix summary view if a phone number is not yet a list.
  [bsuttor]


1.1.15 (2017-09-13)
-------------------

- Fix batched events on faceted-agenda-ungrouped-view-items view : #18695
  [laulaz]


1.1.14 (2017-09-13)
-------------------

- Change order on event_summary view between organiser and contact.
  [bsuttor]


1.1.13 (2017-09-12)
-------------------

- Add a class on li of contact in event_summary view.
  [bsuttor]


1.1.12 (2017-09-12)
-------------------

- Set ical at the end of event summary view.
  [bsuttor]

- Use cpskin as i18n domain for event_summary.pt.
  [bsuttor]


1.1.11 (2017-09-12)
-------------------

- Order taxonomy fields for event summary view.
  [bsuttor]

- Check if taxonomies are list or string.
  [bsuttor]


1.1.10 (2017-08-30)
-------------------

- Fix events unbatching : #18540
  [laulaz]


1.1.9 (2017-07-26)
------------------

- Add missing i18n zcml header.
  [bsuttor]


1.1.8 (2017-07-17)
------------------

- Add new agenda 'ungrouped events' faceted view with special sort order
  [laulaz]


1.1.7 (2017-06-21)
------------------

- Fix get taxonomy value when token is no more an id.
  [bsuttor]


1.1.6 (2017-06-15)
------------------

- Add taxonomies to event_summary view.
  [bsuttor]

- Add new agenda faceted view and use same markup as index view
  Old faceted-events-preview-items is kept until all the sites are migrated
  [laulaz]


1.1.5 (2016-11-24)
------------------

- By default (if no search criteria), faceted-events-preview-items will show
  only future events : #15531
  [laulaz]


1.1.4 (2016-11-22)
------------------

- Fix not working limit parameter on events view : #15517
  [laulaz]

- Fix accented character for i18n extraction
  [mpeeters]


1.1.3 (2016-09-08)
------------------

- Minor HTML change to ease styling
  [laulaz]


1.1.2 (2016-09-02)
------------------

- View field when related contact behavior is not enable.
  [bsuttor]


1.1.1 (2016-09-02)
------------------

- Add more_occurrences_text property.
  [bsuttor]

- Change limit message text and id
  [laulaz]

- Fix tests
  [laulaz]


1.1.0 (2016-08-17)
------------------

- Use collection setting to limit numbers of days displayed in events results.
  This avoids overriding query() (thus fixes #14644) and remove the need for
  batching, as well as fixing #14646.
  [laulaz]


1.0.4 (2016-08-05)
------------------

- Handle results per page and pagination on event preview view
  [laulaz]


1.0.3 (2016-08-05)
------------------

- Get image scale for events previews from collection setting (if possible)
  [laulaz]


1.0.2 (2016-07-26)
------------------

- Need to unconfigure original daterange widget to make ours available
  [laulaz]

- Don't use today date by default for simpledate widget anymore
  [laulaz]

- Rename related contact behavior.
  [bsuttor]


1.0.1 (2016-06-08)
------------------

- Use today date by default for simpledate widget
  [laulaz]


1.0 (2016-06-02)
----------------

- Add override of plone.app.event event_summary view.
  [bsuttor]


0.1 (2016-06-01)
----------------

- Initial release
