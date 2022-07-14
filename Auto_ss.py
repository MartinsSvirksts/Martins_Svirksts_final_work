import requests
import time
from bs4 import BeautifulSoup as bs
import csv
import re
import string


URL = "https://www.ss.lv/lv/transport/cars/today/sell/filter/"

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

        time.sleep(3)

def No(htmlSkaitlis):
    with open(htmlSkaitlis, "r", encoding="utf-8") as f:
            html = f.read()

    putra = bs(html, "html.parser")
    
    tabulas = putra.find_all("table")
    
    skaitTabula = tabulas[5]
    
    skaitRindas = skaitTabula.find_all("a")

    Saite = skaitRindas[0]

    string = Saite.get('href')

    Skaitlis = str(re.search(r'\d+', string).group())
    
    with open("Pieprasijumi/Lapu_skaits.txt", "w", encoding="utf-8") as text_file:

       text_file.write(f"{Skaitlis}")

       text_file.close()

    #novilkt_lapas(Skaitlis)        
No("Pieprasijumi/Lapa_1.html")

def info(htmlDatne):
    with open(htmlDatne, "r", encoding="utf-8") as f:
        html = f.read()

    zupa = bs(html, "html.parser")
    
    tabulas = zupa.find_all("table")
    
    autoTabula = tabulas[4]

    autoRindas = autoTabula.find_all("tr")

    dati = []
        
    for rinda in autoRindas[1:-1]:
        auto = {}
        lauki = rinda.find_all("td")

        if lauki[4].text == "-" or lauki[6].text == "-" or not lauki[3].br:
            continue

        auto ['Gads'] = lauki[4].text
        tilpums = lauki[5].text

        if "D" in tilpums:
            auto['Dzinējs'] = 'Dīzelis'
            auto['Tilpums'] = tilpums[:-1]
        elif "H" in tilpums:
            auto['Dzinējs'] = 'Hibrīds'
            auto['Tilpums'] = tilpums[:-1]
        elif "E" in tilpums:
            continue
        else:
            auto['Dzinējs'] = 'Benzīns'
            auto['Tilpums'] = tilpums
        
        auto['Nobraukums'] = lauki[6].text.replace(" tūkst.", "")

        
        auto['Cena'] = lauki[7].text.replace("  €", "").replace(",","")
        
        lauki[3].br.replace_with("!")
        auto['Marka'] = lauki[3].text.replace("!", " ")
        auto['Ražotājs'] = lauki[3].text.split("!")[0]
        auto['Modelis'] = lauki[3].text.split("!")[1]
        
        dati.append(auto)
    return dati
def saglabat_datus(autoDati):
    with open("Pieprasijumi/SS_auto.csv","w", encoding="utf=8", newline="") as f:
        kolonnas = ['Ražotājs', 'Modelis', 'Marka', 'Gads', 'Dzinējs', 'Tilpums', 'Nobraukums', 'Cena']
        w = csv.DictWriter(f, fieldnames=kolonnas)
        w.writeheader()

        for auto in autoDati:
            w.writerow(auto)

   
def izvilkt_datus(daudzums):
    
    visiDati = []

    for i in range(1, daudzums + 1):
        fails = f"Pieprasijumi/Lapa_{i}.html"
        datnesDati = info(fails)
        visiDati = visiDati + datnesDati

    saglabat_datus(visiDati)

Cipars = int(open("Pieprasijumi/Lapu_skaits.txt", "r").read())
izvilkt_datus(Cipars)
print(Cipars)