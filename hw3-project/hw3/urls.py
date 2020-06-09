from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('monte_carlo_simulation', views.monte_carlo_simulation, name='monte_carlo_simulation'),
]
