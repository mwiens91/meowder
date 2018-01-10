"""meowder URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.contrib.auth import views as auth_views
from django.urls import path
import meowder.views as meowder_views

urlpatterns = [
    path(r'', meowder_views.home, name='home'),
    path(r'admin/', admin.site.urls, name='admin'),
    path(r'catedit/<int:catid>/', meowder_views.cat_edit, name='catedit'),
    path(r'cathome/<int:catid>/', meowder_views.cat_home, name='cathome'),
    path(r'catremove/<int:catid>/', meowder_views.cat_remove, name='catremove'),
    path(r'catsignup/', meowder_views.cat_signup, name='catsignup'),
    path(r'editemail/',
         meowder_views.EditEmail.as_view(success_url='/',
                                         template_name="editemail.html"),
         name='editemail'),
    path(r'editlocation/',
         meowder_views.EditLocation.as_view(success_url='/',
                                            template_name="editlocation.html"),
         name='editlocation'),
    path(r'editpassword/',
         auth_views.PasswordChangeView.as_view(success_url='/',
                                               template_name="editpassword.html"),
         name='editpassword'),
    path(r'wrongcat/', meowder_views.error_wrong_cat, name='errorwrongcat'),
    path(r'login/', auth_views.login, {'template_name': 'login.html'}, name='login'),
    path(r'logout/', auth_views.logout, {'next_page': 'login'}, name='logout'),
    path(r'signup/', meowder_views.profile_signup, name='signup'),
    path(r'userprofile/', meowder_views.user_profile, name='userprofile'),
]
