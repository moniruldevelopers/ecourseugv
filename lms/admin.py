from django.contrib import admin
from .models import *
# Register your models here.
class VideoInline(admin.TabularInline):
    model = Video

class CourseAdmin(admin.ModelAdmin):
    inlines = [VideoInline]

admin.site.register(Course, CourseAdmin)
admin.site.register(Author)
admin.site.register(Category)


class EnrollmentAdmin(admin.ModelAdmin):
    list_display = ["approved","phone_number","transaction_id","course_price", "user","student_id","department", "semester","course"]
admin.site.register(Enrollment,EnrollmentAdmin)

admin.site.register(Wishlist)