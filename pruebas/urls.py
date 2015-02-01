
from django.conf.urls import url

from pruebas import views

urlpatterns = [
    url(
        r'^models/(?P<datatxt_id>[A-Za-z0-9\-]+)/test/$',
        views.model_test,
        name='test'
    ),
    url(
        r'^models/(?P<datatxt_id>[A-Za-z0-9\-]+)/results/$',
        views.ClassifierModelList.as_view(),
        name='test-results'
    ),

    url(
        r'^document-group/(?P<doc_pk>[0-9\-]+)/test/$',
        views.BaseDocumentTestList.as_view(),
        name='document-group-test-list'
    ),

    url(
        r'^document-group/(?P<dg_pk>[0-9\-]+)/test/(?P<pk>[0-9\-]+)/$',
        views.BaseDocumentTestDetails.as_view(),
        name='document-group-test-details'
    ),

    url(
        r'^document-group/(?P<dg_pk>[0-9\-]+)/'
        r'run-test/(?P<datatxt_id>[A-Za-z0-9\-]+)/$',
        views.model_document_group,
        name='document-group-run-test'
    ),

    url(
        r'^document/(?P<doc_pk>[0-9\-]+)/test/'
        r'(?P<test_pk>[0-9\-]+)/$',
        views.DocumentAnnotationDetails.as_view(),
        name='document-test-details'
    ),



    # model_document_group

    # url(
    #     r'^models/(?P<datatxt_id>[A-Za-z0-9\-]+)/results/(?P<test_id>[A-Za-z0-9\-]+)/$',
    #     views.ClassifierModelDetail.as_view(),
    #     name='test-result'
    # ),
]

