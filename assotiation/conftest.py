import pytest
from django.contrib.auth.models import User

@pytest.fixture
def uzytkownik():
    user = User.objects.create_user(username='testuser', password='testpassword')
    return user