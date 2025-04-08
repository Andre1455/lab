from django.urls import path
from .views import (
    InstrumentListCreateAPIView,
    InstrumentDetailAPIView,
    OrderListCreateAPIView,
    OrderDetailAPIView
)

urlpatterns = [
    # Instrument routes
    path('instruments/', InstrumentListCreateAPIView.as_view(), name='instrument-list-create'),
    path('instruments/<int:pk>/', InstrumentDetailAPIView.as_view(), name='instrument-detail'),

    # Order routes
    path('orders/', OrderListCreateAPIView.as_view(), name='order-list-create'),
    path('orders/<int:pk>/', OrderDetailAPIView.as_view(), name='order-detail'),
]
