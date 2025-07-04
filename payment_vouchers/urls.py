from django.urls import path
from .views import PaymentVoucherListView, PaymentVoucherDetailView , PaymentVoucherCreateView, PaymentVoucherOptionsView, PaymentVoucherApproveView

urlpatterns = [
    path('', PaymentVoucherListView.as_view(), name='payment-voucher-list'),
    path('create/', PaymentVoucherCreateView.as_view(), name='payment-voucher-create'),
    path('<int:pk>/', PaymentVoucherDetailView.as_view(), name='payment-voucher-detail'),
    path('options/', PaymentVoucherOptionsView.as_view(), name='payment-voucher-options'),
    path('approve/<int:pk>/', PaymentVoucherApproveView.as_view(), name='payment-voucher-approve'),
]
