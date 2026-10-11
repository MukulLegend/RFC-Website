from django import forms
from django.contrib.auth.forms import UserCreationForm, PasswordChangeForm
from django.contrib.auth.models import User
from .models import Contact, Register

class RegisterForm(UserCreationForm):
    email = forms.EmailField(required=True, widget=forms.EmailInput(attrs={
        "style": "width: 100%; padding: 0.75rem; margin-bottom: 1rem; border: 1px solid #cccccc; border-radius: 4px; font-size: 1rem; transition: border-color 0.3s;"
    }))
    contact_no = forms.CharField(max_length=20, required=False, label='Contact Number', widget=forms.TextInput(attrs={
        "style": "width: 100%; padding: 0.75rem; margin-bottom: 1rem; border: 1px solid #cccccc; border-radius: 4px; font-size: 1rem; transition: border-color 0.3s;"
    }))
    username = forms.CharField(widget=forms.TextInput(attrs={
        "style": "width: 100%; padding: 0.75rem; margin-bottom: 1rem; border: 1px solid #cccccc; border-radius: 4px; font-size: 1rem; transition: border-color 0.3s;"
    }))

    class Meta:
        model = User
        fields = ("username", "email", "password1", "password2")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['password1'].widget.attrs.update({
            "style": "width: 100%; padding: 0.75rem; margin-bottom: 1rem; border: 1px solid #cccccc; border-radius: 4px; font-size: 1rem; transition: border-color 0.3s;"
        })
        self.fields['password2'].widget.attrs.update({
            "style": "width: 100%; padding: 0.75rem; margin-bottom: 1rem; border: 1px solid #cccccc; border-radius: 4px; font-size: 1rem; transition: border-color 0.3s;"
        })

    def save(self, commit=True):
        user = super(RegisterForm, self).save(commit=False)
        user.email = self.cleaned_data["email"]
        if commit:
            user.save()
        return user

class ChangePasswordForm(PasswordChangeForm):
    old_password = forms.CharField(widget=forms.PasswordInput(attrs={'autocomplete': 'current-password', 'autofocus': True}), label='Old Password')
    new_password1 = forms.CharField(widget=forms.PasswordInput(attrs={'autocomplete': 'new-password'}), label='New Password')
    new_password2 = forms.CharField(widget=forms.PasswordInput(attrs={'autocomplete': 'new-password'}), label='Confirm New Password')

class UserProfileForm(forms.ModelForm):
    email = forms.EmailField(required=True, label='Email')

    class Meta:
        model = User
        fields = ['email']

class RegisterModelForm(forms.ModelForm):
    contact_no = forms.CharField(max_length=20, required=False, label='Contact Number')

    class Meta:
        model = Register
        fields = ['contact_no']
        # Add exclude or fields attribute to avoid ImproperlyConfigured error


class ContactForm(forms.ModelForm):
    class Meta:
        model = Contact
        fields = ["name", "email", "contact_no", "message"]
        widgets = {
            "name": forms.TextInput(attrs={"class": "form-control mb-2", "placeholder": "Your name"}),
            "email": forms.EmailInput(attrs={"class": "form-control mb-2", "placeholder": "you@example.com"}),
            "contact_no": forms.TextInput(attrs={"class": "form-control mb-2", "placeholder": "Phone number"}),
            "message": forms.Textarea(attrs={"class": "form-control mb-2", "rows": 4,
                                              "placeholder": "How can we help? (trials, sponsorship, matches...)"}),
        }
        labels = {"contact_no": "Contact No."}
