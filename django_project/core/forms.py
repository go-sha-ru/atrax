from django import forms


class PhoneInfoForm(forms.Form):
    phone_number = forms.CharField(max_length=11,
                                   label='Номер телефона', widget=forms.TextInput(attrs={'placeholder': '7923111111'}))
