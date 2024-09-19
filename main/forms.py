from .models import CustomUser, IndividualOwner
from .models import CustomUser
from django.contrib.auth.forms import UserChangeForm, PasswordChangeForm
from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import CustomUser, IndividualOwner, FleetOwner, SupportEngineer, Renter


class CustomUserRegistrationForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = ('username', 'email', 'first_name', 'last_name',
                  'user_type', 'password1', 'password2')


class IndividualOwnerForm(forms.ModelForm):
    class Meta:
        model = IndividualOwner
        fields = ('address1', 'address2', 'city', 'state', 'country', 'pin', 'primary_contact_no',
                  'emergency_contact_no', 'whatsapp_number', 'product_serial_no', 'home_location',
                  'geo_fencing_location')


class FleetOwnerForm(forms.ModelForm):
    class Meta:
        model = FleetOwner
        fields = ('address1', 'address2', 'city', 'state', 'country', 'pin', 'primary_contact_no',
                  'whatsapp_number', 'product_serial_no', 'launch_city', 'launch_area',
                  'deploy_location', 'geo_fencing_location', 'support_engineer_first_name',
                  'support_engineer_last_name', 'support_engineer_contact_number')


class SupportEngineerForm(forms.ModelForm):
    class Meta:
        model = SupportEngineer
        fields = ('address1', 'address2', 'city', 'state', 'country', 'pin', 'primary_contact_no',
                  'whatsapp_number', 'service_state', 'service_city', 'service_area')


class RenterForm(forms.ModelForm):
    class Meta:
        model = Renter
        fields = ('address1', 'address2', 'city', 'state', 'country', 'pin', 'primary_contact_no',
                  'emergency_contact_no', 'whatsapp_number', 'product_serial_no', 'home_location',
                  'geo_fencing_location')


class CustomAuthenticationForm(AuthenticationForm):
    username = forms.CharField(
        max_length=254, widget=forms.TextInput(attrs={'autofocus': True}))
    password = forms.CharField(
        label='Password', strip=False, widget=forms.PasswordInput)


class ProfileEditForm(forms.ModelForm):
    """Form to edit user profile information."""
    password = forms.CharField(widget=forms.PasswordInput, required=False)

    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'first_name', 'last_name', 'password']

    def clean_password(self):
        password = self.cleaned_data.get('password', None)
        if password:
            self.instance.set_password(password)
        return password


class IndividualOwnerProfileForm(forms.ModelForm):
    class Meta:
        model = IndividualOwner
        fields = [
            'address1', 'address2', 'city', 'state', 'country', 'pin',
            'primary_contact_no', 'emergency_contact_no', 'whatsapp_number',
            'product_serial_no', 'home_location', 'geo_fencing_location'
        ]


class FleetOwnerProfileForm(forms.ModelForm):
    class Meta:
        model = FleetOwner
        fields = [
            'address1', 'address2', 'city', 'state', 'country', 'pin',
            'primary_contact_no', 'whatsapp_number', 'product_serial_no',
            'launch_city', 'launch_area', 'deploy_location',
            'geo_fencing_location', 'support_engineer_first_name',
            'support_engineer_last_name', 'support_engineer_contact_number'
        ]


class SupportEngineerProfileForm(forms.ModelForm):
    class Meta:
        model = SupportEngineer
        fields = [
            'address1', 'address2', 'city', 'state', 'country', 'pin',
            'primary_contact_no', 'whatsapp_number', 'service_state',
            'service_city', 'service_area'
        ]


class RenterProfileForm(forms.ModelForm):
    class Meta:
        model = Renter
        fields = [
            'address1', 'address2', 'city', 'state', 'country', 'pin',
            'primary_contact_no', 'emergency_contact_no', 'whatsapp_number',
            'product_serial_no', 'home_location', 'geo_fencing_location'
        ]
