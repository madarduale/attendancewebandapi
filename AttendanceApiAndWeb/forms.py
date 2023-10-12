# forms.py
from django.contrib.auth import get_user_model
# from django.contrib.auth.models import User
from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import Department, Class, Student, TeacherUser, Attendance
from rest_framework.authtoken.models import Token

class DepartmentForm(forms.ModelForm):
    class Meta:
        model = Department
        fields = ['name']
        
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['name'].widget.attrs.update({'class': 'form-control'})

class ClassForm(forms.ModelForm):
    class Meta:
        model = Class
        fields = ['department', 'teacher', 'name']
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['department'].widget.attrs.update({'class': 'form-control'})
        self.fields['teacher'].widget.attrs.update({'class': 'form-control'})
        self.fields['name'].widget.attrs.update({'class': 'form-control'})

class StudentForm(forms.ModelForm):
    class Meta:
        model = Student
        fields = ['class_name','name','ID']
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['class_name'].widget.attrs.update({'class': 'form-control'})
        self.fields['name'].widget.attrs.update({'class': 'form-control'})
        self.fields['ID'].widget.attrs.update({'class': 'form-control'})

# class TeacherForm(forms.ModelForm):
#     user = forms.ModelChoiceField(queryset=TeacherUser.objects.all())

#     class Meta:
#         model = TeacherUser
#         fields = '__all__' 
#     def __init__(self, *args, **kwargs):
#         super().__init__(*args, **kwargs)
#         self.fields['__all__'].widget.attrs.update({'class': 'form-control'})
#         # self.fields['name'].widget.attrs.update({'class': 'form-control'})

class TeacherSignUpForm(UserCreationForm):
    class Meta:
        model = get_user_model()
        fields = ['username', 'password1', 'password2','is_teacher', 'firstname', 'lastname', 'username', 'email', 'teacher_id', 'is_superuser', 'is_teacher', 'is_active', 'is_staff', 
]
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].widget.attrs.update({'class': 'form-control'})
        self.fields['password1'].widget.attrs.update({'class': 'form-control'})
        self.fields['password2'].widget.attrs.update({'class': 'form-control'})
        self.fields['firstname'].widget.attrs.update({'class': 'form-control'})
        self.fields['lastname'].widget.attrs.update({'class': 'form-control'})
        self.fields['email'].widget.attrs.update({'class': 'form-control'})
        self.fields['teacher_id'].widget.attrs.update({'class': 'form-control'})
        self.fields['is_superuser'].widget.attrs.update({'class': 'form-control'})
        self.fields['is_teacher'].widget.attrs.update({'class': 'form-control'})
        self.fields['is_active'].widget.attrs.update({'class': 'form-control'})
        self.fields['is_staff'].widget.attrs.update({'class': 'form-control'})


class TeacherSignUpFormUpdate(forms.ModelForm):
    class Meta:
        model = get_user_model()
        fields = ['firstname', 'lastname', 'username', 'email', 'teacher_id', 'is_teacher', 'is_superuser', 'is_teacher', 'is_active', 'is_staff', 
]
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].widget.attrs.update({'class': 'form-control'})
        # self.fields['password1'].widget.attrs.update({'class': 'form-control'})
        # self.fields['password2'].widget.attrs.update({'class': 'form-control'})
        self.fields['firstname'].widget.attrs.update({'class': 'form-control'})
        self.fields['lastname'].widget.attrs.update({'class': 'form-control'})
        self.fields['email'].widget.attrs.update({'class': 'form-control'})
        self.fields['teacher_id'].widget.attrs.update({'class': 'form-control'})
        self.fields['is_superuser'].widget.attrs.update({'class': 'form-control'})
        self.fields['is_teacher'].widget.attrs.update({'class': 'form-control'})
        self.fields['is_active'].widget.attrs.update({'class': 'form-control'})
        self.fields['is_staff'].widget.attrs.update({'class': 'form-control'})




class AttendanceForm(forms.Form):
    def __init__(self, *args, **kwargs):
        students = kwargs.pop('students')
        super(AttendanceForm, self).__init__(*args, **kwargs)
        
        for student in students:
            self.fields[f'student_{student.id}'] = forms.BooleanField(label=student.name, required=False)



class MonthlyReportForm(forms.Form):
    year = forms.IntegerField(label='Year')
    month = forms.IntegerField(label='Month')
    student_names = forms.MultipleChoiceField(label='Students', choices=[], widget=forms.SelectMultiple(attrs={'class': 'select2'}))

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['student_names'].choices = self.get_student_choices()

    def get_student_choices(self):
        students = Student.objects.all()
        choices = [(student.name, student.name) for student in students]
        return choices
    



