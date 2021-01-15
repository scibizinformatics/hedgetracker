from rest_framework import routers

from main import views


app_name = "main"

router = routers.DefaultRouter()

router.register("metrics", views.MetricViewSet)

urlpatterns = router.urls
