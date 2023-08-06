from django.forms import CheckboxInput as Ci


class CheckboxInput(Ci):
    template_name = "web/forms/widgets/checkbox.html"

    def __init__(self, attrs=None, check_test=None):
        super().__init__(attrs, check_test)
        self.attrs.update({'class': 'checkbox'})
