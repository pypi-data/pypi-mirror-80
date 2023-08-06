from django.forms import HiddenInput as Hi


class HiddenInput(Hi):
    template_name = "web/forms/widgets/hidden.html"

    def __init__(self, attrs=None):
        super().__init__(attrs)
        self.attrs.update({'class': 'input'})
