from ..models import ImportSetup

from .literals import (
    TEST_IMPORT_SETUP_LABEL, TEST_IMPORT_SETUP_LABEL_EDITED,
    TEST_IMPORT_SETUP_PROCESS_SIZE, TEST_IMPORTER_BACKEND_PATH
)
from .test_importers import TestImporter


class ImportSetupTestMixin:
    def _create_test_import_setup(self):
        self.test_import_setup = ImportSetup.objects.create(
            backend_path=TEST_IMPORTER_BACKEND_PATH,
            label=TEST_IMPORT_SETUP_LABEL,
            document_type=self.test_document_type
        )


class ImportSetupItemTestMixin:
    def _create_test_import_setup_item(self):
        test_item_list = TestImporter().get_item_list()
        self.test_import_setup_item = self.test_import_setup.items.create(
            identifier=test_item_list[0].id
        )


class ImportSetupViewTestMixin:
    def _request_test_import_setup_backend_selection_view(self):
        return self.post(
            viewname='importer:import_setup_backend_selection', data={
                'backend': TEST_IMPORTER_BACKEND_PATH,
            }
        )

    def _request_test_import_setup_create_view(self):
        return self.post(
            viewname='importer:import_setup_create', kwargs={
                'class_path': TEST_IMPORTER_BACKEND_PATH
            }, data={
                'label': TEST_IMPORT_SETUP_LABEL,
                'document_type': self.test_document_type.pk,
                'process_size': TEST_IMPORT_SETUP_PROCESS_SIZE,
            }
        )

    def _request_test_import_setup_delete_view(self):
        return self.post(
            viewname='importer:import_setup_delete', kwargs={
                'import_setup_id': self.test_import_setup.pk
            }
        )

    def _request_test_import_setup_edit_view(self):
        return self.post(
            viewname='importer:import_setup_edit', kwargs={
                'import_setup_id': self.test_import_setup.pk
            }, data={
                'label': TEST_IMPORT_SETUP_LABEL_EDITED,
                'credential': self.test_credential.pk,
                'document_type': self.test_document_type.pk,
                'process_size': TEST_IMPORT_SETUP_PROCESS_SIZE
            }
        )

    def _request_test_import_setup_list_view(self):
        return self.get(viewname='importer:import_setup_list')


class ImportSetupItemViewTestMixin:
    def _request_test_import_setup_clear_view(self):
        return self.post(
            viewname='importer:import_setup_clear', kwargs={
                'import_setup_id': self.test_import_setup.pk
            }
        )

    def _request_test_import_setup_process_view(self):
        return self.post(
            viewname='importer:import_setup_process', kwargs={
                'import_setup_id': self.test_import_setup.pk
            }
        )

    def _request_test_import_setup_populate_view(self):
        return self.post(
            viewname='importer:import_setup_populate', kwargs={
                'import_setup_id': self.test_import_setup.pk
            }
        )
