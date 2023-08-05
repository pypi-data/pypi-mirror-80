"""module for shape validator."""
from typing import Dict, Any, Optional
from inflection import underscore, camelize
from ..field_description import FieldDescription, FieldType
from ..config import Config
from ..exceptions import ValidationException
from .validator import Validator
from ..utils.keypath import keypath
from ..utils.nonnull_note import NonnullNote
from ..fields import collection_argument_type_to_types


class ShapeValidator(Validator):
    """Shape validator validates a dict of values with defined shape."""

    def __init__(self, types: Dict[str, Any]) -> None:
        if not isinstance(types, dict):
            raise ValueError('argument passed to ShapeValidator should be dict')
        self.types = types

    def define(self, field_description: FieldDescription) -> None:
        field_description.field_type = FieldType.SHAPE
        field_description.shape_types = self.types

    def validate(self, value: Any, key_path: str, root: Any, all_fields: bool, config: Config) -> None:
        if value is None:
            return
        if not isinstance(value, dict):
            raise ValidationException(
                {key_path: f'Value \'{value}\' at \'{key_path}\' should be a dict.'},
                root
            )
        keypath_messages = {}
        for k, t in self.types.items():
            try:
                value_at_key = value[k]
            except KeyError:
                value_at_key = None
            types = collection_argument_type_to_types(t, config.linked_class)
            if types:
                try:
                    types.validator.validate(value_at_key, keypath(key_path, k), root, all_fields, config)
                except ValidationException as exception:
                    if all_fields:
                        keypath_messages.update(exception.keypath_messages)
                    else:
                        raise exception
        if len(keypath_messages) > 0:
            raise ValidationException(keypath_messages=keypath_messages, root=root)

    def transform(
        self,
        value: Any,
        key_path: str,
        root: Any,
        all_fields: bool,
        config: Config
    ) -> Optional[Dict[str, Any]]:
        if value is None:
            return None
        elif isinstance(value, NonnullNote):
            value = {}
        elif type(value) is not dict:
            return value
        unused_keys = list(self.types.keys())
        retval = {}
        for k, field_value in value.items():
            new_key = underscore(k) if config.camelize_json_keys else k
            if new_key in unused_keys:
                t = self.types[new_key]
                types = collection_argument_type_to_types(t, config.linked_class)
                if types:
                    retval[new_key] = types.validator.transform(
                        field_value, keypath(key_path, new_key), root, all_fields, config)
                else:
                    retval[new_key] = field_value
                unused_keys.remove(new_key)
        for k in unused_keys:
            retval[k] = None
        return retval

    def tojson(self, value: Any, config: Config) -> Optional[Dict[str, Any]]:
        if value is None:
            return None
        if type(value) is not dict:
            return value
        retval = {}
        for k, t in self.types.items():
            key = camelize(k, False) if config.camelize_json_keys else k
            try:
                value_at_key = value[k]
            except KeyError:
                value_at_key = None
            types = collection_argument_type_to_types(t, config.linked_class)
            if types:
                retval[key] = types.validator.tojson(value_at_key, config)
            else:
                retval[key] = value_at_key
        return retval
