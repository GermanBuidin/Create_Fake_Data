from django import forms
from django.core.exceptions import ValidationError

from proj.utils import collection
from .constants import *
from django.forms import formset_factory, BaseFormSet, HiddenInput


def validation_name(name):
    if collection.find_one({"name": name}):
        raise ValidationError(" Choice another name ")


class LoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)


class SchemaForm(forms.Form):
    name = forms.CharField(max_length=100, validators=[validation_name])
    separator = forms.ChoiceField(choices=COLUMN_SEPARATOR)
    quote = forms.ChoiceField(choices=STRING_CHARACTER)


class SchemaForm2(forms.Form):
    name = forms.CharField(max_length=100)
    separator = forms.ChoiceField(choices=COLUMN_SEPARATOR)
    quote = forms.ChoiceField(choices=STRING_CHARACTER)


class TypeDataForm(forms.Form):
    title = forms.CharField(max_length=100, widget=forms.TextInput(attrs={'size': '30'}))
    type = forms.ChoiceField(choices=TYPE, widget=forms.Select(attrs={'onchange': "openBlock(id, this.value)"}))
    From = forms.IntegerField(required=False, widget=forms.TextInput(attrs={'size': '8'}))
    To = forms.IntegerField(required=False, widget=forms.TextInput(attrs={'size': '8'}))


class BaseTypeDataFormSet(BaseFormSet):

    def clean(self):
        if any(self.errors):
            return
        titles = []
        orders = []
        for form in self.forms:
            title = form.cleaned_data.get("title")
            order = form.cleaned_data.get("ORDER")
            if title in titles:
                raise ValidationError("Aticles Title in a set must have distinct titles")
            titles.append(title)
            if order in orders:
                raise ValidationError("Aticles Order in a set must have distinct number")
            if order < 0:
                raise ValidationError("Order value must be a positive number")
            orders.append(order)
            types = form.cleaned_data.get("type")
            if types == "integer":
                if form.cleaned_data.get("From") and form.cleaned_data.get("To"):
                    if form.cleaned_data.get("From") >= form.cleaned_data.get("To"):
                        raise ValidationError("Aticles From in a set must be lees To")
                else:
                    raise ValidationError("Aticles From and To can't be empty")


TypeDataFormSet = formset_factory(TypeDataForm, formset=BaseTypeDataFormSet, extra=0, can_order=True)
