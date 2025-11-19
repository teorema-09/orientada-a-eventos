from rest_framework.routers import DefaultRouter
from .views import MotocicletaViewSet

router = DefaultRouter()
router.register(r'motocicletas', MotocicletaViewSet)

urlpatterns = router.urls
