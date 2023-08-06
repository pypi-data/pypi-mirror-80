from django.forms import FileInput as Fi


class FileInput(Fi):
    template_name = "web/forms/widgets/file_input.html"

    def __init__(self, attrs=None):
        super().__init__(attrs)
        self.attrs.update({'class': 'input'})