Changelog
=========

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
