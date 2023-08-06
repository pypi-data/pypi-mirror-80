from datetime import datetime, date

from django.core.exceptions import ValidationError


def not_passed(value: date):
    if not ((value - datetime.now()).total_seconds() > 0):
        raise ValidationError('%(value)s is passed', params={'value': value})
