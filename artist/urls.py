from django.urls import include, path
from rest_framework import routers
from . import views

app_name = 'artist'

router = routers.DefaultRouter()
#router.register(r'users', views.UserViewSet)
#router.register(r'groups', views.GroupViewSet)

# Wire up our API using automatic URL routing.
# Additionally, we include login URLs for the browsable API.
urlpatterns = [
    path('', views.all_artists, name='all'),
    path('<int:pk>', views.artist_detail, name='detail'),
    ]