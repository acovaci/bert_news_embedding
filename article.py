from bs4 import BeautifulSoup
from loguru import logger
import time
import urllib3
import yaml

http = urllib3.PoolManager()

class Article:
    def __init__(self, components: dict):
        self._components = components

        self.page_title = components['page_title']

        self.title = components['title']
        self.author = components['author'] if 'author' in components else None
        self.date = components['date'] if 'date' in components else None

        self.paragraphs = components['paragraphs']

        self.url = components['url']
        self.scrape_date = components['scrape_date']

    @staticmethod
    def download(url: str, method: str = 'GET', article_tag: str = 'article',
                 paragraph_tag: str = 'p'):
        response = http.request('GET', url)

        dom = BeautifulSoup(response.data, 'html.parser')
        logger.trace(dom.findAll(article_tag))
        try:
            article = dom.findAll(article_tag)[0]
        except IndexError:
            logger.warning(f'Could not find <{article_tag}>. Try something else?')
            article_tag = input()

            if article_tag in ['n', 'N', 'no', 'NO', 'No']:
                logger.warning(f'Cancelling')
                return None
            
            logger.info(f'Continuing with <{article_tag}>')
            return Article.download(url, method, article_tag, paragraph_tag)

        c = {
            'page_title': str(dom.title),
            'title': dom.h1.text,
            'paragraphs': [p.text.strip() for p in article.findAll(paragraph_tag) if p.text.strip()],
            'url': url,
            'scrape_date': time.time()
        }

        logger.trace(c)

        return Article(c)

    def to_yaml(self, file: str = None):
        content = yaml.dump(self._components)

        if file is not None:
            with open(file, 'w+') as f:
                print(content, file=f)
        
        return content