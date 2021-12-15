from django.conf.urls.i18n import i18n_patterns
from django.urls import include, path

urlpatterns = i18n_patterns(path('core/', include('applications.core.urls')), prefix_default_language=False)
