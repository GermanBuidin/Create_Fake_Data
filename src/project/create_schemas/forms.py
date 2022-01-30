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
    From = forms.IntegerField()
    to = forms.IntegerField()
    order = forms.IntegerField()





SchemaFormSet = formset_factory(SchemaForm, extra=1)
TypeDataFormSet = formset_factory(TypeDataForm, extra=1, can_delete=True )