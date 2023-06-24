import pandas as pd
import requests
from bs4 import BeautifulSoup
import re
import numpy as np

url = 'https://www.procyclingstats.com/rider/miguel-angel-lopez/statistics/overview'
r = requests.get(url)
soup = BeautifulSoup(r.content, "html.parser")

# Find the bar diagram with visits
views = []
views_diagram = soup.find_all("div", {"class": "bg hide"})
for item in views_diagram:
    print(item)
    views.append(int(item.contents[0]))

total_views_week = sum(views[-7:])  # takes the sum of the last 7 elements
