import requests
import time
import pandas as pd


def get_reviews(pageID, params={'json': 1}):
    url = 'https://store.steampowered.com/appreviews/'
    response = requests.get(url=url + str(pageID), params=params, headers={'User-Agent': 'Mozilla/5.0'})
    return response.json()


def get_n_reviews(pageID, n=100):
    reviews = []
    cursor = '*'
    params = {
        'json': 1,
        'filter': 'all',
        'language': 'koreana',
        'day_range': 9223372036854775807,
        'review_type': 'all',
        'purchase_type': 'all'
    }

    while n > 0:
        time.sleep(2)
        params['cursor'] = cursor.encode()
        params['num_per_page'] = min(100, n)
        n -= 100

        response = get_reviews(pageID, params)
        cursor = response['cursor']
        reviews += response['reviews']

        if len(response['reviews']) < 100: break

    return reviews

reviews = get_n_reviews(1446780, 1000) #https://steamcommunity.com/app/1446780/reviews/?filterLanguage=koreana

reviews[:5]

df = pd.DataFrame.from_dict(reviews)

#불필요한 부분 전처리
df['review'] = df['review'] \
  .replace(r'[^가-힣 ]', ' ', regex=True) \
  .replace("'", '') \
  .replace(r'\s+', ' ', regex=True) \
  .str.strip() \
  .str[:255]

df = df[df['review'].str.strip().astype(bool)]

df['review'].values.tolist()[:5]
print(df['review'].values.tolist()[:5])
df.to_csv('reviews_ko.csv', index=False)

