from django.db.models import Manager
from .choices import UserType

class EmployeeManager(Manager):
    def get_queryset(self, *args, **kwargs) :
        return super().get_queryset(*args, **kwargs).filter(usertype=UserType.EMPLOYEE)

class CounsellorManager(Manager):
    def get_queryset(self, *args, **kwargs) :
        return super().get_queryset(*args, **kwargs).filter(usertype=UserType.COUNSELLOR)

class EnquiryManager(Manager):
    def get_queryset(self, *args, **kwargs):
        return super().get_queryset(*args, **kwargs)
    
    def getAllPublicEnquiries(self):
        return self.get_queryset().filter(public=True)
    
    def getAllPrivateEnquiries(self, user):
        return self.get_queryset().filter(public=False, claimed_by=user)