from django.forms import PasswordInput as Pi


class PasswordInput(Pi):
    template_name = "web/forms/widgets/password.html"

    def __init__(self, attrs=None):
        super().__init__(attrs)
        self.attrs.update({'class': 'input'})
