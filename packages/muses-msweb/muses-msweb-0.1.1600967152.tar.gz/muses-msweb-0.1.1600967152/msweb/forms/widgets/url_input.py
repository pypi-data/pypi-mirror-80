from django.forms import URLInput as Ui


class URLInput(Ui):
    template_name = "web/forms/widgets/url_input.html"

    def __init__(self, attrs=None):
        super().__init__(attrs)
        self.attrs.update({'class': 'input'})
