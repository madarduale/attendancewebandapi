from rest_framework import serializers
from rest_framework.authtoken.models import Token

from .models import Department, Student, Class, TeacherUser, Attendance

class DepartmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Department
        fields = '__all__'

class StudentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Student
        fields = '__all__'

class ClassSerializer(serializers.ModelSerializer):
    class Meta:
        model = Class
        fields = '__all__'



class AttendanceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Attendance
        fields = ['student', 'is_present']

class TeacherUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = TeacherUser
        fields = '__all__'
        extra_kwargs = {'password': {'write_only': True}}

  

    def create(self, validated_data):
        user = TeacherUser.objects.create_user(**validated_data)
        token = Token.objects.create(user=user)
        print(token, user)
        return user