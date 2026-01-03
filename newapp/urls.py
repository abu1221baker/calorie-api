from django.urls import path
from . import views
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

urlpatterns = [
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('calories/', views.calorie_view, name='calorie_view'),
    path('calories/<str:name>/', views.per_item, name='per_item'),
    path('create/profile/', views.create_profile, name='create_profile'),
    path('view/profile/', views.view_profile, name='view_profile'),
]
