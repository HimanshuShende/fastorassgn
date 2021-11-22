from django.db import models
from django.contrib.auth.models import AbstractUser


from .managers import EmployeeManager, CounsellorManager, EnquiryManager
from .choices import UserType
# Create your models here.


class User(AbstractUser):
    username = models.EmailField(
                verbose_name="Email",
                blank=False,
                unique=True,
                error_messages={
                        'unique': "A user with that email already exists."
                    }
            )
    REQUIRED_FIELDS = []

    usertype = models.CharField(
                verbose_name="User type",
                max_length=20,
                choices=UserType.choices,
                default=UserType.EMPLOYEE
            )


class Employee(User):
    class Meta:
        proxy = True

    objects = EmployeeManager()

    def save(self, *args, **kwargs):
        self.type_ = UserType.EMPLOYEE
        return super.save(*args, **kwargs)

class Counsellor(User):
    class Meta:
        proxy = True

    objects = CounsellorManager()

    def save(self, *args, **kwargs):
        self.type_ = UserType.COUNSELLOR
        return super.save(*args, **kwargs)


class Enquiry(models.Model):
    class Meta:
        verbose_name = "Enquiry"
        verbose_name_plural = "Enquiries"
    
    objects = EnquiryManager()
    
    name = models.CharField(
                verbose_name="Name",
                max_length=200
            )
    email = models.EmailField( verbose_name="Email" )
    mobile = models.CharField(
                verbose_name="Mobile Number",
                max_length=10
             )
    interests = models.TextField( verbose_name="Course interest")
    public = models.BooleanField(
                verbose_name="Visible to all",
                default=True
            )

    claimed_by = models.ForeignKey(
                    to=User,
                    verbose_name="Claimed by",
                    on_delete=models.SET_NULL,
                    default=None, 
                    null=True,
                    blank=True
                )

    created_on = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return f"{self.name}"

    @property
    def isPublic(self): return self.public

    @property
    def isPrivate(self): return not self.public
