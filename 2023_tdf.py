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

    total_views_week = sum(views[-28:])  # takes the sum of the last 28 elements
    return total_views_week


# Load the starting list
df = pd.read_excel(r'data/2023_06_27_tdf.xlsx')
df_scrape = df.copy()
df_scrape['views'] = np.zeros(len(df))

for i in range(len(df)):
    url = df['Link'][i] + str('/statistics')
    print('Scraping rider %i' %i)
    df_scrape['views'][i] = get_total_views_last_week(url)

df_scrape = df_scrape.sort_values('views', ascending=False)
df_scrape.to_excel('data/2023_06_30_tdf_scraped_28_days.xlsx', index=False)