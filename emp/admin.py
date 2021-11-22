from django.contrib import admin
from .models import (
    User,
    Employee,
    Counsellor,
    Enquiry
)
# Register your models here.


admin.site.register(User)
admin.site.register(Employee)
admin.site.register(Counsellor)
admin.site.register(Enquiry)