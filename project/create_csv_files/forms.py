from django import forms


class NumberRows (forms.Form):
    rows = forms.IntegerField(min_value=1, required=False, widget=forms.TextInput(attrs={'size': '8'}))

