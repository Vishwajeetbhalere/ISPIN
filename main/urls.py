# main/urls.py

from django.urls import path
from . import views
from .views import (
    homepage, register_user, user_login, fleet_owner_dashboard,
    individual_owner_dashboard, support_engineer_dashboard, renter_dashboard,
    edit_individual_owner, edit_fleet_owner, edit_support_engineer, edit_renter,
    logout_view, toggle_panic_button, toggle_lock_status, fleet_toggle_lock_status
)

urlpatterns = [
    path('', homepage, name='homepage'),
    path('login/', user_login, name='login'),
    path('register/', register_user, name='register'),

    # Dashboard paths for each user role
    path('dashboard/fleet_owner/', fleet_owner_dashboard,
         name='fleet_owner_dashboard'),
    path('dashboard/individual_owner/', individual_owner_dashboard,
         name='individual_owner_dashboard'),
    path('dashboard/support_engineer/', support_engineer_dashboard,
         name='support_engineer_dashboard'),
    path('dashboard/renter/', renter_dashboard, name='renter_dashboard'),

    # Toggle status paths for panic button and lock
    path('toggle_panic_button/', toggle_panic_button, name='toggle_panic_button'),
    path('toggle_lock_status/', toggle_lock_status, name='toggle_lock_status'),
    path('toggle-status/<int:vehicle_id>/',
         views.toggle_wheelchair_status, name='toggle_wheelchair_status'),
    path('fleet-toggle-lock-status/<int:vehicle_id>/',
         views.fleet_toggle_lock_status, name='fleet_toggle_lock_status'),
    path('toggle-vehicle-status/<int:vehicle_id>/',
         views.toggle_vehicle_status, name='toggle_vehicle_status'),



    # Profile edit paths for each user role
    path('profile/edit/individual_owner/<int:id>/',
         views.edit_individual_owner, name='edit_individual_owner'),
    path('profile/edit/fleet_owner/', edit_fleet_owner, name='edit_fleet_owner'),
    path('profile/edit/support_engineer/',
         edit_support_engineer, name='edit_support_engineer'),
    path('profile/edit/renter/', edit_renter, name='edit_renter'),

    # Logout path
    path('logout/', logout_view, name='logout'),
    path('dashboard/update_status/', views.update_status, name='update_status'),

]
