from django.urls import path

from Uzum.views import UzumViewSet

urlpatterns = [
    path('payment/uzum/check/', UzumViewSet.as_view({'post': 'verify'}), name='uzum_check'),
    path('payment/uzum/create/', UzumViewSet.as_view({'post': 'create'}), name='uzum_create'),
    path('payment/uzum/confirm/', UzumViewSet.as_view({'post': 'confirm'}), name='uzum_confirm'),
    path('payment/uzum/reverse/', UzumViewSet.as_view({'post': 'cancel'}), name='uzum_reverse'),
    path('payment/uzum/status/', UzumViewSet.as_view({'post': 'check_status'}), name='uzum_status'),

]
