import requests
from requests import get
from bs4 import BeautifulSoup
import pandas as pd
import numpy as np
from csv import writer
from time import sleep
from random import randint


Adressen = []
Postcodes = []
Woningoppervlaktes = []
Prijzen = []

# Huizenzoeker
pages = np.arange(1, 30, 1)


for page in pages:
    page = requests.get(
        "https://www.huizenzoeker.nl/koop/utrecht/utrecht/" + str(page) + '/')
    soup = BeautifulSoup(page.text, 'html.parser')
    listings = soup.find_all('tr', id=True)
    sleep(randint(2, 10))

    for listing in listings:

        # Adres
        adres = listing.find(class_='titel').get_text()
        Adressen.append(adres)

        # Postcode
        postcode = listing.find(
            class_='titel').next_sibling.next_sibling.replace(
            '\n', '').replace('Utrecht', '').replace(' ', '').strip()
        Postcodes.append(postcode)

        # Woningoppervlakte
        woningoppervlakte = listing.find(
            class_='prijs').find_previous_sibling().find_previous_sibling().get_text().replace(
            'm²', '').strip()
        Woningoppervlaktes.append(woningoppervlakte)

        # Prijs
        prijs = listing.find(class_='prijs').get_text().replace(
            'k.k', '').replace('€', '').replace('.', '').replace('Op aanvraag', '-').strip().split()[0]
        Prijzen.append(prijs)


# Jaap
pages = np.arange(1, 20, 1)


for page in pages:
    page = requests.get(
        "https://www.jaap.nl/koophuizen/utrecht/utrecht/utrecht/p" + str(page))
    soup = BeautifulSoup(page.text, 'html.parser')
    listings = soup.find_all(class_="property-info")
    sleep(randint(2, 10))

    for listing in listings:

        if 'm²' in listing.find_all(class_="property-feature")[-1].get_text():
            # Adres
            adres = listing.find(
                class_="property-address-street").get_text()
            Adressen.append(adres)

            # Postcode
            postcode = listing.find(
                class_="property-address-zipcity").get_text().replace(',', '').replace('Utrecht', '').replace(' ', '').strip()
            Postcodes.append(postcode)

            # Woningoppervlakte
            woningoppervlakte = listing.find_all(
                class_="property-feature")[-1].get_text().replace(' m²', '').strip()
            Woningoppervlaktes.append(woningoppervlakte)

            # Prijs
            prijs = listing.find(class_='property-price').get_text().replace(
                'k.k.', '').replace('€ ', '').replace('.', '').strip()
            Prijzen.append(prijs)

# VBO

pages = np.arange(1, 3, 1)


for page in pages:
    page = requests.get(
        "https://www.vbo.nl/koopwoningen/utrecht.html?l=36&p=" + str(page) + '/')
    soup = BeautifulSoup(page.text, 'html.parser')
    listings = soup.find_all(class_="object-tiles")
    sleep(randint(2, 10))

    for listing in listings:

        if listing.find(class_="price").get_text() != 'verkocht onder voorbehoud':

            # Adres
            adres = listing.find('h3').get_text().replace('Utrecht', '')
            Adressen.append(adres)

            # Postcode
            postcode = '-'
            Postcodes.append(postcode)

            # Woningoppervlakte
            woningoppervlakte = listing.find('li').next_sibling.get_text().replace(
                'Woonoppervlakte', '').replace('m²', '').replace(':', '').strip()
            Woningoppervlaktes.append(woningoppervlakte)

            # Prijs
            prijs = listing.find(class_="price").get_text().replace(
                'k.k.', '').replace('€', '').replace(',-', '').replace('.', '').strip().split()[0]
            Prijzen.append(prijs)


# Huislijn
pages = np.arange(1, 14, 1)


for page in pages:
    page = requests.get(
        "https://www.huislijn.nl/koopwoning/nederland/utrecht/utrecht?page=" + str(page) + '&order=relevance')
    soup = BeautifulSoup(page.text, 'html.parser')
    listings = soup.find_all(class_="object-panel")
    sleep(randint(2, 10))

    for listing in listings:

        # Adres
        adres = listing.find(
            class_="object-street").get_text().replace(', Utrecht', '')
        Adressen.append(adres)

        # Postcode
        postcode = '-'
        Postcodes.append(postcode)

        # Woningoppervlakte
        woningoppervlakte = listing.find(
            'sup').previous_sibling.replace(' m', '').strip()
        Woningoppervlaktes.append(woningoppervlakte)

        # Prijs
        prijs = listing.find(
            class_="object-price").get_text().replace('.00', '').strip()
        Prijzen.append(prijs)


# building our Pandas dataframe
Huizen = pd.DataFrame({
    'Adres': Adressen,
    'Postcode': Postcodes,
    'Woningoppervlakte m2': Woningoppervlaktes,
    'Prijs': Prijzen,
})

# To see dataframe with duplicates
# print(Huizen)

# Delete duplicate rows based on Adres column
Huizen = Huizen.drop_duplicates(subset=['Adres'])
print("Cleaned Dataframe", Huizen)

# Write to CSV
Huizen.to_csv('Uberlist.csv')

# py Uberscraper.py
