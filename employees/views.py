from django.shortcuts import render, redirect
from .models import Employee
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import AuthenticationForm

def employee_form(request):
    """
    Handles both displaying the form (GET request) 
    and processing form submissions (POST request)
    """
    if request.method == 'POST':
        try:
            # Extract all form data from POST request
            first_name = request.POST.get('firstname')
            surname = request.POST.get('surname')
            other_name = request.POST.get('othername')
            employee_id = request.POST.get('employeeid')
            email = request.POST.get('email')
            contact_number = request.POST.get('contactnumber')
            department = request.POST.get('department')
            date_of_birth = request.POST.get('dob')
            gender = request.POST.get('gender')
            address = request.POST.get('address')
            state = request.POST.get('state')
            lga = request.POST.get('lga')
            ward = request.POST.get('ward')
            role = request.POST.get('role')
            
            # Create and save new employee
            employee = Employee(
                first_name=first_name,
                surname=surname,
                other_name=other_name,
                employee_id=employee_id,
                email=email,
                contact_number=contact_number,
                department=department,
                date_of_birth=date_of_birth,
                gender=gender,
                address=address,
                state=state,
                lga=lga,
                ward=ward,
                role=role,
                profile_picture=request.FILES.get('profile_picture')
            )
            
            employee.save()
            
            # Success - redirect to success page
            return redirect('success_page')
            
        except Exception as e:
            # If there's an error (like duplicate email), show error message
            messages.error(request, f"Error saving employee: {str(e)}")
            return render(request, 'employees/form.html')
    
    # If it's a GET request, just show the empty form
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

@login_required
@superuser_required
def view_records(request):
    """Displays all employee records with filtering capability - Superusers only"""
    employees = Employee.objects.all().order_by('id')
    
    context = {
        'records': employees
    }
    return render(request, 'employees/records.html', context)


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