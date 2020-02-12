import datetime
import time
import subprocess

import requests
from bs4 import BeautifulSoup



post = "https://platforma.polsl.pl/rau2/login/index.php"
data = {"username": "USERNAME",
        "password": "PASSWORD"}

# use a Session to persist cookies.
with requests.Session() as s:
    r = s.post(post, data=data) # log us in
    while True:
        try:
            algo = s.get("https://platforma.polsl.pl/rau2/mod/assign/view.php?id=21559") # get Algorithms page
            structures = s.get("https://platforma.polsl.pl/rau2/mod/assign/view.php?id=21562") # get Structures page
            algo_soup = BeautifulSoup(algo.content, features="html.parser")
            structure_soup = BeautifulSoup(structures.content, features="html.parser")
            algorithms_graded = algo_soup.find("td", class_="submissiongraded")
            structures_graded = structure_soup.find("td", class_="submissiongraded")
            now = '{0:%Y-%m-%d %H:%M:%S}'.format(datetime.datetime.now())
            if algorithms_graded:
                # cmd = 'echo "OCENILI ALGORYTMY" | say --voice=Zosia'
                # subprocess.call(cmd, shell=True)
                print(f"{now}: SĄ OCENKI Z ALGO")
            else:
                print(f"{now}: NIE MA OCENEK Z ALGO")
            if structures_graded:
                cmd = 'echo "OCENILI STRUKTURY" | say --voice=Zosia'
                subprocess.call(cmd, shell=True)
                print(f"{now}: SĄ OCENKI ZE STRUKTUR")
            else:
                print(f"{now}: NIE MA OCENEK ZE STRUKTUR")
            time.sleep(60)
        except Exception:
            print("trututu")
