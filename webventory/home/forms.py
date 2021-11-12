from django import forms

class ItemForm(forms.Form):
    id = forms.IntegerField()
    name = forms.CharField(max_length=30)
    description = forms.CharField(max_length=100)
    price = forms.FloatField()
    user_visibility = forms.CharField(max_length=30)