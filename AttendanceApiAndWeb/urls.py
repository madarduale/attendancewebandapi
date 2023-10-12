from django.urls import path
# from django.contrib.auth.views import LoginView, LogoutView


from .views import (
   
   #DJANGO API VIEWS

   HomeAPIView,
   DepartmentCreateAPIView,
   DepartmentListAPIView,
   DepartmentDetailAPIView,
   DepartmentUpdateAPIView,
   DepartmentDeleteAPIView,


    StudentCreateAPIView,
    StudentListAPIView,
    StudentDetailAPIView,
    StudentUpdateAPIView,
    StudentDeleteAPIView,

    ClassCreateAPIView,
    ClassListAPIView,
    ClassDetailAPIView,
    ClassUpdateAPIView,
    ClassDeleteAPIView,

    ClassAttendanceAPIView,


    TeacherUserCreateAPIView,
    TeacherUserListAPIView,
    TeacherUserDetailAPIView,
    TeacherUserUpdateAPIView,
    TeacherUserDeleteAPIView,

    UserProfileAPIView,

    GenerateStudentReportAPIView,

    LoginAPIView,
    LogoutAPIView,

#DJANGO VIEWS

     department_list, 
    department_detail, 
    class_detail, 
    student_detail,
    teacher_detail, 
    department_create, 
    class_create, 
    student_create, 
    class_attendance, 
    generate_student_report, 
    department_update,
    class_update,
    student_update,
    teacher_update,
    # teacher_create,
    teacher_list,
    home,
    logout_view,
    delete_department,
    delete_class,
    delete_student,
    delete_teacher,
    TeacherSignUpView, 
    TeacherLoginView, 
    TeacherProfileView, 
    ClassListView, 
    StudentListView,
    login,
)




urlpatterns = [

    #DJANGO API VIEWS


    path('api/home/', HomeAPIView.as_view(), name='api_home'),
    path('api/login/', LoginAPIView.as_view(), name='api_login'),
    path('api/logout/', LogoutAPIView.as_view(), name='api_logout'),
    # DEPARTMENT
    path('api/create_department/', DepartmentCreateAPIView.as_view(), name='api_create_department'),
    path('api/department_list/', DepartmentListAPIView.as_view(), name='api_department_list'),
    path('api/department_detail/<int:department_id>/', DepartmentDetailAPIView.as_view(), name='api_department_detail'),
    path('api/department_update/<int:department_id>/', DepartmentUpdateAPIView.as_view(), name='api_department_update'),
    path('api/department_delete/<int:department_id>/', DepartmentDeleteAPIView.as_view(), name='api_department_delete'),

    # STUDENTS
    path('api/student-create/', StudentCreateAPIView.as_view(), name='student_create_api'),
    path('api/student-list/', StudentListAPIView.as_view(), name='student_list_api'),
    path('api/student-detail/<int:student_id>/', StudentDetailAPIView.as_view(), name='student_detail_api'),
    path('api/student-update/<int:student_id>/', StudentUpdateAPIView.as_view(), name='student_update_api'),
    path('api/student-delete/<int:student_id>/', StudentDeleteAPIView.as_view(), name='student_delete_api'),


    # CLASSES
    path('api/class-create/', ClassCreateAPIView.as_view(), name='class_create_api'),
    path('api/class-list/', ClassListAPIView.as_view(), name='class_list_api'),
    path('api/class-detail/<int:class_id>/', ClassDetailAPIView.as_view(), name='class_detail_api'),
    path('api/class-update/<int:class_id>/', ClassUpdateAPIView.as_view(), name='Class_update_api'),
    path('api/class-delete/<int:class_id>/', ClassDeleteAPIView.as_view(), name='class_delete_api'),

    #ATTENDANCE
    path('api/class-attendance/<int:class_id>/', ClassAttendanceAPIView.as_view(), name='class_attendance_api'),


    path('api/teacher-create/', TeacherUserCreateAPIView.as_view(), name='teacher_create_api'),
    path('api/teacher-list/', TeacherUserListAPIView.as_view(), name='teacher_list_api'),
    path('api/teacher-detail/<int:teacher_id>/', TeacherUserDetailAPIView.as_view(), name='teacher_detail_api'),
    path('api/teacher-update/<int:teacher_id>/', TeacherUserUpdateAPIView.as_view(), name='teacher_update_api'),
    path('api/teacher-delete/<int:teacher_id>/', TeacherUserDeleteAPIView.as_view(), name='teacher_delete_api'),

    #TeacherProfile
    path('api/user-profile/', UserProfileAPIView.as_view(), name='user_profile_api'),


    path('api/generate_student_report/', GenerateStudentReportAPIView.as_view(), name='generate_student_report'),
   


#DJANGO VIEWS URLS


 path("", home, name="home"),
    path('departments/', department_list, name='department_list'),
    path('departments/create/', department_create, name='department_create'),
    path('departments/<int:department_id>/', department_detail, name='department_detail'),
    path('department/<int:department_id>/delete/', delete_department, name='delete_department'),
    path('classes/', ClassListView.as_view(), name='class_list'),
    path('classes/<int:class_id>/', class_detail, name='class_detail'),
    path('classes/<int:class_id>/delete/', delete_class, name='delete_class'),
    path('classes/create/', class_create, name='class_create'),
    path('students/', StudentListView.as_view(), name='student_list'),
    path('students/<int:student_id>/', student_detail, name='student_detail'),
    path('student/<int:student_id>/delete/', delete_student, name='delete_student'),
    path('teachers/<int:teacher_id>/', teacher_detail, name='teacher_detail'),
    path('teacher/<int:teacher_id>/delete/', delete_teacher, name='delete_teacher'),
    path('students/create/', student_create, name='student_create'),
    path('teachers/', teacher_list, name='teacher_list'),
    # path('teachers/create/', teacher_create, name='teacher_create'),
    path('teachers/signup/', TeacherSignUpView.as_view(), name='teacher_signup'),
    path('teachers/login/', TeacherLoginView.as_view(), name='teacher_login'),
    path('logout/', logout_view, name='logout'),
    path('teachers/profile/', TeacherProfileView.as_view(), name='teacher_profile'),
    path('classes/<int:class_id>/attendance/', class_attendance, name='class_attendance'),
    path('generate-report/', generate_student_report, name='generate_student_report'),
    path('department/<int:department_id>/update/', department_update, name='department_update'),
    path('class/<int:class_id>/update/', class_update, name='class_update'),
    path('student/<int:student_id>/update/', student_update, name='student_update'),
    path('teacher/<int:teacher_id>/update/', teacher_update, name='teacher_update'),
    # path('admin/login/', LoginView.as_view(), name='admin_login'),
    # path('admin/logout/', LogoutView.as_view(), name='admin_logout'),

]