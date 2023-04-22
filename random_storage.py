from datetime import datetime
import requests
import json

def themain(query, set_amount):
    url = f"https://api.twitter.com/2/tweets/search/recent?query={query}&max_results={set_amount}"
    bearer_token = "AAAAAAAAAAAAAAAAAAAAAAe2kQEAAAAA1R82X51MUKlYmmX%2BP%2BOKjew3ZpA%3D2WqE3HjJnJQOHSzt8cF7p0Uydi3ocKLQXPZL1duelZ1D0FdVqw"
    headers = {
    "Authorization": f"Bearer {bearer_token}",  "User-Agent": "TwitterDevRandomSearchPython"
    }
    response = requests.get(url, headers=headers)
    data = json.loads(response.text)
    with open('stored_random.txt', 'a') as c:
        today = datetime.now()
        c.write(f'---------Retrieved at: {today}, query: {query}-------------\n\n')
    for tweet in data["data"]:
        print(tweet["text"])
        with open('stored_random.txt', 'a') as f:
            try:
              f.write(f"Tweet: {tweet['text']}\n\n")
            except:
               pass


