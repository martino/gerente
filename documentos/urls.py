from django.conf.urls import url
from documentos import views

urlpatterns = [
    url(
        r'^documents/(?P<pk>[0-9\-]+)/$',
        views.DocumentGroupList.as_view(),
        name='documents'
    )
]
