import json

from django.conf import settings
from django.contrib.humanize.templatetags.humanize import intcomma
from django.db import models, transaction
from django.utils.module_loading import import_string
from django.utils.translation import ugettext_lazy as _

from mayan.apps.common.serialization import yaml_load
from mayan.apps.common.validators import YAMLValidator
from mayan.apps.documents.models.document_type_models import DocumentType
from mayan.apps.events.classes import (
    EventManagerMethodAfter, EventManagerSave
)
from mayan.apps.events.decorators import method_event
from mayan.apps.metadata.models import MetadataType

from credentials.models import StoredCredential

from .classes import NullBackend
from .events import (
    event_import_setup_created, event_import_setup_edited,
    event_import_setup_executed
)
from .literals import (
    DEFAULT_PROCESS_SIZE, ITEM_STATE_CHOICES, ITEM_STATE_COMPLETE,
    ITEM_STATE_DOWNLOADED, ITEM_STATE_ERROR, ITEM_STATE_QUEUED,
    ITEM_STATE_NONE, SETUP_STATE_CHOICES, SETUP_STATE_ERROR,
    SETUP_STATE_EXECUTING, SETUP_STATE_NONE, SETUP_STATE_POPULATING
)
from .tasks import task_import_setup_item_process


class BackendModelMixin(models.Model):
    backend_path = models.CharField(
        max_length=128,
        help_text=_('The dotted Python path to the backend class.'),
        verbose_name=_('Backend path')
    )
    backend_data = models.TextField(
        blank=True, verbose_name=_('Backend data')
    )

    class Meta:
        abstract = True

    def get_backend(self):
        """
        Retrieves the backend by importing the module and the class.
        """
        try:
            return import_string(dotted_path=self.backend_path)
        except ImportError:
            return NullBackend

    def get_backend_label(self):
        """
        Return the label that the backend itself provides. The backend is
        loaded but not initialized. As such the label returned is a class
        property.
        """
        return self.get_backend().label

    get_backend_label.short_description = _('Backend')
    get_backend_label.help_text = _('The backend class for this entry.')

    def get_backend_data(self):
        return json.loads(s=self.backend_data or '{}')

    def set_backend_data(self, obj):
        self.backend_data = json.dumps(obj=obj)


class ImportSetup(BackendModelMixin, models.Model):
    label = models.CharField(
        help_text=_('Short description of this import setup.'), max_length=128,
        unique=True, verbose_name=_('Label')
    )
    credential = models.ForeignKey(
        on_delete=models.CASCADE, related_name='import_setups',
        to=StoredCredential, verbose_name=_('Credential')
    )
    document_type = models.ForeignKey(
        on_delete=models.CASCADE, related_name='import_setups',
        to=DocumentType, verbose_name=_('Document type')
    )
    process_size = models.PositiveIntegerField(
        default=DEFAULT_PROCESS_SIZE, help_text=_(
            'Number of items to process per execution.'
        ), verbose_name=_('Process size.')
    )
    metadata_map = models.TextField(
        blank=True, help_text=_(
            'A YAML encoded dictionary to save the content of the item '
            'properties as metadata values. The dictionary must consist of '
            'an import item property key matched to a metadata type name.'
        ), validators=[YAMLValidator()], verbose_name=_('Metadata map')
    )
    state = models.PositiveIntegerField(
        choices=SETUP_STATE_CHOICES, default=SETUP_STATE_NONE, help_text=_(
            'The last recorded state of the import setup.'
        ), verbose_name=_('State')
    )

    class Meta:
        ordering = ('label',)
        verbose_name = _('Import setup')
        verbose_name_plural = _('Import setups')

    def __str__(self):
        return self.label

    def execute(self):
        """
        Iterate of the ImportSetupItem instances downloading and creating
        documents from them.
        """
        self.state = SETUP_STATE_EXECUTING
        self.save()

        try:
            queryset = self.items.filter(state=ITEM_STATE_NONE)[:self.process_size]

            for item in queryset.all():
                task_import_setup_item_process.apply_async(
                    kwargs={
                        'import_setup_item_id': item.pk
                    }
                )
        except Exception:
            self.state = SETUP_STATE_ERROR
            self.save()

            if settings.DEBUG:
                raise
        else:
            self.state = SETUP_STATE_NONE
            self.save()

    @method_event(
        event_manager_class=EventManagerMethodAfter,
        event=event_import_setup_executed,
        target='self',
    )
    def get_backend_instance(self):
        return self.get_backend()(
            credential_class=self.credential.get_backend(),
            credential_data=self.credential.get_backend_data(),
            kwargs=self.get_backend_data()
        )

    def get_state_label(self):
        return self.get_state_display()
    get_state_label.short_description = _('State')
    get_state_label.help_text = _(
        'The last recorded state of the setup item. The field will be '
        'sorted by the numeric value of the state and not the actual text.'
    )

    def item_count_all(self):
        return self.items.count()

    item_count_all.short_description = _('Items')

    def item_count_complete(self):
        return self.items.filter(state=ITEM_STATE_COMPLETE).count()

    item_count_complete.short_description = _('Items complete')

    def item_count_percent(self):
        items_complete = self.item_count_complete()
        items_all = self.item_count_all()

        if items_all == 0:
            percent = 0
        else:
            percent = items_complete / items_all * 100.0

        return '{} of {} ({:.0f}%)'.format(
            intcomma(value=items_complete), intcomma(value=items_all),
            percent
        )

    item_count_percent.short_description = _('Progress')

    def items_clear(self):
        self.items.all().delete()

    def populate_items(self):
        self.state = SETUP_STATE_POPULATING
        self.save()

        try:
            backend = self.get_backend_instance()

            for item in backend.get_item_list():
                setup_item, created = self.items.get_or_create(
                    identifier=item[backend.item_identifier]
                )
                if created:
                    setup_item.set_metadata(
                        obj=item
                    )
                    setup_item.save()
        except Exception:
            self.state = SETUP_STATE_ERROR
            self.save()

            if settings.DEBUG:
                raise
        else:
            self.state = SETUP_STATE_NONE
            self.save()

    @method_event(
        event_manager_class=EventManagerSave,
        created={
            'event': event_import_setup_created,
            'target': 'self',
        },
        edited={
            'event': event_import_setup_edited,
            'target': 'self',
        }
    )
    def save(self, *args, **kwargs):
        return super().save(*args, **kwargs)


class ImportSetupItem(models.Model):
    import_setup = models.ForeignKey(
        on_delete=models.CASCADE, related_name='items',
        to=ImportSetup, verbose_name=_('Import setup')
    )
    identifier = models.CharField(
        db_index=True, max_length=64, verbose_name=_('Identifier')
    )
    metadata = models.TextField(blank=True, verbose_name=_('Metadata'))
    state = models.IntegerField(
        choices=ITEM_STATE_CHOICES, default=ITEM_STATE_NONE,
        verbose_name=_('State')
    )
    state_data = models.TextField(blank=True, verbose_name=_('State data'))

    class Meta:
        verbose_name = _('Import setup item')
        verbose_name_plural = _('Import setup items')

    def __str__(self):
        return self.identifier

    def create_document(self, shared_uploaded_file):
        """
        Create a document from a downloaded ImportSetupItem instance.
        """
        backend_class = self.import_setup.get_backend()

        document = None

        with transaction.atomic():
            try:
                with shared_uploaded_file.open() as file_object:
                    document = self.import_setup.document_type.new_document(
                        file_object=file_object, label=self.get_metadata_key(
                            key=backend_class.item_label
                        )
                    )
            except Exception as exception:
                self.state = ITEM_STATE_ERROR
                self.state_data = str(exception)
                self.save()
                if settings.DEBUG:
                    raise
            else:
                self.state = ITEM_STATE_COMPLETE
                self.state_data = ''
                self.save()

        if document:
            item_setup_metadata_map = yaml_load(
                stream=self.import_setup.metadata_map or '{}'
            )

            for key, metadata_name in item_setup_metadata_map.items():
                document.metadata.create(
                    metadata_type=MetadataType.objects.get(name=metadata_name),
                    value=self.get_metadata_key(key=key)
                )

    @method_event(
        event_manager_class=EventManagerMethodAfter,
        event=event_import_setup_edited,
        action_object='self',
        target='import_setup',
    )
    def delete(self):
        return super().delete()

    def download(self):
        shared_uploaded_file = None

        with transaction.atomic():
            try:
                backend_instance = self.import_setup.get_backend_instance()
                shared_uploaded_file = backend_instance.get_item(
                    identifier=self.identifier
                )
            except Exception as exception:
                self.state = ITEM_STATE_ERROR
                self.state_data = str(exception)
                self.save()
                if settings.DEBUG:
                    raise
            else:
                self.state = ITEM_STATE_DOWNLOADED
                self.state_data = ''
                self.save()

        return shared_uploaded_file

    def get_metadata(self):
        return json.loads(s=self.metadata or '{}')

    def get_metadata_display(self):
        metadata = self.get_metadata()
        metadata.pop('id')
        return ', '.join(
            ['{}: {}'.format(key, value) for key, value in metadata.items()]
        )
    get_metadata_display.short_description = _('Metadata')

    def get_metadata_key(self, key):
        return self.get_metadata().get(key, self.id)

    def set_metadata(self, obj):
        self.metadata = json.dumps(obj=obj)

    def get_state_label(self):
        return self.get_state_display()
    get_state_label.help_text = _(
        'The last recorded state of the item. The field will be sorted by '
        'the numeric value of the state and not the actual text.'
    )
    get_state_label.short_description = _('State')

    def process(self):
        shared_uploaded_file = self.download()

        if shared_uploaded_file:
            self.create_document(shared_uploaded_file=shared_uploaded_file)
