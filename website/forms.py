from django import forms
from website.models import *


class Contactform(forms.ModelForm):
    name = forms.CharField()
    email = forms.EmailField()
    subject = forms.CharField()
    message = forms.CharField()

    class Meta:
        model = contactmodel
        fields = [
            'name',
            'email',
            'subject',
            'message'
        ]


class Ticketform(forms.ModelForm):
    subject = forms.CharField()
    gravity = forms.CharField()
    message = forms.CharField()

    class Meta:
        model = ticketmodel
        fields = [
            'subject',
            'gravity',
            'message'
        ]


class Fileform(forms.ModelForm):
    name = forms.CharField()
    description = forms.CharField()
    file = forms.FileField()

    class Meta:
        model = filemodel
        fields = [
            'name',
            'description',
            'file'
        ]


class Profileform(forms.ModelForm):
    first_name = forms.CharField()
    last_name = forms.CharField()
    email = forms.CharField()
    bio = forms.CharField()
    image = forms.ImageField()

    class Meta:
        model = User
        fields = [
            'first_name',
            'last_name',
            'email',
            'bio',
            'image'
        ]
