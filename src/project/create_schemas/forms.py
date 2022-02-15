from django import forms
from django.core.exceptions import ValidationError
from django.forms import formset_factory, BaseFormSet

from main_catalog.utils import collection
from .constants import COLUMN_SEPARATOR, \
                       STRING_CHARACTER, \
                       TYPE


def validation_name(name):
    if collection.find_one({"name": name}):
        raise ValidationError(" Choice another name ")


class LoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)


class SchemaFormNew(forms.Form):
    name = forms.CharField(label='Name', max_length=100, validators=[validation_name],
                           widget=forms.TextInput(attrs={'size': '30'}))
    separator = forms.ChoiceField(label='Column separator', choices=COLUMN_SEPARATOR,
                                  widget=forms.Select(attrs={'class': "schema"}))
    quote = forms.ChoiceField(label='String character', choices=STRING_CHARACTER,
                              widget=forms.Select(attrs={'class': "schema"}))


class SchemaFormEdit(forms.Form):
    name = forms.CharField(max_length=100)
    separator = forms.ChoiceField(choices=COLUMN_SEPARATOR)
    quote = forms.ChoiceField(choices=STRING_CHARACTER)


class TypeDataForm(forms.Form):
    title = forms.CharField(max_length=100, widget=forms.TextInput(attrs={'size': '30'}))
    type = forms.ChoiceField(choices=TYPE, widget=forms.Select(attrs={'onchange': "openBlock(id, this.value)",
                                                                      'class': 'schema-2'}))
    min_value = forms.IntegerField(label='From', required=False, widget=forms.TextInput(attrs={'size': '8'}))
    max_value = forms.IntegerField(label='To', required=False, widget=forms.TextInput(attrs={'size': '8'}))


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
                raise ValidationError("Field 'Title' in a set must have distinct titles")
            titles.append(title)
            if order:
                if order in orders:
                    raise ValidationError("Field 'Order' in a set must have distinct number")
                if order <= 0:
                    raise ValidationError("'Order' value must be a positive number")
            else:
                raise ValidationError("Field 'Order' must not be empty")
            orders.append(order)
            types = form.cleaned_data.get("type")
            if types == "integer":
                min_value = form.cleaned_data.get("min_value")
                max_value = form.cleaned_data.get("max_value")
                print(min_value, max_value)
                if min_value and max_value:
                    if min_value >= max_value:
                        raise ValidationError("Field 'From' in a set must be lees To")
                else:
                    raise ValidationError("Fields 'From' and 'To' can't be empty")


TypeDataFormSet = formset_factory(TypeDataForm, formset=BaseTypeDataFormSet, extra=0, can_order=True)
