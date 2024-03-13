from django.contrib.auth.models import User
from django.views import View
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, get_object_or_404, redirect
from .models import Membership, Competition, WaterBody, Fish, Catch
from .forms import MembershipForm, CompetitionForm, WaterBodyForm, FishForm, CatchForm, CustomUserCreationForm
from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm
from django.views.generic.edit import CreateView
from django.contrib.auth.mixins import LoginRequiredMixin
from .forms import MembershipForm
from .models import InformationForAnglers, Contact


class CreateUserView(View):

    def get(self, request):
        return render(request, 'create_user.html')

    def post(self, request):
        username = request.POST['username']
        password = request.POST['password1']
        re_password = request.POST['password2']
        if password != re_password:
            return render(request, 'create_user.html', {'error': 'Hasła są różne !!!'})
        u = User(username=username)
        u.set_password(password)
        u.save()
        return redirect('memberships')


class LoginView(View):
    def get(self, request):
        return render(request, 'login.html')

    def post(self, request):
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('home')
        return render(request, 'login.html')


class LogoutView(View):
    def get(self, request):
        logout(request)
        return redirect('home')



class MembershipView(LoginRequiredMixin, View):
    form_class = MembershipForm

    def get(self, request):
        form = self.form_class()
        return render(request, 'membership_list.html', {'form': form})

    def post(self, request):
        form = self.form_class(request.POST)
        if form.is_valid():
            membership = form.save(commit=False)
            membership.angler = request.user
            membership.save()
            return redirect('/')
        return render(request,'membership_list.html', {'form': form})


class MembershipListView(View):
    def get(self, request):
        query = request.GET.get('search')
        members = Membership.objects.all()
        if query:
            members = members.filter(angler__username__contains=query)
        return render(request, 'members_list.html', {'members': members})


class MembershipUpdateView(LoginRequiredMixin,View):
    def get(self, request, pk):
        membership = get_object_or_404(Membership, pk=pk)
        form = MembershipForm(instance=membership)
        return render(request, 'membership_detail.html', {'membership': membership, 'form': form})

    def post(self, request, pk):
        membership = get_object_or_404(Membership, pk=pk)
        form = MembershipForm(request.POST, instance=membership)
        if form.is_valid():
            form.save()
        return redirect('membership_update', pk=pk)


class MembershipDeleteView(LoginRequiredMixin, View):
    def get(self, request, pk):
        membership = get_object_or_404(Membership, pk=pk)
        form = MembershipForm(instance=membership)
        return render(request, 'membership_delete.html', {'membership': membership, 'form': form})

    def post(self, request, pk):
        operation = request.POST.get('delete')
        if operation == 'tak':
            membership = get_object_or_404(Membership, pk=pk)
            membership.delete()
        return redirect('memberships')


class FishListView(View):
    def get(self, request):
        fishes = Fish.objects.all()
        form = FishForm()
        return render(request, 'fish_list.html', {'fishes': fishes, 'form': form})

    def post(self, request):
        form = FishForm(request.POST)
        if form.is_valid():
            form.save()
        return redirect('fish_list')


class FishCreateView(LoginRequiredMixin,View):
    def get(self, request):
        form = FishForm()
        return render(request, 'fish_form.html', {'form': form})

    def post(self, request):
        form = FishForm(request.POST)
        if form.is_valid():
            fish_instance = form.save()
            water_body = WaterBody.objects.get(pk=request.POST['water_body'])
            fish_instance.water_bodies.add(water_body)
            return redirect('water_bodies')
        return render(request, 'fish_form.html', {'form': form})


class CatchListView(View):
    def get(self, request):
        catches = Catch.objects.all()
        form = CatchForm()
        return render(request, 'catch_list.html', {'catches': catches, 'form': form})

    def post(self, request):
        form = CatchForm(request.POST)
        if form.is_valid():
            form.save()
        return redirect('catch_list')


class CompetitionListView(View):
    def get(self, request):
        competitions = Competition.objects.all()
        form = CompetitionForm()
        return render(request, 'competitions.html', {'competitions': competitions, 'form': form})

    def post(self, request):
        form = CompetitionForm(request.POST)
        if form.is_valid():
            form.save()
        return redirect('competitions')


class WaterBodyListView(View):
    def get(self, request):
        water_bodies = WaterBody.objects.all().distinct().order_by('name', 'location')
        form = WaterBodyForm()
        fish_form = FishForm()
        return render(request, 'water_body_list.html',
                      {'water_bodies': water_bodies, 'form': form, 'fish_form': fish_form})

    def post(self, request):
        form = WaterBodyForm(request.POST)
        fish_form = FishForm(request.POST)
        if form.is_valid():
            form.save()
            if fish_form.is_valid():
                fish_instance = fish_form.save(commit=False)
                fish_instance.water_body_id = form.instance.id
                fish_instance.save()
        return redirect('water_bodies')


class WaterBodyUpdateView(LoginRequiredMixin,View):
    def get(self, request, pk):
        water_body = get_object_or_404(WaterBody, pk=pk)
        form = WaterBodyForm(instance=water_body)
        fish_species = ', '.join(fish.name for fish in water_body.fish_species.all())
        return render(request, 'water_body_detail.html',
                      {'water_body': water_body, 'form': form, 'fish_species': fish_species})

    def post(self, request, pk):
        water_body = get_object_or_404(WaterBody, pk=pk)
        form = WaterBodyForm(request.POST, instance=water_body)
        if form.is_valid():
            form.save()
        return redirect('water_bodies_update', pk=pk)


class InformationForAnglersListView(View):
    def get(self, request):
        informations = InformationForAnglers.objects.all()
        return render(request, 'informations_list.html', {'informations': informations})


class ContactListView(View):
    def get(self, request):
        contacts = Contact.objects.all()
        return render(request, 'contacts_list.html', {'contacts': contacts})
