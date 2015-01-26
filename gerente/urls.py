from django.conf.urls import patterns, include, url
from django.contrib import admin


urlpatterns = patterns(
    '',
    # Examples:
    url(r'', include('clasificador.urls')),
    url(r'', include('pruebas.urls')),
    url(r'', include('documentos.urls')),
    url(r'^tasks/', include('djcelery.urls')),
    url(r'^admin/', include(admin.site.urls)),
)
