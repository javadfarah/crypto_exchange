from django.urls import path
from .views import LoginView, LogoutView, SignupView, AuthMeView

urlpatterns = [
    path('login/', LoginView.as_view(), name='login'),
    path('me/', AuthMeView.as_view(), name='me'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('signup/', SignupView.as_view(), name='signup'),
]
