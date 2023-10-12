from django.contrib import admin

from .models import TeacherUser, Student, Attendance, Class, Department
# Register your models here.

# admin.site.register(TeacherUser),
# admin.site.register(Student),
# admin.site.register(Attendance),
# admin.site.register(Class),
admin.site.register(Department),

class AttendanceAdmin(admin.ModelAdmin):
    list_display = ('student', 'date', 'is_present')
    list_filter = ('student__class_name', 'student__class_name__teacher')
    search_fields = ('student__name', 'student__ID', 'student__class_name__name', 'student__class_name__teacher__username')
admin.site.register(Attendance, AttendanceAdmin)

class StudentAdmin(admin.ModelAdmin):
    list_display = ('name', 'ID', 'class_name')
    list_filter = ('class_name', 'class_name__teacher')
    search_fields = ('name', 'ID', 'class_name__name', 'class_name__teacher__username')
    list_display_links = ('name', 'ID')
admin.site.register(Student, StudentAdmin)

class ClassAdmin(admin.ModelAdmin):
    list_display = ('name','department', 'teacher')
    list_filter = ('department__name','teacher__username')  
    search_fields = ('name','department__name','teacher__username')
admin.site.register(Class, ClassAdmin)

class TeacherUserAdmin(admin.ModelAdmin):
    list_display = ('username', 'firstname', 'lastname', 'email', 'teacher_id')
    list_filter = ('firstname', 'lastname', 'teacher_id')  
    search_fields = ('username', 'firstname', 'lastname', 'teacher_id','email')  
admin.site.register(TeacherUser, TeacherUserAdmin)