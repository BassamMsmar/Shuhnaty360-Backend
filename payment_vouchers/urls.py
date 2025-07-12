from django.urls import path
from .views import PaymentVoucherListView, PaymentVoucherDetailView , PaymentVoucherCreateView, PaymentVoucherOptionsView, PaymentVoucherUpdateView

urlpatterns = [
    path('', PaymentVoucherListView.as_view(), name='payment-voucher-list'),
    path('create/', PaymentVoucherCreateView.as_view(), name='payment-voucher-create'),
    path('<int:pk>/', PaymentVoucherDetailView.as_view(), name='payment-voucher-detail'),
    path('update/<int:pk>/', PaymentVoucherUpdateView.as_view(), name='payment-voucher-update'),
    path('approve/<int:pk>/', PaymentVoucherUpdateView.as_view(), name='payment-voucher-update'),
    path('options/', PaymentVoucherOptionsView.as_view(), name='payment-voucher-options'),

]
