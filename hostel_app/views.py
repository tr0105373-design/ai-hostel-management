from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from django.db.models import Count, Case, When, Value, IntegerField
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib import messages
from .models import Student, Room, Complaint, Fee, Visitor, Activity, Notice
from .forms import StudentForm


# ══════════════════════════════════════════
# AI FUNCTIONS
# ══════════════════════════════════════════

def ai_complaint_priority(text):
    text = text.lower()
    if "water" in text or "electricity" in text or "fire" in text:
        return "High"
    elif "cleaning" in text or "fan" in text or "light" in text:
        return "Medium"
    else:
        return "Low"


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


# ══════════════════════════════════════════
# ADMIN AUTH VIEWS
# ══════════════════════════════════════════

def user_login(request):
    if request.user.is_authenticated:
        return redirect('home')

    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, 'Invalid username or password!')

    return render(request, 'hostel_app/login.html')


def user_logout(request):
    logout(request)
    return redirect('login')


# ══════════════════════════════════════════
# ADMIN MAIN VIEWS
# ══════════════════════════════════════════

@login_required(login_url='login')
def home(request):
    students = Student.objects.count()
    rooms = Room.objects.count()
    complaints = Complaint.objects.filter(status='Pending').count()
    fees = Fee.objects.filter(status='Pending').count()

    return render(request, 'hostel_app/home.html', {
        'students': students,
        'rooms': rooms,
        'complaints': complaints,
        'fees': fees,
    })


@login_required(login_url='login')
def dashboard(request):
    students = Student.objects.count()
    rooms = Room.objects.count()
    complaints = Complaint.objects.filter(status='Pending').count()
    fees = Fee.objects.filter(status='Pending').count()
    high_priority = Complaint.objects.filter(priority='High').count()
    resolved = Complaint.objects.filter(status='Resolved').count()
    activities = Activity.objects.order_by('-created_at')[:5]

    return render(request, 'hostel_app/dashboard.html', {
        'students': students,
        'rooms': rooms,
        'complaints': complaints,
        'fees': fees,
        'high_priority': high_priority,
        'resolved': resolved,
        'activities': activities,
    })


def suggest_room():
    return Room.objects.filter(occupied=False).first()


@login_required(login_url='login')
def add_student(request):
    if request.method == "POST":
        form = StudentForm(request.POST)
        if form.is_valid():
            student = form.save(commit=False)

            # Room suggest karo
            room = suggest_room()
            if room:
                student.room_number = room.room_number
                room.occupied = room.occupied + 1
                room.save()

            # Django User banao student ke liye
            email = form.cleaned_data.get('email')
            name = form.cleaned_data.get('name')
            username = email.split('@')[0]
            password = request.POST.get('password', '12345678')

            user = User.objects.create_user(
                username=username,
                email=email,
                password=password,
                first_name=name
            )
            student.user = user
            student.save()

            Activity.objects.create(message=f"New student added: {name}")
            return redirect('student_list')
    else:
        form = StudentForm()
    return render(request, 'hostel_app/add_student.html', {'form': form})


@login_required(login_url='login')
def student_list(request):
    query = request.GET.get('q')
    course = request.GET.get('course')
    students = Student.objects.all()
    if query:
        students = students.filter(name__icontains=query)
    if course:
        students = students.filter(course__icontains=course)
    return render(request, 'hostel_app/student_list.html', {'students': students})


@login_required(login_url='login')
def edit_student(request, id):
    student = get_object_or_404(Student, id=id)
    form = StudentForm(request.POST or None, instance=student)
    if form.is_valid():
        form.save()
        return redirect('student_list')
    return render(request, 'hostel_app/edit_student.html', {'form': form})


@login_required(login_url='login')
def delete_student(request, id):
    student = get_object_or_404(Student, id=id)
    student.delete()
    return redirect('student_list')


@login_required(login_url='login')
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
        Activity.objects.create(message="New complaint submitted")
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


@login_required(login_url='login')
def resolve_complaint(request, id):
    c = Complaint.objects.get(id=id)
    c.status = "Resolved"
    c.save()
    return redirect('complaint')


@login_required(login_url='login')
def fee(request):
    students = Student.objects.all()
    if request.method == "POST":
        student_id = request.POST.get("student")
        amount = request.POST.get("amount")
        Fee.objects.create(student_id=student_id, amount=amount, status="Pending")
        return redirect('fee')
    fees = Fee.objects.all()
    return render(request, 'hostel_app/fee.html', {'students': students, 'fees': fees})


@login_required(login_url='login')
def pay_fee(request, id):
    f = Fee.objects.get(id=id)
    f.status = "Paid"
    f.save()
    return redirect('fee')


@login_required(login_url='login')
def room_list(request):
    rooms = Room.objects.all()
    return render(request, 'hostel_app/rooms.html', {'rooms': rooms})


@login_required(login_url='login')
def visitor(request):
    if request.method == "POST":
        visitor_name = request.POST.get("visitor_name")
        student = request.POST.get("student")
        Visitor.objects.create(
            visitor_name=visitor_name,
            student_id=student
        )
        Activity.objects.create(message="Visitor entry added")
        return redirect('visitor')

    visitors = Visitor.objects.all()
    frequent_visitors = Visitor.objects.values('visitor_name') \
        .annotate(count=Count('visitor_name')) \
        .filter(count__gt=3)

    return render(request, 'hostel_app/visitor.html', {
        'visitors': visitors,
        'frequent_visitors': frequent_visitors
    })


# ══════════════════════════════════════════
# STUDENT SIDE VIEWS
# ══════════════════════════════════════════

def student_login(request):
    if request.method == "POST":
        email = request.POST.get('email')
        password = request.POST.get('password')

        try:
            student = Student.objects.get(email=email)
            user = authenticate(
                request,
                username=student.user.username,
                password=password
            )
            if user is not None:
                login(request, user)
                return redirect('student_dashboard')
        except:
            pass

        return render(request, 'hostel_app/student/login.html',
                      {'error': 'Invalid Email or Password!'})

    return render(request, 'hostel_app/student/login.html')


def student_logout(request):
    logout(request)
    return redirect('student_login')


@login_required(login_url='/student/login/')
def student_dashboard(request):
    student = Student.objects.get(user=request.user)
    fees = Fee.objects.filter(student=student)
    complaints = Complaint.objects.filter(student=student)
    notices = Notice.objects.order_by('-created_at')[:5]

    return render(request, 'hostel_app/student/dashboard.html', {
        'student': student,
        'pending_fees': fees.filter(status='Pending').count(),
        'paid_fees': fees.filter(status='Paid').count(),
        'total_complaints': complaints.count(),
        'pending_complaints': complaints.filter(status='Pending').count(),
        'notices': notices,
    })


@login_required(login_url='/student/login/')
def student_profile(request):
    student = Student.objects.get(user=request.user)
    return render(request, 'hostel_app/student/profile.html',
                  {'student': student})


@login_required(login_url='/student/login/')
def my_room(request):
    student = Student.objects.get(user=request.user)
    roommates = Student.objects.filter(
        room_number=student.room_number
    ).exclude(id=student.id)
    return render(request, 'hostel_app/student/room.html', {
        'student': student,
        'roommates': roommates
    })


@login_required(login_url='/student/login/')
def student_complaint(request):
    student = Student.objects.get(user=request.user)
    complaints = Complaint.objects.filter(student=student)

    if request.method == "POST":
        message = request.POST.get('description')
        priority = ai_complaint_priority(message)
        category = ai_complaint_category(message)

        Complaint.objects.create(
            student=student,
            title=request.POST.get('title', 'General'),
            message=message,
            priority=priority,
            category=category,
            status='Pending'
        )
        return redirect('student_complaint')

    return render(request, 'hostel_app/student/complaint.html', {
        'student': student,
        'complaints': complaints
    })


@login_required(login_url='/student/login/')
def visitor_request(request):
    student = Student.objects.get(user=request.user)
    visitors = Visitor.objects.filter(student=student)

    if request.method == "POST":
        Visitor.objects.create(
            visitor_name=request.POST.get('name'),
            purpose=request.POST.get('purpose', 'Visit'),
            student=student
        )
        return redirect('visitor_request')

    return render(request, 'hostel_app/student/visitor.html', {
        'student': student,
        'visitors': visitors
    })


@login_required(login_url='/student/login/')
def my_fees(request):
    student = Student.objects.get(user=request.user)
    fees = Fee.objects.filter(student=student)
    return render(request, 'hostel_app/student/fees.html', {
        'student': student,
        'fees': fees
    })


@login_required(login_url='/student/login/')
def student_notices(request):
    student = Student.objects.get(user=request.user)
    notices = Notice.objects.order_by('-created_at')
    return render(request, 'hostel_app/student/notices.html', {
        'student': student,
        'notices': notices
    })