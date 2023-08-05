import requests
from bs4 import BeautifulSoup
from urllib.parse import unquote as decode_url
import re
from urllib.parse import urljoin

from .selector import Selector


def get(url, params=None, **kwargs):
    resp = requests.get(url, params=params, **kwargs)
    return Spidy(resp)


def post(url, data=None, json=None, **kwargs):
    resp = requests.post(url, data=data, json=json, **kwargs)
    return Spidy(resp)


def parse(text, **kwargs):
    soup = Spidy(BeautifulSoup(text, "html.parser"))
    soup.url = kwargs.get("url", None)
    soup.status_code = kwargs.get("status_code", None)
    soup.headers = kwargs.get("headers", None)
    soup.cookies = kwargs.get("cookies", None)
    soup.ok = kwargs.get("ok", None)
    soup.reason = kwargs.get("reason", None)
    return soup


class Spidy:
    def __init__(self, o, headers={}, cookies={}, timeout=10):
        if type(o) is BeautifulSoup:
            self.soup = o
            self.url = None
            self.status_code = None
            self.headers = None
            self.cookies = None
            self.ok = None
            self.reason = None
            self.content = str(o).encode("utf-8")
            self.title = Selector(self.soup.title)
        elif type(o) is str:
            self.soup = BeautifulSoup(o, "html.parser")
            self.url = None
            self.status_code = None
            self.headers = None
            self.cookies = None
            self.ok = None
            self.reason = None
            self.content = None
            self.title = Selector(self.soup.title)
        else:
            if type(o) is requests.models.Response:
                self.url = o.url
                resp = o
            else:
                self.url = o
                resp = requests.get(o, headers=headers, cookies=cookies, timeout=timeout)
            self.soup = BeautifulSoup(resp.content, "html.parser")
            self.status_code = resp.status_code
            self.headers = resp.headers
            self.cookies = resp.cookies
            self.ok = resp.ok
            self.reason = resp.reason
            self.content = resp.content
            self.title = Selector(self.soup.title)

    def __repr__(self):
        return str(self.soup)

    def css(self, selector):
        els = []

        sels = self.soup.select(selector)
        for sel in sels:
            els.append(sel)

        if len(els) == 1:
            return Selector(els[0])
        else:
            return Selector(els)

    def images(self):
        imgs = []

        sels = self.soup.select("img")
        for sel in sels:
            src = sel["src"].strip()
            if src == "#" and src == "":
                continue    
            if not src.startswith("http://") or not src.startswith("https://"):
                if self.url is not None:
                    imgs.append(urljoin(self.url, src))
                else:
                    imgs.append(src)
            else:
                imgs.append(src)

        return imgs    



# if __name__ == "__main__":
#     spidy = Spidy("https://www.google.com/search?q=Prithiv+tamilbotnet&num=100")
    
#     print(spidy.css("script")[0].text())
    
    # links = spidy.css("a[href^='/url?q=']").attr("href")
    # emails = []

    # for link in links:
    #     url = decode_url(link.split("/url?q=")[-1])
    #     print("Navigating to '{}'".format(url))
    #     try:
    #         spidy = Spidy(url, headers={"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.116 Safari/537.36 Edg/83.0.478.61"})
    #     except KeyboardInterrupt:
    #         break
    #     except:
    #         continue
    #     spidy.css("script").dispose()
    #     matches = spidy.css("body *").regex(r"[a-z0-9](?!.*?[^\na-z0-9]{2})[^\s@]+@[^\s@]+\.[^\s@]+[a-z0-9]")
    #     for match in matches:
    #         emails.append(match)

    # print("\n\nEmails:\n\n")
    # for email in set(emails):
    #     print(email)
