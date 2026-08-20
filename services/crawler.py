from bs4 import BeautifulSoup as bs
from services.alert import report

class Crawler:
    def __init__(self, source):
        self.crawler_client = bs(source, 'html.parser')

    def el_select(self, pattern, limit=5):
        elements = self.crawler_client.select(pattern, limit=limit)
        if not elements:
            report({
                'error': f'elements with pattern {pattern} not found'
            })
            exit()
        return elements