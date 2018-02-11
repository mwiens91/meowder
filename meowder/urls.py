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
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.contrib.auth import views as auth_views
from django.urls import path
import cats.views_cats as cat_views
import cats.views_profile as profile_views


handler403 = 'meowder.views.handler403'
handler404 = 'meowder.views.handler404'
handler500 = 'meowder.views.handler500'

urlpatterns = [
    path(r'', profile_views.home, name='home'),
    path(r'admin/', admin.site.urls, name='admin'),
    path(r'cat/<int:catid>/edit', cat_views.cat_edit, name='catedit'),
    path(r'cat/<int:catid>/', cat_views.cat_home, name='cathome'),
    path(r'cat/<int:catid>/remove', cat_views.cat_remove, name='catremove'),
    path(r'cat/<int:votercatid>/vote/<int:voteecatid>',
         cat_views.cat_vote, name='catvote'),
    path(r'cat/signup/', cat_views.cat_signup, name='catsignup'),
    path(r'cat/wrongcat/', cat_views.error_wrong_cat, name='errorwrongcat'),
    path(r'editpassword/',
         auth_views.PasswordChangeView.as_view(success_url='/',
                                               template_name="editpassword.html"),
         name='editpassword'),
    path(r'editprofile/', profile_views.profile_edit, name='editprofile'),
    path(r'login/', auth_views.login, {'template_name': 'login.html'}, name='login'),
    path(r'logout/', auth_views.logout, {'next_page': 'login'}, name='logout'),
    path(r'matches/', profile_views.matches, name='matches'),
    path(r'signup/', profile_views.profile_signup, name='signup'),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
