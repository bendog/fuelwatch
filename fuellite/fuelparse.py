#!/usr/bin/env python
from bs4 import BeautifulSoup
from dataclasses import dataclass

with open("rss.xml") as fo:
    content = fo.read()

print(content)

soup = BeautifulSoup(content, 'xml')


@dataclass
class FuelPrice(object):
    description: str
    brand: str
    price: float


prices = []
for item in soup.rss.channel.find_all('item')[:10]:
    prices.append(FuelPrice(
        item.description,
        item.brand,
        item.price
    ))

for x in prices:
    print(x)
