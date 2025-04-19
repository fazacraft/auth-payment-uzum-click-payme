from django.urls import path

from click.views import ClickViewSet


urlpatterns = [
    path('payment/', ClickViewSet.as_view({'post': 'prepare'}), name='click_prepare'),
]
