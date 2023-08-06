
"""Returns the fetched data by crawling"""
from urllib.parse import urlparse, urljoin
from urllib.error import URLError
from urllib.error import HTTPError
from collections import deque
from tqdm import tqdm
import urllib.request
import re
import sys
import datetime
import time
import random
import ssl
import traceback
from multiprocessing.pool import Pool

total_urls_visited = 0

class KeyboardInterruptError(Exception): 
    pass


class Pycrawler(object):
    """ Class Pycrawler id made"""

    def __init__(self, start_url):  # called when object is initialized
        self.start_url = start_url
        self.internal_urls = set()
        self.external_urls = set()
        self.broken_links = set()
        self.external = set()
        self.new_urls = deque([])
        self.processed_urls = set()
        self.total = 0
        self.dic = {}
        self.Dict = {}
        self.Dict["Internal"] = {}
        self.Dict["broken"] = {}
        self.Dict["External"] = {}
        self.internallist = []
        self.externallist = []
        self.brokenlist = []

    def startu(self):
        """Start Crawling"""
        self.crawl(self.start_url)

    def get_response_time(self, link):
        """get response time of url"""
        start = time.time()
        urllib.request.urlopen(link)
        diff = time.time() - start
        responsetime = round(diff, 2)
        return responsetime

    def is_valid(self, url):
        tokens = [urllib.parse.urlparse(url)]
        min_attributes = ("scheme", "netloc")  # add attrs to your liking
        for token in tokens:
            if not all([getattr(token, attr) for attr in min_attributes]):
                error = "'{url}' string has no scheme or netloc.".format(
                    url=token.geturl()
                )
                print(error)
            else:
                return True
            return False

    def get_all_website_links(self, url):
        """get all website links for the url passed"""
        self.urls = set()
        domain = urlparse(url).netloc
        try:
            response = urllib.request.urlopen(
                url, context=ssl._create_unverified_context()
            )
            responsetime = self.get_response_time(url)
            self.Dict["Internal"][url] = responsetime
            with response as resp:
                data = resp.read().decode("latin-1")
        except HTTPError as error:
            if error.code == 429:
                print("Too many requests, wait for sometime to continue the execution")
                time.sleep(360)
                print("Total External links:", len(self.external_urls))
                print(" Total Internal links:", len(self.internal_urls))
                total = (
                    len(self.external_urls)
                    + len(self.internal_urls)
                    + len(self.broken_links)
                )
                print("Total links:", self.total)
                return None
            else:
                if url in self.internal_urls:
                    if url not in self.broken_links:
                        self.broken_links.add(url)
                        self.Dict["broken"][url] = str(error)[11:]
                    self.internal_urls.remove(url)
                return None
        except (URLError, ValueError) as error:
            time.sleep(5)
            traceback.print_exc()
            if url in self.internal_urls:
                if url not in self.broken_links:
                    self.broken_links.add(url)
                    self.Dict["broken"][url] = str(error)[11:]
                self.internal_urls.remove(url)
            return None
        links = re.findall(
            '''<a\s+(?:[^>]*?\s+)?href="([^"]*)"''', data
        )  # Extracting the matching urls
        rlinks = re.findall('''<img\s+(?:[^>]*?\s+)?src="([^"]*)"''', data)
        all_links = links + rlinks
        for link in tqdm(all_links):
            href = link
            if href == "" or href is None:
                continue
            href = urljoin(url, href)
            parsed_href = urlparse(href)
            # remove URL GET parameters, URL fragments, etc.
            href = parsed_href.scheme + "://" + parsed_href.netloc + parsed_href.path
            if not self.is_valid(href):  # not a valid URL
                continue
            if href in self.internal_urls:
                continue  # already in the set
            if href in self.broken_links:
                continue
            if domain not in href:  # external link
                if href not in self.external_urls:
                    self.external_urls.add(href)
                continue
            self.urls.add(href)
            self.internal_urls.add(href)
        return self.urls  # return internal_urls to be crawled

    def crawl(self, url):
        """
        Crawls a web page and extracts all links.
        You'll find all links in `external_urls` and `internal_urls` global set variables.
        params:
        """
        if url == self.start_url:
            print(f"Crawling {url} ...")
        self.new_urls.append(url)
        while len(self.new_urls) > 0:
            link = self.new_urls[0]
            self.new_urls.popleft()
            try:
                time.sleep(3)
                global total_urls_visited
                total_urls_visited += 1
                if total_urls_visited % 10 == 0:
                    print(f"Total No of links crawled so far={total_urls_visited}")
                links = self.get_all_website_links(link)
                self.processed_urls.add(link)
                if links:
                    for each in links:
                        self.new_urls.append(each)
            except (RuntimeError, TypeError, NameError):
                time.sleep(2)
                traceback.print_exc()
            except:
                print("Unexpected error:", sys.exc_info()[0])
                raise


def mainfunc(webname):
    try:
        """All the main implementation of crawling and presenting information is handled"""
        crawler = Pycrawler(webname)
        crawler.startu()
        time.sleep(10)
        # remove broken links from external_links
        for link in crawler.external_urls:
            try:
                responsetime = crawler.get_response_time(link)
                crawler.external.add(link)
                crawler.Dict["External"][link] = responsetime
            except (HTTPError, URLError) as error:
                crawler.broken_links.add(link)
                crawler.Dict["broken"][link] = str(error)[11:]
        crawler.total = (
            len(crawler.external) + len(crawler.internal_urls) + len(crawler.broken_links)
        )
        print(f"Searched website: {crawler.start_url}")
        if crawler.total > 0:
            print(
                f"Found {crawler.total-len(crawler.broken_links)} links ("
                + str(len(crawler.external))
                + " external references, "
                + str(len(crawler.internal_urls))
                + " internal references)"
            )
            now = datetime.datetime.now()
            dt_string = now.strftime("%d/%m/%Y %H:%M:%S IST")
            string = "abcdefghijklmnopqrstuvwxyz0123456789"
            reportid = "".join(random.sample(string, 6))
            crawler.dic = {
                "report-id": reportid,
                "starting_url": crawler.start_url,
                "External links": crawler.external,
                "Internal links": crawler.internal_urls,
                "Broken links": crawler.broken_links,
                "Date and Time": dt_string,
                "Total links": crawler.total,
            }
            print("Report generated with unique-id:", reportid)
            del crawler.Dict["Internal"][crawler.start_url]
            for i in crawler.Dict["Internal"].items():
                webinfo = []
                webinfo.append(i[0])
                webinfo.append(str(i[1]) + "s")
                crawler.internallist.append(list(webinfo))
            for i in crawler.Dict["External"].items():
                webinfo = []
                webinfo.append(i[0])
                webinfo.append(str(i[1]) + "s")
                crawler.externallist.append(list(webinfo))
            for i in crawler.Dict["broken"].items():
                webinfo = []
                webinfo.append(i[0])
                webinfo.append(i[1])
                crawler.brokenlist.append(list(webinfo))
            data = {}
            data["report_id"] = crawler.dic["report-id"]
            data["website_link"] = crawler.dic["starting_url"]
            data["total_links"] = crawler.dic["Total links"]
            data["external_links"] = crawler.externallist
            data["internal_links"] = crawler.internallist
            data["broken_links"] = crawler.brokenlist
            data["date_time"] = crawler.dic["Date and Time"]
            return data
        else:
            print("Invalid URL or No Links Found")
        
    except KeyboardInterrupt:
        print("Ctrl + c Captured")
        print()
        raise KeyboardInterruptError()



def concurrency(ipurls):
    with Pool(4) as tasks:
        somelist = tasks.map(mainfunc,ipurls)
    return somelist

if __name__=="__main__":
    concurrency(["https://httpbin.org/","https://erp.aktu.ac.in/webpages/oneview/oneview.aspx"])
    