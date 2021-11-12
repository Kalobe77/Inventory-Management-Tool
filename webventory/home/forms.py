from django import forms

class ItemForm(forms.Form):
    id = forms.IntegerField()
    name = forms.CharField(max_length=30)
    description = forms.CharField(max_length=100)
    quantity = forms.IntegerField()
    price = forms.FloatField()
    user_visability = forms.CharField(max_length=30)