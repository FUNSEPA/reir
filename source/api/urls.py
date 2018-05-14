from rest_framework import routers
from api import views as api_v

router = routers.SimpleRouter()
router.register(r'semana', api_v.SemanaViewSet)

urlpatterns = router.urls
