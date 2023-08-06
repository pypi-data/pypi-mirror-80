from django.forms import TextInput as Ti


class TextInput(Ti):
    template_name = "web/forms/widgets/text_input.html"

    def __init__(self, attrs=None):
        super().__init__(attrs)
        self.attrs.update({'class': 'input'})
