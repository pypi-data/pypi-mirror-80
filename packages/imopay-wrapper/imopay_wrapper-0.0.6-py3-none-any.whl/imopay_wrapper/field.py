from dataclasses import Field, MISSING


class ImopayField(Field):
    def __init__(
        self, opitional, default, default_factory, init, repr, hash, compare, metadata
    ):

        self.optional = opitional

        super().__init__(default, default_factory, init, repr, hash, compare, metadata)


# This function is used instead of exposing Field creation directly,
# so that a type checker can be told (via overloads) that this is a
# function whose type depends on its parameters.
def field(
    *,
    optional=False,
    default=MISSING,
    default_factory=MISSING,
    init=True,
    repr=True,
    hash=None,
    compare=True,
    metadata=None,
):
    """Return an object to identify dataclass fields.

    default is the default value of the field.  default_factory is a
    0-argument function called to initialize a field's value.  If init
    is True, the field will be a parameter to the class's __init__()
    function.  If repr is True, the field will be included in the
    object's repr().  If hash is True, the field will be included in
    the object's hash().  If compare is True, the field will be used
    in comparison functions.  metadata, if specified, must be a
    mapping which is stored but not otherwise examined by dataclass.

    It is an error to specify both default and default_factory.
    """

    if default is not MISSING and default_factory is not MISSING:
        raise ValueError("cannot specify both default and default_factory")
    return ImopayField(
        optional, default, default_factory, init, repr, hash, compare, metadata
    )
