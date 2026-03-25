from django.contrib import admin
from .models import Student, Room, Fee, Complaint, Warden, Visitor

admin.site.register(Student)
admin.site.register(Room)
admin.site.register(Fee)
admin.site.register(Complaint)
admin.site.register(Warden)
admin.site.register(Visitor)