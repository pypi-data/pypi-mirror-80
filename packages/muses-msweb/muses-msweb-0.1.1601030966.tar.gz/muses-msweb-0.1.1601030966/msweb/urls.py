from django.utils.translation import ugettext as _
from django.urls import path
from msweb import views

urlpatterns = [
    # Home Page
    path(
        "",
        views.TemplateView.as_view(
            template_name="web/home.html",
            section_name=_('Home')
        ),
        name="muses_home"
    ),
    # About
    path(
        "about/",
        views.TemplateView.as_view(
            template_name="web/about.html",
            section_name=_('About')
        ),
        name="muses_about"
    ),
    # Faq
    path(
        "faq/",
        views.TemplateView.as_view(
            template_name="web/faq.html",
            section_name=_('Faq')
        ),
        name="muses_faq"
    ),
    # Terms of Use
    path(
        "terms_of_use/",
        views.TemplateView.as_view(
            template_name="web/terms_of_use.html",
            section_name=_('Terms of Use')
        )
    )
]
