from django.urls import path
from rest_framework.permissions import AllowAny
from rest_framework.routers import SimpleRouter
from rest_framework_simplejwt.views import (TokenObtainPairView,
                                            TokenRefreshView)

from users.apps import UsersConfig
from users.views import (CoursePaymentCreateAPIView, PaymentCreateAPIView,
                         PaymentDestroyAPIView, PaymentListAPIView,
                         PaymentRetrieveAPIView, PaymentUpdateAPIView,
                         SubscriptionToggleAPIView, UserCreateAPIView,
                         UserDestroyAPIView, UserListAPIView,
                         UserRetrieveAPIView, UserUpdateAPIView)

app_name = UsersConfig.name

urlpatterns = [
    path("register/", UserCreateAPIView.as_view(), name="register"),
    path("", UserListAPIView.as_view(), name="users_list"),
    path("<int:pk>/", UserRetrieveAPIView.as_view(), name="users_retrieve"),
    path(
        "<int:pk>/delete/",
        UserDestroyAPIView.as_view(),
        name="users_delete",
    ),
    path(
        "<int:pk>/update/",
        UserUpdateAPIView.as_view(),
        name="users_update",
    ),
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
        name="payments_update",
    ),
    path(
        "login/",
        TokenObtainPairView.as_view(permission_classes=(AllowAny,)),
        name="login",
    ),
    path(
        "token/refresh/",
        TokenRefreshView.as_view(permission_classes=(AllowAny,)),
        name="token_refresh",
    ),
    path(
        "<int:pk>/subscribe/",
        SubscriptionToggleAPIView.as_view(permission_classes=(AllowAny,)),
        name="subscribe",
    ),
    path(
        "course_payment/",
        CoursePaymentCreateAPIView.as_view(),
        name="course_payment",
    ),
]
