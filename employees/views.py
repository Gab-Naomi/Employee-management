from .models import Employee
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import AuthenticationForm
from django.core.paginator import Paginator
import csv
from django.http import HttpResponse
from django.utils import timezone
from django.db.models import Count

def employee_form(request):
    if request.method == 'POST':
        try:
            # Extract all form data
            first_name = request.POST.get('firstname', '').strip()
            surname = request.POST.get('surname', '').strip()
            employee_id = request.POST.get('employeeid', '').strip()
            email = request.POST.get('email', '').strip()
            
            # Basic validation
            if not first_name:
                messages.error(request, "First name is required.")
                return render(request, 'employees/form.html')
            
            if not surname:
                messages.error(request, "Surname is required.")
                return render(request, 'employees/form.html')
            
            if not employee_id:
                messages.error(request, "Employee ID is required.")
                return render(request, 'employees/form.html')
            
            # Check for duplicate employee ID
            if Employee.objects.filter(employee_id=employee_id).exists():
                messages.error(request, f"Employee ID '{employee_id}' already exists.")
                return render(request, 'employees/form.html')
            
            # Check for duplicate email
            if Employee.objects.filter(email=email).exists():
                messages.error(request, f"Email '{email}' is already registered.")
                return render(request, 'employees/form.html')
            
            # Create and save employee
            employee = Employee(
                first_name=first_name,
                surname=surname,
                other_name=request.POST.get('othername', '').strip(),
                employee_id=employee_id,
                email=email,
                contact_number=request.POST.get('contactnumber', '').strip(),
                department=request.POST.get('department', '').strip(),
                date_of_birth=request.POST.get('dob'),
                gender=request.POST.get('gender'),
                address=request.POST.get('address', '').strip(),
                state=request.POST.get('state'),
                lga=request.POST.get('lga'),
                ward=request.POST.get('ward'),
                role=request.POST.get('role'),
                profile_picture=request.FILES.get('profile_picture')
            )
            
            employee.save()
            messages.success(request, f"Employee {first_name} {surname} added successfully!")
            return redirect('success_page')
            
        except Exception as e:
            messages.error(request, f"Error saving employee: {str(e)}")
            return render(request, 'employees/form.html')
    
    return render(request, 'employees/form.html')

def success_page(request):
    """Shows success message after form submission"""
    return render(request, 'employees/success.html')

def custom_login(request):
    """Custom login view to use our template"""
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                # Check if user is superuser
                if user.is_superuser:
                    login(request, user)
                    next_url = request.GET.get('next', 'view_records')
                    return redirect(next_url)
                else:
                    messages.error(request, "Only admin users can access this system.")
            else:
                messages.error(request, "Invalid username or password.")
        else:
            messages.error(request, "Invalid username or password.")
    else:
        form = AuthenticationForm()
    
    # Updated path to match your template location
    return render(request, 'registration/login.html', {'form': form})

def access_denied(request):
    """Show access denied page for non-superusers"""
    # Updated path to match your template location
    return render(request, 'registration/access_denied.html')

def superuser_required(view_func):
    """Decorator that checks if user is superuser, else redirect to access denied"""
    def _wrapped_view(request, *args, **kwargs):
        if not request.user.is_superuser:
            return redirect('access_denied')
        return view_func(request, *args, **kwargs)
    return _wrapped_view

from django.contrib.auth import logout

def custom_logout(request):
    """Custom logout view"""
    logout(request)
    return render(request, 'registration/logout.html')

@login_required
@superuser_required
def edit_employee(request, employee_id):
    employee = get_object_or_404(Employee, id=employee_id)
    
    if request.method == 'POST':
        try:
            # Update all fields
            employee.first_name = request.POST.get('firstname')
            employee.surname = request.POST.get('surname')
            employee.other_name = request.POST.get('othername')
            employee.employee_id = request.POST.get('employeeid')
            employee.email = request.POST.get('email')
            employee.contact_number = request.POST.get('contactnumber')
            employee.department = request.POST.get('department')
            employee.date_of_birth = request.POST.get('dob')
            employee.gender = request.POST.get('gender')
            employee.address = request.POST.get('address')
            employee.state = request.POST.get('state')
            employee.lga = request.POST.get('lga')
            employee.ward = request.POST.get('ward')
            employee.role = request.POST.get('role')
            
            employee.save()
            messages.success(request, 'Employee updated successfully!')
            return redirect('view_records')
            
        except Exception as e:
            messages.error(request, f'Error updating employee: {str(e)}')
    
    return render(request, 'employees/edit_form.html', {'employee': employee})

@login_required
@superuser_required
def delete_employee(request, employee_id):
    employee = get_object_or_404(Employee, id=employee_id)
    
    if request.method == 'POST':
        try:
            employee_name = f"{employee.first_name} {employee.surname}"
            employee.delete()
            messages.success(request, f'Employee "{employee_name}" has been deleted successfully!')
            return redirect('view_records')
        except Exception as e:
            messages.error(request, f'Error deleting employee: {str(e)}')
            return redirect('view_records')
    
    # If it's a GET request, show the confirmation page
    return render(request, 'employees/confirm_delete.html', {'employee': employee})

@login_required
@superuser_required
def view_employee(request, employee_id):
    """View individual employee details"""
    employee = get_object_or_404(Employee, id=employee_id)
    return render(request, 'employees/view_employee.html', {'employee': employee})

@login_required
@superuser_required
def view_records(request):
    """Displays all employee records with pagination"""
    employees_list = Employee.objects.all().order_by('id')
    
    # Pagination - 10 records per page
    paginator = Paginator(employees_list, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'page_obj': page_obj,
        'records': page_obj,  # Keep for backward compatibility
    }
    return render(request, 'employees/records.html', context)

@login_required
@superuser_required
def export_employees_csv(request):
    """Export employees to CSV"""
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = f'attachment; filename="employees_{timezone.now().strftime("%Y%m%d_%H%M")}.csv"'
    
    writer = csv.writer(response)
    writer.writerow([
        'Employee ID', 'First Name', 'Surname', 'Other Name', 'Email', 
        'Contact Number', 'Department', 'Role', 'Gender', 'Date of Birth',
        'Address', 'State', 'LGA', 'Ward', 'Date Created'
    ])
    
    employees = Employee.objects.all().order_by('id')
    for employee in employees:
        writer.writerow([
            employee.employee_id,
            employee.first_name,
            employee.surname,
            employee.other_name or '',
            employee.email,
            employee.contact_number,
            employee.department,
            employee.role,
            employee.gender,
            employee.date_of_birth,
            employee.address,
            employee.state,
            employee.lga,
            employee.ward,
            employee.created_at.strftime("%Y-%m-%d %H:%M")
        ])
    
    return response
@login_required
@superuser_required
def dashboard(request):
    """Enhanced employee statistics dashboard with charts data"""
    # Handle filters
    department_filter = request.GET.get('department')
    date_from = request.GET.get('date_from')
    date_to = request.GET.get('date_to')
    
    # Base queryset
    employees_queryset = Employee.objects.all()
    
    # Apply filters
    if department_filter:
        employees_queryset = employees_queryset.filter(department=department_filter)
    
    if date_from:
        employees_queryset = employees_queryset.filter(created_at__gte=date_from)
    
    if date_to:
        employees_queryset = employees_queryset.filter(created_at__lte=date_to)
    
    # Calculate statistics based on filtered data
    total_employees = employees_queryset.count()
    
    # Department data for bar chart
    departments = employees_queryset.values('department').annotate(
        count=Count('id')
    ).filter(department__isnull=False).exclude(department='').order_by('-count')
    
    # Enhanced gender data for doughnut chart
    gender_data = []
    for choice in ['Male', 'Female', 'Other']:
        count = employees_queryset.filter(gender=choice).count()
        if count > 0:
            percentage = round((count / total_employees) * 100, 1) if total_employees > 0 else 0
            gender_data.append({
                'gender': choice, 
                'count': count,
                'percentage': percentage
            })
    
    # Role distribution for horizontal bar chart
    roles = employees_queryset.values('role').annotate(
        count=Count('id')
    ).filter(role__isnull=False).exclude(role='').order_by('-count')[:8]  # Increased to 8 for better chart
    
    recent_employees = employees_queryset.select_related().order_by('-created_at')[:5]
    
    # Monthly hiring trend for line chart (last 6 months)
    from django.db.models.functions import TruncMonth
    from datetime import datetime, timedelta
    
    six_months_ago = timezone.now() - timedelta(days=180)
    monthly_hires = employees_queryset.filter(
        created_at__gte=six_months_ago
    ).annotate(
        month=TruncMonth('created_at')
    ).values('month').annotate(
        count=Count('id')
    ).order_by('month')
    
    # Get unique departments for filter dropdown
    department_choices = Employee.objects.values_list('department', flat=True).distinct()
    
    context = {
        'total_employees': total_employees,
        'departments': departments,
        'genders': gender_data,
        'roles': roles,
        'recent_employees': recent_employees,
        'monthly_hires': list(monthly_hires),
        'department_choices': department_choices,
        'applied_filters': {
            'department': department_filter,
            'date_from': date_from,
            'date_to': date_to,
        }
    }
    return render(request, 'employees/dashboard.html', context)

@login_required
@superuser_required
def bulk_delete_employees(request):
    """Bulk delete employees"""
    if request.method == 'POST':
        employee_ids = request.POST.getlist('employee_ids')
        if employee_ids:
            employees = Employee.objects.filter(id__in=employee_ids)
            count = employees.count()
            employees.delete()
            messages.success(request, f"Successfully deleted {count} employees.")
        else:
            messages.error(request, "No employees selected for deletion.")
    
    return redirect('view_records')
