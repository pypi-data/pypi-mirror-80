from django.forms import MultipleHiddenInput as Mhi


class MultipleHiddenInput(Mhi):
    template_name = "web/forms/widgets/multiple_hidden.html"

    def __init__(self, attrs=None):
        super().__init__(attrs)
        self.attrs.update({'class': 'input'})
