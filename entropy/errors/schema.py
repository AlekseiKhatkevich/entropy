from dataclasses import dataclass, field
from string import Template
from typing import ClassVar


@dataclass(frozen=True)
class ErrorMessage:
    """
    Class represents error message + metadata

    section - error section eg. (auth, files, etc)
    error_code_number - int error code eg. 46
    title - short human readable error description
    detail - error full text
    error_code - final error code to be sent to FE , eg 'auth_1'
    """
    section: str
    error_code_number: int

    title: str
    detail: str

    error_code_template: ClassVar[str] = Template('${section}_${error_code_number}')
    error_code: str = field(init=False)

    code_to_instance: ClassVar[dict] = {}

    def __post_init__(self):
        """
        Dynamically creates error_code
        """
        # https://stackoverflow.com/questions/53756788/
        # how-to-set-the-value-of-dataclass-field-in-post-init-when-frozen-true
        super().__setattr__('error_code', self.error_code_template.substitute(
                section=self.section,
                error_code_number=self.error_code_number,
            ),
        )

    def __str__(self):
        return rf'{self.error_code} --- {self.title}'

    def __iter__(self):
        """
        Method __iter__  implemented in order to use class instance as an 'Exception' argument
        with unpacking operator *.
        Exception(*ErrorMessage(*args, **kwargs)) ->
        -> Exception(message=self, code=self)
        """
        # noinspection PyRedundantParentheses
        yield from (self, self.error_code)

    def __new__(cls, section, error_code_number, *args, **kwargs):
        """
        Singleton pattern implementation. If we already have class instance with a specific
        error code, then we probably don't need to create another one and had better reuse one
        already created.
        """
        code = cls.error_code_template.substitute(
            section=section,
            error_code_number=error_code_number,
        )

        try:
            instance = cls.code_to_instance[code]
        except KeyError:
            instance = super().__new__(cls)
            cls.code_to_instance[code] = instance

        return instance
