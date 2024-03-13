from assotiation.models import Membership,Fish,Catch,Competition,WaterBody,InformationForAnglers,Contact

from django import forms

class UserCreationForm(forms.Form):
    username = forms.CharField(max_length=150)
    password1 = forms.CharField(widget=forms.PasswordInput)
    password2 = forms.CharField(widget=forms.PasswordInput)

class MembershipForm(forms.ModelForm):
    class Meta:
        model = Membership
        fields = ['date', 'fee', 'angler']  #

class FishForm(forms.ModelForm):
    class Meta:
        model = Fish
        fields = ['name', 'max_weight']  # sprawdzic jeszcze raz modele !!!


class CatchForm(forms.ModelForm):
    class Meta:
        model = Catch
        fields = ['angler', 'fish', 'weight', 'date']  # sprawdzic jeszcze raz modele !!!

class CompetitionForm(forms.ModelForm):
    class Meta:
        model = Competition
        fields = ['name', 'date', 'description', 'available_places', 'first_place', 'second_place', 'third_place'] # sprawdzic jeszcze raz modele !!!


class WaterBodyForm(forms.ModelForm):
    class Meta:
        model = WaterBody
        fields = ['name', 'location', 'fish_species'] # sprawdzic jeszcze raz modele !!!

class CompetitionForm(forms.ModelForm):
    class Meta:
        model = Competition
        fields = ['name', 'date', 'description', 'available_places', 'first_place', 'second_place', 'third_place']# sprawdzic jeszcze raz modele !!!

class WaterBodyForm(forms.ModelForm):
    class Meta:
        model = WaterBody
        fields = ['name', 'location', 'fish_species'] # sprawdzic jeszcze raz modele !!!