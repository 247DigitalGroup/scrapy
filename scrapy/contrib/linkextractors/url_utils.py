"""
    URL utils for URL joining stuff
"""

import re
# import tldextract
from urlparse import urlparse, urljoin


# def get_domain(url):
#     " get domain from the url"
# 
#     ext = tldextract.extract(url)
#     if ext[1]:
#         return '.'.join(ext[:3])
#     return None


def tricky_join(url, href):
    """ - the standard urljoin fails when it joins "http://www.example.com/"
        and "example.com/a", so this tricky method prepends "http" into
        "example.com" (if exists) before joining
        - href must not contain spaces 
    """


    # text in href
    if ' ' in href:
        return url
    # # not the same domain
    # domain = get_domain(href)
    # if domain and domain != get_domain(url):
    #     return url
    result = re.search(r'^([a-zA-Z0-9]+(-[a-zA-Z0-9]+)*\.)+[a-z]{2,}', href)
    if result:
        href = 'http://' + href
    return urljoin(url, href.strip())

