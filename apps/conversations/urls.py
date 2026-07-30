from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import *


router = DefaultRouter()

router.register('conversations', ConversationViewSet, basename='conversation')
router.register('participants', ParticipantViewSet, basename='participant')

urlpatterns = [
    path('', include(router.urls)),
]