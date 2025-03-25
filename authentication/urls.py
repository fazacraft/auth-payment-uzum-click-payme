from django.urls import path

from authentication.views import UserViewSet, UserLoginViewSet

urlpatterns = [
    path('user/create/', UserViewSet.as_view({'post': 'create'})),
    path('user/verify/', UserViewSet.as_view({'post': 'otp_verify'})),
    path('user/resend/', UserViewSet.as_view({'post': 'otp_resend'})),
    path('user/get_detail/<int:pk>/', UserViewSet.as_view({'get': 'get', 'patch': 'update', 'delete': 'delete'})),
    path('user/login/', UserLoginViewSet.as_view({'post': 'login'}))
]
