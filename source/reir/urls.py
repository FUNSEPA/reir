from django.urls import path, include
from django.conf.urls import url
from django.contrib import admin
from django.contrib.auth import views as auth_views
from juego import views as juego_v

urlpatterns = [
    # path('about/', juego_v.HomeView.as_view()),
    path('admin/', admin.site.urls),
    path('api/', include('api.urls')),
    path('', include('juego.urls')),
    url(r'^login/$', auth_views.login, name='login'),
    url(r'^logout/$', auth_views.logout, {'next_page': '/'}, name='logout'),
]
