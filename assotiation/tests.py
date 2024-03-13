from django.shortcuts import get_object_or_404
from django.test import TestCase
import pytest
from django.contrib.auth.models import User
from decimal import Decimal
from django.contrib.auth import get_user_model
from django.test import Client
from django.urls import reverse
from assotiation.models import Membership, WaterBody, Fish, Contact, InformationForAnglers
from datetime import datetime, date


# Create your tests here.


def test_create_user_get():
    client = Client()
    url = reverse('create_user')
    response = client.get(url)
    assert response.status_code == 200


def test_create_user_post_diff_password():
    client = Client()
    url = reverse('create_user')
    data = {'username': 'u', 'password1': 'abc', 'password2': 'cba'}
    response = client.post(url, data)
    assert response.status_code == 200
    assert response.context['error'] == 'Hasła są różne !!!'


@pytest.mark.django_db
def test_create_user_post():
    client = Client()
    url = reverse('create_user')
    data = {'username': 'u', 'password1': 'abc', 'password2': 'abc'}
    response = client.post(url, data)
    assert response.status_code == 302
    user = User.objects.get(username='u')
    assert response.url == reverse('memberships')
    assert user is not None


@pytest.mark.django_db
def test_login_view_get():
    client = Client()
    url = reverse('login')
    response = client.get(url)
    assert response.status_code == 200


@pytest.mark.django_db
def test_login_view_post():
    client = Client()
    user = User.objects.create_user(username='testuser', password='testpassword')
    url = reverse('login')
    data = {'username': 'testuser', 'password': 'testpassword'}
    response = client.post(url, data)
    assert response.status_code == 302


@pytest.mark.django_db
def test_login_view_post_redirect():
    User = get_user_model()
    user = User.objects.create_user(username='testuser', password='testpassword')
    assert user is not None
    client = Client()
    url = reverse('login')
    data = {'username': 'testuser', 'password': 'testpassword'}
    response = client.post(url, data)
    assert response.status_code == 302
    assert response.url == reverse('home')



@pytest.mark.django_db
def test_logout_view_get():
    client = Client()
    url = reverse('wyloguj')
    response = client.get(url)
    assert response.status_code == 302
    assert response.url == reverse('home')


# Spr. czy żądanie nie zawiera użytkownika - po wylogowaniu request.user powinno być AnonymousUser.

@pytest.mark.django_db
def test_logout_get_user_is_anonymous():
    user = User.objects.create_user('testuser', password='12345')
    client = Client()
    logged_in = client.login(username='testuser', password='12345')
    assert logged_in
    url = reverse('wyloguj')
    response = client.get(url)
    assert response.wsgi_request.user.is_anonymous


# zadamy chronionego widoku i spr. czy został przekierowany do logowania.
@pytest.mark.django_db
def test_logout_get_redirect_protected_view():
    user = User.objects.create_user('testuser', password='12345')
    client = Client()
    logged_in = client.login(username='testuser', password='12345')
    assert logged_in
    url = reverse('wyloguj')
    client.get(url)
    protected_view_url = reverse('memberships')
    response = client.get(protected_view_url)
    assert response.status_code == 302
    assert reverse('login') in response.url


@pytest.mark.django_db
def test_membership_view_get():
    client = Client()
    url = reverse('memberships')
    response = client.get(url)
    assert response.status_code == 302
    assert response.url == reverse('login') + '?next=' + reverse('memberships')#Domyślnie widok LoginRequiredMixin przekierowuje niezalogowanych użytkowników do adresu URL zdefiniowanego w ustawieniach LOGIN_URL Django, dodając parametr next ze ścieżką, do której użytkownik próbował uzyskać dostęp. Taki mechanizm jest używany w Django, aby po zalogowaniu przekierować użytkownika z powrotem na stronę, którą próbował wcześniej odwiedzić


@pytest.mark.django_db
def test_membership_view_post():
    client = Client()
    url = reverse('memberships')
    data = {'membership_data': 'xxx'}
    response = client.post(url, data)
    assert response.status_code == 302
    assert response.url == reverse('login') + '?next=' + reverse('memberships')


@pytest.mark.django_db
def test_membership_list_view_get():
    client = Client()
    url = reverse('memberships_list')
    response = client.get(url)
    assert response.status_code == 200
    # Sprawdzanie, czy szablon HTML jest używany przez widok
    assert 'members_list.html' in [template.name for template in response.templates]
    # Sprawdzanie, czy w odpowiedzi znajdują się elementy członkostw
    assert 'members' in response.context



# Spr. czy widok poprawnie przeszukuje użytkowników
@pytest.mark.django_db
def test_membership_list_view_search_valid():
    user = User.objects.create_user('testuser', password='12345')
    membership = Membership.objects.create(date=datetime.today(), fee=100.0, angler=user)
    client = Client()
    url = reverse('memberships_list')
    response = client.get(url, {'search': 'testuser'})
    assert response.status_code == 200
    assert len(response.context['members']) == 1
    assert response.context['members'][0] == membership


# Spr.czy widok poprawnie obsługuje puste zapytanie wyszukiwania.
@pytest.mark.django_db
def test_membership_list_view_search_empty():
    client = Client()
    url = reverse('memberships_list')
    response = client.get(url)
    assert response.status_code == 200
    assert len(response.context['members']) == Membership.objects.count()


# Spr. czy widok działa poprawnie, gdy zapytanie wyszukiwania nie zwraca wyników.
@pytest.mark.django_db
def test_membership_list_view_search_no_results():
    user = User.objects.create_user('testuser', password='12345')
    membership = Membership.objects.create(date=datetime.today(), fee=100.0, angler=user)
    client = Client()
    url = reverse('memberships_list')
    response = client.get(url, {'search': 'not_exist'})
    assert response.status_code == 200
    assert len(response.context['members']) == 0


@pytest.mark.django_db
def test_membership_update_view_get():
    client = Client()
    user = get_user_model().objects.create_user(username='testuser', password='12345')
    membership = Membership.objects.create(date=datetime.now(), fee=Decimal('100'), angler=user)
    url = reverse('membership_update', kwargs={'pk': membership.pk})
    response = client.get(url)
    assert response.status_code == 302



@pytest.mark.django_db
def test_membership_exists():
    user = get_user_model().objects.create_user(username='testuser', password='12345')
    membership = Membership.objects.create(date=datetime.now(), fee=Decimal('100'), angler=user)
    assert Membership.objects.filter(pk=membership.pk).exists()


@pytest.mark.django_db
def test_membership_delete_view_get():
    client = Client()
    user = get_user_model().objects.create_user(username='testuser', password='12345')
    client.login(username='testuser', password='12345')  # zalogowanie użytkownika
    membership = Membership.objects.create(date=datetime.now(), fee=Decimal('100'), angler=user)
    url = reverse('membership_delete', kwargs={'pk': membership.pk})
    response = client.get(url)
    assert response.status_code == 200
    assert 'membership_delete.html' in [template.name for template in response.templates]


@pytest.mark.django_db
def test_membership_delete_view_post():
    client = Client()
    user = get_user_model().objects.create_user(username='testuser', password='12345')
    client.login(username='testuser', password='12345')  # zalogowanie użytkownika
    membership = Membership.objects.create(date=datetime.now(), fee=Decimal('100'), angler=user)
    url = reverse('membership_delete', kwargs={'pk': membership.pk})
    response = client.post(url, data={'delete': 'tak'})
    assert response.status_code == 302
    if Membership.objects.filter(pk=membership.pk).exists():
        assert False, "Członkowstow nadal istnieje po usunieciu widoku"


@pytest.mark.django_db
def test_fish_list_view_get():
    client = Client()
    url = reverse('fish_list')
    response = client.get(url)
    assert response.status_code == 200
    assert response.templates[0].name == 'fish_list.html'#Na koniec sprawdzamy, czy pierwszy szablon użyty do wyrenderowania odpowiedzi to fish_list.html. W Django, lista użytych szablonów jest dostępna jako response.templates. W tym przypadku bierzemy pierwszy szablon z listy za pomocą response.templates[0] i porównujemy jego nazwę z oczekiwanym szablonem.


@pytest.mark.django_db
def test_fish_list_view_post():
    client = Client()
    url = reverse('fish_list')
    data = {'fish_type': 'salmon'}
    response = client.post(url, data)
    assert response.status_code == 302
    assert response.url == reverse('fish_list')


@pytest.mark.django_db
def test_fish_create_view_get():
    client = Client()
    url = reverse('fish_list')
    response = client.get(url)
    assert response.status_code == 200
    assert response.context['form']


# Test sprawdzający, czy nowa ryba jest poprawnie dodawana
@pytest.mark.django_db
def test_fish_create_view_post():
    client = Client()
    url = reverse('fish_list')  #
    water_body = WaterBody.objects.create(name='Kanalek', location='Kolo')
    response = client.post(url, {'name': 'sum', 'max_weight': 2.2, })
    assert response.status_code == 302
    fish = Fish.objects.last()
    assert fish.name == 'sum'
    assert fish.max_weight == 2.2


@pytest.mark.django_db
def test_catch_list_view_get():
    client = Client()
    url = reverse('catch_list')
    response = client.get(url)
    assert response.status_code == 200
    assert response.context['form']


@pytest.mark.django_db
def test_catch_list_view_post():
    client = Client()
    url = reverse('catch_list')
    response = {'fish_type': 'salmon'}
    assert client.post(url, response).status_code == 302

@pytest.mark.django_db
def test_catch_list_view_redirect_after_succes_add():
    client = Client()
    user = get_user_model().objects.create_user(username='testuser', password='12345')
    fish = Fish.objects.create(name='Salmon', max_weight=10.0)
    url = reverse('catch_list')
    response = client.post(url, {'angler': user.id, 'fish': fish.id, 'weight': 2.5, 'date': date.today()})
    assert response.status_code == 302
    assert response.url == reverse('catch_list')



@pytest.mark.django_db
def test_CompetitionListView_get():
    client = Client()
    url = reverse('competitions')
    response = client.get(url)
    assert response.status_code == 200
    assert response.context['form']


@pytest.mark.django_db
def test_CompetitionListView_post():
    client = Client()
    url = reverse('competitions')
    data = {'name': 'competition_name', 'date': '2022-01-01'}
    response = client.post(url, data)
    assert response.status_code == 302
    assert response.url == reverse('competitions')


@pytest.mark.django_db
def test_WaterBodyListView_get():
    client = Client()
    url = reverse('water_bodies')
    response = client.get(url)
    assert response.status_code == 200
    assert response.context['form']


@pytest.mark.django_db
def test_WaterBodyListView_post():
    client = Client()
    url = reverse('water_bodies')
    data = {'name': 'water_body_name'}
    response = client.post(url, data)
    assert response.status_code == 302
    assert response.url == reverse('water_bodies')

@pytest.mark.django_db
def test_water_body_update_view_get():# to jest loginreqaremixin wiec na meytodzie get jest 302 a nie 200
    client = Client()
    water_body = WaterBody.objects.create(name='water_body_name', location='location')
    # Tworzymy obiekt WaterBody bezpośrednio, bez przypisywania gatunków ryb
    fish_species = Fish.objects.create(name='fish_species', max_weight=0.5)
    water_body.fish_species.add(fish_species)
    # Przypisujemy gatunek ryby do obiektu WaterBody za pomocą metody add()
    url = reverse('water_bodies_update', kwargs={'pk': water_body.pk})
    response = client.get(url)
    assert response.status_code == 302


@pytest.mark.django_db
def test_water_body_update_view_post():
    user = User.objects.create(username='test_user')
    water_body = WaterBody.objects.create(name='test', location='testowa')
    client = Client()
    updated_name = 'test'
    updated_location = 'testowa'
    post_data = {'name': updated_name,'location': updated_location}
    url = reverse('water_bodies_update', kwargs={'pk': water_body.pk})
    response = client.post(url, post_data)
    assert response.status_code == 302
    updated_water_body = get_object_or_404(WaterBody, pk=water_body.pk)
    assert updated_water_body.name == updated_name
    assert updated_water_body.location == updated_location


@pytest.mark.django_db
def test_information_for_anglers_list_view_get():
    client = Client()
    url = reverse('informations_list')
    response = client.get(url)
    assert response.status_code == 200
    assert len(response.context['informations']) == InformationForAnglers.objects.count()# ???? widok spr. czy liczba "informacji" zwracanych przez widok jest taka sama jak liczba obiektów InformationForAnglers w bazie danych.InformationForAnglers.objects.count() zwraca liczbę obiektów InformationForAnglers w bazie danych.Jeśli te dwie wartości są równe, oznacza to, że wszystkie obiekty InformationForAnglers są poprawnie zwracane przez widok i wyświetlane na stronie. Jest to przydatne do sprawdzania, czy widok poprawnie łączy się z bazą danych i zwraca oczekiwane informacje.Powiedziane innymi słowy, ten test sprawdza, czy strona ładowania jest właściwa (status_code == 200) oraz czy wszystkie obiekty InformationForAnglers są prezentowane na stronie.

@pytest.mark.django_db
def test_information_for_anglers_list_view_get_all_informations():
    InformationForAnglers.objects.create(title='info1', content='content1', PZW_fees=100.00)
    InformationForAnglers.objects.create(title='info2', content='content2', PZW_fees=200.00)
    client = Client()
    url = reverse('informations_list')
    response = client.get(url)
    assert len(response.context['informations']) == 2
    assert response.status_code == 200


@pytest.mark.django_db
def test_contact_list_view_get():
    client = Client()
    url = reverse('contact_list')
    response = client.get(url)
    assert response.status_code == 200

@pytest.mark.django_db
def test_contact_list_view_get_all_contacts():
    Contact.objects.create(address='address1', phone_number='123456', email='test1@.com')
    Contact.objects.create(address='address2', phone_number='456789', email='test2@.com')
    client = Client()
    url = reverse('contact_list')
    response = client.get(url)
    assert len(response.context['contacts']) == 2
    assert response.status_code == 200





@pytest.mark.django_db
def test_information_for_anglers_list_view_get_all_informations():
    InformationForAnglers.objects.create(title='info1', content='content1', PZW_fees=100.00)
    InformationForAnglers.objects.create(title='info2', content='content2', PZW_fees=200.00)
    client = Client()
    url = reverse('informations_list')
    response = client.get(url)
    assert len(response.context['informations']) == 2
    assert response.status_code == 200


@pytest.mark.django_db
def test_contact_list_view_get_all_contacts():
    Contact.objects.create(address='address1', phone_number='123456', email='test1@.com')
    Contact.objects.create(address='address2', phone_number='456789', email='test2@.com')
    client = Client()
    url = reverse('contact_list')
    response = client.get(url)
    assert len(response.context['contacts']) == 2
    assert response.status_code == 200
