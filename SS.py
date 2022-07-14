import requests
import time
from bs4 import BeautifulSoup as bs
import re
import string


URL = "https://www.ss.lv/lv/transport/cars/today/sell/filter/"

lapa = requests.get(URL)


def saglabat_lapu(adrese, fails):
        pieprasijums = requests.get(adrese)

        if pieprasijums.status_code == 200:
            lapa = pieprasijums.text

            with open(fails, "w", encoding="utf-8") as f:
                f.write(lapa)
        else:
            print("Kļūda lapas pieprasīšanā! Kļūda:", pieprasijums.status_code)

def novilkt_lapas(daudzums):
    for i in range(1, daudzums +1):
        adrese = f"{URL}page{i}.html"
        fails = f"Pieprasijumi/Lapa_{i}.html"
        
        print("Pieprasijums no", adrese)
        saglabat_lapu(adrese, fails)
        #novilkt_lapas(5)      
        time.sleep(3)

def No(htmlDatne):
    with open(htmlDatne, "r", encoding="utf-8") as f:
        html = f.read()
    zupa = bs(html, "html.parser")
    
    tabulas = zupa.find_all("table")
    
    autoTabula = tabulas[5]
    
    autoRindas = autoTabula.find_all("a")

    Saite = autoRindas[0]
    string1 = Saite.get('href')
    Skaitlis = int(re.search(r'\d+', string1).group())
    
    
    print(Skaitlis)
           

    #novilkt_lapas(5)


No("Pieprasijumi/Lapa_1.html")