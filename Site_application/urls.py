from django.urls import path
from .views import main_page, income_page, contact_page, accountant_authorization_page, accountant_page

urlpatterns = [
    path('', main_page),
    path('income', income_page),
    path('contacts', contact_page),
    path('authorization', accountant_authorization_page),
    path('accounting', accountant_page)
]
