import datetime
import time

import requests
from bs4 import BeautifulSoup



post = "https://platforma.polsl.pl/rau2/login/index.php"
data = {"username": "TUTAJ WPISZ SWOJ LOGIN NA PLATFORMIE",
        "password": "TUTAJ WPISZ SWOJE HASLO"}
months = {"stycznia": 1,
          "lutego": 2}

# use a Session to persist cookies.
with requests.Session() as s:
    r = s.post(post, data=data) # log us in 
    while True:
        r = s.get("https://platforma.polsl.pl/rau2/user/profile.php?id=0") # get account page
        soup = BeautifulSoup(r.content, features="html.parser")
        # this code is very beautiful
        array = soup.find("dt", string="Ostatni dostęp do strony").next_sibling.string.replace(',', ' ').replace(u'\xa0', u' ').split()[1:5]
        array[1] = months[array[1]]
        time_list = array[3].split(':')
        array.pop()
        array = list(map(int, array))
        time_list = list(map(int, time_list))
        last_activity = datetime.datetime(year=array[2], month=array[1], day=array[0], hour=time_list[0], minute=time_list[1])
        time_diff = datetime.datetime.now() - last_activity
        hours = time_diff.seconds // 3600
        minutes = (time_diff.seconds//60)%60
        now = '{0:%Y-%m-%d %H:%M:%S}'.format(datetime.datetime.now())
        if time_diff.days == 0 and minutes < 2:
            print(f"{now}: PROWADZĄCY AKTYWNY!!!")
        else:
            print(f"{now}: PROWADZACY NIEAKTYWNY JUŻ OD {time_diff.days} DNI, {hours} GODZIN, {minutes} MINUT :(")
        time.sleep(60)