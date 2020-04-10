from django.urls import include, path

from . import views

app_name = 'app_course'

urlpatterns = [
    path('', views.index, name='index'),
    path('results/', views.results, name='results'),
    path('details/<str:course_id>/', views.details, name='details'),
    path('providers/<str:course_id>/', views.providers, name='providers'),
    path('fetch/', views.fetch, name='fetch'),
    path('fetch_details/', views.fetch_details, name='fetch_details'),
    path('fetch_data/', views.fetch_data, name='fetch_data'),

    # course finder new layout
    path('finder/', views.finder, name='finder'),
]
