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


# To see dataframe
print(Huizen)

# Write to CSV
# Huizen.to_csv('Huislijn.csv')
