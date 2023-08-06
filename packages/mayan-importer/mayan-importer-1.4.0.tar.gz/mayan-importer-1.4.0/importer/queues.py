from django.utils.translation import ugettext_lazy as _

from mayan.apps.task_manager.classes import CeleryQueue
from mayan.apps.task_manager.workers import worker_medium

queue_importer = CeleryQueue(
    label=_('Importer'), name='importer', worker=worker_medium
)

queue_importer.add_task_type(
    label=_('Process an import setup'),
    dotted_path='importer.tasks.task_import_setup_process'
)
queue_importer.add_task_type(
    label=_('Process an import setup item'),
    dotted_path='importer.tasks.task_import_setup_item_process'
)
queue_importer.add_task_type(
    label=_('Populate the items of an import setup'),
    dotted_path='importer.tasks.task_import_setup_populate'
)
