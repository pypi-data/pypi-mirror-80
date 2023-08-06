from django.forms import DateInput as Di


class DateInput(Di):
    def __init__(self, attrs=None, fmt=None):
        super().__init__(attrs, fmt)
        self.attrs.update({'class': 'input'})
