from datetime import datetime, date
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

months = {
    'stycznia': 1, 'lutego': 2, 'marca': 3, 'kwietnia': 4, 'maja': 5, 'czerwca': 6,
    'lipca': 7, 'sierpnia': 8, 'września': 9, 'października': 10, 'listopada': 11, 'grudnia': 12
}


# Wersja dla kawalerek (0 pokoi)
def create_arrays_1():
    #url = "https://www.olx.pl/nieruchomosci/mieszkania/wynajem/krakow/?search%5Bfilter_enum_rooms%5D%5B0%5D=one"
    url1 = "https://www.olx.pl/nieruchomosci/mieszkania/wynajem/krakow/?search%5Bfilter_enum_rooms%5D%5B0%5D=one&search%5Border%5D=created_at%3Adesc"
    #url = "https://www.olx.pl/nieruchomosci/mieszkania/wynajem/krakow/?search%5Border%5D=created_at:desc&search%5Bfilter_enum_rooms%5D%5B0%5D=one"

    # Pobranie zawartości strony
    response = requests.get(url1)
    response.encoding = 'utf-8'
    html_content = response.text
    soup = BeautifulSoup(html_content, "html.parser")

    # Wyszukiwanie divów z klasą "css-1sw7q4x" zawierających oferty
    divs = soup.find_all("div", class_="css-1sw7q4x")

    # Przetwarzanie zawartości divów, ich id i innych klas wewnątrz nich
    for div in divs:
        div_id = div.get("id")
        sub_classes = div.find_all(class_=["css-veheph er34gjf0"])
        link = div.find(class_="css-10b0gli er34gjf0")

        # Tworzenie do zapisu danych
        row = [div_id, None, 1, None, None, None]

        # Przetwórz dane o dacie dodania wpisu i lokalizacji
        if sub_classes:
            sub_text = sub_classes[0].get_text()
            sub_text = sub_text.encode(sys.stdout.encoding, errors='replace').decode(sys.stdout.encoding)

            # Podział sub_text na datę i lokalizację
            sub_text_parts = sub_text.split('- ')
            if len(sub_text_parts) >= 2:
                location = sub_text_parts[0].strip()
                date = sub_text_parts[1].strip()
                row[3] = date
                row[4] = location

        # Przetwórz dane o cenie wynajmu
        if link is not None:
            link_text = link.get_text()
            link_text = link_text.encode(sys.stdout.encoding, errors='replace').decode(sys.stdout.encoding)
            row[5] = link_text

        div_data_1.append(row)

    # Wyświetlanie zawartości tablicy
    for row in div_data_1:
        print(row)


# Normalizacja danych w tablicy
def modify_arrays_1():
    # Usunięcie ostatniego pustego wiersza
    div_data_1.pop()

    # Określenie dzisiejszej daty
    current_date = date.today()
    formatted_date = current_date.strftime('%Y-%m-%d')

    # Podmień daty na unormowane
    for row in div_data_1:
        date_str = row[3]
        if 'Dzisiaj' in date_str:
            row[3] = formatted_date
        else:
            # Przypadki inne niż "Dzisiaj"
            regex = r'Odświeżono dnia (\d+) (\w+) (\d+)'
            match = re.search(regex, date_str)

            if match:
                # Przypadek "Odświeżono dnia DD MM YYYY"
                day = match.group(1)
                month_name = match.group(2)
                year = match.group(3)

                if month_name in months:
                    # Przetwórz "Odświeżono dnia DD nazwa_miesiąca YYYY" na datę
                    month_number = months[month_name]
                    parsed_date = datetime(int(year), month_number, int(day)).strftime('%Y-%m-%d')
                    row[3] = parsed_date
            else:
                # Przypadek "DD MM YYYY"
                for month_name, month_number in months.items():
                    if month_name in date_str:
                        # Przetwórz dane na datę
                        date_str = date_str.replace(month_name, str(month_number))
                        break
                try:
                    parsed_date = datetime.strptime(date_str, '%d %m %Y').strftime('%Y-%m-%d')
                    row[3] = parsed_date
                except ValueError:
                    pass

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
        record[0] = int(record[0])
        record[1] = record[0]*-1
        try:
            record[4] = int(record[4])
        except Exception as e:
            record[4] = 0
        if record[5] <= 1000:
            record[4] = 0

    # Wyświetlanie zawartości tablicy
    for record in div_data_1:
        print(record)


# Wersja dla dwu-pokojowych (2 pokoje)
def create_arrays_2():
    #url = "https://www.olx.pl/nieruchomosci/mieszkania/wynajem/krakow/?search%5Bfilter_enum_rooms%5D%5B0%5D=one"
    url2 = "https://www.olx.pl/nieruchomosci/mieszkania/wynajem/krakow/?search%5Border%5D=created_at:desc&search%5Bfilter_enum_rooms%5D%5B0%5D=two"
    #url = "https://www.olx.pl/nieruchomosci/mieszkania/wynajem/krakow/?search%5Border%5D=created_at:desc&search%5Bfilter_enum_rooms%5D%5B0%5D=one"

    # Pobranie zawartości strony
    response = requests.get(url2)
    response.encoding = 'utf-8'
    html_content = response.text
    soup = BeautifulSoup(html_content, "html.parser")

    # Wyszukiwanie divów z klasą "css-1sw7q4x" zawierających oferty
    divs = soup.find_all("div", class_="css-1sw7q4x")

    # Przetwarzanie zawartości divów, ich id i innych klas wewnątrz nich
    for div in divs:
        div_id = div.get("id")
        sub_classes = div.find_all(class_=["css-veheph er34gjf0"])
        link = div.find(class_="css-10b0gli er34gjf0")

        # Tworzenie do zapisu danych
        row = [div_id, None, 2, None, None, None]

        # Przetwórz dane o dacie dodania wpisu i lokalizacji
        if sub_classes:
            sub_text = sub_classes[0].get_text()
            sub_text = sub_text.encode(sys.stdout.encoding, errors='replace').decode(sys.stdout.encoding)

            # Podział sub_text na datę i lokalizację
            sub_text_parts = sub_text.split('- ')
            if len(sub_text_parts) >= 2:
                location = sub_text_parts[0].strip()
                date = sub_text_parts[1].strip()
                row[3] = date
                row[4] = location

        # Przetwórz dane o cenie wynajmu
        if link is not None:
            link_text = link.get_text()
            link_text = link_text.encode(sys.stdout.encoding, errors='replace').decode(sys.stdout.encoding)
            row[5] = link_text

        div_data_2.append(row)

    # Wyświetlanie zawartości tablicy
    for row in div_data_2:
        print(row)


# Normalizacja danych w tablicy
def modify_arrays_2():
    # Usunięcie ostatniego pustego wiersza
    div_data_2.pop()

    # Określenie dzisiejszej daty
    current_date = date.today()
    formatted_date = current_date.strftime('%Y-%m-%d')

    # Podmień daty na unormowane
    for row in div_data_2:
        date_str = row[3]
        if 'Dzisiaj' in date_str:
            row[3] = formatted_date
        else:
            # Przypadki inne niż "Dzisiaj"
            regex = r'Odświeżono dnia (\d+) (\w+) (\d+)'
            match = re.search(regex, date_str)

            if match:
                # Przypadek "Odświeżono dnia DD MM YYYY"
                day = match.group(1)
                month_name = match.group(2)
                year = match.group(3)

                if month_name in months:
                    # Przetwórz "Odświeżono dnia DD nazwa_miesiąca YYYY" na datę
                    month_number = months[month_name]
                    parsed_date = datetime(int(year), month_number, int(day)).strftime('%Y-%m-%d')
                    row[3] = parsed_date
            else:
                # Przypadek "DD MM YYYY"
                for month_name, month_number in months.items():
                    if month_name in date_str:
                        # Przetwórz dane na datę
                        date_str = date_str.replace(month_name, str(month_number))
                        break
                try:
                    parsed_date = datetime.strptime(date_str, '%d %m %Y').strftime('%Y-%m-%d')
                    row[3] = parsed_date
                except ValueError:
                    pass

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
        record[0] = int(record[0])
        record[1] = record[0]*-1
        try:
            record[4] = int(record[4])
        except Exception as e:
            record[4] = 0
        if record[5] <= 1000 or record[5] > 9500:
            record[4] = 0

    # Wyświetlanie zawartości tablicy
    for record in div_data_2:
        print(record)


# Wersja dla trzy-pokojowych (3 pokoje)
def create_arrays_3():
    #url = "https://www.olx.pl/nieruchomosci/mieszkania/wynajem/krakow/?search%5Bfilter_enum_rooms%5D%5B0%5D=one"
    url3 = "https://www.olx.pl/nieruchomosci/mieszkania/wynajem/krakow/?search%5Border%5D=created_at:desc&search%5Bfilter_enum_rooms%5D%5B0%5D=three"
    #url = "https://www.olx.pl/nieruchomosci/mieszkania/wynajem/krakow/?search%5Border%5D=created_at:desc&search%5Bfilter_enum_rooms%5D%5B0%5D=one"

    # Pobranie zawartości strony
    response = requests.get(url3)
    response.encoding = 'utf-8'
    html_content = response.text
    soup = BeautifulSoup(html_content, "html.parser")

    # Wyszukiwanie divów z klasą "css-1sw7q4x" zawierających oferty
    divs = soup.find_all("div", class_="css-1sw7q4x")

    # Przetwarzanie zawartości divów, ich id i innych klas wewnątrz nich
    for div in divs:
        div_id = div.get("id")
        sub_classes = div.find_all(class_=["css-veheph er34gjf0"])
        link = div.find(class_="css-10b0gli er34gjf0")

        # Tworzenie do zapisu danych
        row = [div_id, None, 3, None, None, None]

        # Przetwórz dane o dacie dodania wpisu i lokalizacji
        if sub_classes:
            sub_text = sub_classes[0].get_text()
            sub_text = sub_text.encode(sys.stdout.encoding, errors='replace').decode(sys.stdout.encoding)

            # Podział sub_text na datę i lokalizację
            sub_text_parts = sub_text.split('- ')
            if len(sub_text_parts) >= 2:
                location = sub_text_parts[0].strip()
                date = sub_text_parts[1].strip()
                row[3] = date
                row[4] = location

        # Przetwórz dane o cenie wynajmu
        if link is not None:
            link_text = link.get_text()
            link_text = link_text.encode(sys.stdout.encoding, errors='replace').decode(sys.stdout.encoding)
            row[5] = link_text

        div_data_3.append(row)

    # Wyświetlanie zawartości tablicy
    for row in div_data_3:
        print(row)


# Normalizacja danych w tablicy
def modify_arrays_3():
    # Usunięcie ostatniego pustego wiersza
    div_data_3.pop()

    # Określenie dzisiejszej daty
    current_date = date.today()
    formatted_date = current_date.strftime('%Y-%m-%d')

    # Podmień daty na unormowane
    for row in div_data_3:
        date_str = row[3]
        if 'Dzisiaj' in date_str:
            row[3] = formatted_date
        else:
            # Przypadki inne niż "Dzisiaj"
            regex = r'Odświeżono dnia (\d+) (\w+) (\d+)'
            match = re.search(regex, date_str)

            if match:
                # Przypadek "Odświeżono dnia DD MM YYYY"
                day = match.group(1)
                month_name = match.group(2)
                year = match.group(3)

                if month_name in months:
                    # Przetwórz "Odświeżono dnia DD nazwa_miesiąca YYYY" na datę
                    month_number = months[month_name]
                    parsed_date = datetime(int(year), month_number, int(day)).strftime('%Y-%m-%d')
                    row[3] = parsed_date
            else:
                # Przypadek "DD MM YYYY"
                for month_name, month_number in months.items():
                    if month_name in date_str:
                        # Przetwórz dane na datę
                        date_str = date_str.replace(month_name, str(month_number))
                        break
                try:
                    parsed_date = datetime.strptime(date_str, '%d %m %Y').strftime('%Y-%m-%d')
                    row[3] = parsed_date
                except ValueError:
                    pass

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
        record[0] = int(record[0])
        record[1] = record[0]*-1
        try:
            record[4] = int(record[4])
        except Exception as e:
            record[4] = 0
        if record[5] <= 1000 or record[5] > 9500:
            record[4] = 0

    # Wyświetlanie zawartości tablicy
    for record in div_data_3:
        print(record)

async def create_new_record_olx(database):
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
