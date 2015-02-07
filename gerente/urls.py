from django.conf.urls import patterns, include, url
from django.contrib import admin


api_patterns = patterns(
    '',
    url(r'', include('clasificador.urls')),
    url(r'', include('pruebas.urls')),
    url(r'', include('documentos.urls')),
    url(r'^tasks/', include('djcelery.urls')),
    url(r'^admin/', include(admin.site.urls)),
)

urlpatterns = patterns(
    '',
    url(r'^api/', include(api_patterns)),
)
