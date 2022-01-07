from django.urls import include, path
from rest_framework import routers
from . import views

app_name = 'venue'

router = routers.DefaultRouter()
#router.register(r'users', views.UserViewSet)
#router.register(r'groups', views.GroupViewSet)

# Wire up our API using automatic URL routing.
# Additionally, we include login URLs for the browsable API.
urlpatterns = [
    path('<str:location>/', views.all_events, name='events'),
    path('<int:pk>', views.venue_detail, name='detail'),
    path('', views.all_venues, name='all'),
    ]
