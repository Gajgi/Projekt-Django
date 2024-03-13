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
from django.contrib import admin
from django.urls import path
from django.views.generic import TemplateView
from assotiation import views
from assotiation.views import CreateUserView
    #MembershipUpdateView, MembershipDeleteView,MembershipView, FishUpdateView, \
    #FishDeleteView, CatchUpdateView, CatchDeleteView, CompetitionDeleteView, CompetitionUpdateView, CompetitionListView, \
    #WaterBodyListView, WaterBodyUpdateView, WaterBodyDeleteView)
#from django.contrib.auth.views import LoginView


urlpatterns = [
    path('admin/', admin.site.urls),
    path("", TemplateView.as_view(template_name='base.html'), name="home"),
    path("create_user/", views.CreateUserView.as_view(), name="create_user"),
    path("logowanie/", views.LoginView.as_view(), name="zaloguj"),
    path("wyloguj/", views.LogoutView.as_view(), name="wyloguj"),]
#     path("membership/update/<int:pk>/", views.MembershipUpdateView.as_view(), name="membership_update"),
#     path("membership/delete/<int:pk>/", views.MembershipDeleteView.as_view(), name="membership_delete"),
#     path("memberships/", views.MembershipView.as_view(), name="memberships"),
#     path("fish/update/<int:pk>/", views.FishUpdateView.as_view(), name="fish_update"),
#     path("fish/delete/<int:pk>/", views.FishDeleteView.as_view(), name="fish_delete"),
#     path("catch/update/<int:pk>/", views.CatchUpdateView.as_view(), name="catch_update"),
#     path("catch/delete/<int:pk>/", views.CatchDeleteView.as_view(), name="catch_delete"),
#     path('competitions/', views.CompetitionListView.as_view(), name='competitions'),
#     path('competition/update/<int:pk>/', views.CompetitionUpdateView.as_view(), name='competition_update'),
#     path('competition/delete/<int:pk>/', views.CompetitionDeleteView.as_view(), name='competition_delete'),
#     path('water_bodies/', views.WaterBodyListView.as_view(), name='water_bodies'),
#     path('water_body/update/<int:pk>/', views.WaterBodyUpdateView.as_view(), name='water_body_update'),
#     path('water_body/delete/<int:pk>/', views.WaterBodyDeleteView.as_view(), name='water_body_delete'),
# ]
#
