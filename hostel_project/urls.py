"""
URL configuration for hostel_project project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/6.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.contrib import admin
from django.urls import path, include
from hostel_app import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.home, name='home'),
    path('add_student/', views.add_student, name='add_student'),
    path('student/', views.student_list, name='student_list'),
    path('edit_student/<int:id>/', views.edit_student, name='edit_student'),
    path('delete_student/<int:id>/', views.delete_student, name='delete_student'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('complaint/', views.complaint, name='complaint'),
    path('resolve/<int:id>/', views.resolve_complaint, name='resolve_complaint'),
    path('suggest_room/', views.suggest_room, name='suggest_room'),
    path('fee/', views.fee, name='fee'),
    path('pay_fee/<int:id>/', views.pay_fee, name='pay_fee'),
    path('rooms/', views.room_list, name='rooms'),
    path('visitors/', views.visitor, name='visitors'),
    path('', include('hostel_app.urls')),
    path('student-login/', views.student_login, name='student_login'),
    path('student-dashboard/', views.student_dashboard, name='student_dashboard'),
    path('student-profile/', views.student_profile, name='student_profile'),
    path('my-room/', views.my_room, name='my_room'),
    path('student-complaint/', views.student_complaint, name='student_complaint'),
    path('visitor-request/', views.visitor_request, name='visitor_request'),
    path('my-fees/', views.my_fees, name='my_fees'),
    path('allocate-room/', views.allocate_room, name='allocate_room'),
    path('pay-fee/<int:fee_id>/', views.pay_fee, name='pay_fee'),
    path('payment-success/', views.payment_success, name='payment_success'),
    ] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)