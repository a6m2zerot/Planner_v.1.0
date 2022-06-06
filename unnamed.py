from datetime import datetime, date

print("date_today=", date.today())

# создадим даты как строки
ds1 = 'Friday, November 17, 2020'
ds2 = '11/17/20'
ds3 = '11-17-2020'

# Конвертируем строки в объекты datetime и сохраним
dt1 = datetime.strptime(ds1, '%A, %B %d, %Y')
dt2 = datetime.strptime(ds2, '%m/%d/%y')
dt3 = datetime.strptime(ds3, '%m-%d-%Y')

print(dt1)
print(dt2)
print(dt3)

# еще пример
date_string = 'Oct 17 2020 9:00PM'
date_object = datetime.strptime(date_string, '%b %d %Y %I:%M%p')
print("*", date_object)

#  **************************************************************

# Dateutil  - парсер, сводит всё в один формат. Для установки через терминал: pip install python-dateutil
from dateutil import parser

dt_obj = parser.parse('Thu Oct 17 17:10:28 2019')
print(dt_obj)
dt_obj1 = parser.parse('Thursday, 17. October 2019 5:10PM')
print(dt_obj1)
dt_obj2 = parser.parse('10/17/2019 17:10:28')
print(dt_obj2)
t_obj = parser.parse('10/17/2019')
print(t_obj)
