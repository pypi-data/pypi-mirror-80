from django.forms import ClearableFileInput as Cfi


class ClearableFileInput(Cfi):
    template_name = "web/forms/widgets/clearable_file_input.html"

    def __init__(self, attrs=None):
        super().__init__(attrs)
        self.attrs.update({'class': 'input'})
