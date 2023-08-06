from django.forms import Textarea as T


class Textarea(T):
    template_name = "web/forms/widgets/textarea.html"

    def __init__(self, attrs=None):
        super().__init__(attrs)
        self.attrs.update({'class': 'textarea'})
