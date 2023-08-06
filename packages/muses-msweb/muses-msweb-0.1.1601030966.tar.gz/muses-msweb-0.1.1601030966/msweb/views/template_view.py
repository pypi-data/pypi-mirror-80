from django.utils.decorators import classonlymethod
from django.views.generic import TemplateView as Tv


class TemplateView(Tv):
    section_name = ""

    @classonlymethod
    def as_view(cls, section_name: str = "", **initkwargs):
        cls.section_name = section_name
        return super().as_view(**initkwargs)
