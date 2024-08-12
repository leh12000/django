
from django import forms
from .models import Customer


class CustomerForm(forms.ModelForm):

    password2=forms.CharField(widget=forms.PasswordInput(attrs={"class":"form-control","placeholder":"Confirm your password"}))
    class Meta:
        model=Customer
        fields=["first_name","last_name","username","email","phone","password"]
        widgets={
            'first_name':forms.TextInput(attrs={"class":"form-control"}),
            'last_name': forms.TextInput(attrs={"class": "form-control"}),
            'username': forms.TextInput(attrs={"class": "form-control"}),
            'email':forms.EmailInput(attrs={"class":"form-control","placeholder":"Email Adresse"}),
            'phone':forms.TextInput(attrs={"class":"form-control"}),
            "password":forms.PasswordInput(attrs={"class":"form-control","placeholder":"Password"})
        }

    def clean(self):
        cleaned_data=super().clean()
        password2=cleaned_data.get("password2")
        password=cleaned_data.get("password")
        if password and password2 and password !=password2:
            self.add_error('password2',"The two passwords do not match")
