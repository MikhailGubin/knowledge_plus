from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

from django.urls import path
from rest_framework.routers import SimpleRouter

from users.apps import UsersConfig
from users.views import (
    PaymentCreateAPIView,
    PaymentDestroyAPIView,
    PaymentListAPIView,
    PaymentRetrieveAPIView,
    PaymentUpdateAPIView,
    UserViewSet,
    UserCreateAPIView,
)

app_name = UsersConfig.name

router = SimpleRouter()
router.register("", UserViewSet)
urlpatterns = [
    path("register/", UserCreateAPIView.as_view(), name="register"),
    path("payments/", PaymentListAPIView.as_view(), name="payments_list"),
    path(
        "payments/<int:pk>/", PaymentRetrieveAPIView.as_view(), name="payments_retrieve"
    ),
    path("payments/create/", PaymentCreateAPIView.as_view(), name="payments_create"),
    path(
        "payments/<int:pk>/delete/",
        PaymentDestroyAPIView.as_view(),
        name="payments_delete",
    ),
    path(
        "payments/<int:pk>/update/",
        PaymentUpdateAPIView.as_view(),
        name="payments_update"),
    path('login/', TokenObtainPairView.as_view(), name='login'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]

urlpatterns += router.urls
