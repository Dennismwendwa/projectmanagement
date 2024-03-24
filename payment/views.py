from django.shortcuts import render, reverse, redirect
from django.views.generic import TemplateView
from django.http import JsonResponse, HttpResponse
from django.conf import settings
from django.views import View
from django.shortcuts import get_object_or_404
from django.db.models import F

from django.core.mail import send_mail
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator

import json
import stripe
import requests

from datetime import datetime
import json
import base64
from django.http import JsonResponse
from accounts.models import SubscriptionPlan, UserSubscription
from .generateAccesstoken import get_access_token


class SuccessView(TemplateView):
    template_name = "payment/success.html"


class CancelView(TemplateView):
    template_name = "payment/cancel.html"


# @method_decorator(csrf_exempt, name='dispatch')
class CreateCheckoutSessionView(View):
    def post(self, request, *args, **kwargs):
        success_url=reverse("payment:success")
        cancel_url=reverse("payment:cancel")
        product_type = self.kwargs["product_type"]
        if product_type == "service":
            try:
                product_id = self.kwargs["pk"]
                product = SubscriptionPlan.objects.get(id=product_id)
            except Exception as e:
                print(e)
        elif product_type == "course":
            try:
                product_id = self.kwargs["pk"]
               # product = Course.objects.get(id=product_id)
            except Exception as e:
                print(e)
        YOUR_DOMAIN = settings.YOUR_DOMAIN
        payment_method_types="card"

        try:
            return redirect("payment:cancel")
        except:
            pass

        checkout_session = stripe.checkout.Session.create(
            payment_method_types=['card'],
            line_items=[
                {
                    'price_data': {
                        'currency': 'usd',
                        'unit_amount': int(product.price * 100),
                        'product_data': {
                            'name': product.title,
                            'images':["product.image.url",]
                        },
                    },
                    'quantity': 1,
                },
            ],
            metadata={
                "product_id": product.id
            },
            mode='payment',
            success_url=YOUR_DOMAIN + f"{success_url}",
            cancel_url=YOUR_DOMAIN + f"{cancel_url}",
        )
        
        return JsonResponse({
            'id': checkout_session.id
        })


@csrf_exempt
def stripe_webhook(request):
    payload = request.body
    sig_header = request.META['HTTP_STRIPE_SIGNATURE']
    event = None

    try:
        event = stripe.Webhook.construct_event(
            payload, sig_header, settings.STRIPE_WEBHOOK_SECRET
        )
    except ValueError as e:
        # Invalid payload
        return HttpResponse(status=400)
    except stripe.error.SignatureVerificationError as e:
        # Invalid signature
        return HttpResponse(status=400)

    # Handle the checkout.session.completed event
    if event['type'] == 'checkout.session.completed':
        session = event['data']['object']

        customer_email = session["customer_details"]["email"]
        product_id = session["metadata"]["product_id"]

        product = UserSubscription.objects.get(id=product_id)

        send_mail(
            subject="Here is your product",
            message=f"""
            Thanks for your purchase. Here is the product you ordered.
            The URL is {product.url}
            """,
            recipient_list=[customer_email],
            from_email="dennismusembi2@gmail.com"
        )

    elif event["type"] == "payment_intent.succeeded":
        intent = event['data']['object']

        stripe_customer_id = intent["customer"]
        stripe_customer = stripe.Customer.retrieve(stripe_customer_id)

        customer_email = stripe_customer['email']
        product_id = intent["metadata"]["product_id"]

        product = UserSubscription.objects.get(id=product_id)

        send_mail(
            subject="Here is your product",
            message=f"""
            Thanks for your purchase. Here is the product you ordered.
            The URL is {product.url}
            """,
            recipient_list=[customer_email],
            from_email="dennismusembi2@gmail.com"
        )

    return HttpResponse(status=200)


class StripeIntentView(View):
    def post(self, request, *args, **kwargs):
        
        try:
            req_json = json.loads(request.body)
            customer = stripe.Customer.create(email=req_json['email'])
            product_id = self.kwargs["pk"]

            if self.kwargs["product_type"] == "service":
                product = UserSubscription.objects.get(id=product_id)
            elif self.kwargs["product_type"] == "course":
                product = UserSubscription.objects.get(id=product_id)
            intent = stripe.PaymentIntent.create(
                amount=int(product.price * 100),
                currency='usd',
                customer=customer['id'],
                metadata={
                    "product_id": product.id
                }
            )
            return JsonResponse({
                'clientSecret': intent['client_secret']
            })
        except Exception as e:
            return JsonResponse({'error': str(e)})


def mpesa_checkout_view(request, pk, security_key):
    """This view is for mpesa form details"""
    course = UserSubscription.objects.get(pk=pk)

    context = {
        "course": course,
    }
    return render(request, "payment/mpesa.html", context)


def mpesa_session(request):
    """This view hundles lipa na mpesa payments"""
    access_token_response = get_access_token()
    if request.method == "POST":
        amount = request.POST.get("amount")
        phone = request.POST.get("phone")
        desc = request.POST.get("description", 'stkpush test')
        service = request.POST.get("service")
        service_type = request.POST.get("service_type")
        
        if len(phone) == 10 and phone.startswith("0"):
            phone = "254" + phone[1:]
        elif len(phone) == 13 and phone.startswith("+"):
            phone = phone[1:]
        
        if isinstance(access_token_response, JsonResponse):
            access_token = access_token_response.content.decode('utf-8')
            access_token_json = json.loads(access_token)
            access_token = access_token_json.get('access_token')
            if access_token:
                amount = float(amount)
                phone = phone
                passkey = settings.MPESA_PASSKEY
                business_short_code = settings.MPESA_SHORTCODE
                process_request_url = 'https://sandbox.safaricom.co.ke/mpesa/stkpush/v1/processrequest'
                callback_url = settings.MPESA_CALLBACK_URL
                timestamp = datetime.now().strftime('%Y%m%d%H%M%S')
                password = base64.b64encode((business_short_code + passkey + timestamp).encode()).decode()
                party_a = phone
                party_b = '254708374149'
                account_reference = 'WELEARNCODES SOFTWARE'
                transaction_desc = desc
                stk_push_headers = {
                    'Content-Type': 'application/json',
                    'Authorization': 'Bearer ' + access_token
                }
                
                stk_push_payload = {
                    'BusinessShortCode': business_short_code,
                    'Password': password,
                    'Timestamp': timestamp,
                    'TransactionType': 'CustomerPayBillOnline',
                    'Amount': amount,
                    'PartyA': party_a,
                    'PartyB': business_short_code,
                    'PhoneNumber': party_a,
                    'CallBackURL': callback_url,
                    'AccountReference': account_reference,
                    'TransactionDesc': transaction_desc
                }

                try:
                    response = requests.post(process_request_url, headers=stk_push_headers, json=stk_push_payload)
                    response.raise_for_status()   
                    response_data = response.json()
                    checkout_request_id = response_data['CheckoutRequestID']
                    response_code = response_data['ResponseCode']
                    
                    if response_code == "0":
                        try:
                            UserSubscription.objects.create(
                                service=service,
                                checkout_request_id=checkout_request_id,
                                customer=request.user,
                                phone_number=phone,
                                amount=amount,
                                service_type=service_type,
                            )
                        except Exception as e:
                            return JsonResponse({"error": "Error while creating the transaction recond"}, status=500)
                        return JsonResponse({'CheckoutRequestID': checkout_request_id, 'ResponseCode': response_code}, status=200)
                    else:
                        
                        return JsonResponse({'error': 'STK push failed.'})
                except requests.exceptions.RequestException as e:
                    return JsonResponse({'error': str(e)})
            else:
                return JsonResponse({'error': 'Access token not found.'})
    else:
        return JsonResponse({'error': 'Failed to retrieve access token.'})
    

def stk_push_callback(request):
    mpesa_pay_load = json.loads(request.body)
    
    merchart_request_id = mpesa_pay_load["Body"]["stkCallback"]["MerchartRequestID"]
    checkout_request_id = mpesa_pay_load["Body"]["stkCallback"]["CheckoutRequestID"]
    result_code = mpesa_pay_load["Body"]["stlCallback"]["ResultCode"]
    result_desc = mpesa_pay_load["Body"]["stkCallback"]["ResultDesc"]
    amount = mpesa_pay_load["Body"]["stkCallback"]["CallbackMetadata"]["Item"][0]["Value"]
    transaction_id = mpesa_pay_load["Body"]["stkCallback"]["CallbackMetadata"]["Item"][1]["Value"]
    user_phone_number = mpesa_pay_load["Body"]["stkCallback"]["CallbackMetadata"]["Item"][4]["Value"]
    
    if result_code == 0:
        transaction = get_object_or_404(UserSubscription,
                                        checkout_request_id=checkout_request_id)
        transaction.pay_status = True
        transaction.save()
        
        if transaction.service_type == "course":
            payment_method_types = "Mpesa"
            bought_course = get_object_or_404(UserSubscription, name=transaction.service)
            
            
            return JsonResponse({"success": "Payment success"}, status=200)

        elif transaction.service_type == "service":
            bought_service = get_object_or_404(UserSubscription, title=transaction.service)
            product_type = "service"

            return JsonResponse({"success": "Payment success"}, status=200)
    
    return HttpResponse({"error": "Payment was not done"}, status=400)

