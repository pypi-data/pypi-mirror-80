import urllib.parse


def parse_query_url(url):
    return urllib.parse.quote_plus(url, safe="=&")
