from random import randint
from time import sleep
from csv import writer
import numpy as np
import pandas as pd
from bs4 import BeautifulSoup
from requests import get
import requests


Adressen = []
Postcodes = []
Woningoppervlaktes = []
Prijzen = []

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

# building our Pandas dataframe
Huizen = pd.DataFrame({
    'Adres': Adressen,
    'Postcode': Postcodes,
    'Woningoppervlakte m2': Woningoppervlaktes,
    'Prijs': Prijzen,
})


# To see dataframe
print(Huizen)

# Write to CSV
Huizen.to_csv('Vbo.csv')
