from django.urls import path
from .views import claimEnquiry, employeeOperations, enquiryOperations, myClaimedEnquiry
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
urlpatterns = [
    path('enquiry/', login_required(csrf_exempt(enquiryOperations)), name="enquiryOperations"),
    path('employee/', login_required(employeeOperations), name="employeeOperations"),
    path('claim/<int:pk>/', csrf_exempt(login_required(claimEnquiry)), name="claimEnquiry"),
    path('myClaim/', login_required(csrf_exempt(myClaimedEnquiry)), name="myClaimedEnquiry"),
]