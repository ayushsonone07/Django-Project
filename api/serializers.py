from rest_framework import serializers
from django.contrib.auth import get_user_model
from . import models

User = get_user_model()

class UserSerializer(serializers.ModelSerializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)
    class Meta:
        model = User
        fields = '__all__'


    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        if user is not None:
            return user
        
    
    def validate(self, attrs):
        phone_no = attrs.get('phone_no')
        if not phone_no:
            raise serializers.ValidationError('Phone number is required')
        if len(str(phone_no)) != 10:
            raise serializers.ValidationError('Phone number must be 10 digits')
        return attrs

    

class UserLoginSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    class Meta:
        model = User
        fields = ['email', 'password']


class StaffUserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    class Meta:
        model = User
        fields = '__all__'

    def validate(self, attrs):
        if attrs.get('is_staff') == False:
            serializers.ValidationError('This is staff route')
        return attrs
    

class LeaveSerializer(serializers.ModelSerializer):
    UserSerializer()
    class Meta:
        model = models.LeaveModel
        fields = '__all__'


    # def validate(self, attrs):
    #     leave = attrs.get('leave_status')
    #     if leave:
    #         raise serializers.ValidationError('you are already appleid for leave')
    #     return attrs


class ProfileSerializer(serializers.ModelSerializer):
    UserSerializer()
    class Meta:
        model = models.ProfileModel
        fields = ['user', 'leave']


    