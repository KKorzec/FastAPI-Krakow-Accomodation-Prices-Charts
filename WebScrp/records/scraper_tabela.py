from datetime import date
import pymysql
import requests
from fastapi import FastAPI
from WebScrp.records import models
from bs4 import BeautifulSoup
import sys
import re

app = FastAPI()

# Inicjalizacja tablic
div_data_1 = []
div_data_2 = []
div_data_3 = []

districts = {
    "Stare Miasto": 1, "Grzegórzki": 2, "Prądnik Czerwony": 3, "Prądnik Biały": 4, "Krowodrza": 5, "Bronowice": 6,
    "Zwierzyniec": 7, "Dębniki": 8, "Łagiewniki-Borek Fałęcki": 9, "Swoszowice": 10, "Podgórze Duchackie": 11,
    "Bieżanów-Prokocim": 12, "Podgórze": 13, "Czyżyny": 14, "Mistrzejowice": 15, "Bieńczyce": 16,
    "Wzgórza Krzesławickie": 17, "Nowa Huta": 18,
}

# Wersja dla kawalerek (0 pokoi)
def create_arrays_1():
    url = "https://tabelaofert.pl/mieszkania-1-pokojowe-na-wynajem/krakow?prs=0&sz=1&lokalizacja=Krak%C3%B3w"

    # Pobranie zawartości strony
    response = requests.get(url)
    response.encoding = 'utf-8'
    html_content = response.text
    soup = BeautifulSoup(html_content, "html.parser")

    divs = soup.find_all("div", class_=re.compile(r"^oferta-box market-after sector-none"))

    # Przetwarzanie zawartości divów, ich id i innych klas wewnątrz nich
    for div in divs:
        div_id = div.get("data-identyfikator")  # Pobieranie wartości atrybutu "data-identyfikator"
        div_id = int(div_id.split("-")[-1])  # Wyciąganie tylko liczby z końca
        sub_classes = div.find("h3", class_="info__adres")  # Pobieranie nagłówka <h3 class="info__adres">
        location = sub_classes.get_text() if sub_classes else None
        link = div.find(class_="image__badge cena")

        # Tworzenie do zapisu danych
        row = [None, div_id, 1, None, None, None]

        # Przetwórz dane o dacie dodania wpisu i lokalizacji
        if sub_classes:
            row[3] = date.today().strftime('%Y-%m-%d')
            row[4] = location

        # Przetwórz dane o cenie wynajmu
        if link is not None:
            link_text = link.get_text()
            link_text = link_text.encode(sys.stdout.encoding, errors='replace').decode(sys.stdout.encoding)
            row[5] = link_text

        div_data_1.append(row)

    # Wyświetlanie zawartości tablicy
    #for row in div_data_1:
      #print(row)


# Normalizacja danych w tablicy
def modify_arrays_1():
    # Podmień dzielnice na unormowane liczby
    for i in range(len(div_data_1)):
            if isinstance(div_data_1[i][4], str):
                for name, number in districts.items():
                    if name in div_data_1[i][4]:
                        div_data_1[i][4] = str(number)

    # Podmień ceny na unormowane
    for row in div_data_1:
        price_str = row[5]
        # Usuwanie wszystkich znaków nie będących cyframi
        price_str = re.sub(r'\D', '', price_str)
        # Konwersja na wartość liczbową
        try:
            price = int(price_str)
            row[5] = price
        except ValueError:
            row[5] = None

    # Zamień stringi na inty
    for record in div_data_1:
        record[0] = record[1]*-1
        record[1] = int(record[1])
        try:
            record[4] = int(record[4])
        except Exception as e:
            record[4] = 0
        if record[5] <= 1000:
            record[4] = 0

    # Wyświetlanie zawartości tablicy
    for record in div_data_1:
        print(record)

# Wersja dla kawalerek (0 pokoi)
def create_arrays_2():
    url = "https://tabelaofert.pl/mieszkania-2-pokojowe-na-wynajem/krakow?sz=1&prs=0&lokalizacja=Krak%C3%B3w"

    # Pobranie zawartości strony
    response = requests.get(url)
    response.encoding = 'utf-8'
    html_content = response.text
    soup = BeautifulSoup(html_content, "html.parser")

    divs = soup.find_all("div", class_=re.compile(r"^oferta-box market-after sector-none"))

    # Przetwarzanie zawartości divów, ich id i innych klas wewnątrz nich
    for div in divs:
        div_id = div.get("data-identyfikator")  # Pobieranie wartości atrybutu "data-identyfikator"
        div_id = int(div_id.split("-")[-1])  # Wyciąganie tylko liczby z końca
        sub_classes = div.find("h3", class_="info__adres")  # Pobieranie nagłówka <h3 class="info__adres">
        location = sub_classes.get_text() if sub_classes else None
        link = div.find(class_="image__badge cena")

        # Tworzenie do zapisu danych
        row = [None, div_id, 2, None, None, None]

        # Przetwórz dane o dacie dodania wpisu i lokalizacji
        if sub_classes:
            row[3] = date.today().strftime('%Y-%m-%d')
            row[4] = location

        # Przetwórz dane o cenie wynajmu
        if link is not None:
            link_text = link.get_text()
            link_text = link_text.encode(sys.stdout.encoding, errors='replace').decode(sys.stdout.encoding)
            row[5] = link_text

        div_data_2.append(row)

    # Wyświetlanie zawartości tablicy
    #for row in div_data_2:
      #print(row)


# Normalizacja danych w tablicy
def modify_arrays_2():
    # Podmień dzielnice na unormowane liczby
    for i in range(len(div_data_2)):
            if isinstance(div_data_2[i][4], str):
                for name, number in districts.items():
                    if name in div_data_2[i][4]:
                        div_data_2[i][4] = str(number)

    # Podmień ceny na unormowane
    for row in div_data_2:
        price_str = row[5]
        # Usuwanie wszystkich znaków nie będących cyframi
        price_str = re.sub(r'\D', '', price_str)
        # Konwersja na wartość liczbową
        try:
            price = int(price_str)
            row[5] = price
        except ValueError:
            row[5] = None

    # Zamień stringi na inty
    for record in div_data_2:
        record[0] = record[1]*-1
        record[1] = int(record[1])
        try:
            record[4] = int(record[4])
        except Exception as e:
            record[4] = 0
        if record[5] <= 1000:
            record[4] = 0

    # Wyświetlanie zawartości tablicy
    for record in div_data_2:
        print(record)

# Wersja dla kawalerek (0 pokoi)
def create_arrays_3():
    url = "https://tabelaofert.pl/mieszkania-3-pokojowe-na-wynajem/krakow?sz=1&prs=0&lokalizacja=Krak%C3%B3w"

    # Pobranie zawartości strony
    response = requests.get(url)
    response.encoding = 'utf-8'
    html_content = response.text
    soup = BeautifulSoup(html_content, "html.parser")

    divs = soup.find_all("div", class_=re.compile(r"^oferta-box market-after sector-none"))

    # Przetwarzanie zawartości divów, ich id i innych klas wewnątrz nich
    for div in divs:
        div_id = div.get("data-identyfikator")  # Pobieranie wartości atrybutu "data-identyfikator"
        div_id = int(div_id.split("-")[-1])  # Wyciąganie tylko liczby z końca
        sub_classes = div.find("h3", class_="info__adres")  # Pobieranie nagłówka <h3 class="info__adres">
        location = sub_classes.get_text() if sub_classes else None
        link = div.find(class_="image__badge cena")

        # Tworzenie do zapisu danych
        row = [None, div_id, 3, None, None, None]

        # Przetwórz dane o dacie dodania wpisu i lokalizacji
        if sub_classes:
            row[3] = date.today().strftime('%Y-%m-%d')
            row[4] = location

        # Przetwórz dane o cenie wynajmu
        if link is not None:
            link_text = link.get_text()
            link_text = link_text.encode(sys.stdout.encoding, errors='replace').decode(sys.stdout.encoding)
            row[5] = link_text

        div_data_3.append(row)

    # Wyświetlanie zawartości tablicy
    #for row in div_data_3:
      #print(row)


# Normalizacja danych w tablicy
def modify_arrays_3():
    # Podmień dzielnice na unormowane liczby
    for i in range(len(div_data_3)):
            if isinstance(div_data_3[i][4], str):
                for name, number in districts.items():
                    if name in div_data_3[i][4]:
                        div_data_3[i][4] = str(number)

    # Podmień ceny na unormowane
    for row in div_data_3:
        price_str = row[5]
        # Usuwanie wszystkich znaków nie będących cyframi
        price_str = re.sub(r'\D', '', price_str)
        # Konwersja na wartość liczbową
        try:
            price = int(price_str)
            row[5] = price
        except ValueError:
            row[5] = None

    # Zamień stringi na inty
    for record in div_data_3:
        record[0] = record[1]*-1
        record[1] = int(record[1])
        try:
            record[4] = int(record[4])
        except Exception as e:
            record[4] = 0
        if record[5] <= 1000 or record[5] > 9500:
            record[4] = 0

    # Wyświetlanie zawartości tablicy
    for record in div_data_3:
        print(record)

async def create_new_record_tabela(database):
    create_arrays_1()
    modify_arrays_1()
    create_arrays_2()
    modify_arrays_2()
    create_arrays_3()
    modify_arrays_3()

    for record in div_data_1:
        new_record = models.Record(id_olx=record[0],
                                   id_otodom=record[1],
                                   rooms=record[2],
                                   date=record[3],
                                   district_id=record[4],
                                   price=record[5])
        database.add(new_record)
        try:
            database.commit()
        except pymysql.err.IntegrityError as e:
            database.rollback()
        except Exception as e:
            database.rollback()


    for record in div_data_2:
        new_record = models.Record(id_olx=record[0],
                                   id_otodom=record[1],
                                   rooms=record[2],
                                   date=record[3],
                                   district_id=record[4],
                                   price=record[5])
        database.add(new_record)
        try:
            database.commit()
        except pymysql.err.IntegrityError as e:
            database.rollback()
        except Exception as e:
            database.rollback()

    for record in div_data_3:
        new_record = models.Record(id_olx=record[0],
                                   id_otodom=record[1],
                                   rooms=record[2],
                                   date=record[3],
                                   district_id=record[4],
                                   price=record[5])
        database.add(new_record)
        try:
            database.commit()
        except pymysql.err.IntegrityError as e:
            database.rollback()
        except Exception as e:
            database.rollback()
    return new_record
