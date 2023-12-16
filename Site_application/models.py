from decimal import Decimal
from django.db import models
from django.contrib.auth.models import User
from phonenumber_field.modelfields import PhoneNumberField
from djmoney.models.fields import MoneyField
from django.core.validators import MinValueValidator, MaxValueValidator

PERCENTAGE_VALIDATOR = [MinValueValidator(0), MaxValueValidator(100)]


class SiteInformation(models.Model):
    """Інформація про вебсайт"""
    site_name = models.CharField(max_length=150)
    site_landline_phone_number = PhoneNumberField(null=True, blank=True, unique=True)
    site_phone_number_1 = PhoneNumberField(null=True, blank=True, unique=True)
    site_phone_number_2 = PhoneNumberField(null=True, blank=True, unique=True)
    site_email = models.EmailField(max_length=100, null=True, blank=True, unique=True)
    address = models.CharField(max_length=100)
    working_days_schedule = models.CharField(max_length=30)
    saturday_schedule = models.CharField(max_length=30)
    sunday_schedule = models.CharField(max_length=30)

    class Meta:
        db_table = 'site_information'
        ordering = ['site_name']
        managed = True
        verbose_name = 'Site information'
        verbose_name_plural = 'Site information'

    def __str__(self):
        return f'{str(self.site_name)}'


class Company(models.Model):
    """Інформація про компанії"""
    company_name = models.CharField(max_length=200)
    site = models.ForeignKey(SiteInformation, on_delete=models.CASCADE, related_name="CompaniesInfo")

    class Meta:
        db_table = 'companies'
        ordering = ['company_name']
        managed = True
        verbose_name = 'Companies information'
        verbose_name_plural = 'Companies information'

    def __str__(self):
        return f'{str(self.company_name)}'


class Tax(models.Model):
    """Інформація про податки"""
    tax_name = models.CharField(max_length=100)
    tax_value = models.DecimalField(max_digits=3, decimal_places=0, default=Decimal(0), validators=PERCENTAGE_VALIDATOR)
    site = models.ForeignKey(SiteInformation, on_delete=models.CASCADE, related_name="TaxesInfo")

    class Meta:
        db_table = 'taxes'
        ordering = ['tax_name']
        managed = True
        verbose_name = 'Taxes'
        verbose_name_plural = 'Taxes'

    def __str__(self):
        return f'{str(self.tax_name)}'


class UsersWork(models.Model):
    """Інформація про працівників та їх роботу (компанію та ставку)"""
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='UserProfile_Work')
    user_patronymic = models.CharField(max_length=150)
    user_id_card_number = models.CharField(max_length=9)
    user_ipn = models.CharField(max_length=10)
    company = models.ForeignKey(Company, on_delete=models.CASCADE, related_name="UserInfo")
    hourly_rate = MoneyField(max_digits=6, decimal_places=2)

    class Meta:
        db_table = 'users_work'
        ordering = ['user']
        managed = True
        verbose_name = 'Users work'
        verbose_name_plural = 'Users work'

    def __str__(self):
        return f'{str(self.user.last_name)} {str(self.user.first_name)} {str(self.user_patronymic)}'


class Payment(models.Model):
    """Інформація про кількість відпрацьованих працівником годин (за місяць), премії, лікарняні та відпускні"""
    user_work = models.ForeignKey(UsersWork, on_delete=models.CASCADE, related_name='UserWork_Payments')
    month_and_year = models.DateField()
    working_hours = models.IntegerField()
    bonus_payments = MoneyField(max_digits=8, decimal_places=2)
    hospital_payments = MoneyField(max_digits=8, decimal_places=2)
    vacation_payments = MoneyField(max_digits=8, decimal_places=2)
    pdfo_tax = models.ForeignKey(Tax, on_delete=models.CASCADE, related_name='PFDO_Tax')
    pdfo_tax_value = MoneyField(max_digits=8, decimal_places=2)
    military_tax = models.ForeignKey(Tax, on_delete=models.CASCADE, related_name='Military_Tax')
    military_tax_value = MoneyField(max_digits=8, decimal_places=2)
    social_tax = models.ForeignKey(Tax, on_delete=models.CASCADE, related_name='Social_Tax')
    social_tax_value = MoneyField(max_digits=8, decimal_places=2)
    taxes_amount = MoneyField(max_digits=8, decimal_places=2)
    gross_income = MoneyField(max_digits=8, decimal_places=2)
    net_income = MoneyField(max_digits=8, decimal_places=2)

    class Meta:
        db_table = 'payments'
        ordering = ['user_work']
        managed = True
        verbose_name = 'Payments'
        verbose_name_plural = 'Payments'

    def __str__(self):
        return (f'{str(self.month_and_year)} {str(self.user_work.user.last_name)} '
                f' {str(self.user_work.user.first_name)} {str(self.user_work.user_patronymic)}')
