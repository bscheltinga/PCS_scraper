import pandas as pd
import requests
from bs4 import BeautifulSoup
import re
import numpy as np


def scrape_page(url):
    r = requests.get(url)
    soup = BeautifulSoup(r.content, "html.parser")
    job_elements = soup.find_all("div", class_="rdr-info-cont")
    for node in job_elements:
        string = node.text

    # Extract data
    weight_pattern = re.compile(r"Weight:\s+(\d+)\s+kg")
    height_pattern = re.compile(r"Height:\s+(\d+\.\d+)\s+m")

    world_rank = re.search(r'UCI World(\d+)', string)
    world_rank_number = int(world_rank.group(1)) if world_rank else None

    # Extracting the captured numbers
    weight_match = re.search(weight_pattern, string)
    height_match = re.search(height_pattern, string)

    if weight_match:
        weight = int(weight_match.group(1))
    else:
        weight = None

    if height_match:
        height = float(height_match.group(1))
    else:
        height = None

    return weight, height, world_rank_number


# Load the starting list
df = pd.read_excel('start_list.xlsx')
df_scrape = df.copy()
df_scrape['weight'] = np.zeros(len(df))
df_scrape['height'] = np.zeros(len(df))
df_scrape['world rank'] = np.zeros(len(df))
df_scrape['BMI'] = np.zeros(len(df))
df_scrape['outliers'] = np.zeros(len(df))

# Loop over the dataframe
for i in range(len(df)):
    url = df['URL'][i][:-1]  ## to get to stats: + str('/statistics')
    df_scrape['weight'][i], df_scrape['height'][i], df_scrape['world rank'][i] = scrape_page(url)

df_scrape['BMI'] = df_scrape['weight']/df_scrape['height']**2

df_scrape['outliers'] = ((df_scrape['weight']-df_scrape['weight'].mean())/df_scrape['weight'].mean()*100 +
                         (df_scrape['height']-df_scrape['height'].mean())/df_scrape['height'].mean()*100)

df_scrape['weight'].mean()
df_scrape['height'].mean()

# df_scrape.to_excel('df_scraped.xlsx')
