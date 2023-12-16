"""Script for project initialization, need to run only once when creating a project.
Script create a database, superuser and insert test data in db tables."""

import os
import django
from time import sleep
from colorama import Fore
from mysql.connector import connect
from mysql.connector.errors import Error, ProgrammingError

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Site_project.settings')
django.setup()

DB_CREATION_CONNECT = connect(host='127.0.0.1',
                              port='3306',
                              user='root',
                              passwd='1111')

DB_ALREADY_EXIST_CONNECT = connect(host='127.0.0.1',
                                   port='3306',
                                   user='root',
                                   passwd='1111',
                                   database='Payroll_Automation_System_DB')

DB_CREATION_CURSOR = DB_CREATION_CONNECT.cursor(buffered=True)

DB_ALREADY_EXIST_CURSOR = DB_ALREADY_EXIST_CONNECT.cursor(buffered=True)


def database_creations():
    """Function for creating a database Payroll_Automation_System_DB"""
    try:
        DB_CREATION_CURSOR.execute("CREATE DATABASE Payroll_Automation_System_DB")
    except Error:
        print(Fore.RED + f"Database already exists!\n" + Fore.YELLOW)

        DB_CREATION_CURSOR.execute("DROP DATABASE Payroll_Automation_System_DB")
        print(Fore.GREEN + "Database successfully deleted!\n" + Fore.YELLOW)
        sleep(1)

        DB_CREATION_CURSOR.execute("CREATE DATABASE Payroll_Automation_System_DB")
        print(Fore.GREEN + "Database Payroll_Automation_System_DB has been created!\n" + Fore.YELLOW)
    else:
        print(Fore.GREEN + "Database Payroll_Automation_System_DB has been created!\n" + Fore.YELLOW)


def database_migrations():
    """Carrying out database migrations"""
    files_list = os.listdir('Site_application/migrations')

    for file in files_list:
        if file != '__init__.py' and file != '__pycache__':
            os.remove(f'Site_application/migrations/{file}')
            print(Fore.CYAN + f'File {file} has been removed!' + Fore.YELLOW)
            sleep(0.5)
    print()

    os.system('python manage.py makemigrations')
    print(Fore.GREEN + f"\nMigration file created!\n" + Fore.BLUE)
    sleep(1)

    os.system('python manage.py migrate')
    print(Fore.GREEN + f"\nMigration successfully applied!\n")


def superuser_creations():
    """Function for creating an admin-superuser with login parameters:
    'username': 'admin',
    'password': '1111'"""

    from django.contrib.auth.models import User
    from django.db.utils import IntegrityError, ProgrammingError

    superuser_info = {'username': 'admin',
                      'password': '1111',
                      'user_type': 'Admin',
                      'email': 'admin@gmail.ua'}

    try:
        User.objects.create_user(username=superuser_info.get('username'),
                                 password=superuser_info.get('password'),
                                 email=superuser_info.get('email'),
                                 is_active=True,
                                 is_staff=True,
                                 is_superuser=True)

    except IntegrityError:
        print(Fore.RED + f"Username `{superuser_info.get('username')}` already exist!\n")
    except ProgrammingError:
        print(Fore.RED + f"Problem with database! Maybe it doesn't exist.\n")
    else:
        print(Fore.GREEN + f"Superuser profile `{superuser_info.get('username')}` has been created!\n")


def accountants_creations():
    """Function for creating an accountants with login parameters:
    accountant 1
    'username': 'accountant_1',
    'password': '1111'
    accountant 2
    'username': 'accountant_2',
    'password': '1111'"""

    from django.contrib.auth.models import User
    from django.db.utils import IntegrityError, ProgrammingError

    accountants_info = [{'username': 'accountant_1',
                         'first_name': 'Людмила',
                         'last_name': 'Федина',
                         'password': '2222',
                         'user_type': 'Accountant',
                         'email': 'accountant_1@gmail.ua',
                         'patronymic': None},
                        {'username': 'accountant_2',
                         'first_name': 'Вероніка',
                         'last_name': 'Балан',
                         'password': '3333',
                         'user_type': 'Accountant',
                         'email': 'accountant_2@gmail.ua',
                         'patronymic': None}]

    for accountant in accountants_info:
        try:
            User.objects.create_user(username=accountant.get('username'),
                                     first_name=accountant.get('first_name'),
                                     last_name=accountant.get('last_name'),
                                     password=accountant.get('password'),
                                     email=accountant.get('email'),
                                     is_active=True,
                                     is_staff=True,
                                     is_superuser=False)

        except IntegrityError:
            print(Fore.RED + f"Username `{accountant.get('username')}` already exist!\n")
        except ProgrammingError:
            print(Fore.RED + f"Problem with database! Maybe it doesn't exist.\n")
        else:
            print(Fore.GREEN + f"Accountant profile `{accountant.get('username')}` has been created!\n")


def insert_data():
    """Inserting data into database tables"""
    from django.contrib.auth.models import User

    site_info = {'site_name': 'Інформаційна система автоматизації нарахування заробітної плати',
                 'site_landline_phone_number': '+380344696042',
                 'site_phone_number_1': '+380986543234',
                 'site_phone_number_2': '+380685023453',
                 'site_email': 'PayrolSystemLviv@gmail.com',
                 'address': 'Львів, вул. Івана Франка, 11',
                 'working_days_schedule': 'пн-пт: 10:00-19:00;',
                 'saturday_schedule': 'сб: 10:00-18:00;',
                 'sunday_schedule': 'нд: вихідний'}

    companies_info = [{'company_name': 'Ligos', 'site': '1'},
                      {'company_name': 'Епіцентр', 'site': '1'},
                      {'company_name': 'Сільпо', 'site': '1'}]

    taxes_info = [{'tax_name': 'Податок на доходи', 'tax_value': '18', 'site': '1'},
                  {'tax_name': 'Військовий збір', 'tax_value': '1.5', 'site': '1'},
                  {'tax_name': 'Єдиний соціальний внесок', 'tax_value': '10', 'site': '1'}]

    workers_info = [
        {'user_id': '4',
         'username': 'ValMik',
         'password': 'p2111112p',
         'email': 'ValMik@gmail.ua',
         'first_name': 'Валерій',
         'last_name': 'Грикуляк',
         'patronymic': 'Миколайович',
         'user_id_card_number': '000058374',
         'user_ipn': '4749238427',
         'company_id': '1',
         'hourly_rate': '80'},
        {'user_id': '5',
         'username': 'VolVin',
         'password': 'p2111112p',
         'email': 'VolVin@gmail.ua',
         'first_name': 'Володимир',
         'last_name': 'Винниченко',
         'patronymic': 'Григорович',
         'user_id_card_number': '000085393',
         'user_ipn': '9405734895',
         'company_id': '1',
         'hourly_rate': '120'},
        {'user_id': '6',
         'username': 'MikhVol',
         'password': 'p2111112p',
         'email': 'MikhVol@gmail.ua',
         'first_name': 'Михайло',
         'last_name': 'Волошин',
         'patronymic': 'Петрович',
         'user_id_card_number': '000056352',
         'user_ipn': '4852097461',
         'company_id': '1',
         'hourly_rate': '115'},
        {'user_id': '7',
         'username': 'AnaMax',
         'password': 'p2111112p',
         'email': 'AnaMax@gmail.ua',
         'first_name': 'Анатолій',
         'last_name': 'Максимів',
         'patronymic': 'Вікторович',
         'user_id_card_number': '000023796',
         'user_ipn': '5973619603',
         'company_id': '2',
         'hourly_rate': '94'},
        {'user_id': '8',
         'username': 'VikPet',
         'password': 'p2111112p',
         'email': 'VikPet@gmail.ua',
         'first_name': 'Вікторія',
         'last_name': 'Петришин',
         'patronymic': 'Василівна',
         'user_id_card_number': '000012386',
         'user_ipn': '1529524949',
         'company_id': '2',
         'hourly_rate': '88'},
        {'user_id': '9',
         'username': 'VikSlo',
         'password': 'p2111112p',
         'email': 'VikSlo@gmail.ua',
         'first_name': 'Віктор',
         'last_name': 'Слобудяк',
         'patronymic': 'Андрійович',
         'user_id_card_number': '000083701',
         'user_ipn': '1970272859',
         'company_id': '2',
         'hourly_rate': '144'},
        {'user_id': '10',
         'username': 'PanSht',
         'password': 'p2111112p',
         'email': 'PanSht@gmail.ua',
         'first_name': 'Панас',
         'last_name': 'Штефурак',
         'patronymic': 'Романович',
         'user_id_card_number': '000038261',
         'user_ipn': '1352852242',
         'company_id': '3',
         'hourly_rate': '102'},
        {'user_id': '11',
         'username': 'SolPan',
         'password': 'p2111112p',
         'email': 'SolPan@gmail.ua',
         'first_name': 'Соломія',
         'last_name': 'Паньків',
         'patronymic': 'Володимирівна',
         'user_id_card_number': '000087644',
         'user_ipn': '5395339920',
         'company_id': '3',
         'hourly_rate': '89'},
        {'user_id': '12',
         'username': 'YarAnt',
         'password': 'p2111112p',
         'email': 'YarAnt@gmail.ua',
         'first_name': 'Ярема',
         'last_name': 'Антонів',
         'patronymic': 'Сергійович',
         'user_id_card_number': '000012903',
         'user_ipn': '9582592686',
         'company_id': '3',
         'hourly_rate': '117'},
        {'user_id': '13',
         'username': 'ArtMal',
         'password': 'p2111112p',
         'email': 'ArtMal@gmail.ua',
         'first_name': 'Артур',
         'last_name': 'Маланюк',
         'patronymic': 'Генадійович',
         'user_id_card_number': '000038291',
         'user_ipn': '4248582815',
         'company_id': '3',
         'hourly_rate': '75'}
    ]

    currency_info = {'currency_name': 'UAH'}

    payments_info = [
        {'user_work': '1',
         'working_hours': '450',
         'month_and_year': '2023-01-30',
         'bonus_payments': '400',
         'hospital_payments': '220',
         'vacation_payments': '445',
         'pdfo_tax': '6671.7',
         'military_tax': '556.0',
         'social_tax': '3706.5',
         'taxes_amount': '10934.2',
         'gross_income': '37065.0',
         'net_income': '26130.8'},

        {'user_work': '1',
         'working_hours': '230',
         'month_and_year': '2023-02-28',
         'bonus_payments': '100',
         'hospital_payments': '0',
         'vacation_payments': '0',
         'pdfo_tax': '3330.0',
         'military_tax': '277.5',
         'social_tax': '1850.0',
         'taxes_amount': '5457.5',
         'gross_income': '18500.0',
         'net_income': '13042.5'},

        {'user_work': '1',
         'working_hours': '330',
         'month_and_year': '2023-03-30',
         'bonus_payments': '40',
         'hospital_payments': '200',
         'vacation_payments': '0',
         'pdfo_tax': '4795.2',
         'military_tax': '399.6',
         'social_tax': '2664.0',
         'taxes_amount': '7858.8',
         'gross_income': '26640.0',
         'net_income': '18781.2'},

        {'user_work': '2',
         'working_hours': '400',
         'month_and_year': '2023-01-30',
         'bonus_payments': '1200',
         'hospital_payments': '0',
         'vacation_payments': '300',
         'pdfo_tax': '8910.0',
         'military_tax': '742.5',
         'social_tax': '4950.0',
         'taxes_amount': '14602.5',
         'gross_income': '49500.0',
         'net_income': '34897.5'},

        {'user_work': '2',
         'working_hours': '246',
         'month_and_year': '2023-02-28',
         'bonus_payments': '390',
         'hospital_payments': '4450',
         'vacation_payments': '0',
         'pdfo_tax': '6184.8',
         'military_tax': '515.4',
         'social_tax': '3436.0',
         'taxes_amount': '10136.2',
         'gross_income': '34360.0',
         'net_income': '24223.8'},

        {'user_work': '3',
         'working_hours': '200',
         'month_and_year': '2023-01-30',
         'bonus_payments': '2500',
         'hospital_payments': '0',
         'vacation_payments': '0',
         'pdfo_tax': '4590.0',
         'military_tax': '382.5',
         'social_tax': '2550.0',
         'taxes_amount': '7522.5',
         'gross_income': '25500.0',
         'net_income': '17977.5'},

        {'user_work': '3',
         'working_hours': '286',
         'month_and_year': '2023-02-28',
         'bonus_payments': '0',
         'hospital_payments': '500',
         'vacation_payments': '260',
         'pdfo_tax': '6057.0',
         'military_tax': '504.8',
         'social_tax': '3365.0',
         'taxes_amount': '9926.8',
         'gross_income': '33650.0',
         'net_income': '23723.2'},

        {'user_work': '3',
         'working_hours': '145',
         'month_and_year': '2023-03-30',
         'bonus_payments': '500',
         'hospital_payments': '0',
         'vacation_payments': '2000',
         'pdfo_tax': '3451.5',
         'military_tax': '287.6',
         'social_tax': '1917.5',
         'taxes_amount': '5656.6',
         'gross_income': '19175.0',
         'net_income': '13518.4'},

        {'user_work': '3',
         'working_hours': '376',
         'month_and_year': '2023-04-30',
         'bonus_payments': '600',
         'hospital_payments': '1260',
         'vacation_payments': '0',
         'pdfo_tax': '8118.0',
         'military_tax': '676.5',
         'social_tax': '4510.0',
         'taxes_amount': '13304.5',
         'gross_income': '45100.0',
         'net_income': '31795.5'},

        {'user_work': '4',
         'working_hours': '200',
         'month_and_year': '2023-01-30',
         'bonus_payments': '200',
         'hospital_payments': '0',
         'vacation_payments': '1200',
         'pdfo_tax': '3636.0',
         'military_tax': '303.0',
         'social_tax': '2020.0',
         'taxes_amount': '5959.0',
         'gross_income': '20200.0',
         'net_income': '14241.0'},

        {'user_work': '4',
         'working_hours': '340',
         'month_and_year': '2023-02-28',
         'bonus_payments': '500',
         'hospital_payments': '0',
         'vacation_payments': '0',
         'pdfo_tax': '5842.8',
         'military_tax': '486.9',
         'social_tax': '3246.0',
         'taxes_amount': '9575.7',
         'gross_income': '32460.0',
         'net_income': '22884.3'},

        {'user_work': '4',
         'working_hours': '170',
         'month_and_year': '2023-03-30',
         'bonus_payments': '600',
         'hospital_payments': '1300',
         'vacation_payments': '0',
         'pdfo_tax': '3218.4',
         'military_tax': '268.2',
         'social_tax': '1788.0',
         'taxes_amount': '5274.6',
         'gross_income': '17880.0',
         'net_income': '12605.4'},

        {'user_work': '4',
         'working_hours': '110',
         'month_and_year': '2023-04-30',
         'bonus_payments': '1000',
         'hospital_payments': '0',
         'vacation_payments': '400',
         'pdfo_tax': '2113.2',
         'military_tax': '176.1',
         'social_tax': '1174.0',
         'taxes_amount': '3463.3',
         'gross_income': '11740.0',
         'net_income': '8276.7'},

        {'user_work': '5',
         'working_hours': '290',
         'month_and_year': '2023-01-30',
         'bonus_payments': '0',
         'hospital_payments': '3000',
         'vacation_payments': '2000',
         'pdfo_tax': '5493.6',
         'military_tax': '457.8',
         'social_tax': '3052.0',
         'taxes_amount': '9003.4',
         'gross_income': '30520.0',
         'net_income': '21516.6'},

        {'user_work': '5',
         'working_hours': '300',
         'month_and_year': '2023-02-28',
         'bonus_payments': '1200',
         'hospital_payments': '0',
         'vacation_payments': '0',
         'pdfo_tax': '4968.0',
         'military_tax': '414.0',
         'social_tax': '2760.0',
         'taxes_amount': '8142.0',
         'gross_income': '27600.0',
         'net_income': '19458.0'},

        {'user_work': '5',
         'working_hours': '200',
         'month_and_year': '2023-03-30',
         'bonus_payments': '1000',
         'hospital_payments': '0',
         'vacation_payments': '300',
         'pdfo_tax': '3402.0',
         'military_tax': '283.5',
         'social_tax': '1890.0',
         'taxes_amount': '5575.5',
         'gross_income': '18900.0',
         'net_income': '13324.5'},

        {'user_work': '5',
         'working_hours': '280',
         'month_and_year': '2023-04-30',
         'bonus_payments': '400',
         'hospital_payments': '2000',
         'vacation_payments': '1300',
         'pdfo_tax': '5101.2',
         'military_tax': '425.1',
         'social_tax': '2834.0',
         'taxes_amount': '8360.3',
         'gross_income': '28340.0',
         'net_income': '19979.7'},

        {'user_work': '5',
         'working_hours': '300',
         'month_and_year': '2023-05-30',
         'bonus_payments': '600',
         'hospital_payments': '0',
         'vacation_payments': '1300',
         'pdfo_tax': '5094.0',
         'military_tax': '424.5',
         'social_tax': '2830.0',
         'taxes_amount': '8348.5',
         'gross_income': '28300.0',
         'net_income': '19951.5'},

        {'user_work': '6',
         'working_hours': '100',
         'month_and_year': '2023-01-30',
         'bonus_payments': '300',
         'hospital_payments': '0',
         'vacation_payments': '2000',
         'pdfo_tax': '3006.0',
         'military_tax': '250.5',
         'social_tax': '1670.0',
         'taxes_amount': '4926.5',
         'gross_income': '16700.0',
         'net_income': '11773.5'},

        {'user_work': '6',
         'working_hours': '250',
         'month_and_year': '2023-02-28',
         'bonus_payments': '3000',
         'hospital_payments': '0',
         'vacation_payments': '0',
         'pdfo_tax': '7020.0',
         'military_tax': '585.0',
         'social_tax': '3900.0',
         'taxes_amount': '11505.0',
         'gross_income': '39000.0',
         'net_income': '27495.0'},

        {'user_work': '6',
         'working_hours': '180',
         'month_and_year': '2023-03-30',
         'bonus_payments': '0',
         'hospital_payments': '1200',
         'vacation_payments': '600',
         'pdfo_tax': '4989.6',
         'military_tax': '415.8',
         'social_tax': '2772.0',
         'taxes_amount': '8177.4',
         'gross_income': '27720.0',
         'net_income': '19542.6'},

        {'user_work': '6',
         'working_hours': '200',
         'month_and_year': '2023-04-30',
         'bonus_payments': '760',
         'hospital_payments': '0',
         'vacation_payments': '350',
         'pdfo_tax': '5383.8',
         'military_tax': '448.7',
         'social_tax': '2991.0',
         'taxes_amount': '8823.5',
         'gross_income': '29910.0',
         'net_income': '21086.5'},

        {'user_work': '7',
         'working_hours': '200',
         'month_and_year': '2023-01-30',
         'bonus_payments': '600',
         'hospital_payments': '0',
         'vacation_payments': '0',
         'pdfo_tax': '3780.0',
         'military_tax': '315.0',
         'social_tax': '2100.0',
         'taxes_amount': '6195.0',
         'gross_income': '21000.0',
         'net_income': '14805.0'},

        {'user_work': '7',
         'working_hours': '306',
         'month_and_year': '2023-02-28',
         'bonus_payments': '0',
         'hospital_payments': '390',
         'vacation_payments': '1200',
         'pdfo_tax': '5904.4',
         'military_tax': '492.0',
         'social_tax': '3280.2',
         'taxes_amount': '9676.6',
         'gross_income': '32802.0',
         'net_income': '23125.4'},

        {'user_work': '7',
         'working_hours': '300',
         'month_and_year': '2023-03-30',
         'bonus_payments': '300',
         'hospital_payments': '0',
         'vacation_payments': '0',
         'pdfo_tax': '5562.0',
         'military_tax': '463.5',
         'social_tax': '3090.0',
         'taxes_amount': '9115.5',
         'gross_income': '30900.0',
         'net_income': '21784.5'},

        {'user_work': '7',
         'working_hours': '100',
         'month_and_year': '2023-04-30',
         'bonus_payments': '0',
         'hospital_payments': '3000',
         'vacation_payments': '0',
         'pdfo_tax': '2376.0',
         'military_tax': '198.0',
         'social_tax': '1320.0',
         'taxes_amount': '3894.0',
         'gross_income': '13200.0',
         'net_income': '9306.0'},

        {'user_work': '7',
         'working_hours': '200',
         'month_and_year': '2023-05-30',
         'bonus_payments': '0',
         'hospital_payments': '2000',
         'vacation_payments': '200',
         'pdfo_tax': '4068.0',
         'military_tax': '339.0',
         'social_tax': '2260.0',
         'taxes_amount': '6667.0',
         'gross_income': '22600.0',
         'net_income': '15933.0'},

        {'user_work': '7',
         'working_hours': '370',
         'month_and_year': '2023-06-30',
         'bonus_payments': '0',
         'hospital_payments': '0',
         'vacation_payments': '3700',
         'pdfo_tax': '7459.2',
         'military_tax': '621.6',
         'social_tax': '4144.0',
         'taxes_amount': '12224.8',
         'gross_income': '41440.0',
         'net_income': '29215.2'},

        {'user_work': '7',
         'working_hours': '450',
         'month_and_year': '2023-07-30',
         'bonus_payments': '0',
         'hospital_payments': '0',
         'vacation_payments': '0',
         'pdfo_tax': '8262.0',
         'military_tax': '688.5',
         'social_tax': '4590.0',
         'taxes_amount': '13540.5',
         'gross_income': '45900.0',
         'net_income': '32359.5'},

        {'user_work': '7',
         'working_hours': '400',
         'month_and_year': '2023-08-30',
         'bonus_payments': '0',
         'hospital_payments': '4400',
         'vacation_payments': '0',
         'pdfo_tax': '8136.0',
         'military_tax': '678.0',
         'social_tax': '4520.0',
         'taxes_amount': '13334.0',
         'gross_income': '45200.0',
         'net_income': '31866.0'},

        {'user_work': '8',
         'working_hours': '590',
         'month_and_year': '2023-01-30',
         'bonus_payments': '0',
         'hospital_payments': '0',
         'vacation_payments': '400',
         'pdfo_tax': '9523.8',
         'military_tax': '793.7',
         'social_tax': '5291.0',
         'taxes_amount': '15608.5',
         'gross_income': '52910.0',
         'net_income': '37301.6'},

        {'user_work': '8',
         'working_hours': '200',
         'month_and_year': '2023-02-28',
         'bonus_payments': '0',
         'hospital_payments': '2000',
         'vacation_payments': '0',
         'pdfo_tax': '3564.0',
         'military_tax': '297.0',
         'social_tax': '1980.0',
         'taxes_amount': '5841.0',
         'gross_income': '19800.0',
         'net_income': '13959.0'},

        {'user_work': '8',
         'working_hours': '315',
         'month_and_year': '2023-03-30',
         'bonus_payments': '400',
         'hospital_payments': '0',
         'vacation_payments': '0',
         'pdfo_tax': '5118.3',
         'military_tax': '426.5',
         'social_tax': '2843.5',
         'taxes_amount': '8388.3',
         'gross_income': '28435.0',
         'net_income': '20046.7'},

        {'user_work': '9',
         'working_hours': '200',
         'month_and_year': '2023-01-30',
         'bonus_payments': '0',
         'hospital_payments': '0',
         'vacation_payments': '4230',
         'pdfo_tax': '4973.4',
         'military_tax': '414.5',
         'social_tax': '2763.0',
         'taxes_amount': '8150.9',
         'gross_income': '27630.0',
         'net_income': '19479.2'},

        {'user_work': '9',
         'working_hours': '250',
         'month_and_year': '2023-02-28',
         'bonus_payments': '3000',
         'hospital_payments': '0',
         'vacation_payments': '0',
         'pdfo_tax': '5805.0',
         'military_tax': '483.8',
         'social_tax': '3225.0',
         'taxes_amount': '9513.8',
         'gross_income': '32250.0',
         'net_income': '22736.2'},

        {'user_work': '9',
         'working_hours': '320',
         'month_and_year': '2023-03-30',
         'bonus_payments': '0',
         'hospital_payments': '3800',
         'vacation_payments': '0',
         'pdfo_tax': '7423.2',
         'military_tax': '618.6',
         'social_tax': '4124.0',
         'taxes_amount': '12165.8',
         'gross_income': '41240.0',
         'net_income': '29074.2'},

        {'user_work': '9',
         'working_hours': '260',
         'month_and_year': '2023-04-30',
         'bonus_payments': '0',
         'hospital_payments': '2300',
         'vacation_payments': '0',
         'pdfo_tax': '5889.6',
         'military_tax': '490.8',
         'social_tax': '3272.0',
         'taxes_amount': '9652.4',
         'gross_income': '32720.0',
         'net_income': '23067.6'},

        {'user_work': '9',
         'working_hours': '240',
         'month_and_year': '2023-05-30',
         'bonus_payments': '0',
         'hospital_payments': '4500',
         'vacation_payments': '0',
         'pdfo_tax': '5864.4',
         'military_tax': '488.7',
         'social_tax': '3258.0',
         'taxes_amount': '9611.1',
         'gross_income': '32580.0',
         'net_income': '22968.9'},

        {'user_work': '9',
         'working_hours': '300',
         'month_and_year': '2023-06-30',
         'bonus_payments': '300',
         'hospital_payments': '0',
         'vacation_payments': '0',
         'pdfo_tax': '6372.0',
         'military_tax': '531.0',
         'social_tax': '3540.0',
         'taxes_amount': '10443.0',
         'gross_income': '35400.0',
         'net_income': '24957.0'},

        {'user_work': '9',
         'working_hours': '250',
         'month_and_year': '2023-07-30',
         'bonus_payments': '200',
         'hospital_payments': '0',
         'vacation_payments': '800',
         'pdfo_tax': '5445.0',
         'military_tax': '453.8',
         'social_tax': '3025.0',
         'taxes_amount': '8923.8',
         'gross_income': '30250.0',
         'net_income': '21326.2'},

        {'user_work': '9',
         'working_hours': '250',
         'month_and_year': '2023-08-30',
         'bonus_payments': '500',
         'hospital_payments': '0',
         'vacation_payments': '300',
         'pdfo_tax': '5409.0',
         'military_tax': '450.8',
         'social_tax': '3005.0',
         'taxes_amount': '8864.8',
         'gross_income': '30050.0',
         'net_income': '21185.2'},

        {'user_work': '9',
         'working_hours': '440',
         'month_and_year': '2023-09-30',
         'bonus_payments': '0',
         'hospital_payments': '0',
         'vacation_payments': '500',
         'pdfo_tax': '9356.4',
         'military_tax': '779.7',
         'social_tax': '5198.0',
         'taxes_amount': '15334.1',
         'gross_income': '51980.0',
         'net_income': '36645.9'},

        {'user_work': '9',
         'working_hours': '340',
         'month_and_year': '2023-10-30',
         'bonus_payments': '300',
         'hospital_payments': '0',
         'vacation_payments': '0',
         'pdfo_tax': '7214.4',
         'military_tax': '601.2',
         'social_tax': '4008.0',
         'taxes_amount': '11823.6',
         'gross_income': '40080.0',
         'net_income': '28256.4'},

        {'user_work': '10',
         'working_hours': '250',
         'month_and_year': '2023-01-30',
         'bonus_payments': '500',
         'hospital_payments': '0',
         'vacation_payments': '1600',
         'pdfo_tax': '3753.0',
         'military_tax': '312.8',
         'social_tax': '2085.0',
         'taxes_amount': '6150.8',
         'gross_income': '20850.0',
         'net_income': '14699.2'}
    ]

    try:
        DB_ALREADY_EXIST_CURSOR.execute("INSERT INTO site_information "
                                        "(site_name, site_landline_phone_number, site_phone_number_1, "
                                        "site_phone_number_2, site_email, address, "
                                        "working_days_schedule, saturday_schedule, sunday_schedule) "
                                        f"VALUES ("
                                        f"'{site_info.get('site_name')}', "
                                        f"'{site_info.get('site_landline_phone_number')}', "
                                        f"'{site_info.get('site_phone_number_1')}', "
                                        f"'{site_info.get('site_phone_number_2')}', "
                                        f"'{site_info.get('site_email')}', "
                                        f"'{site_info.get('address')}', "
                                        f"'{site_info.get('working_days_schedule')}', "
                                        f"'{site_info.get('saturday_schedule')}', "
                                        f"'{site_info.get('sunday_schedule')}')")

        DB_ALREADY_EXIST_CONNECT.commit()

    except ProgrammingError:
        print(Fore.RED + "Inserting error!")
    else:
        print(Fore.MAGENTA + "Successfully inserted data into `site_information` table!")

    for company in companies_info:
        try:
            DB_ALREADY_EXIST_CURSOR.execute("INSERT INTO companies "
                                            "(company_name, site_id) "
                                            f"VALUES ("f"'{company.get('company_name')}', "
                                            f"'{company.get('site')}')")

            DB_ALREADY_EXIST_CONNECT.commit()

        except ProgrammingError:
            print(Fore.RED + "Inserting error!")
    else:
        print(Fore.MAGENTA + "Successfully inserted data into `companies` table!")

    for tax in taxes_info:
        try:
            DB_ALREADY_EXIST_CURSOR.execute("INSERT INTO taxes "
                                            "(tax_name, tax_value, site_id) "
                                            f"VALUES ("f"'{tax.get('tax_name')}', "
                                            f"'{tax.get('tax_value')}', "
                                            f"'{tax.get('site')}')")

            DB_ALREADY_EXIST_CONNECT.commit()

        except ProgrammingError:
            print(Fore.RED + "Inserting error!")
    else:
        print(Fore.MAGENTA + "Successfully inserted data into `taxes` table!")

    for worker in workers_info:
        user = User.objects.create_user(username=worker.get('username'),
                                        password=worker.get('password'),
                                        email=worker.get('email'),
                                        first_name=worker.get('first_name'),
                                        last_name=worker.get('last_name'),
                                        is_active=True,
                                        is_staff=False,
                                        is_superuser=False)

        user.set_password(worker.get('password'))
        user.save()

        try:
            DB_ALREADY_EXIST_CURSOR.execute("INSERT INTO users_work "
                                            "(user_id, user_patronymic, user_id_card_number, user_ipn, "
                                            "company_id, hourly_rate_currency, hourly_rate) "
                                            f"VALUES ("f"'{worker.get('user_id')}', "
                                            f"'{worker.get('patronymic')}', "
                                            f"'{worker.get('user_id_card_number')}', "
                                            f"'{worker.get('user_ipn')}', "
                                            f"'{worker.get('company_id')}', "
                                            f"'{currency_info.get('currency_name')}', "
                                            f"'{worker.get('hourly_rate')}')")

            DB_ALREADY_EXIST_CONNECT.commit()

        except ProgrammingError:
            print(Fore.RED + "Inserting error!")
    else:
        print(Fore.MAGENTA + "Successfully inserted data into `users_work` table!")

    for payment in payments_info:
        try:
            DB_ALREADY_EXIST_CURSOR.execute("INSERT INTO payments "
                                            "(user_work_id, month_and_year, working_hours, bonus_payments, "
                                            "bonus_payments_currency, hospital_payments, hospital_payments_currency, "
                                            "vacation_payments, vacation_payments_currency, "
                                            "pdfo_tax_id, pdfo_tax_value, pdfo_tax_value_currency, "
                                            "military_tax_id, military_tax_value, military_tax_value_currency,"
                                            "social_tax_id, social_tax_value, social_tax_value_currency, "
                                            "taxes_amount, taxes_amount_currency,"
                                            "gross_income, gross_income_currency, net_income, net_income_currency) "
                                            f"VALUES ("f"'{payment.get('user_work')}', "
                                            f"'{payment.get('month_and_year')}', "
                                            f"'{payment.get('working_hours')}', "
                                            f"'{payment.get('bonus_payments')}', "
                                            f"'{currency_info.get('currency_name')}', "
                                            f"'{payment.get('hospital_payments')}', "
                                            f"'{currency_info.get('currency_name')}', "
                                            f"'{payment.get('vacation_payments')}', "
                                            f"'{currency_info.get('currency_name')}', "
                                            f"'1', "
                                            f"'{payment.get('pdfo_tax')}', "
                                            f"'{currency_info.get('currency_name')}', "
                                            f"'2', "
                                            f"'{payment.get('military_tax')}', "
                                            f"'{currency_info.get('currency_name')}', "
                                            f"'3', "
                                            f"'{payment.get('social_tax')}', "
                                            f"'{currency_info.get('currency_name')}', "
                                            f"'{payment.get('taxes_amount')}', "
                                            f"'{currency_info.get('currency_name')}', "
                                            f"'{payment.get('gross_income')}', "
                                            f"'{currency_info.get('currency_name')}', "
                                            f"'{payment.get('net_income')}', "
                                            f"'{currency_info.get('currency_name')}')")

            DB_ALREADY_EXIST_CONNECT.commit()

        except ProgrammingError:
            print(Fore.RED + "Inserting error!")
    else:
        print(Fore.MAGENTA + "Successfully inserted data into `payments` table!")


if __name__ == '__main__':
    database_creations()
    sleep(1)
    database_migrations()
    sleep(1)
    superuser_creations()
    sleep(1)
    accountants_creations()
    sleep(1)
    insert_data()
