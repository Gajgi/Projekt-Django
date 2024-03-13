from django.contrib.auth.models import User
from django.shortcuts import render

# Create your views here.

# Importuje formularz UserCreationForm z Django, używany do tworzenia nowych użytkowników
from django.contrib.auth.forms import UserCreationForm
# Importuje View z Django, używany jako klasa bazowa do tworzenia Django Views
from django.views import View
# Importuje LoginRequiredMixin z Django, które ogranicza dostęp tylko do zalogowanych użytkowników
from django.contrib.auth.mixins import LoginRequiredMixin
# Importuje Django's auth functions
from django.contrib.auth import authenticate, login, logout
# Importuje Django's shortcuts module, umożliwiający korzystanie z przydatnych funkcji jak render, get_object_or_404, i redirect
from django.shortcuts import render, get_object_or_404, redirect
# Importuje modele używane w tym pliku
from .models import Membership, Competition, WaterBody, Fish, Catch
# Importuje formularze używane w tym pliku
from .forms import MembershipForm, CompetitionForm, WaterBodyForm, FishForm, CatchForm




# Klasa CreateUser służy do tworzenia nowych użytkowników
# mixin LoginRequiredMixin tutaj sprawia, że tylko zalogowani użytkownicy mogą tworzyć nowe konta
class CreateUserView(View):

    def get(self, request):
        return render(request, 'create_user.html')

    def post(self, request):
        username = request.POST['username']
        password = request.POST['password']
        re_password = request.POST['password2']
        if password != re_password:
            return render(request,'create_user.html', {'error':'hasła są różne'})
        u = User(username=username)
        u.set_password(password)
        u.save()
        return redirect('home')


# Klasa bazy logowania
class LoginView(View):
    def get(self, request):
        # Renderuje login.html na żądanie GET
        return render(request, 'login.html')

    def post(self, request):
        # Na żądanie POST, bierze parametr 'next' z żądania GET, domyślnie 'home', jeśli 'next' nie istnieje.
        # Następnie pobiera 'username' i 'password' z żądania POST.
        # Następnie uwierzytelnia użytkownika. Jeśli użytkownik jest uwierzytelniony, loguje go i przekierowuje go do url określonego przez 'next'
        # Jeśli uwierzytelnienie się nie powiedzie, renderuje stronę logowania ponownie.
        url = request.GET.get('next', 'home')
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect(url)
        return render(request, 'login.html')


# Klasa LogoutView - używana do wylogowywania użytkowników.Wylogowuje użytkownika i przekierowuje do strony głównej
class LogoutView(View):
    def get(self, request):
        logout(request)
        return redirect('home')
#
#
# # ...
#
# # Klasa MembershipView wyświetla wszystkich członków (instancje modelu Membership)
# # oraz umożliwia dodanie nowego członka za pomocą formularza MembershipForm
# class MembershipView(View):
#     def get(self, request):
#         # Na żądanie GET, pobiera wszystkie instancje Membership i
#         # inicjalizuje pusty formularz MembershipForm
#         memberships = Membership.objects.all()
#         form = MembershipForm()
#         return render(request, 'membership_list.html', {'memberships': memberships, 'form': form})
#
#     def post(self, request):
#         # W odpowiedzi na żądanie POST, formularz MembershipForm jest sprawdzany
#         # Jeśli formularz jest ważny, dane z formularza są zapisywane
#         form = MembershipForm(request.POST)
#         if form.is_valid():
#             form.save()
#         return redirect('memberships')
#
# # Klasa MembershipUpdateView służy do aktualizacji istniejącej instancji Membership
# class MembershipUpdateView(View):
#     def get(self, request, pk):
#         # Na żądanie GET, pobiera konkretną instancję modelu Membership za pomocą pk i
#         # inicjalizuje formularz MembershipForm danymi z tej instancji
#         membership = get_object_or_404(Membership, pk=pk)
#         form = MembershipForm(instance=membership)
#         return render(request, 'membership_detail.html', {'membership': membership, 'form': form})
#
#     def post(self, request, pk):
#         # Przy żądaniu POST, formularz MembershipForm jest sprawdzany pod kątem prawidłowości
#         # Jeśli formularz jest prawidłowy, dane z formularza są zapisywane
#         membership = get_object_or_404(Membership, pk=pk)
#         form = MembershipForm(request.POST, instance=membership)
#         if form.is_valid():
#             form.save()
#         return redirect('membership_detail', pk=pk)
#
# # Klasa MembershipDeleteView służy do usuwania istniejącej instancji Membership
# class MembershipDeleteView(View):
#     def get(self, request, pk):
#         # Przy żądaniu GET, pobiera konkretną instancję modelu Membership za pomocą pk i
#         # inicjalizuje formularz MembershipForm danymi dla tej instancji
#         membership = get_object_or_404(Membership, pk=pk)
#         form = MembershipForm(instance=membership)
#         return render(request, 'membership_delete.html', {'membership': membership, 'form': form})
#
#     def post(self, request, pk):
#         # Na żądanie POST, konkretna instancja członkostwa jest usuwana.
#         membership = get_object_or_404(Membership, pk=pk)
#         membership.delete()
#         return redirect('memberships')
#
# # Klasa FishListView wyświetla wszystkie ryby (instancje modelu Fish) oraz
# # umożliwia dodanie nowej ryby za pomocą formularza FishForm
# class FishListView(View):
#     def get(self, request):
#         # Na żądanie GET, pobiera wszystkie instancje Fish i
#         # inicjalizuje pusty formularz FishForm
#         fishes = Fish.objects.all()
#         form = FishForm()
#         return render(request, 'fish_list.html', {'fishes': fishes, 'form': form})
#
#     def post(self, request):
#         # Na żądanie POST, formularz FishForm jest sprawdzany
#         # Jeśli formularz jest ważny, dane z formularza są zapisywane
#         form = FishForm(request.POST)
#         if form.is_valid():
#             form.save()
#         return redirect('fishes')
#
# # ...
#
# # Klasa FishUpdateView umożliwia aktualizację istniejących instancji ryb
# class FishUpdateView(View):
#     def get(self, request, pk):
#         # Na żądanie GET, pobiera wybraną instancję modelu Fish i
#         # inicjalizuje formularz FishForm danymi z tej instancji
#         fish = get_object_or_404(Fish, pk=pk)
#         form = FishForm(instance=fish)
#         return render(request, 'fish_detail.html', {'fish': fish, 'form': form})
#
#     def post(self, request, pk):
#         # Na żądanie POST, formularz FishForm jest sprawdzany pod kątem poprawności
#         # Jeżeli formularz jest poprawny, dane z formularza są zapisywane
#         fish = get_object_or_404(Fish, pk=pk)
#         form = FishForm(request.POST, instance=fish)
#         if form.is_valid():
#             form.save()
#         return redirect('fish_detail', pk=pk)
#
# # Klasa FishDeleteView służy do usuwania istniejących instancji ryb
# class FishDeleteView(View):
#     def get(self, request, pk):
#         # Na żądanie GET, pobiera wybraną instancję modelu ryb i
#         # inicjalizuje formularz FishForm danymi dla tej instancji
#         fish = get_object_or_404(Fish, pk=pk)
#         form = FishForm(instance=fish)
#         return render(request, 'fish_delete.html', {'fish': fish, 'form': form})
#
#     def post(self, request, pk):
#         # Na żądanie POST, wybrana instancja fish jest usuwana
#         fish = get_object_or_404(Fish, pk=pk)
#         fish.delete()
#         return redirect('fishes')
#
# # Klasa CatchListView pozwala na wyświetlenie wszystkich złowionych ryb
# # (instancje modelu Catch) oraz dodanie nowych złowionych ryb za pomocą formularza CatchForm
# class CatchListView(View):
#     def get(self, request):
#         # Na żądanie GET pobiera wszystkie instancje Catch i
#         # inicjalizuje pusty formularz CatchForm
#         catches = Catch.objects.all()
#         form = CatchForm()
#         return render(request, 'catch_list.html', {'catches': catches, 'form': form})
#
#     def post(self, request):
#         # Na żądanie POST, formularz CatchForm jest sprawdzany pod kątem poprawności
#         # Jeśli formularz jest ważny, dane z formularza są zapisane
#         form = CatchForm(request.POST)
#         if form.is_valid():
#             form.save()
#         return redirect('catches')
#
# # CatchUpdateView pozwala na aktualizację istniejących rekordów złowionych ryb
# class CatchUpdateView(View):
#     def get(self, request, pk):
#         # Na żądanie GET, pobiera konkretną instancję modelu Catch i
#         # inicjalizuje formularz CatchForm danymi z tej instancji
#         catch = get_object_or_404(Catch, pk=pk)
#         form = CatchForm(instance=catch)
#         return render(request, 'catch_detail.html', {'catch': catch, 'form': form})
#
#     def post(self, request, pk):
#         # Na żądanie POST, formularz CatchForm jest sprawdzany pod kątem poprawności
#         # Jeśli formularz jest ważny, dane z formularza są zapisane
#         catch = get_object_or_404(Catch, pk=pk)
#         form = CatchForm(request.POST, instance=catch)
#         if form.is_valid():
#             form.save()
#         return redirect('catch_detail', pk=pk)
#
# # ...
#
# # Klasa CatchDeleteView służy do usuwania istniejących instancji Catch
# class CatchDeleteView(View):
#     def get(self, request, pk):
#         # Na żądanie GET, pobierana jest określona instancja modelu Catch i
#         # inicjalizowany jest formularz CatchForm danymi z tej instancji
#         catch = get_object_or_404(Catch, pk=pk)
#         form = CatchForm(instance=catch)
#         return render(request, 'catch_delete.html', {'catch': catch, 'form': form})
#
#     def post(self, request, pk):
#         # Na żądanie POST, określona instancja Catch jest usuwana
#         catch = get_object_or_404(Catch, pk=pk)
#         catch.delete()
#         return redirect('catches')
#
# class CompetitionListView(View):
#     def get(self, request):
#         # Na żądanie GET, pobiera wszystkie instancje Competition i
#         # inicjalizuje pusty formularz CompetitionForm
#         competitions = Competition.objects.all()
#         form = CompetitionForm()
#         return render(request, 'competition_list.html', {'competitions': competitions, 'form': form})
#
#     def post(self, request):
#         # Na żądanie POST, formularz CompetitionForm jest sprawdzany
#         # Jeśli formularz jest ważny, dane z formularza są zapisywane
#         form = CompetitionForm(request.POST)
#         if form.is_valid():
#             form.save()
#         return redirect('competitions')
#
#
# class CompetitionUpdateView(View):
#     def get(self, request, pk):
#         # Na żądanie GET, pobiera konkretne zawody (instancję modelu Competition) za pomocą pk i
#         # inicjalizuje formularz CompetitionForm danymi z tej konkretnej instancji
#         competition = get_object_or_404(Competition, pk=pk)
#         form = CompetitionForm(instance=competition)
#         return render(request, 'competition_detail.html', {'competition': competition, 'form': form})
#
#     def post(self, request, pk):
#         # Na żądanie POST, formularz CompetitionForm jest sprawdzany
#         # Jeśli formularz jest ważny, dane z formularza są zapisywane
#         competition = get_object_or_404(Competition, pk=pk)
#         form = CompetitionForm(request.POST, instance=competition)
#         if form.is_valid():
#             form.save()
#         return redirect('competition_detail', pk=pk)
#
#
# class CompetitionDeleteView(View):
#     def get(self, request, pk):
#         # Na żądanie GET, pobiera konkretne zawody (instancję modelu Competition) za pomocą pk i
#         # inicjalizuje formularz CompetitionForm danymi z tej konkretnej instancji
#         competition = get_object_or_404(Competition, pk=pk)
#         form = CompetitionForm(instance=competition)
#         return render(request, 'competition_delete.html', {'competition': competition, 'form': form})
#
#     def post(self, request, pk):
#         # Na żądanie POST, konkretne zawody (instancja modelu Competition) są usuwane
#         competition = get_object_or_404(Competition, pk=pk)
#         competition.delete()
#         return redirect('competitions')
#
#
# # Widok listy dla WaterBody
# class WaterBodyListView(View):
#     def get(self, request):
#         # Na żądanie GET, pobiera wszystkie instancje WaterBody i
#         # inicjalizuje pusty formularz WaterBodyForm
#         water_bodies = WaterBody.objects.all()
#         form = WaterBodyForm()
#         return render(request, 'water_body_list.html', {'water_bodies': water_bodies, 'form': form})
#
#     def post(self, request):
#         # Na żądanie POST, formularz WaterBodyForm jest sprawdzany
#         # Jeśli jest prawidłowy, dane są zapisane (tworzy WaterBody)
#         form = WaterBodyForm(request.POST)
#         if form.is_valid():
#             form.save()
#         return redirect('water_bodies')
#
#
# # Widok aktualizacji dla WaterBody
# class WaterBodyUpdateView(View):
#     def get(self, request, pk):
#         # Na żądanie GET, pobiera konkretną instancję WaterBody za pomocą pk i
#         # inicjalizuje formularz WaterBodyForm danymi z tej instancji
#         water_body = get_object_or_404(WaterBody, pk=pk)
#         form = WaterBodyForm(instance=water_body)
#         return render(request, 'water_body_detail.html', {'water_body': water_body, 'form': form})
#
#     def post(self, request, pk):
#         # Na żądanie POST, formularz WaterBodyForm jest sprawdzany
#         # Jeżeli jest prawidłowy, dane są zapisane (aktualizuje WaterBody)
#         water_body = get_object_or_404(WaterBody, pk=pk)
#         form = WaterBodyForm(request.POST, instance=water_body)
#         if form.is_valid():
#             form.save()
#         return redirect('water_body_detail', pk=pk)
#
#
# # Widok usuwania dla WaterBody
# class WaterBodyDeleteView(View):
#     def get(self, request, pk):
#         # Na żądanie GET, pobiera konkretną instancję WaterBody za pomocą pk i
#         # inicjalizuje formularz WaterBodyForm danymi z tej instancji
#         water_body = get_object_or_404(WaterBody, pk=pk)
#         form = WaterBodyForm(instance=water_body)
#         return render(request, 'water_body_delete.html', {'water_body': water_body, 'form': form})
#
#     def post(self, request, pk):
#         # Na żądanie POST, konkretna instancja WaterBody jest usuwana
#         water_body = get_object_or_404(WaterBody, pk=pk)
#         water_body.delete()
#         return redirect('water_bodies')
