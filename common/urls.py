from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

app_name = 'common'

urlpatterns = [
    path('login/',auth_views.LoginView.as_view(
        template_name = 'common/login.html'),name = 'login'), # 장고 auth앱의 loginview를 활용하므로 별도의 기능추가가 필요없음.
    path('logout/',auth_views.LogoutView.as_view(),name='logout'),
    path('signup/',views.signup, name = 'signup'),
]