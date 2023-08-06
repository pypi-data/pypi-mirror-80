from django.forms import NumberInput as Ni


class NumberInput(Ni):
    template_name = "web/forms/widgets/number.html"

    def __init__(self, attrs=None):
        super().__init__(attrs)
        self.attrs.update({'class': 'input'})
