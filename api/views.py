import random, string, qrcode
from io import BytesIO
from django.shortcuts import render, get_object_or_404
from django.core.mail import EmailMessage, send_mail
from django.conf import settings
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import StoreUser

otp_storage = {}

def login_page(request):
    return render(request, 'login.html')

def store_frontend(request, user_slug):
    user = get_object_or_404(StoreUser, user_id_slug=user_slug, is_active=True)
    return render(request, 'index.html', {'user': user})

@api_view(['POST'])
def truthscan_verify(request):
    """Explicitly defined to resolve AttributeError"""
    return Response({"status": "READY"})

@api_view(['POST'])
def handle_login(request):
    email = request.data.get('email')
    password = request.data.get('password')
    slug = 'COASTAL-' + ''.join(random.choices(string.ascii_uppercase + string.digits, k=6))
    user, _ = StoreUser.objects.get_or_create(email=email, defaults={'password': password, 'user_id_slug': slug})
    user.user_id_slug, user.is_active = slug, True
    user.save()
    return Response({"url_id": slug})

@api_view(['POST'])
def send_otp(request):
    email = request.data.get('email')
    otp = str(random.randint(100000, 999999))
    otp_storage[email] = otp
    send_mail('Coastal Verification', f'Your OTP is: {otp}', settings.EMAIL_HOST_USER, [email])
    return Response({"status": "sent"})

@api_view(['POST'])
def finalize_order(request):
    data = request.data
    email, user_otp, slug = data.get('email'), data.get('otp'), data.get('url_id')
    qty, total, address = data.get('qty'), data.get('total'), data.get('address')

    if otp_storage.get(email) == user_otp:
        # Generate Unique Order QR
        order_info = f"ORDER:{slug}\nQTY:{qty}\nTOTAL:INR {total}\nADDR:{address}"
        qr = qrcode.make(order_info)
        buf = BytesIO()
        qr.save(buf, format="PNG")
        
        msg = EmailMessage(f"NEW ORDER: {slug}", order_info, settings.EMAIL_HOST_USER, ['saffar1618web@gmail.com'])
        msg.attach(f'receipt_{slug}.png', buf.getvalue(), 'image/png')
        msg.send()
        return Response({"status": "success", "order_id": slug})
    return Response({"error": "Invalid OTP"}, status=400)
