from django.urls import path
from .views import profile, RegisterPage, index, CustomLoginView
from django.contrib.auth.views import LogoutView, LoginView

app_name = 'accounts'

urlpatterns = [

    # path('', index, name='index'),
    path('register/', RegisterPage.as_view(), name='register'),
    path('profile/', profile, name='profile'),
    path('login/', CustomLoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(next_page='accounts:login'), name='logout'),


]
