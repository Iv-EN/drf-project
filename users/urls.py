from django.urls import include, path
from rest_framework.permissions import AllowAny
from rest_framework.routers import SimpleRouter
from rest_framework_simplejwt.views import TokenRefreshView

from users.apps import UsersConfig
from users.views import MyTokenObtainPairView, PaymentViewSet, UserViewSet

app_name = UsersConfig.name

router = SimpleRouter()
router.register("user", UserViewSet)
router.register("payment", PaymentViewSet)


urlpatterns = [
    path(
        "token/",
        MyTokenObtainPairView.as_view(permission_classes=(AllowAny,)),
        name="token_obtain_pair",
    ),
    path(
        "token/refresh/",
        TokenRefreshView.as_view(permission_classes=(AllowAny,)),
        name="token_refresh",
    ),
    path("", include(router.urls)),
]
