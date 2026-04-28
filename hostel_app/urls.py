from django.urls import path
from . import views

urlpatterns = [

    # ── AUTH ──
    path('login/', views.user_login, name='login'),
    path('logout/', views.user_logout, name='logout'),

    # ── HOME & DASHBOARD ──
    path('', views.home, name='home'),
    path('dashboard/', views.dashboard, name='dashboard'),

    # ── STUDENT ──
    path('add-student/', views.add_student, name='add_student'),
    path('students/', views.student_list, name='student_list'),
    path('edit-student/<int:id>/', views.edit_student, name='edit_student'),
    path('delete-student/<int:id>/', views.delete_student, name='delete_student'),

    # ── ROOM ──
    path('rooms/', views.room_list, name='rooms'),

    # ── FEES ──
    path('fees/', views.fee, name='fee'),
    path('pay-fee/<int:id>/', views.pay_fee, name='pay_fee'),

    # ── OTHER ──
    path('complaint/', views.complaint, name='complaint'),
    path('resolve/<int:id>/', views.resolve_complaint, name='resolve_complaint'),
    path('visitor/', views.visitor, name='visitor'),

    # ════════════════════════════
    # ── STUDENT PORTAL ──
    # ════════════════════════════
    path('student/login/', views.student_login, name='student_login'),
    path('student/logout/', views.student_logout, name='student_logout'),
    path('student/dashboard/', views.student_dashboard, name='student_dashboard'),
    path('student/profile/', views.student_profile, name='student_profile'),
    path('student/room/', views.my_room, name='my_room'),
    path('student/fees/', views.my_fees, name='my_fees'),
    path('student/complaint/', views.student_complaint, name='student_complaint'),
    path('student/visitor/', views.visitor_request, name='visitor_request'),
    path('student/notices/', views.student_notices, name='student_notices'),

]