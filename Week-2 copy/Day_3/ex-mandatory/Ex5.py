import datetime

today_date = datetime.date.today()

new_years_date = datetime.date(2027, 1, 1)

time_between = new_years_date - today_date
print(time_between)
