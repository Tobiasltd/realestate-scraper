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
# Huizen.to_csv('Huislijn.csv')
