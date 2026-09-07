from django.urls import include, path

from productApp.views import UserViewset
from . import views
from rest_framework.routers import DefaultRouter
router  = DefaultRouter()

router.register(r'', UserViewset, basename='user-viewset')


urlpatterns = [
    path('register/', views.RegisterView.as_view()),
    path('verify-otp/', views.VerifyOTPView.as_view()),
    path('get-otp/', views.GetOTPView.as_view()),
    path('login/', views.LoginView.as_view()),
    path('', include(router.urls)),
    
]
