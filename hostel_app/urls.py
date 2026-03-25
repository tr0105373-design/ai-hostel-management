from django.urls import path
from . import views

urlpatterns = [

    # Home & Dashboard
    path('', views.home, name='home'),
    path('dashboard/', views.dashboard, name='dashboard'),

    # Student
    path('add-student/', views.add_student, name='add_student'),
    path('students/', views.student_list, name='student_list'),
    path('edit-student/<int:id>/', views.edit_student, name='edit_student'),
    path('delete-student/<int:id>/', views.delete_student, name='delete_student'),

    # Room
    path('rooms/', views.room_list, name='rooms'),
    path('suggest-room/', views.suggest_room, name='suggest_room'),

    # Fees
    path('fees/', views.fee, name='fee'),
    path('pay-fee/<int:id>/', views.pay_fee, name='pay_fee'),

    # Other
    path('complaint/', views.complaint, name='complaint'),
    path('visitor/', views.visitor, name='visitor'),
]