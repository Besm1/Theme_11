import requests
import pprint
from html.parser import HTMLParser
from urllib.parse import urljoin

class LinkExtractor(HTMLParser):

    def __init__(self, base_url, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.links = {}
        self.base_url = base_url


    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        if tag == 'img' and 'class' in attrs and 'alt' in attrs and 'шина' in attrs['alt'].lower() : # and
            self.links[attrs['alt']] = attrs['src']

    def _refine(self, url):
        return urljoin(base=self.base_url, url=url)


def main():
    url = ('https://market.yandex.ru/catalog--avtomobilnye-shiny/54469/list?hid=90490&rs=eJwz4g1g_MTIwcEgwaDw6xCrUxMjl'
           'zQXBwejgIIErwKLAJsUZ0pqWmJpTkm8kQKDBgOXIlRSUIEVKMkPkzSML0hMT0VVIqvAgazECEkJzApGBUZkKwxBkgJMXhwmhqaGxmZpiUF'
           'GhuZGlsYmRpaGxoaGBvqpqYaWyRYWqZZpycYWiZYWRoapBgbmBmYpJkYmBmYGBvqG-oYAht4qLw%2C%2C')
    resp = requests.get(url=url)
    if resp.ok:
        # pprint.pprint(resp.text)
        ex = LinkExtractor(url)
        ex.feed(resp.text)
        pprint.pprint(ex.links)
    else:
        print(resp)


if __name__ == '__main__':
    main()