from django.urls import path
from .views import PaymentVoucherListCreateView, PaymentVoucherDetailView

urlpatterns = [
    path('payment-vouchers/', PaymentVoucherListCreateView.as_view(), name='payment-voucher-list'),
    path('payment-vouchers/<int:pk>/', PaymentVoucherDetailView.as_view(), name='payment-voucher-detail'),
]
