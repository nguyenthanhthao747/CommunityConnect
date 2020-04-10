from django.urls import include, path

from . import views

app_name = 'app_provider'

urlpatterns = [
    path('', views.index, name='index'),
    path('results/', views.results, name='results'),
    path('details/<str:provider_id>/', views.details, name='details'),
    path('suburbs/<str:provider_id>/', views.suburbs, name='suburbs'),
    path('fetch/', views.fetch, name='fetch'),
    path('fetch_details/', views.fetch_details, name='fetch_details'),
    path('fetch_data/', views.fetch_data, name='fetch_data'),


    path('compare-suburbs/<str:provider_id>/<str:suburb_id1>/<str:suburb_id2>/', views.compare, name='compare'),

]
