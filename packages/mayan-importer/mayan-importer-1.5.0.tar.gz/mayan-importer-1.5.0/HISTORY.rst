1.5.0 (2020-09-25)
==================
- Add model filer to load and save models from and to CSV.

1.4.0 (2020-09-24)
==================
- Add import setup item completion event.
- Commit the import setup executed event when the execute
  method is called instead of the get get_backend_intsance.
- Add more tests.
- Rename fields and models for clarity. Item metadata field
  renamed to 'data' to avoid confusion with document metadata.
- Event, permission, and action named "Execute" is now "Process".
- Filter items by regular expressions during population and also
  during processing.
- Add team_admin_id field to the Dropbox backend to avoid an
  extra API call for each item to be imported.
- Multiple values are now cached for higher performance.
- Process and clear links are disabled for empty import setups.
- Smarter backend import error exclusion.
- Automatic backend keyword argument setup from dynamic fields.
- Support import item fields as attributes or dictionary keys.

1.3.0 (2020-09-23)
==================
- Add support to process individual items.
- Add background task support for individual items.
  Each item is now processed independently and in parallel.
- Add thousand comma separator to the progress summary column.

1.2.0 (2020-09-22)
==================
- Support Dropbox Team admin access.
- Add import setup state field.
- Add import setup item list view.
- Add import setup item delete view.

1.1.0 (2020-09-08)
==================
- Convert app into a general import app.
  Dropbox code moved into a separate importers module.

1.0.2 (2020-09-07)
==================
- Update absolute imports to self.

1.0.1 (2020-09-07)
==================
- Update absolute imports to the Credentials app.

1.0.0 (2020-09-01)
==================
- Initial release
