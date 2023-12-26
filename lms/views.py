from django.shortcuts import render,HttpResponse,redirect, get_object_or_404, redirect
from django.contrib import messages
from .models import *
from django.core.paginator import  PageNotAnInteger, EmptyPage, Paginator# Create your views here.
from django.contrib.auth.decorators import login_required
from django.views.decorators.cache import never_cache
from django.contrib.auth import logout
from .forms import *
from django.views.decorators.cache import never_cache
from django.db.models import Q


@login_required(login_url='profile')
def custom_logout(request):
    logout(request)
    messages.success(request, "You are logged out!")
    return redirect('home')

@never_cache
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
    author = Author.objects.all()
    total_author = author.count()
    
    course = Course.objects.all()
    total_course = course.count()
    enrollments = Enrollment.objects.filter(approved=True)
    total_enrolled_students = enrollments.count()
    courses = Course.objects.order_by('-created_date')[:6]
    context = {
        'total_enrolled_students':total_enrolled_students,
        'total_course': total_course,
        'total_author': total_author,
        'courses': courses,
    }
    return render(request, 'home.html', context)


def courses(request):
    queryset = Course.objects.order_by('-created_date')
    page = request.GET.get('page',1)
    paginator = Paginator(queryset,6)
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
    total_enroll = Enrollment.objects.filter(course=course)
    total_enrolled_students = total_enroll.count()
    context = {
        'course': course,
        'enrollments': enrollments,
        'total_enrolled_students':total_enrolled_students,
    }
    
    return render(request, 'course_details.html', context)

@login_required(login_url='profile')
def dashboard(request):
    user_enrollments = Enrollment.objects.filter(user=request.user, approved=True)
    return render(request, 'dashboard.html', {'user_enrollments': user_enrollments})




# views.py

@login_required(login_url='profile')
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


@login_required(login_url='profile')
def course_playlist(request, course_slug):
    # Get the course using the provided slug
    course = get_object_or_404(Course, slug=course_slug)

    # Check if the user is enrolled in the specified course
    if Enrollment.objects.filter(user=request.user, course=course, approved=True).exists():
        # User is enrolled and approved, render the playlist page
        return render(request, 'playlist.html', {'course': course})
    else:
        # User is not enrolled or not approved, redirect them to another page or show an error message
        return redirect('courses')  # Redirect to the courses page or another appropriate page



def search_courses(request):
    search_key = request.GET.get('search', None)
    courses = Course.objects.filter(
        Q(title__icontains=search_key) |
        Q(price__icontains=search_key) |     
        Q(skill_level__icontains=search_key) |
        Q(language__icontains=search_key) |
        Q(category__title__icontains=search_key) |
        Q(author__name__icontains=search_key)
    )
    
    # Get the count of search results
    search_results_count = courses.count()

    context = {
        "courses": courses,
        "search_key": search_key,
        "search_results_count": search_results_count,
    }
    return render(request, 'search_result.html', context)


   