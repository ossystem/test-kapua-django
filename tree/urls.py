from django.conf.urls import url, include
from rest_framework.routers import DefaultRouter

from views import NodeViewSet


router = DefaultRouter()
router.register(r'nodes', NodeViewSet)

urlpatterns = [
    url(r'^', include(router.urls)),
]
