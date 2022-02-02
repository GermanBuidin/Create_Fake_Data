from django import forms
from .constants import *
from django.forms import formset_factory, BaseFormSet, HiddenInput


class LoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)


class SchemaForm(forms.Form):
    name = forms.CharField(max_length=100)
    separator = forms.ChoiceField(choices=COLUMN_SEPARATOR)
    quote = forms.ChoiceField(choices=STRING_CHARACTER)


class TypeDataForm(forms.Form):
    title = forms.CharField(max_length=100)
    type = forms.ChoiceField(choices=TYPE)
    From = forms.IntegerField(required=False)
    to = forms.IntegerField(required=False)
    order = forms.IntegerField()


TypeDataFormSet = formset_factory(TypeDataForm, extra=0)

