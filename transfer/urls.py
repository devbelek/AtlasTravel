from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import TransferViewSet, IconsAfterNameViewSet

router = DefaultRouter()
router.register(r'transfers', TransferViewSet, basename='transfers')
router.register(r'icons-after-name', IconsAfterNameViewSet, basename='icons-after-name')

urlpatterns = [
    path('', include(router.urls)),
    path('transfers/<int:pk>/add_comment/', TransferViewSet.as_view({'post': 'add_comment'}), name='transfers-add-comment'),
    path('transfers/<int:pk>/add_inquiry/', TransferViewSet.as_view({'post': 'add_inquiry'}), name='flights-add-inquiry'),

]
