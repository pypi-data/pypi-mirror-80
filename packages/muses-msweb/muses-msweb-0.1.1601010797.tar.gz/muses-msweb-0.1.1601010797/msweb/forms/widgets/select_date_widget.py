from django.forms import SelectDateWidget as Sdw


class SelectDateWidget(Sdw):
    def __init__(self, attrs=None, years=None, months=None, empty_label=None):
        super().__init__(attrs, years, months, empty_label)
        self.attrs.update({'class': 'select'})
