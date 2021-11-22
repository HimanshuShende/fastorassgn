from django.db.models import TextChoices

class UserType(TextChoices):
        EMPLOYEE = "EMPLOYEE", "Employee"
        COUNSELLOR = "COUNSELLOR", "Counsellor"