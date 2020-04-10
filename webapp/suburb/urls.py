from django.urls import include, path

from . import views

app_name = 'app_suburb'

urlpatterns = [
    path('', views.index, name='index'),
    path('load_suburbs/', views.index_ajax, name='index_ajax'),
    path('results/', views.results, name='results'),
    path('details/<str:suburb_id>/', views.details, name='details'),
    path('fetch/', views.fetch, name='fetch'),
    path('fetch_details/', views.fetch_details, name='fetch_details'),

    path('fetch_data/', views.fetch_data, name='fetch_data'),
    path('info/<str:suburb_id>/', views.suburb_info, name='suburb_info'),
    path('fetch_suburbs/', views.fetch_suburbs, name='fetch_suburbs'),

    path('boundary_ajax/', views.boundary_ajax, name='boundary_ajax'),
    path('institutes/', views.institutes, name='institutes'),
]
