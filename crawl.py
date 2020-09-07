#! /opt/conda/envs/20newsgroups/bin/python

from article import Article

import click
from GoogleNews import GoogleNews
from loguru import logger
import os
from urllib3.exceptions import MaxRetryError

@click.command()
@click.option('--search', '-s', type=str,
              help="Search term for finding articles.")
@click.option('--lang', '-l', default="en", type=str,
              help='Language of articles.')
@click.option('--directory', '-d', default=None, type=str,
              help="Search term for finding articles.")
def crawl(search: str, lang: str = "en", directory: str = None) -> list:
    gn = GoogleNews()
    gn.setlang(lang)
    gn.search(search)
    result = gn.result()

    articles = []

    for res in result:
        try:
            article = Article.download(res['link'])
            articles.append(article)
        except MaxRetryError:
            logger.error(f'MaxRetryError for {res["link"]}')

    if directory is not None:
        for idx, article in enumerate(articles):
            if article is not None:
                filename = f'{search}_{idx}_{lang}.yml'
                filename = filename.lower().replace(' ', '_')
                article.to_yaml(f'{directory}/{filename}')
    
    return articles

if __name__ == "__main__":
    crawl()