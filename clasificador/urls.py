from django.conf.urls import patterns, url
from rest_framework.urlpatterns import format_suffix_patterns
from clasificador import views

urlpatterns = [
    url(r'^models/$', views.ClassifierModelList.as_view()),
    url(
        r'^models/(?P<datatxt_id>[A-Za-z0-9\-]+)/$',
        views.ClassifierModelDetail.as_view()),
    url(r'^create-new-model/$',
        views.ClassifierCreate.as_view())
]

urlpatterns += format_suffix_patterns(urlpatterns)
