import logging

from django.utils import six
from django.utils.translation import ugettext_lazy as _

# Change this to mayan.apps.common.class_mixins for Mayan EDMS 3.5
from credentials.compat import AppsModuleLoaderMixin

logger = logging.getLogger(name=__name__)

__all__ = ('ImportSetupBackend',)


class ImportSetupBackendMetaclass(type):
    _registry = {}

    def __new__(mcs, name, bases, attrs):
        new_class = super().__new__(
            mcs, name, bases, attrs
        )
        if not new_class.__module__ == 'importer.classes':
            mcs._registry[
                '{}.{}'.format(new_class.__module__, name)
            ] = new_class

        return new_class


class ImportSetupBackendBase(AppsModuleLoaderMixin):
    """
    Base class for the backends.

    The fields attribute is a list of dictionaries with the format:
    {
        'name': ''  # Field internal name
        'label': ''  # Label to show to users
        'initial': ''  # Field initial value
        'default': ''  # Default value.
    }

    """
    fields = {}

    @classmethod
    def get_class_fields(cls):
        backend_field_list = getattr(cls, 'fields', {}).keys()
        return getattr(cls, 'class_fields', backend_field_list)


class ImportSetupBackend(
    six.with_metaclass(ImportSetupBackendMetaclass, ImportSetupBackendBase)
):
    _loader_module_name = 'importers'

    @classmethod
    def get(cls, name):
        return cls._registry[name]

    @classmethod
    def get_all(cls):
        return cls._registry

    @classmethod
    def get_choices(cls):
        return sorted(
            [
                (
                    key, backend.label
                ) for key, backend in cls.get_all().items()
            ], key=lambda x: x[1]
        )

    def __init__(self, **kwargs):
        for class_field in getattr(self, 'class_fields', ()):
            setattr(self, class_field, kwargs.get(class_field, None))

        self.credential_class = kwargs.get('credential_class', None)
        self.credential_data = kwargs.get('credential_data', None)

    def check_valid(self, identifier, data):
        return True


class NullBackend(ImportSetupBackend):
    label = _('Null backend')
