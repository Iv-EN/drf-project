from django.urls import include, path
from rest_framework.routers import SimpleRouter

from users.apps import UsersConfig
from users.views import PaymentViewSet, UserViewSet

app_name = UsersConfig.name

router = SimpleRouter()
router.register("user", UserViewSet)
router.register("payment", PaymentViewSet)

urlpatterns = [path("", include(router.urls))]
