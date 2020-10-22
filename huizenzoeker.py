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
            class_='titel').next_sibling.next_sibling
        Postcodes.append(postcode)

        # Woningoppervlakte
        woningoppervlakte = listing.find(
            class_='prijs').find_previous_sibling().find_previous_sibling().get_text()
        Woningoppervlaktes.append(woningoppervlakte)

        # Prijs + cleaning data
        prijs = listing.find(class_='prijs').get_text().replace(
            'k.k', '').replace('€', '').replace('.', '').replace('Op aanvraag', '-').strip().split()[0]
        Prijzen.append(prijs)

# building our Pandas dataframe
Huizen = pd.DataFrame({
    'Adres': Adressen,
    'Postcode': Postcodes,
    'Woningoppervlakte m2': Woningoppervlaktes,
    'Prijs': Prijzen,
})

# Cleaning data with Pandas

# Cleaning postcode
Huizen['Postcode'] = Huizen['Postcode'].str.replace(
    '\n', '').str.replace('Utrecht', '').str.replace(' ', '').str.strip()

# Cleaning Woningoppervlakte m2
Huizen['Woningoppervlakte m2'] = Huizen['Woningoppervlakte m2'].str.replace(
    'm²', '').str.strip()


# To see dataframe
print(Huizen)

# Write to CSV
Huizen.to_csv('Huizenzoeker.csv')

# py huizenscraper.py
