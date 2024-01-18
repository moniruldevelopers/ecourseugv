from django.contrib import admin
from .models import *
import csv
from django.http import HttpResponse
from import_export.admin import ImportExportModelAdmin
from django.utils.translation import gettext as _
from reportlab.pdfgen import canvas
# Register your models here.
class VideoInline(admin.TabularInline):
    model = Video

class CourseAdmin(admin.ModelAdmin):  # Inherit from ImportExportModelAdmin
    inlines = [VideoInline]
    list_filter = ['author', 'category']
    search_fields = ['title', 'author__name']
    list_display = ['author', 'category', 'title']  

admin.site.register(Course, CourseAdmin)

admin.site.register(Author)
admin.site.register(Category)


class EnrollmentAdmin(ImportExportModelAdmin):
    list_display = ["approved", "phone_number", "transaction_id","batch_no", "course_price", "user", "student_id", "department", "semester", "course"]

    
    list_filter = ["batch_no","approved", "department", "semester", "course"]

    # Define the export action
    def export_selected(self, request, queryset):
        return super().export_action(request, queryset)
    export_selected.short_description = "Export selected Enrollers"



admin.site.register(Enrollment, EnrollmentAdmin)
admin.site.register(Wishlist)
admin.site.register(Team)
admin.site.register(Contact)