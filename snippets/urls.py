from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework.urlpatterns import format_suffix_patterns
from snippets import views

router = DefaultRouter()
router.register(r"snippets", views.SnippetViewSet, basename="snippet")
router.register(r"users", views.UserViewSet, basename="user")
router.register(r"bans", views.BannedUserViewSet, basename="banned")

urlpatterns = [
    path("", include(router.urls)),
]
