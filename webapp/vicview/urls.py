"""vicview URL Configuration

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
from django.contrib import admin
from django.urls import include, path
from django.conf.urls import url
from django.conf import settings
from django.conf.urls.static import static
from . import views

urlpatterns = [
    path('accounts/', include('django.contrib.auth.urls')),
    url(r'^admin/', admin.site.urls),


    # static pages will be from main app
    path('', views.index, name='index'),
    path('about-us', views.about, name='about'),
    path('seek-support/search', views.seek_support_search, name='seek_support_search'),

    path('volunteer-landing', views.volunteer_add, name='volunteer_add'),
    path('donate', views.donate, name='donate'),

    path('signup', views.signup, name='signup'),
    path('login-page', views.login, name='login'),

    path('search', views.search_integrated, name='search'),

    path('get-geolocation', views.geolocation, name='geolocation'),

    path('volunteers/', include('course.urls')),
    path('essentials/', include('provider.urls')),
    path('occupations/', include('occupation.urls')),
    path('suburbs/', include('suburb.urls')),

]

handler404 = 'vicview.views.page_not_found_view'
handler500 = 'vicview.views.error_view'
handler403 = 'vicview.views.permission_denied_view'
handler400 = 'vicview.views.bad_request_view'
