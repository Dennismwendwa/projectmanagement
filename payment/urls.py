from django.urls import path
from .import views

app_name = "payment"

urlpatterns = [
    path('create-payment-intent/<pk>/', views.StripeIntentView.as_view(),
        name='create-payment-intent'),
    path('webhooks/stripe/', views.stripe_webhook, name='stripe-webhook'),
    path('cancel/', views.CancelView.as_view(), name='cancel'),
    path('success/', views.SuccessView.as_view(), name='success'),
    path("pay/<int:pk>/<uuid:security_key>/", views.mpesa_checkout_view,
        name="mpesa_checkout_view"),
    path('create-checkout-session/<str:product_type>/<int:pk>',
        views.CreateCheckoutSessionView.as_view(), name='create-checkout-session'),
    path("expresspay", views.mpesa_session, name="mpesa_pay"),
    path('daraja/stk-push', views.stk_push_callback, name='mpesa_stk_push_callback'),
    #path("response", views.mpesa_response, name="mpesa_response"),
]
