from django.contrib import admin
from .models import Employee

@admin.register(Employee)
class EmployeeAdmin(admin.ModelAdmin):
    # Fields to display in the list view
    list_display = [
        'employee_id', 
        'first_name', 
        'surname', 
        'email', 
        'profile_picture',
        'department', 
        'role',
        'created_at'
    ]
    
    # Fields that can be used for searching
    search_fields = [
        'employee_id',
        'first_name', 
        'surname', 
        'email', 
        'department'
    ]
    
    # Filters for the right sidebar
    list_filter = [
        'department',
        'role',
        'gender',
        'state',
        'created_at'
    ]
    
    # Fields that are read-only (can't be edited)
    readonly_fields = ['created_at', 'updated_at']
    
    # Fieldsets for organizing the detail form
    fieldsets = [
        ('Personal Information', {
            'fields': [
                'first_name',
                'surname', 
                'other_name',
                'employee_id',
                'email',
                'contact_number',
                'date_of_birth',
                'gender',
                'address'
            ]
        }),
        ('Location Information', {
            'fields': [
                'state',
                'lga',
                'ward'
            ]
        }),
        ('Professional Information', {
            'fields': [
                'department',
                'role',
                'profile_picture'
            ]
        }),
        ('System Information', {
            'fields': [
                'created_at',
                'updated_at'
            ],
            'classes': ['collapse']  # This makes the section collapsible
        }),
    ]
    
    # Ordering of records in admin
    ordering = ['-created_at']