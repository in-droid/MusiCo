from django.urls import include, path
from rest_framework import routers
from . import views

app_name = 'event'

router = routers.DefaultRouter()

# Wire up our API using automatic URL routing.
# Additionally, we include login URLs for the browsable API.
urlpatterns = [
    path('', views.all_events, name='all'),
    path('<int:pk>', views.event_detail, name='detail'),
    path('recommend/', views.recommended_events, name='recommend'),
    ]