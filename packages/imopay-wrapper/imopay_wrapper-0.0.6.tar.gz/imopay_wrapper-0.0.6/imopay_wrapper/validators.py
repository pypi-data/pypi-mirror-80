import re

from datetime import date

from .exceptions import FieldError


def _get_value_from_attr_or_value(obj, attr, value=None):
    """
    Método para extrair um valor de algum atributo do objeto.

    Caso seja passado um `value`, retorna o próprio value!

    Pode retornar None caso o atributo não exista!
    """
    if value is None:
        value = getattr(obj, attr, None)
    return value


def validate_obj_attr_type(obj, attr, types, value=None):
    """
    Método para validar que o valor de um atributo do objeto
    é de um determinado tipo.

    Note:
        pode ser passado uma tupla de tipos, o isinstance aceita isso!

    Caso o valor não seja do tipo, lança o erro!
    """
    value = _get_value_from_attr_or_value(obj, attr, value=value)

    if not isinstance(value, types):
        raise FieldError(attr, f"{value} não é do tipo {types}")


def validate_obj_attr_in_collection(obj, attr, collection, value=None):
    """
    Método para validar que o valor de um atributo do objeto
    está na coleção de possíveis valores.

    Caso o valor não esteja na coleção, lança o erro!
    """
    value = _get_value_from_attr_or_value(obj, attr, value=value)

    if value not in collection:
        raise FieldError(attr, f"{value} não está na coleção {collection}")


def validate_obj_attr_regex(obj, attr, regex, value=None):
    """
    Método para validar que o valor de um atributo do objeto
    é do formato de um determinado regex.

    Caso o valor não siga o regex, lança o erro!
    """
    value = _get_value_from_attr_or_value(obj, attr, value=value)

    result = re.search(regex, value)
    if result is None:
        raise FieldError(attr, f"{value} não é do formato f{regex}!")


def validate_date_1_gt_date_2(attr, d1, d2, allow_equal=False):
    """
    Método para validar se data 1 é maior do que data 2.

    Caso allow_equal seja True, data 1 pode ser igual à data 2.
    """
    if allow_equal:
        if d1 < d2:
            raise FieldError(attr, f"{d1} não é igual ou maior do que {d2}")

    elif d1 <= d2:
        raise FieldError(attr, f"{d1} não é estritamente maior do que {d2}")


def validate_date_isoformat(
    obj, attr, future=None, past=None, allow_today=False, value=None
):
    """
    Método para validar uma data que siga a iso YYYY-mm-dd
    https://en.wikipedia.org/wiki/ISO_8601

    É possível validar se é uma data futura ou passada também!

    Com o allow_today é possível flexibilizar se é
    permitido a data de hoje ou não!
    """
    if past and future:
        raise ValueError(
            "Não se pode verificar se é uma data futura e passada ao mesmo tempo!"
        )

    value = _get_value_from_attr_or_value(obj, attr, value=value)

    d = date.fromisoformat(value)

    today = date.today()

    if past:
        try:
            validate_date_1_gt_date_2(attr, today, d, allow_equal=allow_today)
        except FieldError as e:
            raise FieldError(attr, f"{value} não é uma data do passado!") from e

    if future:
        try:
            validate_date_1_gt_date_2(attr, d, today, allow_equal=allow_today)
        except FieldError as e:
            raise FieldError(attr, f"{value} não é uma data do futuro!") from e
