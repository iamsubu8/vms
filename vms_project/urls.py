from django.contrib import admin
from django.urls import path, include
from app.views import *
from rest_framework_simplejwt import views as jwt_views
from rest_framework import routers
router=routers.DefaultRouter()
# router.register(r"vendor",VendorView)
urlpatterns = [
    path('token/obtain/', jwt_views.TokenObtainPairView.as_view()),
    path('token/refresh/', jwt_views.TokenRefreshView.as_view()),
    path("login", UserLogin.as_view(),name="user-login"),
    path('admin/', admin.site.urls),
    path("api/vendors", VendorView.as_view(),name="vendor-create"),
    path('api/vendors/<int:vendor_id>', VendorOperations.as_view(),name="vendor-operations-detail"),
    path('api/purchase_orders', Purchase_Order.as_view(),name="purchase-order-list"),
    path('api/purchase_orders/<int:po_id>', PO_operations.as_view()),
    path('api/statusupdate/<int:po_id>', POStatusOperation.as_view()),
    path('api/purchase_orders/<int:po_id>/acknowledge', POAcknowledgeDateUpdate.as_view()),
    path('api/vendors/<int:vendor_id>/performance', VendorPerformanceEvaluation.as_view()),
    
]
