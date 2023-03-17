import re
from rest_framework.serializers import ValidationError


def username_validator(value):

    if value == 'me':
        raise ValidationError('Cоздание пользователя me запрещено')
    checked_value = re.match('^[\\w.@+-]+', value)
    if checked_value is None or checked_value.group() != value:
        forbidden_simbol = value[0] if (
            checked_value is None
        ) else value[checked_value.span()[1]]
        raise ValidationError(f'Нельзя использовать символ {forbidden_simbol} '
                              'в username. Имя пользователя может содержать '
                              'только буквы, цифры и символы @ . + - _.')
    return value
