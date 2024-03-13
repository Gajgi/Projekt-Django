from assotiation.models import Membership,Fish,Catch,Competition,WaterBody,InformationForAnglers,Contact
from django import forms
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User


class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ("username", "password1", "password2")

class MembershipForm(forms.ModelForm):
    class Meta:
        model = Membership
        fields = ['date', 'fee', ]
        widgets = { 'date': forms.DateInput(attrs={'type': 'date'}) }
            #'category': forms.CheckboxSelectMultiple,
            #'type': forms.RadioSelect()


class FishForm(forms.ModelForm):
    class Meta:
        model = Fish
        fields = ['name', 'max_weight']


class CatchForm(forms.ModelForm):
    weight = forms.FloatField()
    class Meta:
        model = Catch
        fields = ['angler', 'fish', 'weight', 'date']
        widgets = {'date': forms.DateInput(attrs={'type': 'date'})}




class WaterBodyForm(forms.ModelForm):
    class WaterBodyForm(forms.ModelForm):
        water_body = forms.ModelChoiceField(queryset=WaterBody.objects.all(), empty_label="Wybierz zbiornik")
    class Meta:
        model = WaterBody
        fields = ['name', 'location', 'fish_species']

class CompetitionForm(forms.ModelForm):
    class Meta:
        model = Competition
        fields = ['name', 'date', 'description', 'available_places', 'first_place', 'second_place', 'third_place']
        widgets = {'date': forms.DateInput(attrs={'type': 'date'})}
class WaterBodyForm(forms.ModelForm):
    class Meta:
        model = WaterBody
        fields = ['name', 'location', 'fish_species']