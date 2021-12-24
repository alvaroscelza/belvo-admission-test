from rest_framework.routers import DefaultRouter

from applications.core.views.user_transactions_view import UserTransactionsView

router = DefaultRouter()
router.register(r'user_transactions', UserTransactionsView, basename='user_transactions')
urlpatterns = router.urls
