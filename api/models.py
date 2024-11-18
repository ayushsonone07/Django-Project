from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager

# Create your models here.

class UserManager(BaseUserManager):

    def create_user(self, username, email, password, phone_no, user_role,date_of_birth, is_admin=False, is_staff=False, is_active=True, is_superuser=False ):
        if username is None:
            raise ValueError('username is required')
        if email is None:
            raise ValueError('email is required')
        if not password:
            raise ValueError('Password is required')
        

        user = self.model(
            username=username,
            email = self.normalize_email(email),
            user_role=user_role,
            phone_no=phone_no,
            date_of_birth=date_of_birth,
            is_active=True,
            is_admin=is_admin,
            is_staff=is_staff,
            is_superuser=is_superuser,
        )

        user.set_password(password)

        user.save(using=self._db)

        return user
    

    def create_superuser(self, username, email, password, user_roll=None, phone_no=None, date_of_birth=None):

        super_user = self.create_user(
            username=username,
            email = self.normalize_email(email),
            password=password,
            phone_no=None,
            user_role=user_roll,
            date_of_birth=None,
            is_active=True,
        )

        super_user.is_admin = True
        super_user.is_staff = True
        super_user.is_superuser = True

        super_user.save(using=self.db)

        return super_user
    
    

class UserModel(AbstractBaseUser):
    username = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    phone_no = models.IntegerField(null=True, blank=True)
    user_role = models.CharField(max_length=100, null=True, blank=True)
    date_of_birth = models.CharField(max_length=50)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_admin = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    createdat = models.DateTimeField(auto_now=True)
    last_login = models.DateTimeField(auto_now_add=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    objects = UserManager()

    def __str__(self):
        return f'{self.username}'
    
    def has_perm(self, perm, obj=None):
        if self.is_superuser:
            return True
        print(perm, obj)
        return perm, obj 

    def has_module_perms(self, app_label):
        if self.is_superuser:
            return True
        print(app_label)
        return app_label



class LeaveModel(models.Model):
    user = models.ForeignKey(UserModel, on_delete=models.CASCADE)
    leave_reason = models.CharField(max_length=250)
    start_leave_date = models.CharField(max_length=10)
    end_leave_date = models.CharField(max_length=10, null=True, blank=True)
    applied_leave_date = models.DateTimeField(auto_now_add=True)
    leave_status = models.BooleanField(default=False) 
    


class ProfileModel(models.Model):
    user = models.OneToOneField(UserModel, on_delete=models.CASCADE)
    leave = models.ForeignKey(LeaveModel, on_delete=models.CASCADE)