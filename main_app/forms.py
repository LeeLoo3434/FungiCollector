from django import forms
from userprofile.models import UserProfile


class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['photo', 'bio', 'location']  # Add any other fields you want in the form
