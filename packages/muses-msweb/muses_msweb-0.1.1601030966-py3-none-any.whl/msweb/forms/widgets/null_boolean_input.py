from django.forms import NullBooleanSelect as Nbs


class NullBooleanSelect(Nbs):
    template_name = "web/forms/widgets/select.html"

    def __init__(self, attrs=None):
        super().__init__(attrs)
        self.attrs.update({'class': 'select'})
