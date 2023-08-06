from django.forms import EmailInput as Ei


class EmailInput(Ei):
    template_name = "web/forms/widgets/email.html"

    def __init__(self, attrs=None):
        super().__init__(attrs)
        self.attrs.update({'class': 'input'})
