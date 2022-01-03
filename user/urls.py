from django.urls import include, path
from rest_framework import routers
from . import views

app_name = 'user'

router = routers.DefaultRouter()
#router.register(r'users', views.UserViewSet)
#router.register(r'groups', views.GroupViewSet)

# Wire up our API using automatic URL routing.
# Additionally, we include login URLs for the browsable API.
urlpatterns = [
    path('', views.index, name='index'),
    path('register/', views.register_users, name='register'),
    path('login/', views.login_user, name='login'),
    path('spotify-auth/', views.spotify_auth, name='spotify'),
    path('spotify-callback/', views.spotify_callback, name='callback'),
    path('spotify-is-auth/', views.is_spotify_auth, name='spotify-auth-check'),
    path('profile/', views.my_profile, name='profile'),
]