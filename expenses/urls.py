from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ExpenseViewSet, AnalyticsView

router = DefaultRouter()
router.register(r'expenses', ExpenseViewSet)

urlpatterns = [
    path('register/', UserViewSet.as_view({'post': 'create'})),
    path('login/', include('dj_rest_auth.urls')),  
    path('profile/', UserViewSet.as_view({'patch': 'partial_update'})),
    path('analytics/', AnalyticsView.as_view(), name='analytics'),
    path('', include(router.urls)),
]
