from django.urls import path

from click.views import ClickViewSet


urlpatterns = [
    path('payment/click/prepare/', ClickViewSet.as_view({'post': 'prepare'}), name='click_prepare'),
    path('payment/click/complete', ClickViewSet.as_view({'post': 'complete'}), name='click_complete'),
]
