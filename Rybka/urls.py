"""
URL configuration for ProjektKoncowy project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from django.views.generic import TemplateView

from assotiation import views

#MembershipUpdateView, MembershipDeleteView,MembershipView, FishUpdateView, \
    #FishDeleteView, CatchUpdateView, CatchDeleteView, CompetitionDeleteView, CompetitionUpdateView, CompetitionListView, \WaterBodyListView, WaterBodyUpdateView, WaterBodyDeleteView)


urlpatterns = [
    path('admin/', admin.site.urls),
    path("", TemplateView.as_view(template_name='base.html'), name="home"),
    path("create_user/", views.CreateUserView.as_view(), name="create_user"),
    path("logowanie/", views.LoginView.as_view(), name="login"),
    path("wyloguj/", views.LogoutView.as_view(), name="wyloguj"),
    path("memberships/", views.MembershipView.as_view(), name="memberships"),
    path("membership/update/<int:pk>/", views.MembershipUpdateView.as_view(), name="membership_update"),
    path("memberships/list/", views.MembershipListView.as_view(), name="memberships_list"),
    path("membership/delete/<int:pk>/", views.MembershipDeleteView.as_view(), name="membership_delete"),
    path("fish/list/", views.FishListView.as_view(), name="fish_list"),
    path("catch/list/", views.CatchListView.as_view(), name="catch_list"),
    path('competitions/', views.CompetitionListView.as_view(), name='competitions'),
    path('water_bodies/', views.WaterBodyListView.as_view(), name='water_bodies'),
    path("water_bodies/update/<int:pk>/", views.WaterBodyUpdateView.as_view(), name="water_bodies_update"),
    path('informations_list/', views.InformationForAnglersListView.as_view(), name='informations_list'),
    path('contacts_list/', views.ContactListView.as_view(), name='contact_list')
]

