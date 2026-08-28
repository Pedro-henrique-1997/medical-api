from django.contrib import admin
from django.urls import include, path
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

from appointments.views import AppointmentViewSet
from professionals.views import ProfessionalViewSet

router = DefaultRouter()
router.register("professionals", ProfessionalViewSet, basename="professionals")
router.register("appointments", AppointmentViewSet, basename="appointments")


urlpatterns = [
    path("admin/", admin.site.urls),

    path(
        "api/token/",
        TokenObtainPairView.as_view(),
        name="token_obtain_pair",
    ),
    path(
        "api/token/refresh/",
        TokenRefreshView.as_view(),
        name="token_refresh",
    ),

    path("api/", include(router.urls)),
]