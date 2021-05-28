from django import forms
from .models import User
from django.contrib.auth.forms import AuthenticationForm, UsernameField


class UserLoginForm(AuthenticationForm):
    username = UsernameField(
        max_length=254,
        label="Email",
        widget=forms.TextInput(attrs={'autofocus': True}),
    )


class UserRegistrationForm(forms.ModelForm):
    password = forms.CharField(label='Password',
                               widget=forms.PasswordInput)
    password2 = forms.CharField(label='Repeat password',
                                widget=forms.PasswordInput)
    username = forms.CharField(widget=forms.HiddenInput, required=False)

    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email',
                  'username', 'address', 'phone')

    def clean_password2(self):
        cd = self.cleaned_data
        if cd['password'] != cd['password2']:
            raise forms.ValidationError('Passwords don\'t match.')
        if len(cd['password']) < 6:
            raise forms.ValidationError(
                'Your password should be more than 6 characters.')
        return cd['password2']

    def clean_username(self):
        cd = self.cleaned_data
        cd['username'] = cd['email']
        return cd['username']
