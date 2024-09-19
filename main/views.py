from .models import VehicleFleet, FleetOwner
import json
from .models import VehicleStatusIndividual
from django.middleware.csrf import get_token
from django.views.decorators.csrf import csrf_protect
from django.http import JsonResponse
from django.contrib.auth.forms import AuthenticationForm
from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, authenticate, logout
from django.contrib import messages
from .forms import (
    CustomUserRegistrationForm, ProfileEditForm,
    IndividualOwnerForm, FleetOwnerForm,
    SupportEngineerForm, RenterForm,
    IndividualOwnerProfileForm, FleetOwnerProfileForm,
    SupportEngineerProfileForm, RenterProfileForm
)
from .models import (
    CustomUser, IndividualOwner, FleetOwner,
    SupportEngineer, Renter, VehicleStatusIndividual
)
from .utils import get_location_name, get_route_url


def homepage(request):
    """Redirect to respective dashboard based on user role."""
    if request.user.is_authenticated:
        user_type = request.user.user_type
        if user_type == CustomUser.FLEET_OWNER:
            return redirect('fleet_owner_dashboard')
        elif user_type == CustomUser.INDIVIDUAL_OWNER:
            return redirect('individual_owner_dashboard')
        elif user_type == CustomUser.SUPPORT_ENGINEER:
            return redirect('support_engineer_dashboard')
        elif user_type == CustomUser.RENTER:
            return redirect('renter_dashboard')
    return render(request, 'main/homepage.html')

# def register_user(request):
#     """Register a new user and handle role-specific data."""
#     forms = {
#         'individual_owner_form': IndividualOwnerForm,
#         'fleet_owner_form': FleetOwnerForm,
#         'support_engineer_form': SupportEngineerForm,
#         'renter_form': RenterForm
#     }

#     if request.method == 'POST':
#         user_form = CustomUserRegistrationForm(request.POST)
#         if user_form.is_valid():
#             user = user_form.save(commit=False)
#             user.user_type = user_form.cleaned_data['user_type']
#             user.save()

#             # Get the correct role form class and initialize it with POST data
#             role_form_class = forms[f'{user.user_type.lower()}_form']
#             role_form = role_form_class(request.POST)

#             if role_form.is_valid():
#                 role_instance = role_form.save(commit=False)
#                 role_instance.user = user  # Associate the user with the role instance
#                 role_instance.save()

#             messages.success(request, "Registration successful!")
#             return redirect('login')
#         else:
#             messages.error(
#                 request, "Please correct the errors in the user form.")

#     # Initialize empty forms for GET request
#     return render(request, 'main/register.html', {
#         'user_form': CustomUserRegistrationForm(),
#         'individual_owner_form': IndividualOwnerForm(),
#         'fleet_owner_form': FleetOwnerForm(),
#         'support_engineer_form': SupportEngineerForm(),
#         'renter_form': RenterForm(),
#     })


def register_user(request):
    """Register a new user and handle role-specific data."""
    forms = {
        'individual_owner_form': IndividualOwnerForm,
        'fleet_owner_form': FleetOwnerForm,
        'support_engineer_form': SupportEngineerForm,
    }

    if request.method == 'POST':
        # Print the POST data to check what is being submitted
        print("POST Data: ", request.POST)

        user_form = CustomUserRegistrationForm(request.POST)
        user_type = request.POST.get('user_type')

        if user_form.is_valid():
            user = user_form.save(commit=False)
            user.user_type = user_type
            user.save()

            role_form_class = forms.get(f'{user_type.lower()}_form')

            if role_form_class:
                role_form = role_form_class(request.POST)

                # Print out any errors in the role-specific form
                if not role_form.is_valid():
                    print("Role Form Errors: ", role_form.errors)

                if role_form.is_valid():
                    role_instance = role_form.save(commit=False)
                    role_instance.user = user
                    role_instance.save()
                else:
                    # Log form errors if the role form is invalid
                    print(
                        f"Role form for {user_type} has errors:", role_form.errors)
            else:
                print(f"No form class found for the user type: {user_type}")

            messages.success(request, "Registration successful!")
            return redirect('login')
        else:
            # Log form errors if the user form is invalid
            print("User Form Errors: ", user_form.errors)
            messages.error(request, "Please correct the errors in the form.")

    return render(request, 'main/register.html', {
        'user_form': CustomUserRegistrationForm(),
        'individual_owner_form': IndividualOwnerForm(),
        'fleet_owner_form': FleetOwnerForm(),
        'support_engineer_form': SupportEngineerForm(),
    })


def user_login(request):
    """Custom login view."""
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)
            if user:
                login(request, user)
                return redirect(homepage)
            messages.error(request, "Invalid username or password.")
    return render(request, 'main/login.html', {'form': AuthenticationForm()})


@login_required
def individual_owner_dashboard(request):
    """Dashboard for Individual Owners."""
    individual_owner = get_object_or_404(IndividualOwner, user=request.user)
    vehicle_status = VehicleStatusIndividual.objects.filter(
        owner=individual_owner).first()

    current_location = get_location_name(
        vehicle_status.current_latitude, vehicle_status.current_longitude) if vehicle_status else None
    starting_location = get_location_name(
        vehicle_status.starting_latitude, vehicle_status.starting_longitude) if vehicle_status else None
    ending_location = get_location_name(
        vehicle_status.ending_latitude, vehicle_status.ending_longitude) if vehicle_status else None
    route_link = get_route_url(vehicle_status.starting_latitude, vehicle_status.starting_longitude,
                               vehicle_status.ending_latitude, vehicle_status.ending_longitude) if vehicle_status else None

    return render(request, 'main/individual_owner_dashboard.html', {
        'individual_owner': individual_owner,
        'vehicle_status': vehicle_status,
        'current_location': current_location,
        'starting_location': starting_location,
        'ending_location': ending_location,
        'route_link': route_link
    })


@login_required
@csrf_exempt
def toggle_panic_button(request):
    """Toggle the Panic Button status."""
    if request.method == 'POST':
        status = request.POST.get('status') == 'true'
        vehicle_status = get_object_or_404(
            VehicleStatusIndividual, owner__user=request.user)
        vehicle_status.panic_button_status = status
        vehicle_status.save()
        return JsonResponse({'message': 'Panic Button Status Updated'}, status=200)
    return JsonResponse({'error': 'Invalid request'}, status=400)


@login_required
@csrf_exempt
def toggle_lock_status(request):
    """Toggle the Lock status."""
    if request.method == 'POST':
        status = request.POST.get('status') == 'true'
        vehicle_status = get_object_or_404(
            VehicleStatusIndividual, owner__user=request.user)
        vehicle_status.lock_status = status
        vehicle_status.save()
        return JsonResponse({'message': 'Lock Status Updated'}, status=200)
    return JsonResponse({'error': 'Invalid request'}, status=400)


@login_required
def fleet_owner_dashboard(request):
    # Get the fleet owner from the request
    fleet_owner = get_object_or_404(FleetOwner, user=request.user)

    # Retrieve active and inactive vehicles for the fleet owner
    active_vehicles = VehicleFleet.objects.filter(status='active')
    inactive_vehicles = VehicleFleet.objects.filter(status='inactive')

    # Render the dashboard template with the fleet owner and vehicle data
    return render(request, 'main/fleet_owner_dashboard.html', {
        'fleet_owner': fleet_owner,
        'active_vehicles': active_vehicles,
        'inactive_vehicles': inactive_vehicles,
    })


def toggle_wheelchair_status(request, vehicle_id):
    # Retrieve the vehicle
    vehicle = get_object_or_404(VehicleFleet, id=vehicle_id)

    # Toggle the vehicle status
    if vehicle.status == 'active':
        vehicle.status = 'inactive'
    else:
        vehicle.status = 'active'

    vehicle.save()

    # Redirect to the fleet owner's dashboard
    return redirect('fleet_owner_dashboard')


def fleet_toggle_lock_status(request, vehicle_id):
    vehicle = get_object_or_404(VehicleFleet, id=vehicle_id)

    # Toggle the lock status
    vehicle.is_locked = not vehicle.is_locked
    vehicle.save()

    return redirect('fleet_owner_dashboard')


# @login_required
# def support_engineer_dashboard(request):
#     support_engineer = get_object_or_404(SupportEngineer, user=request.user)
#     return render(request, 'main/support_engineer_dashboard.html', {'support_engineer': support_engineer})
#     # return render(request, 'main/support_engineer_dashboard.html')
@login_required
def support_engineer_dashboard(request):
    support_engineer = get_object_or_404(SupportEngineer, user=request.user)

    # Fetch Active and Inactive vehicles
    active_vehicles = VehicleFleet.objects.filter(status='active')
    inactive_vehicles = VehicleFleet.objects.filter(status='inactive')

    return render(request, 'main/support_engineer_dashboard.html', {
        'support_engineer': support_engineer,
        'active_vehicles': active_vehicles,
        'inactive_vehicles': inactive_vehicles,
    })


@login_required
def toggle_vehicle_status(request, vehicle_id):
    vehicle = get_object_or_404(VehicleFleet, id=vehicle_id)

    # Toggle lock status
    vehicle.is_locked = not vehicle.is_locked

    # Move to inactive if locked or active if unlocked
    if vehicle.status == 'active':
        vehicle.status = 'inactive'
    else:
        vehicle.status = 'active'

    vehicle.save()

    return redirect('support_engineer_dashboard')


@ login_required
def renter_dashboard(request):
    renter = get_object_or_404(Renter, user=request.user)
    return render(request, 'main/renter_dashboard.html', {'renter': renter})


@ login_required
def edit_individual_owner(request, id):
    user = request.user
    # Ensure the individual owner exists and is associated with the logged-in user
    individual_owner = get_object_or_404(IndividualOwner, id=id, user=user)

    if request.method == 'POST':
        user_form = ProfileEditForm(request.POST, instance=user)
        profile_form = IndividualOwnerProfileForm(
            request.POST, instance=individual_owner)
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(
                request, 'Your profile has been updated successfully.')
            return redirect('individual_owner_dashboard')
    else:
        user_form = ProfileEditForm(instance=user)
        profile_form = IndividualOwnerProfileForm(instance=individual_owner)

    return render(request, 'main/edit_individual_owner.html', {'user_form': user_form, 'profile_form': profile_form})


@ login_required
def edit_fleet_owner(request):
    user = request.user
    fleet_owner = FleetOwner.objects.get(user=user)

    if request.method == 'POST':
        user_form = ProfileEditForm(request.POST, instance=user)
        profile_form = FleetOwnerProfileForm(
            request.POST, instance=fleet_owner)
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(
                request, 'Your profile has been updated successfully.')
            return redirect('fleet_owner_dashboard')
    else:
        user_form = ProfileEditForm(instance=user)
        profile_form = FleetOwnerProfileForm(instance=fleet_owner)

    return render(request, 'main/edit_fleet_owner.html', {'user_form': user_form, 'profile_form': profile_form})


@ login_required
def edit_support_engineer(request):
    user = request.user
    support_engineer = SupportEngineer.objects.get(user=user)

    if request.method == 'POST':
        user_form = ProfileEditForm(request.POST, instance=user)
        profile_form = SupportEngineerProfileForm(
            request.POST, instance=support_engineer)
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(
                request, 'Your profile has been updated successfully.')
            return redirect('support_engineer_dashboard')
    else:
        user_form = ProfileEditForm(instance=user)
        profile_form = SupportEngineerProfileForm(instance=support_engineer)

    return render(request, 'main/edit_support_engineer.html', {'user_form': user_form, 'profile_form': profile_form})


@ login_required
def edit_renter(request):
    user = request.user
    renter = Renter.objects.get(user=user)

    if request.method == 'POST':
        user_form = ProfileEditForm(request.POST, instance=user)
        profile_form = RenterProfileForm(request.POST, instance=renter)
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(
                request, 'Your profile has been updated successfully.')
            return redirect('renter_dashboard')
    else:
        user_form = ProfileEditForm(instance=user)
        profile_form = RenterProfileForm(instance=renter)

    return render(request, 'main/edit_renter.html', {'user_form': user_form, 'profile_form': profile_form})


@ login_required
def logout_view(request):
    """Logout user."""
    logout(request)
    messages.success(request, "You have been logged out successfully.")
    return redirect('homepage')


@ csrf_protect
def update_status(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        # Extract the data from the request
        panic_button_status = data.get('panicButtonStatus')
        lock_status = data.get('lockStatus')
        geo_fencing_location = data.get('geoFencingLocation')

        # Assuming you know which vehicle status to update
        vehicle_status = VehicleStatusIndividual.objects.get(
            id=request.user.id)  # Example query

        # Update the fields
        vehicle_status.panic_button_status = panic_button_status
        vehicle_status.lock_status = lock_status
        vehicle_status.geo_fencing_distance = geo_fencing_location
        vehicle_status.save()

        return JsonResponse({'message': 'Status updated successfully'})
    return JsonResponse({'error': 'Invalid request method'}, status=400)
