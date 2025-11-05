from django.db import models

class Employee(models.Model):
    # Personal Information
    first_name = models.CharField(max_length=100)
    surname = models.CharField(max_length=100)  # Changed from last_name to match form
    other_name = models.CharField(max_length=100, blank=True, null=True)
    employee_id = models.CharField(max_length=50, unique=True)  # NEW field
    email = models.EmailField(unique=True)
    contact_number = models.CharField(max_length=20)  # NEW field
    date_of_birth = models.DateField()
    address = models.TextField()  # NEW field
    
    # Gender choices
    GENDER_CHOICES = [
        ('Male', 'Male'),
        ('Female', 'Female'),
    ]
    gender = models.CharField(max_length=10, choices=GENDER_CHOICES)
    
    # Location Information
    state = models.CharField(max_length=100)
    lga = models.CharField(max_length=100)  # Local Government Area
    ward = models.CharField(max_length=100)
    
    # Professional Information
    department = models.CharField(max_length=100)
    role = models.CharField(max_length=100)
    
    # Profile picture (NEW field - storing file path as string for now)
    profile_picture = models.ImageField(
        upload_to='profile_pictures/', 
        blank=True, 
        null=True,
        verbose_name='Profile Picture'
    )
    
    # Automatic timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.first_name} {self.surname} - {self.employee_id}"
    
    class Meta:
        db_table = 'employees'
        ordering = ['-created_at']  # Newest records first by default