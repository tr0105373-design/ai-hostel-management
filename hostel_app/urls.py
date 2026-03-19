from django.urls import path
from . import views

urlpatterns = [

    path('add_student/', views.add_student, name='add_student'),
    path('students/', views.student_list, name='student_list'),
    path('edit_student/<int:id>/', views.edit_student, name='edit_student'),
    path('delete_student/<int:id>/', views.delete_student, name='delete_student'),
    path('suggest_room/', views.suggest_room, name='suggest_room'),
    path('fee/', views.fee, name='fee'),
    path('pay_fee/<int:id>/', views.pay_fee, name='pay_fee'),
    path('rooms/', views.room_list, name='rooms'),

]