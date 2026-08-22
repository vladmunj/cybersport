from bs4 import BeautifulSoup as bs
from exceptions.crawl import CrawlException

class Crawler:
    @staticmethod
    def root_select(source, pattern, limit = 0, required = True):
        crawler_client = bs(source, 'html.parser')
        elements = crawler_client.select(pattern, limit = limit)
        if not elements:
            if required:
                raise CrawlException({'error': f'elements with pattern {pattern} not found'})
            return None
        return elements

    @staticmethod
    def select(parent, pattern, limit=0, required = True):
        elements = parent.select(pattern, limit = limit)
        if not elements:
            if required:
                raise CrawlException({'error': f'elements with pattern {pattern} not found'})
            return None
        return elements

    @staticmethod
    def select_one(parent, pattern, required = True):
        element = parent.select_one(pattern)
        if not element:
            if required:
                raise CrawlException({'error': f'element with pattern {pattern} not found'})
            return None
        return element

    @staticmethod
    def text(parent, pattern, required = True):
        element = parent.select_one(pattern)
        if not element:
            if required:
                raise CrawlException({'error': f'element with pattern {pattern} not found'})
            return None
        return element.get_text(strip = True)

    @staticmethod
    def attr(element, attr, required = True):
        attribute = element.attrs.get(attr)
        if not attribute:
            if required:
                raise CrawlException({'error': f'element\'s attribute {attr} not found'})
            return None
        return attribute