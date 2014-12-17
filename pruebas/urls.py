
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
    # url(
    #     r'^models/(?P<datatxt_id>[A-Za-z0-9\-]+)/results/(?P<test_id>[A-Za-z0-9\-]+)/$',
    #     views.ClassifierModelDetail.as_view(),
    #     name='test-result'
    # ),
]

