from django.utils.translation import ugettext_lazy as _

from mayan.apps.navigation.classes import Link
from mayan.apps.navigation.utils import get_cascade_condition

from .icons import (
    icon_import_setup_backend_selection, icon_import_setup_delete,
    icon_import_setup_edit, icon_import_setup_execute,
    icon_import_setup_item_delete, icon_import_setup_item_process,
    icon_import_setup_items_clear, icon_import_setup_items_list,
    icon_import_setup_list, icon_import_setup_populate
)
from .permissions import (
    permission_import_setup_create, permission_import_setup_delete,
    permission_import_setup_edit, permission_import_setup_execute,
    permission_import_setup_view
)

link_import_setup_backend_selection = Link(
    icon_class=icon_import_setup_backend_selection,
    permissions=(permission_import_setup_create,),
    text=_('Create import setup'),
    view='importer:import_setup_backend_selection',
)
link_import_setup_delete = Link(
    args='resolved_object.pk',
    icon_class=icon_import_setup_delete,
    permissions=(permission_import_setup_delete,),
    tags='dangerous', text=_('Delete'), view='importer:import_setup_delete'
)
link_import_setup_edit = Link(
    args='resolved_object.pk',
    icon_class=icon_import_setup_edit,
    permissions=(permission_import_setup_edit,), text=_('Edit'),
    view='importer:import_setup_edit'
)
link_import_setup_execute = Link(
    args='resolved_object.pk',
    icon_class=icon_import_setup_execute,
    permissions=(permission_import_setup_execute,), text=_('Execute'),
    view='importer:import_setup_execute'
)
link_import_setup_item_multiple_delete = Link(
    icon_class=icon_import_setup_item_delete,
    permissions=(permission_import_setup_edit,),
    tags='dangerous', text=_('Delete'),
    view='importer:import_setup_item_multiple_delete'
)
link_import_setup_item_multiple_process = Link(
    icon_class=icon_import_setup_item_process,
    permissions=(permission_import_setup_edit,),
    text=_('Process'), view='importer:import_setup_item_multiple_process'
)
link_import_setup_items_clear = Link(
    args='resolved_object.pk',
    icon_class=icon_import_setup_items_clear,
    permissions=(permission_import_setup_execute,), text=_('Clear items'),
    view='importer:import_setup_items_clear'
)
link_import_setup_items_list = Link(
    args='resolved_object.pk',
    icon_class=icon_import_setup_items_list,
    permissions=(permission_import_setup_view,), text=_('Items'),
    view='importer:import_setup_items_list'
)
link_import_setup_list = Link(
    icon_class=icon_import_setup_list,
    text=_('Import setup list'),
    view='importer:import_setup_list'
)
link_import_setup_populate = Link(
    args='resolved_object.pk',
    icon_class=icon_import_setup_populate,
    permissions=(permission_import_setup_execute,), text=_('Populate'),
    view='importer:import_setup_populate'
)
link_import_setup_setup = Link(
    condition=get_cascade_condition(
        app_label='importer', model_name='ImportSetup',
        object_permission=permission_import_setup_view,
        view_permission=permission_import_setup_create,
    ), icon_class=icon_import_setup_list,
    text=_('Importer'),
    view='importer:import_setup_list'
)
