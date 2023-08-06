from django.urls import path
from django.conf.urls import include
from rest_framework import routers
from rest_framework_swagger.views import get_swagger_view
from rest_framework.authtoken.views import obtain_auth_token
from . import views

router = routers.SimpleRouter()
router.register(r'user', views.UserViewSet, basename='user')
router.register(r'group', views.GroupViewSet, basename='group')
router.register(r'register', views.RegisterViewSet, basename='register')

schema_view = get_swagger_view(title='Crazy Coding API')

urlpatterns = [
    path('swagger', schema_view),
    path('', include(router.urls)),

    path('auth/', include('rest_framework.urls', namespace='rest_framework')),
    path('auth-token/', obtain_auth_token)
]