from django.contrib import admin
from django.urls import path
from api import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.login_page, name='login'),
    path('store/<str:user_slug>/', views.store_frontend),
    path('api/login/', views.handle_login),
    path('api/detect-payment/', views.truthscan_verify), # Resolves screenshot error
    path('api/otp/', views.send_otp),
    path('api/finalize/', views.finalize_order),
]
