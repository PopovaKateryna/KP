from time import sleep
from django.shortcuts import render
from .models import SiteInformation, Payment, UsersWork, Tax
from django.db.models import Sum
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth import authenticate, login


def main_page(request):
    site_info = SiteInformation.objects.all()
    return render(request, 'main_page.html', {'site_info': site_info.all()})


def income_page(request):
    if request.method == 'POST':
        form_info = request.POST
        site_info = SiteInformation.objects.all()
        user_ipn = form_info.get('user_ipn')

        try:
            user_work_id = UsersWork.objects.get(user_ipn=user_ipn).id
        except ObjectDoesNotExist:
            workers_info = UsersWork.objects.all()
            return render(request, 'income_page_error.html', {'site_info': site_info.all(),
                                                              'workers_info': workers_info.all()})
        else:
            payments_info = Payment.objects.filter(user_work=user_work_id)
            workers_info = UsersWork.objects.all()
            worker_fullname = Payment.objects.filter(user_work=user_work_id)[0].user_work

            working_hours_sum = {'sum': payments_info.aggregate(Sum('working_hours'))}
            taxes_sum = {'sum': payments_info.aggregate(Sum('taxes_amount'))}
            gross_income_sum = {'sum': payments_info.aggregate(Sum('gross_income'))}
            net_income_sum = {'sum': payments_info.aggregate(Sum('net_income'))}

            if len(payments_info) != 0:
                return render(request, 'income_page.html', {'site_info': site_info.all(),
                                                            'payments_info': payments_info,
                                                            'worker_fullname': worker_fullname,
                                                            'workers_info': workers_info.all(),
                                                            'sum_of_working_hours': working_hours_sum,
                                                            'sum_of_taxes': taxes_sum,
                                                            'sum_of_gross_income': gross_income_sum,
                                                            'sum_of_net_income': net_income_sum})
            else:
                sleep(2)
                return render(request, 'income_page.html', {'site_info': site_info.all(),
                                                            'payments_info': payments_info,
                                                            'workers_info': workers_info.all(),
                                                            'sum_of_working_hours': working_hours_sum,
                                                            'sum_of_taxes': taxes_sum,
                                                            'sum_of_gross_income': gross_income_sum,
                                                            'sum_of_net_income': net_income_sum})

    else:
        site_info = SiteInformation.objects.all()
        workers_info = UsersWork.objects.all()
        return render(request, 'income_page_start.html', {'site_info': site_info.all(),
                                                          'workers_info': workers_info.all()})


def contact_page(request):
    site_info = SiteInformation.objects.all()
    return render(request, 'contact_page.html', {'site_info': site_info.all()})


def accountant_authorization_page(request):
    site_info = SiteInformation.objects.all()
    workers_info = UsersWork.objects.all()

    pdfo_tax_value = Tax.objects.get(tax_name='Податок на доходи').tax_value
    social_tax_value = Tax.objects.get(tax_name='Єдиний соціальний внесок').tax_value
    military_tax_value = Tax.objects.get(tax_name='Військовий збір').tax_value

    if request.method == 'POST' and len(request.POST) == 3:
        form_info = request.POST
        username = form_info.get('username')
        password = form_info.get('password')

        user = authenticate(username=username, password=password)

        if user is not None:
            login(request, user)

            return render(request, 'accountant_page.html', {'site_info': site_info.all(),
                                                            'workers_info': workers_info.all(),
                                                            'pdfo_tax_value': pdfo_tax_value,
                                                            'social_tax_value': social_tax_value,
                                                            'military_tax_value': military_tax_value})
        else:
            return render(request, 'accountant_authorization_page_error.html', {'site_info': site_info.all()})
    elif request.method == 'POST' and len(request.POST) > 3:

        sleep(2)
        form_info = request.POST

        new_bonus_payments = form_info.get('bonus_payments')
        new_hospital_payments = form_info.get('hospital_payments')
        new_vacation_payments = form_info.get('vacation_payments')
        if new_bonus_payments == '':
            new_bonus_payments = 0
        if new_hospital_payments == '':
            new_hospital_payments = 0
        if new_vacation_payments == '':
            new_vacation_payments = 0

        try:
            new_ipn = form_info.get('user_ipn')
            new_user_work_id = workers_info.get(user_ipn=new_ipn)
            new_hourly_rate = str(workers_info.get(user_ipn=new_ipn).hourly_rate).replace('UAH', '')
            new_month_and_year = form_info.get('month_and_year') + '-01'
            new_working_hours = form_info.get('working_hours')

            new_gross_income = (float(new_working_hours) * float(new_hourly_rate) + float(new_bonus_payments)
                                + float(new_hospital_payments) + float(new_vacation_payments))

            new_pdfo_tax_id = Tax.objects.get(id=1)
            new_military_tax_id = Tax.objects.get(id=2)
            new_social_tax_id = Tax.objects.get(id=3)

            new_pdfo_tax = new_gross_income / 100 * float(pdfo_tax_value)
            new_military_tax = new_gross_income / 100 * float(military_tax_value)
            new_social_tax = new_gross_income / 100 * float(social_tax_value)
            new_taxes_amount = float(new_pdfo_tax) + float(new_military_tax) + float(new_social_tax)
            new_net_income = float(new_gross_income) - float(new_taxes_amount)

            new_salary_info = Payment(user_work=new_user_work_id,
                                      month_and_year=str(new_month_and_year),
                                      working_hours=str(new_working_hours),
                                      bonus_payments=str(new_bonus_payments),
                                      bonus_payments_currency='UAH',
                                      hospital_payments=str(new_hospital_payments),
                                      hospital_payments_currency='UAH',
                                      vacation_payments=str(new_vacation_payments),
                                      vacation_payments_currency='UAH',
                                      pdfo_tax=new_pdfo_tax_id,
                                      pdfo_tax_value=str(new_pdfo_tax),
                                      pdfo_tax_value_currency='UAH',
                                      military_tax=new_military_tax_id,
                                      military_tax_value=str(new_military_tax),
                                      military_tax_value_currency='UAH',
                                      social_tax=new_social_tax_id,
                                      social_tax_value=str(new_social_tax),
                                      social_tax_value_currency='UAH',
                                      taxes_amount=str(new_taxes_amount),
                                      taxes_amount_currency='UAH',
                                      gross_income=str(new_gross_income),
                                      gross_income_currency='UAH',
                                      net_income=str(new_net_income),
                                      net_income_currency='UAH', )

            new_salary_info.save()

            return render(request, 'accountant_page.html', {'site_info': site_info.all(),
                                                            'workers_info': workers_info.all(),
                                                            'pdfo_tax_value': pdfo_tax_value,
                                                            'social_tax_value': social_tax_value,
                                                            'military_tax_value': military_tax_value})
        except ObjectDoesNotExist:
            print('Insert error!')
            return render(request, 'accountant_page.html', {'site_info': site_info.all(),
                                                            'workers_info': workers_info.all(),
                                                            'pdfo_tax_value': pdfo_tax_value,
                                                            'social_tax_value': social_tax_value,
                                                            'military_tax_value': military_tax_value})

    return render(request, 'accountant_authorization_page.html', {'site_info': site_info.all()})


def accountant_page(request):
    site_info = SiteInformation.objects.all()
    return render(request, 'accountant_page.html', {'site_info': site_info.all()})
