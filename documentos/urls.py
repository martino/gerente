from django.conf.urls import url
from documentos import views

urlpatterns = [
    url(
        r'^document-group/$',
        views.DocumentGroupList.as_view(),
        name='document-gorup'
    ),
    url(
        r'^document-group/(?P<pk>[0-9\-]+)/$',
        views.DocumentGroupDetails.as_view(),
        name='document-group-details'
    ),

    url(
        r'^document/(?P<pk>[0-9\-]+)/$',
        views.BaseDocumentDetails.as_view(),
        name='base-document-details'
    ),

]
