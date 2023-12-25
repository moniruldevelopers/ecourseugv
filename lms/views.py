from django.shortcuts import render,HttpResponse,redirect, get_object_or_404, redirect
from django.contrib import messages
from .models import *
from django.core.paginator import  PageNotAnInteger, EmptyPage, Paginator# Create your views here.
from django.contrib.auth.decorators import login_required
from django.views.decorators.cache import never_cache
from django.contrib.auth import logout
from .forms import *



@login_required(login_url='profile')
def custom_logout(request):
    logout(request)
    messages.success(request, "You are logged out!")
    return redirect('home')

@login_required
def profile(request):
    if request.user.is_authenticated:
        # Check if the user is a superuser or staff user
        if request.user.is_superuser or request.user.is_staff:
            return redirect('admin:index')  # Redirect to the admin panel
        else:
            messages.success(request, "You are logged in successfully")
            return redirect('home')

    return render(request, 'account/login.html')



def home(request):
    return render(request, 'home.html')


def courses(request):
    queryset = Course.objects.order_by('-created_date')
    page = request.GET.get('page',1)
    paginator = Paginator(queryset,1)
    try:
        courses = paginator.page(page)
    except EmptyPage:
        courses = paginator.page(1)
    except PageNotAnInteger:
        courses = paginator.page(1)
        return redirect('home')

#   end pagination

    context = {
        'courses': courses,
        'paginator': paginator,      
    }
    return render (request, 'courses.html', context)
@login_required(login_url='profile')
def course_details(request, slug):
    course = Course.objects.get(slug=slug)
    enrollments = Enrollment.objects.filter(user=request.user, course=course)
    
    return render(request, 'course_details.html', {'course': course, 'enrollments': enrollments})

@login_required
def dashboard(request):
    user_enrollments = Enrollment.objects.filter(user=request.user, approved=True)
    return render(request, 'dashboard.html', {'user_enrollments': user_enrollments})




# views.py

@login_required
def enroll(request, slug):
    course = Course.objects.get(slug=slug)

    if request.method == 'POST':
        form = EnrollmentForm(request.POST)
        if form.is_valid():
            enrollment = form.save(commit=False)
            enrollment.user = request.user
            enrollment.course = course  # Set the course before saving the enrollment
            enrollment.course_price = course.price  # Set the course price
            enrollment.save()
            messages.success(request, 'Enrollment request submitted. Please wait for approval.')
            return redirect('course_details', slug=slug)
    else:
        form = EnrollmentForm()

    return render(request, 'enroll.html', {'course': course, 'form': form})




