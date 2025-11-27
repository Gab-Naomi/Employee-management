from django.urls import path
from . import views
from django.contrib.auth.decorators import login_required

urlpatterns = [
    path('', views.employee_form, name='employee_form'),  # This handles everything
    path('success/', views.success_page, name='success_page'),
    path('login/', views.custom_login, name='login'),
    path('records/', login_required(views.view_records), name='view_records'),
    path('employee/view/<int:employee_id>/', views.view_employee, name='view_employee'),  
    path('employee/edit/<int:employee_id>/', views.edit_employee, name='edit_employee'),
    path('employee/delete/<int:employee_id>/', views.delete_employee, name='delete_employee'),
    path('access-denied/', views.access_denied, name='access_denied'),
    path('logout/', views.custom_logout, name='logout'),
    path('export/csv/', views.export_employees_csv, name='export_employees_csv'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('bulk-delete/', views.bulk_delete_employees, name='bulk_delete_employees'),
]