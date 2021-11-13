"""home_manager URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
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
from django.urls import path, include
from users import views as user_views


urlpatterns = [
    path('zajednica_admin/', admin.site.urls),
    path('', include('home.urls')),
    path('', include('poll.urls')),
    path('', include('messaging.urls')),
    path('ajax/load-opstine/', user_views.load_opstine, name="ajax_load_opstine"),
    path('ajax/load-ulazi/', user_views.load_ulazi, name="ajax_load_ulazi"),
    path('ajax/cep-load-opstine/', user_views.cep_load_opstine, name="ajax_cep__load_opstine"),
    path('ajax/cep-load-ulazi/', user_views.cep_load_ulazi, name="ajax_cep_load_ulazi"),
    path('register/<str:pk>', user_views.register, name='register'),
    path('register1/', user_views.register1, name='register1'),
    path('register2/<str:yourname>', user_views.register2, name='register2'),
    path('register3/<int:temp_id>', user_views.register3, name='register3'),
    path('register4/<str:yourname>', user_views.register4, name='register4'),
    path('profile/', user_views.profile, name='profile'),
    path('papir/', user_views.papir_servis, name='papir_servis'),
    path('papir/mapa/', user_views.papir_mapa, name='papir_mapa'),
    path('prijavljen_papir/', user_views.prijavljen_papir, name='prijavljen_papir'),
    path('manager/', user_views.manager_profile, name='manager'),
    path('manager_public/<int:pk>', user_views.manager_public, name='manager_public'),
    path('docs/', user_views.documents, name='documents_page'),
    path('managers_page/', user_views.ManagersRankingView.as_view(), name='managers_page'),
    path('profile/<int:pk>', user_views.user_profile, name='user-profile'),
    path('login/', auth_views.LoginView.as_view(template_name="users/login.html"), name='login'),
    path('login_success/', user_views.login_success, name='login-success'),
    path('logout/', auth_views.LogoutView.as_view(template_name="users/logout.html"), name='logout'),
    path('ckeditor/', include('ckeditor_uploader.urls')),
    path('', include('pwa.urls'))
    # path('ulaz-autocomplete/', user_views.UlazAutocomplete.as_view(), name='ulaz-autocomplete'),
]

if settings.DEBUG:
	urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
