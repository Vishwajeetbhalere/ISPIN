from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.contrib.auth.hashers import make_password, check_password
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.contrib.auth.hashers import make_password, check_password


class CustomUserManager(BaseUserManager):
    def create_user(self, username, email, password=None, **extra_fields):
        if not email:
            raise ValueError('The Email field must be set')
        email = self.normalize_email(email)
        user = self.model(username=username, email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        return self.create_user(username, email, password, **extra_fields)


class CustomUser(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(unique=True)
    username = models.CharField(max_length=255, unique=True)
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)

    # User roles
    FLEET_OWNER = 'Fleet_Owner'
    INDIVIDUAL_OWNER = 'Individual_Owner'
    SUPPORT_ENGINEER = 'Support_Engineer'
    RENTER = 'Renter'

    ROLE_CHOICES = [
        (FLEET_OWNER, 'Fleet Owner'),
        (INDIVIDUAL_OWNER, 'Individual Owner'),
        (SUPPORT_ENGINEER, 'Support Engineer'),
        (RENTER, 'Renter')
    ]

    user_type = models.CharField(
        max_length=50, choices=ROLE_CHOICES, default=INDIVIDUAL_OWNER)
    password = models.CharField(max_length=255)

    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    groups = models.ManyToManyField(
        'auth.Group',
        related_name='customuser_groups',  # Add unique related_name
        blank=True,
        help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.',
        verbose_name='groups',
    )

    user_permissions = models.ManyToManyField(
        'auth.Permission',
        related_name='customuser_user_permissions',  # Add unique related_name
        blank=True,
        help_text='Specific permissions for this user.',
        verbose_name='user permissions',
    )

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email']

    objects = CustomUserManager()

    def __str__(self):
        return self.username

    def set_password(self, raw_password):
        """Hash the password and save it."""
        self.password = make_password(raw_password)

    def check_password(self, raw_password):
        """Check if the given password matches the hashed password."""
        return check_password(raw_password, self.password)


class IndividualOwner(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    address1 = models.CharField(max_length=255, null=True, blank=True)
    address2 = models.CharField(max_length=255, null=True, blank=True)
    city = models.CharField(max_length=100, null=True, blank=True)
    state = models.CharField(max_length=100, null=True, blank=True)
    country = models.CharField(max_length=100, null=True, blank=True)
    pin = models.CharField(max_length=10, null=True, blank=True)
    primary_contact_no = models.CharField(max_length=15)
    emergency_contact_no = models.CharField(
        max_length=15, null=True, blank=True)
    whatsapp_number = models.CharField(max_length=15, null=True, blank=True)
    product_serial_no = models.CharField(max_length=100, null=True, blank=True)
    home_location = models.CharField(max_length=255, null=True, blank=True)
    geo_fencing_location = models.CharField(max_length=10, choices=[(
        '1 KM', '1 KM'), ('1.5 KM', '1.5 KM')], default='1 KM')

    def __str__(self):
        return self.user.username


class SupportEngineer(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    address1 = models.CharField(max_length=255, null=True, blank=True)
    address2 = models.CharField(max_length=255, null=True, blank=True)
    city = models.CharField(max_length=100, null=True, blank=True)
    state = models.CharField(max_length=100, null=True, blank=True)
    country = models.CharField(max_length=100, null=True, blank=True)
    pin = models.CharField(max_length=10, null=True, blank=True)
    primary_contact_no = models.CharField(max_length=15)
    whatsapp_number = models.CharField(max_length=15, null=True, blank=True)
    service_state = models.CharField(max_length=100)
    service_city = models.CharField(max_length=100)
    service_area = models.CharField(max_length=100)

    def __str__(self):
        return self.user.username


class FleetOwner(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    address1 = models.CharField(max_length=255, null=True, blank=True)
    address2 = models.CharField(max_length=255, null=True, blank=True)
    city = models.CharField(max_length=100, null=True, blank=True)
    state = models.CharField(max_length=100, null=True, blank=True)
    country = models.CharField(max_length=100, null=True, blank=True)
    pin = models.CharField(max_length=10, null=True, blank=True)
    primary_contact_no = models.CharField(max_length=15)
    whatsapp_number = models.CharField(max_length=15, null=True, blank=True)
    product_serial_no = models.CharField(max_length=100, null=True, blank=True)
    launch_city = models.CharField(max_length=100, null=True, blank=True)
    launch_area = models.CharField(max_length=100, null=True, blank=True)
    deploy_location = models.CharField(max_length=255, null=True, blank=True)
    geo_fencing_location = models.CharField(max_length=10, choices=[(
        '1 KM', '1 KM'), ('1.5 KM', '1.5 KM')], default='1 KM')
    support_engineer_first_name = models.CharField(
        max_length=255, null=True, blank=True)
    support_engineer_last_name = models.CharField(
        max_length=255, null=True, blank=True)
    support_engineer_contact_number = models.CharField(
        max_length=15, null=True, blank=True)

    def __str__(self):
        return f"{self.user.username} (Fleet Owner)"


class Renter(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    address1 = models.CharField(max_length=255, null=True, blank=True)
    address2 = models.CharField(max_length=255, null=True, blank=True)
    city = models.CharField(max_length=100, null=True, blank=True)
    state = models.CharField(max_length=100, null=True, blank=True)
    country = models.CharField(max_length=100, null=True, blank=True)
    pin = models.CharField(max_length=10, null=True, blank=True)
    primary_contact_no = models.CharField(max_length=15)
    emergency_contact_no = models.CharField(
        max_length=15, null=True, blank=True)
    whatsapp_number = models.CharField(max_length=15, null=True, blank=True)
    product_serial_no = models.CharField(max_length=100, null=True, blank=True)
    home_location = models.CharField(max_length=255, null=True, blank=True)
    geo_fencing_location = models.CharField(max_length=10, choices=[(
        '1 KM', '1 KM'), ('1.5 KM', '1.5 KM')], default='1 KM')

    def __str__(self):
        return self.user.username


class VehicleStatusIndividual(models.Model):
    owner = models.OneToOneField(
        IndividualOwner,
        on_delete=models.CASCADE,
        related_name='vehicle_status'
    )

    current_latitude = models.DecimalField(
        max_digits=9, decimal_places=6, default=0.0)
    current_longitude = models.DecimalField(
        max_digits=9, decimal_places=6, default=0.0)
    starting_latitude = models.DecimalField(
        max_digits=9, decimal_places=6, default=0.0)
    starting_longitude = models.DecimalField(
        max_digits=9, decimal_places=6, default=0.0)
    ending_latitude = models.DecimalField(
        max_digits=9, decimal_places=6, null=True, blank=True, default=0.0)
    ending_longitude = models.DecimalField(
        max_digits=9, decimal_places=6, null=True, blank=True, default=0.0)

    panic_button_status = models.BooleanField(default=False)

    main_battery_temp = models.CharField(max_length=50)
    main_battery_current = models.DecimalField(max_digits=5, decimal_places=2)
    auxiliary_battery_status = models.DecimalField(
        max_digits=5, decimal_places=2)

    lock_status = models.BooleanField(default=False)
    route = models.TextField()
    emergency_owner_whatsapp = models.CharField(max_length=255)
    geo_fencing_distance = models.CharField(
        max_length=20, blank=True, null=True)

    def __str__(self):
        return f"Vehicle Status of {self.owner.user.username}"


class VehicleFleet(models.Model):
    # Choices for active and inactive status
    STATUS_CHOICES = (
        ('active', 'Active'),
        ('inactive', 'Inactive'),
    )
    # Link to FleetOwner
    owner = models.ForeignKey(
        FleetOwner, on_delete=models.CASCADE, related_name='vehicles')

    # Basic vehicle details
    serial_number = models.CharField(max_length=50, unique=True)
    default_city = models.CharField(max_length=100)
    default_area = models.CharField(max_length=100)

    # Current location
    current_latitude = models.FloatField(null=True, blank=True)
    current_longitude = models.FloatField(null=True, blank=True)

    # Rental details
    rented_by_mobile = models.CharField(max_length=15, null=True, blank=True)
    rent_received = models.DecimalField(
        max_digits=10, decimal_places=2, null=True, blank=True)
    last_rented_mobile = models.CharField(max_length=15, null=True, blank=True)
    last_rent_received = models.DecimalField(
        max_digits=10, decimal_places=2, null=True, blank=True)

    # Status information
    status = models.CharField(
        max_length=10, choices=STATUS_CHOICES, default='inactive')
    time_remaining = models.DurationField(null=True, blank=True)
    panic_button_status = models.BooleanField(default=False)
    battery_charge_status = models.IntegerField(
        null=True, blank=True)  # percentage

    # Lock/Unlock status
    is_locked = models.BooleanField(default=True)

    # Contact information
    contact_support_person = models.CharField(
        max_length=100, null=True, blank=True)
    whatsapp_message = models.TextField(null=True, blank=True)

    # Ticketing and Service
    is_out_of_service = models.BooleanField(default=False)
    ticket_number = models.CharField(max_length=50, null=True, blank=True)
    issue_description = models.TextField(null=True, blank=True)

    def __str__(self):
        return f'Vehicle {self.serial_number} - {self.status}'
