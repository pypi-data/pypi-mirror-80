from dataclasses import dataclass
from typing import Union, Any
import inspect

from ..exceptions import FieldError, ValidationError


@dataclass
class BaseImopayObj:
    VALIDATION_METHOD_PATTERN = "_validate"

    def __post_init__(self):
        self.__run_validators()
        self._init_nested_fields()

    def _init_nested_fields(self):
        pass

    @classmethod
    def get_fields(cls):
        """
        Método para retornar todos os campos!
        """
        # noinspection PyUnresolvedReferences
        return cls.__dataclass_fields__

    def __get_field(self, name):
        """
        Método para retornar um campo com base no nome passado!
        """
        try:
            # noinspection PyUnresolvedReferences
            return self.get_fields()[name]
        except KeyError as e:
            raise AttributeError(f"Não existe o campo {name} em {self}") from e

    @staticmethod
    def __is_field_optional(field):
        """
        Método para verificar se um campo é opcional ou não!

        Influência na validação!
        """
        return getattr(field, "optional", False)

    def __get_validation_methods(self):
        """
        Método para pegar a lista de métodos de validação
        que seguem o padrão de nomenclatura `_validate`.
        """
        data = inspect.getmembers(self, predicate=inspect.ismethod)

        validation_methods = [
            item[1] for item in data if self.VALIDATION_METHOD_PATTERN in item[0]
        ]

        return validation_methods

    @staticmethod
    def __get_attr_name_from_method(method):
        """
        Método para retornar o nome do atributo/campo a partir de
        um método de validação (que siga o padrão `_validate_attr`).
        """
        name = method.__name__

        initial_index = len(BaseImopayObj.VALIDATION_METHOD_PATTERN) + 1

        return name[initial_index:]

    def __run_validators(self):
        """
        Método que executa todos os métodos de validação.
        """
        validation_methods = self.__get_validation_methods()

        errors = []

        for method in validation_methods:
            error = None
            attr_name = self.__get_attr_name_from_method(method)
            field = self.__get_field(attr_name)
            try:
                method()
            except FieldError as e:
                error = e
            except Exception as e:
                error = FieldError(method.__name__, str(e))
            finally:
                if error is not None and not self.__is_field_optional(field):
                    errors.append(error)

        if errors:
            raise ValidationError(self, errors)

    @staticmethod
    def __is_empty_value(value):
        return value == "" or value is None

    @classmethod
    def from_dict(cls, data: Union[dict, Any]):
        if data is None:
            data = {}

        missing_fields = {
            field_name
            for field_name in cls.get_fields().keys()
            if field_name not in data.keys()
        }

        for missing_field in missing_fields:
            data[missing_field] = None

        # noinspection PyArgumentList
        return cls(**data)

    def to_dict(self):
        data = {}
        for field_name, field in self.get_fields().items():
            value = getattr(self, field_name)

            if self.__is_empty_value(value):
                continue

            if isinstance(value, BaseImopayObj):
                data[field_name] = value.to_dict()
            else:
                data[field_name] = field.type(value)
        return data
