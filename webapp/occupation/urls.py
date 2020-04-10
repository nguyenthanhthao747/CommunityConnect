from django.urls import include, path

from . import views

app_name = 'app_occupation'

urlpatterns = [
    path('', views.index, name='index'),
    path('results/', views.results, name='results'),
    path('details/<str:occupation_id>/', views.details, name='details'),
    path('courses/<str:occupation_id>/', views.courses, name='courses'),
    path('fetch/', views.fetch, name='fetch'),
    path('fetch_details/', views.fetch_details, name='fetch_details'),
    path('fetch_data/', views.fetch_data, name='fetch_data'),
]
