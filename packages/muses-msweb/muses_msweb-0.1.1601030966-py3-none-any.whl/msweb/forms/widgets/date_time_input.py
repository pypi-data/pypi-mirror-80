from django.forms import DateTimeInput as Dti


class DateTimeInput(Dti):
    def __init__(self, attrs=None, fmt=None):
        super().__init__(attrs, fmt)
        self.attrs.update({'class': 'input'})
