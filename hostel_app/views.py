from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from .models import Student, Room, Complaint, Fee, Visitor
from .forms import StudentForm
from django.db.models import Count, Case, When, Value, IntegerField


# AI Complaint Priority Function
def ai_complaint_priority(text):
    text = text.lower()

    if "water" in text or "electricity" in text or "fire" in text:
        return "High"
    elif "cleaning" in text or "fan" in text or "light" in text:
        return "Medium"
    else:
        return "Low"


# AI Complaint Category
def ai_complaint_category(text):
    text = text.lower()

    if "fan" in text:
        return "Fan"
    elif "water" in text or "leak" in text:
        return "Maintenance"
    elif "electricity" in text or "light" in text:
        return "Electrical"
    else:
        return "General"


# Home Page
def home(request):
    return render(request, 'hostel_app/home.html')


# Dashboard
def dashboard(request):
    students = Student.objects.count()
    rooms = Room.objects.count()
    complaints = Complaint.objects.filter(status="Pending").count()
    fees = Fee.objects.filter(status="Pending").count()
    high_priority = Complaint.objects.filter(priority="High").count()
    resolved = Complaint.objects.filter(status="Resolved").count()

    return render(request, 'hostel_app/dashboard.html', {
        'students': students,
        'rooms': rooms,
        'complaints': complaints,
        'fees': fees,
        'high_priority': high_priority,
        'resolved': resolved,
    })


# Room Suggestion
def suggest_room():
    return Room.objects.filter(occupied=False).first()


# Add Student
def add_student(request):
    if request.method == "POST":
        form = StudentForm(request.POST)

        if form.is_valid():
            student = form.save(commit=False)

            room = suggest_room()

            if room:
                student.room_number = room.room_number
                room.occupied = room.occupied + 1
                room.save()

            student.save()
            return redirect('student_list')

    else:
        form = StudentForm()

    return render(request, 'hostel_app/add_student.html', {'form': form})


# Student List
def student_list(request):
    query = request.GET.get('q')
    course = request.GET.get('course')

    students = Student.objects.all()

    if query:
        students = students.filter(name__icontains=query)

    if course:
        students = students.filter(course__icontains=course)

    return render(request, 'hostel_app/student_list.html', {'students': students})


# Edit Student
def edit_student(request, id):
    student = get_object_or_404(Student, id=id)
    form = StudentForm(request.POST or None, instance=student)

    if form.is_valid():
        form.save()
        return redirect('student_list')

    return render(request, 'hostel_app/edit_student.html', {'form': form})


# Delete Student
def delete_student(request, id):
    student = get_object_or_404(Student, id=id)
    student.delete()
    return redirect('student_list')


# Complaint System
def complaint(request):
    if request.method == "POST":
        student_id = request.POST.get("student")
        message = request.POST.get("message")

        priority = ai_complaint_priority(message)
        category = ai_complaint_category(message)

        Complaint.objects.create(
            student_id=student_id,
            message=message,
            status="Pending",
            priority=priority,
            category=category
        )

        return redirect('complaint')

    students = Student.objects.all()
    query = request.GET.get('q')

    complaints = Complaint.objects.annotate(
        priority_order=Case(
            When(priority='High', then=Value(1)),
            When(priority='Medium', then=Value(2)),
            When(priority='Low', then=Value(3)),
            output_field=IntegerField(),
        )
    )

    if query:
        complaints = complaints.filter(message__icontains=query)

    complaints = complaints.order_by('priority_order')

    return render(request, 'hostel_app/complaint.html', {
        'students': students,
        'complaints': complaints
    })


# Resolve Complaint
def resolve_complaint(request, id):
    complaint = Complaint.objects.get(id=id)
    complaint.status = "Resolved"
    complaint.save()
    return redirect('complaint')


# Fee
def fee(request):
    students = Student.objects.all()

    if request.method == "POST":
        student_id = request.POST.get("student")
        amount = request.POST.get("amount")

        Fee.objects.create(
            student_id=student_id,
            amount=amount,
            status="Pending"
        )

        return redirect('fee')

    fees = Fee.objects.all()

    return render(request, 'hostel_app/fee.html', {
        'students': students,
        'fees': fees
    })


def pay_fee(request, id):
    fee = Fee.objects.get(id=id)
    fee.status = "Paid"
    fee.save()
    return redirect('fee')


# Rooms
def room_list(request):
    rooms = Room.objects.all()
    return render(request, 'hostel_app/rooms.html', {'rooms': rooms})


# Visitors
def visitor(request):
    visitors = Visitor.objects.all()

    frequent_visitors = Visitor.objects.values('visitor_name')\
        .annotate(count=Count('visitor_name'))\
        .filter(count__gt=3)

    return render(request, 'hostel_app/visitor.html', {
        'visitors': visitors,
        'frequent_visitors': frequent_visitors
    })