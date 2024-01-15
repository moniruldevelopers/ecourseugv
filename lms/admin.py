from django.contrib import admin
from .models import *
import csv
from django.http import HttpResponse



from django.utils.translation import gettext as _
from reportlab.pdfgen import canvas
# Register your models here.
class VideoInline(admin.TabularInline):
    model = Video

class CourseAdmin(admin.ModelAdmin):
    inlines = [VideoInline]

admin.site.register(Course, CourseAdmin)
admin.site.register(Author)
admin.site.register(Category)


class EnrollmentAdmin(admin.ModelAdmin):
    list_display = ["approved", "phone_number", "transaction_id", "course_price", "user", "student_id", "department", "semester", "course"]

    actions = ['export_selected_csv', 'export_selected_pdf']

    def export_selected_csv(modeladmin, request, queryset):
        return modeladmin.export_selected(request, queryset, file_format='csv')

    export_selected_csv.short_description = "Export selected enrollments as CSV"

    def export_selected_pdf(modeladmin, request, queryset):
        return modeladmin.export_selected(request, queryset, file_format='pdf')

    export_selected_pdf.short_description = "Export selected enrollments as PDF"

    list_filter = ["approved", "department", "semester", "course"]

    # Common export function
    def export_selected(modeladmin, request, queryset, file_format='csv'):
        if file_format == 'csv':
            return modeladmin.export_as_csv(request, queryset)
        elif file_format == 'pdf':
            return modeladmin.export_as_pdf(request, queryset)

    def export_as_csv(self, request, queryset):
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename=enrollment_data.csv'
        writer = csv.writer(response)

        # Write header
        writer.writerow(["student_id", "department","semester","phone_number", "course"])

        # Write data rows
        for enrollment in queryset:
            row_data = [                
                enrollment.student_id,    
                enrollment.department, 
                enrollment.semester,        
                str(enrollment.phone_number),
                enrollment.course
            ]
            writer.writerow(row_data)

        return response

    def export_as_pdf(self, request, queryset):
        response = HttpResponse(content_type='application/pdf')
        response['Content-Disposition'] = 'attachment; filename=enrollment_data.pdf'

        # Create PDF document
        p = canvas.Canvas(response)

        # Write column names as headers
        col_names = ["student_id", "department","semester","phone_number", "course"]
        row_height = 20
        for j, col_name in enumerate(col_names):
            p.drawString(100 + j * 100, 800, col_name)

        # Write data rows
        for i, enrollment in enumerate(queryset, start=1):
            row_data = [  
                enrollment.student_id,    
                enrollment.department, 
                enrollment.semester,        
                str(enrollment.phone_number),
                enrollment.course
            ]
            for j, data in enumerate(row_data):
                p.drawString(100 + j * 100, 800 - i * row_height, str(data))

        p.showPage()
        p.save()

        return response



admin.site.register(Enrollment, EnrollmentAdmin)
admin.site.register(Wishlist)
admin.site.register(Team)
admin.site.register(Contact)