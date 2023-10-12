

# Create your views here.


import os
from io import BytesIO
from reportlab.pdfgen import canvas
from django.http import HttpResponse
from rest_framework.views import APIView
from rest_framework.exceptions import NotFound
from rest_framework.response import Response
from rest_framework import status
from datetime import date
from django.urls import reverse
from django.shortcuts import render, redirect, get_object_or_404
from .authentications import TeacherAuthentication, SuperuserAuthencication
from .permissions import IsTeacherOrSuperuser
from rest_framework.authtoken.models import Token
from .models import Department, Class, Student, Attendance, TeacherUser
from .serializers import DepartmentSerializer, StudentSerializer, ClassSerializer, TeacherUserSerializer, AttendanceSerializer
from django.contrib.auth import login, authenticate, logout
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated


from django.http import HttpResponse



# DJANGO REST FRAMEWORK API VIEWS
class HomeAPIView(APIView):
    def get(self, request):
        data = {
            'message': 'Welcome to the home page!',
            'some_key': 'some_value',
        }

        return Response(data)




class LoginAPIView(APIView):
    def get(self, request):
        return Response({'error': 'Please login to get a token'}, status=status.HTTP_400_BAD_REQUEST)
    
    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')
        
        if username and password:
            user = authenticate(username=username, password=password)
            if user:
                token, created = Token.objects.get_or_create(user=user)
                classes = Class.objects.filter(teacher=user)
                response_data = {
                    'first_name': user.firstname,
                    'last_name': user.lastname,
                    'is_active': user.is_active,
                    'is_staff': user.is_staff,
                    'token': token.key,
                    'user_id': user.id,
                    'username': user.username,
                    'email': user.email,
                    'is_teacher':user.is_teacher,
                    'is_superuser':user.is_superuser,
                    'teacher_id':user.teacher_id,
                    'classes':[class_.name for class_ in classes]   
                }
                
                print(user.is_teacher)
                return Response(response_data)
            else:
                return Response({'error': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)
        else:
            return Response({'error': 'Username and password are required'}, status=status.HTTP_400_BAD_REQUEST)
 

class LogoutAPIView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request):
        # Delete the user's token to logout
        if 'text/html' in request.META.get('HTTP_ACCEPT'):
            logout(request)
            return redirect('api_login')
        
        request.auth.delete()
        return Response(status=status.HTTP_200_OK)



class DepartmentCreateAPIView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    def get(self, request):
        # Handle GET request (if needed)
        return Response({})

    def post(self, request):
        serializer = DepartmentSerializer(data=request.data)
        if serializer.is_valid():
            department = serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class DepartmentListAPIView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    def get(self, request):
        departments = Department.objects.all().order_by('-id')
        if not departments:
            return Response({'message': 'No departments found'}, status=status.HTTP_204_NO_CONTENT)
        
        serializer = DepartmentSerializer(departments, many=True)
        return Response(serializer.data)
    
class DepartmentDetailAPIView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    def get_department(self, department_id):
        try:
            return Department.objects.get(id=department_id)
        except Department.DoesNotExist:
            raise NotFound(detail="Department not found", code=status.HTTP_404_NOT_FOUND)

    def get(self, request, department_id):
        department = self.get_department(department_id)
        serializer = DepartmentSerializer(department)
        return Response(serializer.data)
    
class DepartmentUpdateAPIView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    def get_department(self, department_id):
        try:
            return Department.objects.get(id=department_id)
        except Department.DoesNotExist:
            raise NotFound(detail="Department not found", code=status.HTTP_404_NOT_FOUND)

    def get(self, request, department_id):
        department = self.get_department(department_id)
        serializer = DepartmentSerializer(department)
        return Response(serializer.data)

    def put(self, request, department_id):
        department = self.get_department(department_id)
        serializer = DepartmentSerializer(department, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



class DepartmentDeleteAPIView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    def get_department(self, department_id):
        try:
            return Department.objects.get(id=department_id)
        except Department.DoesNotExist:
            raise NotFound(detail="Department not found", code=status.HTTP_404_NOT_FOUND)

    def get(self, request, department_id):
        department = self.get_department(department_id)
        serializer = DepartmentSerializer(department)
        return Response(serializer.data)

    def delete(self, request, department_id):
        department = self.get_department(department_id)
        department.delete()
        return Response({'message': 'Department deleted successfully ','department':department.name}, status=status.HTTP_204_NO_CONTENT)
        

class StudentCreateAPIView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    def post(self, request):
        serializer = StudentSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class StudentListAPIView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    def post(self, request):
        class_id = request.data.get('class_id')
        if class_id:
            try:
                selected_class = Class.objects.get(id=class_id)
                students = Student.objects.filter(class_name=selected_class)
                if students:
                    serializer = StudentSerializer(students, many=True)
                    return Response(serializer.data)
                else:
                    return Response({'message': 'No students found for this class'}, status=status.HTTP_204_NO_CONTENT)
            except Class.DoesNotExist:
                raise NotFound(detail="Class not found", code=status.HTTP_404_NOT_FOUND)
        else:
            return Response({'error': 'Please provide a valid class_id'}, status=status.HTTP_400_BAD_REQUEST)

class StudentDetailAPIView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    def get_student(self, student_id):
        try:
            return Student.objects.get(id=student_id)
        except Student.DoesNotExist:
            raise NotFound(detail="Student not found", code=status.HTTP_404_NOT_FOUND)

    def get(self, request, student_id):
        student = self.get_student(student_id)
        serializer = StudentSerializer(student)
        return Response(serializer.data)

class StudentUpdateAPIView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    def get_student(self, student_id):
        try:
            return Student.objects.get(id=student_id)
        except Student.DoesNotExist:
            raise NotFound(detail="Student not found", code=status.HTTP_404_NOT_FOUND)

    def get(self, request, student_id):
        student = self.get_student(student_id)
        serializer = StudentSerializer(student)
        return Response(serializer.data)

    def put(self, request, student_id):
        student = self.get_student(student_id)
        serializer = StudentSerializer(student, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class StudentDeleteAPIView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    def get_student(self, student_id):
        try:
            return Student.objects.get(id=student_id)
        except Student.DoesNotExist:
            raise NotFound(detail="Student not found", code=status.HTTP_404_NOT_FOUND)

    def get(self, request, student_id):
        student = self.get_student(student_id)
        serializer = StudentSerializer(student)
        return Response(serializer.data)

    def delete(self, request, student_id):
        student = self.get_student(student_id)
        student.delete()
        return Response({'message': 'Student deleted successfully ','student':student.name}, status=status.HTTP_204_NO_CONTENT)


class ClassCreateAPIView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    def post(self, request):
        class_serializer = ClassSerializer(data=request.data)
        if class_serializer.is_valid():
            class_serializer.save()
            return  Response(class_serializer.data, status=status.HTTP_201_CREATED)
        return Response(class_serializer.error, status=status.HTTP_400_BAD_REQUEST)


class ClassListAPIView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    def get(self, request):
        classes = list(Class.objects.all())
        if classes:
            serializer = ClassSerializer(classes, many=True)
            return Response(serializer.data)
        else:
            return Response({'message': 'No classes found'}, status=status.HTTP_204_NO_CONTENT)
        

class ClassDetailAPIView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    def get_class(self, class_id):
        try:
            return Class.objects.get(id=class_id)
        except Class.DoesNotExist:
            raise NotFound(detail="Class not found", code=status.HTTP_404_NOT_FOUND)
    
    def get(self,request, class_id):
        classe = self.get_class(class_id)
        serializer = ClassSerializer(classe)
        return Response(serializer.data)


class ClassUpdateAPIView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    def get_class(self, class_id):
        try:
            return Class.objects.get(id=class_id)
        except Class.DoesNotExist:
            raise NotFound(detail="Class not found", code=status.HTTP_404_NOT_FOUND)
    
    def get(self, request, class_id):
        classe = self.get_class(class_id)
        serializer = ClassSerializer(classe)
        return Response(serializer.data)
    
    def put(self, request, class_id):
        classe = self.get_class(class_id)
        serializer = ClassSerializer(classe, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ClassDeleteAPIView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    def get_class(self, class_id):
        try:
            return Class.objects.get(id=class_id)
        except Class.DoesNotExist:
            raise NotFound(detail="Class not found", code=status.HTTP_404_NOT_FOUND)
    
    def get(self, request, class_id):
        classe = self.get_class(class_id)
        serializer = ClassSerializer(classe)
        return Response(serializer.data)
    
    def delete(self, request, class_id):
        classe = self.get_class(class_id)
        classe.delete()
        return Response({'message': 'Class deleted successfully ','class':classe.name}, status=status.HTTP_204_NO_CONTENT)



class TeacherUserCreateAPIView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    def post(self, request, format=None):
        serializer = TeacherUserSerializer(data=request.data)
        if serializer.is_valid():
            is_superuser = serializer.validated_data.get('is_superuser', False)
            if is_superuser and not request.user.is_superuser:
                error_message = ['Only superusers can create other superusers.']
                return Response({'error':error_message}, status=status.HTTP_403_FORBIDDEN)
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            error_messages = {}
            for field, errors in serializer.errors.items():
                field_errors = []
                for error in errors:
                    # Customize error messages based on the field name and error message
                    field_errors.append(f"The {field} field {error}")
                error_messages[field] = field_errors
            return Response(error_messages, status=status.HTTP_400_BAD_REQUEST)



# class TeacherUserCreateAPIView(APIView):
#     def post(self, request, format=None):
#         serializer = TeacherUserSerializer(data=request.data)
#         if serializer.is_valid():
#             is_superuser = serializer.validated_data.get('is_superuser', False)
#             if is_superuser and not request.user.is_superuser:
#                 return Response({'error': 'Only superusers can create other superusers.'}, status=status.HTTP_403_FORBIDDEN)
#             serializer.save()
#             return Response(serializer.data, status=status.HTTP_201_CREATED)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    

class TeacherUserListAPIView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    def get(self, request):
        teachers = list(TeacherUser.objects.all())
        if teachers:
            serializer = TeacherUserSerializer(teachers, many=True)
            return Response(serializer.data)
        else:
            return Response({'message': 'No teachers found'}, status=status.HTTP_204_NO_CONTENT)
        
class TeacherUserDetailAPIView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    def get_teacher(self, teacher_id):
        try:
            return TeacherUser.objects.get(id=teacher_id)
        except TeacherUser.DoesNotExist:
            raise NotFound(detail="Teacher not found", code=status.HTTP_404_NOT_FOUND)
    
    def get(self,request, teacher_id):
        teacher = self.get_teacher(teacher_id)
        serializer = TeacherUserSerializer(teacher)
        return Response(serializer.data)
    
class TeacherUserUpdateAPIView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    def get_teacher(self, teacher_id):
        try:
            return TeacherUser.objects.get(id=teacher_id)
        except TeacherUser.DoesNotExist:
            raise NotFound(detail="Teacher not found", code=status.HTTP_404_NOT_FOUND)
    
    def get(self, request, teacher_id):
        teacher = self.get_teacher(teacher_id)
        serializer = TeacherUserSerializer(teacher)
        return Response(serializer.data)
    
    def put(self, request, teacher_id):
        teacher = self.get_teacher(teacher_id)
        serializer = TeacherUserSerializer(teacher, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class TeacherUserDeleteAPIView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    def get_teacher(self, teacher_id):
        try:
            return TeacherUser.objects.get(id=teacher_id)
        except TeacherUser.DoesNotExist:
            raise NotFound(detail="Teacher not found", code=status.HTTP_404_NOT_FOUND)
        
    def get(self, request, teacher_id):
        teacher = self.get_teacher(teacher_id)
        serializer = TeacherUserSerializer(teacher)
        return Response(serializer.data)
    
    def delete(self, request, teacher_id):
        teacher = self.get_teacher(teacher_id)
        teacher.delete()
        return Response({'message': 'teacher deleted successfully ','teacher':teacher.firstname +' '+ teacher.lastname}, status=status.HTTP_204_NO_CONTENT)
    


class UserProfileAPIView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = TeacherUser.objects.get(user=request.user)
        classes = Class.objects.filter(teacher=user)

        print(classes)
        print(user)
        serializer = TeacherUserSerializer(user)
        return Response(serializer.data)

    def put(self, request):
        serializer = TeacherUserSerializer(request.user, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



class ClassAttendanceAPIView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get_class_and_students(self, class_id):
        class_obj = get_object_or_404(Class, id=class_id)
        students = Student.objects.filter(class_name=class_obj)
        return class_obj, students

    def get(self, request, class_id):
        class_obj, students = self.get_class_and_students(class_id)
        attendance_data = Attendance.objects.filter(student__in=students, date=date.today())
        serializer = AttendanceSerializer(attendance_data, many=True)
        return Response(serializer.data)

    def post(self, request, class_id):
        class_obj, students = self.get_class_and_students(class_id)
        serializer = AttendanceSerializer(data=request.data, many=True)

        if serializer.is_valid():
            for student, attendance_status in zip(students, serializer.validated_data):
                Attendance.objects.create(student=student, date=date.today(), is_present=attendance_status['is_present'])
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)






class GenerateStudentReportAPIView(APIView):
    def post(self, request):
        error_message = None
        student_id = request.data.get('student_id')
        
        if student_id:
            student = get_object_or_404(Student, ID=student_id)
            pdf_content = self.generate_monthly_report(student)
            
            if pdf_content:
                # Create the 'pdfs' folder path relative to your Django project's root directory
                pdfs_folder = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'pdfs')
                
                # Check if the 'pdfs' folder exists, if not, create it
                if not os.path.exists(pdfs_folder):
                    os.makedirs(pdfs_folder)
                
                # Generate the file path for the PDF within the 'pdfs' folder
                file_path = os.path.join(pdfs_folder, f"monthly_report_{student.name}.pdf")
                
                # Save the PDF file to the 'pdfs' folder
                with open(file_path, 'wb') as pdf_file:
                    pdf_file.write(pdf_content)
                
                # Generate the PDF response
                response = HttpResponse(pdf_content, content_type='application/pdf')
                response['Content-Disposition'] = f'attachment; filename="monthly_report_{student.name}.pdf"'
                return response
            else:
                error_message = f"No report found for student '{student_id}'"
        else:
            error_message = "Please provide a student ID"
        
        return Response({'error': error_message}, status=400)
    
    def generate_monthly_report(self, student):
        # Create a new PDF file
        buffer = BytesIO()
        c = canvas.Canvas(buffer)
        
        # Get the attendance records for the student
        attendance_list = Attendance.objects.filter(student=student)
        
        # Set the initial y-coordinate for drawing
        y = 800
        
        # Write the student name
        c.setFont("Helvetica-Bold", 12)
        c.drawString(50, y, f"Student Name: {student.name}")
        
        c.setFont("Helvetica", 10)
        y -= 20
        
        # Write the attendance details
        for attendance in attendance_list:
            c.drawString(50, y, f"Date: {attendance.date}, Attendance: {'Present' if attendance.is_present else 'Absent'}")
            y -= 15
        
        # Save and close the PDF file
        c.save()
        
        # Get the PDF content from the buffer
        pdf_content = buffer.getvalue()
        buffer.close()
        
        return pdf_content







# DJANGO VIEWS FOR WEB
#import django abort function to return 403 error
# import  abort
from django.contrib import messages
from django.views import View
from .forms import DepartmentForm, ClassForm, StudentForm, AttendanceForm, TeacherSignUpForm, TeacherSignUpFormUpdate
from django.utils import timezone

from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter

from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
        
def home(request):
    return render(request, 'AttendanceApiAndWeb/home.html')

@login_required
def department_create(request):
    if request.user.is_superuser:
        if request.method == 'POST':
            form = DepartmentForm(request.POST)
            if form.is_valid():
                department_name = form.cleaned_data['name']
                if Department.objects.filter(name=department_name).exists():
                    form.add_error('name', 'Department name already exists.')
                else:
                    form.save()
                    return redirect('department_list')
        else:
            form = DepartmentForm()
        return render(request, 'AttendanceApiAndWeb/department_create.html', {'form': form})
    else:
        return handler403(request, exception=None)

@login_required
def class_create(request):
    if request.user.is_superuser:
        if request.method == 'POST':
            form = ClassForm(request.POST)
            if form.is_valid():
                class_name = form.cleaned_data['name']
                if Class.objects.filter(name=class_name).exists():
                    form.add_error('name', 'class name already exists.')
                else:
                    form.save()
                    return redirect('class_list')
        else:
            form = ClassForm()
        return render(request, 'AttendanceApiAndWeb/class_create.html', {'form': form})
    else:
         return handler403(request, exception=None)

@login_required
def student_create(request):
    if request.user.is_superuser:
        if request.method == 'POST':
            form = StudentForm(request.POST)
            if form.is_valid():
                form.save()
                return redirect('student_list')
        else:
            form = StudentForm()
        return render(request, 'AttendanceApiAndWeb/student_create.html', {'form': form})
    else:
         return handler403(request, exception=None)

# def teacher_create(request):
#     if request.method == 'POST':
#         form = TeacherForm(request.POST)
#         if form.is_valid():
#             form.save()
#             return redirect('teacher_list')
#     else:
#         form = TeacherForm()
#     return render(request, 'AttendanceApiAndWeb/teacher_create.html', {'form': form})

class TeacherSignUpView(View):
    def get(self, request):
        if request.user.is_superuser:
            form = TeacherSignUpForm()
            return render(request, 'AttendanceApiAndWeb/teacher_signup.html', {'form': form})
        else:
            return handler403(request, exception=None)

    def post(self, request):
        form = TeacherSignUpForm(request.POST)
        if form.is_valid():
            is_superuser = form.cleaned_data.get('is_superuser', False)
            if is_superuser and not request.user.is_superuser:
                messages.error(request, 'Only superusers can create other superusers.')
                return redirect('teacher_signup')
            user = form.save()
            # login(request, user)
            return redirect('teacher_login')
        return render(request, 'AttendanceApiAndWeb/teacher_signup.html', {'form': form})


# def Login(request):
#     username = request.POST.get('username')
#     password = request.POST.get('password')
#     user = authenticate(request, username=username, password=password)
#     if user is not None and user.is_teacher:
#         TeacherLoginView(View)
#     elif user is not None and user.is_superuser:
#         LoginView(request, user)
#     elif user is None:
#         error_message = 'Invalid username or password.'
#     else:
#         error_message = 'You are not authorized to log in as a teacher.'
#     return render(request, 'AttendanceApiAndWeb/teacher_login.html', {'error': error_message})


class TeacherLoginView(View):
    def get(self, request):
        return render(request, 'AttendanceApiAndWeb/teacher_login.html')
    def post(self, request):
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        # user_assigned_teacher = TeacherUser.objects.filter(user=user).exists()
        
       
        if user is not None:
            try:
                token = Token.objects.get(user=user)
                token.delete()
                print("token deleted")
            except Token.DoesNotExist:
                pass

            
            if  user.is_teacher:
            # print(user_assigned_teacher)
            # if user_assigned_teacher:  
                token = Token.objects.create(user=user)
                login(request, user)
                return redirect('teacher_profile')
            # else: 
            #      error_message = 'user is not assigned any teacher, your teacher profile is not complete.'
            elif  user.is_superuser:
                token = Token.objects.create(user=user)
                login(request, user)
                return redirect('home')
            else:
                error_message = 'You are not authorized to log in as a teacher.'
        else:
            error_message = 'Invalid username or password.'
        return render(request, 'AttendanceApiAndWeb/teacher_login.html', {'error': error_message})
    
@login_required
def logout_view(request):
    if request.user.is_authenticated:
        user=request.user
        logout(request)
        tokenkey = Token.objects.get(user=user)
        token =tokenkey.key
        username = Token.objects.get(key=token).user
        tokenkey.delete()
        print("token deleted")
        # try:
        #     token = Token.objects.get(user=request.user)
        #     print(token)
        #     token.delete()
        # except Token.DoesNotExist:
        #     pass
    return redirect('home')

class TeacherProfileView(LoginRequiredMixin, View):
    login_url = 'teacher_login'
    def get(self, request):
        teacher = TeacherUser.objects.get(username=request.user)
        classes = Class.objects.filter(teacher=teacher)
        return render(request, 'AttendanceApiAndWeb/teacher_profile.html', {'teacher': teacher, 'classes':classes})
    
@login_required(login_url='teacher_login')    
def department_list(request):
    if request.user.is_superuser:
        departments = Department.objects.all().order_by('-id')
        return render(request, 'AttendanceApiAndWeb/department_list.html', {'departments': departments})
    else:
         return handler403(request, exception=None)
    
@login_required(login_url='teacher_login')   
def department_detail(request, department_id):
    if request.user.is_superuser:
            department = get_object_or_404(Department, id=department_id)
            return render(request, 'AttendanceApiAndWeb/department_detail.html', {'department': department})
    else:
        return handler403(request, exception=None)

@login_required(login_url='teacher_login')   
def class_detail(request, class_id):
    if request.user.is_superuser:
        class_ = get_object_or_404(Class, id=class_id)
        return render(request, 'AttendanceApiAndWeb/class_detail.html', {'class': class_})
    else:
        return handler403(request, exception=None)

@login_required(login_url='teacher_login')   
def student_detail(request, student_id):
    if request.user.is_superuser:
        
        student = get_object_or_404(Student, id=student_id)
        return render(request, 'AttendanceApiAndWeb/student_detail.html', {'student': student})
    else:
        return handler403(request, exception=None)

@login_required(login_url='teacher_login')   
def teacher_list(request):
    teachers = TeacherUser.objects.all().order_by('-id')
    return render(request, 'AttendanceApiAndWeb/teacher_list.html', {'teachers': teachers})

@login_required(login_url='teacher_login')   
def teacher_detail(request, teacher_id):
    if request.user.is_superuser:
        teacher = get_object_or_404(TeacherUser, id=teacher_id)
        return render(request, 'AttendanceApiAndWeb/teacher_detail.html', {'teacher': teacher})
    else:
        return handler403(request, exception=None)

class ClassListView(LoginRequiredMixin, View):
    login_url = 'teacher_login'
    def get(self, request):
        if request.user.is_superuser:
            classes = Class.objects.all()
            return render(request, 'AttendanceApiAndWeb/class_list.html', {'classes': classes})
        else:
            return handler403(request, exception=None)

class StudentListView(LoginRequiredMixin, View):
    login_url = 'teacher_login' 
    def get(self, request):
        if request.user.is_superuser:
            classes = Class.objects.all()
            return render(request, 'AttendanceApiAndWeb/student_list.html', {'classes': classes})
        else:
            # teacher = TeacherUser.objects.get(username=request.user)
            # classes = Class.objects.filter(teacher=teacher)
            # return render(request, 'AttendanceApiAndWeb/student_list.html', {'classes': classes})
            # html = "<html><body>You are not authorized to view this page.</body></html>"
            # return HttpResponse(html)
             return handler403(request, exception=None)
        

    def post(self, request):
        class_id = int(request.POST.get('class_id'))
        error_message=None
        print(type(class_id))
        if class_id and type(class_id) == int:
            selected_class = get_object_or_404(Class, id=class_id)
            
            students = Student.objects.filter(class_name=selected_class)
            if students:
                print(students)
                for student in students:
                        class_name=student.class_name
                return render(request, 'AttendanceApiAndWeb/student_list.html', {'students': students, 'class_name':class_name})
            else:
                error_message = f"No students found for class '{selected_class}'"
                return render(request, 'AttendanceApiAndWeb/student_list.html', {'error_message': error_message})
                print("no students")
            # print(class_name)
        else:
            return redirect('student_list')


@login_required(login_url='teacher_login')   
def class_attendance(request, class_id):
    class_obj = get_object_or_404(Class, id=class_id)

    students = Student.objects.filter(class_name=class_obj)
    attendance_form = AttendanceForm(students=students)
    dat = timezone.now().date()  # Use timezone to get the current date
    print(dat)
    students_ids = [student.id for student in students]
    attendances = Attendance.objects.filter(student__in=students_ids, date=dat)

    if attendances.exists():
        # Attendance has already been taken today
        messages.info(request, 'Attendance for today has already been taken. You can take attendance again tomorrow.')
        return redirect('teacher_profile')  # Redirect to an appropriate page

    elif request.method == 'POST':
        form = AttendanceForm(request.POST, students=students)
        if form.is_valid():
            for student in students:
                attendance_status = form.cleaned_data[f'student_{student.id}']
                Attendance.objects.create(student=student, date=dat, is_present=attendance_status)
                
            # Redirect or display a success message
            # display success message
            messages.success(request, 'Attendance taken successfully')
        
        else:
            print(form.errors)
            # display error message
            messages.error(request, 'Error taking attendance')

            # return redirect('teacher_profile')

    return render(request, 'AttendanceApiAndWeb/class_attendance.html', {'class': class_obj, 'students': students, 'attendance_form': attendance_form, 'attendances':attendances})

@login_required(login_url='teacher_login')   
def department_update(request, department_id):
    if request.user.is_superuser:
        department = get_object_or_404(Department, id=department_id)
        if request.method == 'POST':
            form = DepartmentForm(request.POST, instance=department)
            if form.is_valid():
                form.save()
                return redirect('department_detail', department_id=department.id)
        else:
            form = DepartmentForm(instance=department)
        return render(request, 'AttendanceApiAndWeb/department_update.html', {'form': form, 'department': department})
    else:
        return handler403(request, exception=None)

@login_required(login_url='teacher_login')   
def class_update(request, class_id):
    if request.user.is_superuser:
        class_obj = get_object_or_404(Class, id=class_id)
        if request.method == 'POST':
            form = ClassForm(request.POST, instance=class_obj)
            if form.is_valid():
                form.save()
                return redirect('class_detail', class_id=class_obj.id)
        else:
            form = ClassForm(instance=class_obj)
        return render(request, 'AttendanceApiAndWeb/class_update.html', {'form': form, 'class': class_obj})
    else:
         return handler403(request, exception=None)

@login_required(login_url='teacher_login')   
def student_update(request, student_id):
    if request.user.is_superuser:
        student = get_object_or_404(Student, id=student_id)
        if request.method == 'POST':
            form = StudentForm(request.POST, instance=student)
            if form.is_valid():
                form.save()
                return redirect('student_detail',student_id=student.id)
        else:
            form = StudentForm(instance=student)
        return render(request, 'AttendanceApiAndWeb/student_update.html', {'form': form, 'student': student})
    else:
         return handler403(request, exception=None)

@login_required(login_url='teacher_login')   
def teacher_update(request, teacher_id):
    if request.user.is_superuser:
        teacher = get_object_or_404(TeacherUser, id=teacher_id)
        if request.method == 'POST':
            form = TeacherSignUpFormUpdate(request.POST, instance=teacher)
            if form.is_valid():
                form.save()
                return redirect('teacher_detail', teacher_id=teacher.id)
        else:
            form = TeacherSignUpFormUpdate(instance=teacher)
        return render(request, 'AttendanceApiAndWeb/teacher_update.html', {'form': form, 'teacher': teacher})
    else:
         return handler403(request, exception=None)


@login_required(login_url='teacher_login')   
def delete_department(request, department_id):
    if request.user.is_superuser:
        department = get_object_or_404(Department, id=department_id)
        if request.method == 'POST':
            try:
                department.delete()
                return redirect('department_list')
            except Exception as e:
                error_message = f"An error occurred while deleting the department: {e}"
                return render(request, 'AttendanceApiAndWeb/department_delete_error.html', {'error_message': error_message})

        return render(request, 'AttendanceApiAndWeb/department_confirm_delete.html', {'department': department})
    else:
         return handler403(request, exception=None)

@login_required(login_url='teacher_login')   
def delete_class(request, class_id):
    if request.user.is_superuser:
        clas = get_object_or_404(Class, id=class_id)
        if request.method == 'POST':
            try:
                clas.delete()
                return redirect('class_list')
            except Exception as e:
                error_message = f"An error occurred while deleting the class: {e}"
                return render(request, 'AttendanceApiAndWeb/class_delete_error.html', {'error_message': error_message})

        return render(request, 'AttendanceApiAndWeb/class_confirm_delete.html', {'clas': clas})
    else:
        return handler403(request, exception=None)

@login_required(login_url='teacher_login')   
def delete_student(request, student_id):
    if request.user.is_superuser:
        student = get_object_or_404(Student, id=student_id)
        if request.method == 'POST':
            try:
                student.delete()
                return redirect('student_list')
            except Exception as e:
                error_message = f"An error occurred while deleting the student: {e}"
                return render(request, 'AttendanceApiAndWeb/student_delete_error.html', {'error_message': error_message})

        return render(request, 'AttendanceApiAndWeb/student_confirm_delete.html', {'student': student})
    else:
         return handler403(request, exception=None)

@login_required(login_url='teacher_login')   
def delete_teacher(request, teacher_id):
    if request.user.is_superuser:
        teacher = get_object_or_404(TeacherUser, id=teacher_id)
        if request.method == 'POST':
            try:
                teacher.delete()
                return redirect('teacher_list')
            except Exception as e:
                error_message = f"An error occurred while deleting the teacher: {e}"
                return render(request, 'AttendanceApiAndWeb/teacher_delete_error.html', {'error_message': error_message})

        return render(request, 'AttendanceApiAndWeb/teacher_confirm_delete.html', {'teacher': teacher})
    else:
         return handler403(request, exception=None)

@login_required(login_url='teacher_login')   
def generate_student_report(request):
    error_message = None
    pdf_content = None  
    file_path = None    
    if request.user.is_superuser:
        if request.method == 'POST':
            student_id = request.POST.get('student_id')
            
            if not student_id:
                error_message = "Please enter a student ID"
            else:
                try:
                    student = Student.objects.get(ID=int(student_id))

                    if not pdf_content:
                        pdf_content = generate_monthly_report(student)

                    if pdf_content:
                        pdfs_folder = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'pdfs')

                        if not os.path.exists(pdfs_folder):
                            os.makedirs(pdfs_folder)

                        file_path = os.path.join(pdfs_folder, f"monthly_report_{student.name}.pdf")

                        with open(file_path, 'wb') as pdf_file:
                            pdf_file.write(pdf_content)

                        response = HttpResponse(pdf_content, content_type='application/pdf')
                        response['Content-Disposition'] = f'attachment; filename="monthly_report_{student.name}.pdf"'
                        return response
                    else:
                        error_message = f"No report found for student '{student.name}'"
                except ValueError:
                    error_message = f"Invalid student ID: '{student_id}'"
                except Student.DoesNotExist:
                    error_message = f"No student found with ID: '{student_id}'"

        return render(request, 'AttendanceApiAndWeb/report_form.html', {'error_message': error_message})
    else:
        return handler403(request, exception=None)


def generate_monthly_report(student):
    # Create a new PDF file
    buffer = BytesIO()
    c = canvas.Canvas(buffer)

    # Get the attendance records for the student
    attendance_list = Attendance.objects.filter(student=student)

    # Set the initial y-coordinate for drawing
    y = 800

    # Write the student name
    c.setFont("Helvetica-Bold", 12)
    c.drawString(50, y, f"Student Name: {student.name}")

    c.setFont("Helvetica", 10)
    y -= 20

    # Write the attendance details
    for attendance in attendance_list:
        c.drawString(50, y, f"Date: {attendance.date}, Attendance: {'Present' if attendance.is_present else 'Absent'}")
        y -= 15

    # Save and close the PDF file
    c.save()

    # Get the PDF content from the buffer
    pdf_content = buffer.getvalue()
    buffer.close()

    return pdf_content



def handler404(request, exception):
    return render(request, 'AttendanceApiAndWeb/404.html', status=404)

def handler500(request):
    return render(request, 'AttendanceApiAndWeb/500.html', status=500)

def handler403(request, exception):
    return render(request, 'AttendanceApiAndWeb/403.html', status=403)

def handler400(request, exception):
    return render(request, 'AttendanceApiAndWeb/400.html', status=400)

