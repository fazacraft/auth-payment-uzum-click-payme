from django.urls import path

from authentication.views import UserViewSet, UserLoginViewSet

urlpatterns = [
    path('user/create/', UserViewSet.as_view({'post': 'create'}), name='user_create'),
    path('user/verify/', UserViewSet.as_view({'post': 'otp_verify'}), name='user_verify'),
    path('user/resend/', UserViewSet.as_view({'post': 'otp_resend'}),name='otp_resend'),
    path('user/get_detail/<int:pk>/', UserViewSet.as_view({'get': 'get', 'patch': 'update', 'delete': 'delete'}), name='user_detail'),
    path('user/login/', UserLoginViewSet.as_view({'post': 'login'}), name ='user_login')
]
