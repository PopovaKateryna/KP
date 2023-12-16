def calculator(user_work, hourly_rate, hours, month_and_year, bonus_payments, hospital_payments, vacation_payments):
    gross_income = (float(hours) * float(hourly_rate) + float(bonus_payments) +
                    float(hospital_payments) + float(vacation_payments))
    pdfo_tax = gross_income / 100 * 18
    military_tax = gross_income / 100 * 1.5
    social_tax = gross_income / 100 * 10
    taxes_amount = pdfo_tax + military_tax + social_tax
    net_income = gross_income - taxes_amount

    print("{" + f"'user_work': '{user_work}',")
    print(f"'working_hours': '{hours}',")
    print(f"'month_and_year': '{month_and_year}',")
    print(f"'bonus_payments': '{bonus_payments}',")
    print(f"'hospital_payments': '{hospital_payments}',")
    print(f"'vacation_payments': '{vacation_payments}',")
    print(f"'pdfo_tax': '{round(pdfo_tax, 1)}',")
    print(f"'military_tax': '{round(military_tax, 1)}',")
    print(f"'social_tax': '{round(social_tax, 1)}',")
    print(f"'taxes_amount': '{round(taxes_amount, 1)}',")
    print(f"'gross_income': '{round(gross_income, 1)}',")
    print(f"'net_income': '{round(net_income, 1)}'" + "},")


if __name__ == '__main__':
    user_work_value = 1
    hourly_rate_value = 1
    month_and_year_value = '2023-02-28'

    hours_value = input('hours_value=')
    bonus_payments_value = input('bonus_payments_value=')
    hospital_payments_value = input('hospital_payments_value=')
    vacation_payments_value = input('vacation_payments_value=')
    print()

    calculator(user_work=user_work_value,
               hourly_rate=hourly_rate_value,
               hours=hours_value,
               month_and_year=month_and_year_value,
               bonus_payments=bonus_payments_value,
               hospital_payments=hospital_payments_value,
               vacation_payments=vacation_payments_value)
