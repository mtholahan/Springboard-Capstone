import os, requests
url = "https://api.themoviedb.org/3/search/movie"
params = {"api_key": os.getenv("TMDB_API_KEY"), "query": "ghostbusters"}
resp = requests.get(url, params=params)
print(resp.status_code)
print(resp.json())
