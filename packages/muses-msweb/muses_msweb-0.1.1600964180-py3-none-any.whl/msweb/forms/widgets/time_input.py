from django.forms import TimeInput as Tmi


class TimeInput(Tmi):
    def __init__(self, attrs=None, fmt=None):
        super().__init__(attrs, fmt)
        self.attrs.update({'class': 'input'})
