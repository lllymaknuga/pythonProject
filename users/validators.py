from django.core.validators import RegexValidator
from django.utils.deconstruct import deconstructible
from django.utils.regex_helper import _lazy_re_compile
from django.utils.translation import ugettext_lazy as _


@deconstructible
class TelephoneNumberValidator(RegexValidator):
    """Проверяет номера телефона."""
    regex = _lazy_re_compile(r'^(+7\d{10})$')
    message = _('Неверный формат телефонного номера.'
                ' Необходим формат +7XXXXXXXXXX .')

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def __eq__(self, other):
        return (
                isinstance(other, TelephoneNumberValidator) and
                super().__eq__(other)
        )