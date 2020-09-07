# bert_news_embedding
This repo contains a script that can automatically search Google News and download articles based on a search term. It is based on the `googlenews` Python package.

Example:
```{python}
./crawl.py -s "Donald Trump" -d donald_trump
```

This will download articles as YML under the folder `donald_trump`.

Under the **`acovaci-fakenews`** volume there are also models used to try to train BERT embeddings, as well as all files under this repo.
