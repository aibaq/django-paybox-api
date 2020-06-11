from rest_framework.routers import DefaultRouter

from app.payments import views


router = DefaultRouter()
router.register('paybox', views.PayboxViewSet, basename='paybox')
urlpatterns = router.urls
