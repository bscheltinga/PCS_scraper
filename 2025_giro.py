import requests
from bs4 import BeautifulSoup
import pandas as pd
import numpy as np


def get_total_views_last_week(url):
    r = requests.get(url)
    soup = BeautifulSoup(r.content, "html.parser")

    # Find the bar diagram with visits
    views = []
    views_diagram = soup.find_all("div", {"class": "bg hide"})
    for item in views_diagram:
        views.append(int(item.contents[0]))

    total_views_week = sum(views[-30:])  # takes the sum of the last 28 elements
    return total_views_week

# Load the starting list
df = pd.read_excel('data/2025_05_08_giro.xlsx')
df_scrape = df.copy()
df_scrape['views'] = 0  # initialize column

# Use `.loc` to avoid SettingWithCopyWarning
for i, row in df_scrape.iterrows():
    url = row['Link'] + '/statistics'
    print(f'Scraping rider {i}')
    df_scrape.loc[i, 'views'] = get_total_views_last_week(url)

# Sort and save
df_scrape = df_scrape.sort_values('views', ascending=False)
df_scrape.to_excel('data/2025_05_08_giro_scraped_30_days.xlsx', index=False)
