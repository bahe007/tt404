from bs4 import BeautifulSoup
import requests
import csv
import argparse
import time 

class Crawler:
    
    def __init__(self, base_url:str, output_file:str="tt404_analysis.csv", politeness=0.0, ignore_urls=None, ignore_classes=None, ignore_ids=None):
        """

        :param start_site:
        """
        if base_url[len(base_url)-1] != "/":
            base_url = base_url + "/"

        self.base_url = base_url
        self.output_file = output_file 

        self.politeness = politeness

        self.urls_to_ignore = ignore_urls

        self.classes_to_ignore = ignore_classes
        self.ids_to_ignore = ignore_ids

        self.broken_sites = list() # List Entry Format: (origin, label, target, status)
        self.already_visited = list() # simple string list with all sites that are alreay visited and returned status code 200
        self.todo = list() # List Entry Format: (origin, label, target)

    def crawl(self):
        """
        Main method used to crawl through the website. 
        :return: self.broken_sites
        """
        self.todo.append(("", "", self.base_url))
        while len(self.todo) > 0:
            origin, label, target = self.todo[0]
            del self.todo[0]
            target_url = self.normalize_link(target)
            print(target_url)
            if self.is_url_broken(target_url): # target is a known faulty page
                self.broken_sites.append((origin, label, target_url, self.broken_url_status_code(target_url)))
                continue
            elif self.is_url_already_visited(target_url) or self.should_url_be_ignored(target_url): # target is already visited or should be ignored anyways
                continue
            else: # Seite wurde noch nicht besucht
                content, status_code = self.visit(target_url)
                if status_code != 200:
                    self.broken_sites.append((origin, label, target_url, status_code))
                else:
                    self.already_visited.append(target_url)
                    if self.is_link_to_tld(target_url):
                        is_start_page = False 
                        if target_url == self.base_url: 
                            is_start_page = True 
                        links = self.get_links(content, is_base_url=is_start_page)
                        for link in links:
                            self.todo.append((target_url, link[0], link[1]))




    def visit(self, url:str):
        """
        Calls a given link and returns the site content and status code. 
        :param link: normalisierter Link zur aufzurufenden Seite.
        :return: (content, status)
        """
        time.sleep(self.politeness)
        response = requests.get(url)
        if response.status_code == 200:
            return (response.content, response.status_code)
        else:
            return ("", response.status_code)

    def is_link_to_tld(self, url: str):
        """
        Checks if a normalized link is part of the same top level domain as the base url. 
        :param url:
        :return:
        """
        if len(url) >= len(self.base_url):
            if url[:len(self.base_url)] == self.base_url:
                return True
            else:
                return False
        else:
            return False

    def get_links(self, content: str, is_base_url:bool=False):
        """
        Returns a list with all links that could be found in a given content string that shouldn't be ignored. 

        List format: (label, link)
        :param content:
        :return:
        """
        return_links = list()
        soup = BeautifulSoup(content, "html.parser")

        if self.classes_to_ignore is not None and is_base_url is not True: 
            for css_class in self.classes_to_ignore:
                results = soup.select(".{}".format(css_class))
                if results is not None:
                    for result in results:
                        result.decompose()
        
        if self.ids_to_ignore is not None and is_base_url is not True: 
            for css_id in self.ids_to_ignore:
                results = soup.select("#{}".format(css_id))
                if results is not None:
                    for result in results:
                        result.decompose()

        all_links = soup.find_all("a")
        for link in all_links:
            if link.has_attr("href"):
                url = link["href"]
                if len(url) > 0:
                    if url[0] == "/":
                        if link.string != None:
                            return_links.append((link.string, url))
                        else:
                            return_links.append(("", url))
                        continue
                if len(url) > 8:
                    if url[:8] == "https://":
                        if link.string != None:
                            return_links.append((link.string, url))
                        else:
                            return_links.append(("", url))
                        continue

        return return_links

    def normalize_link(self, link:str):
        """
        Normalizes the link in a way, so that you can paste it directly in your browser and reach the site. 
        :param link:
        :return:str
        """
        if len(link) > 8:
            if link[:8] == "https://":
                return link
            elif link[:7] == "http://":
                return link
        if len(link) > 1:
            if link[0] == "/":
                link = link[1:]
        elif link == "/":
            return self.base_url
        return self.base_url+link

    def is_url_broken(self, url: str):
        """
        Determines, if the url is known as broken. 
        :param url:
        :return: Boolean
        """
        for element in self.broken_sites:
            if element[2] == url:
                return True
        return False

    def broken_url_status_code(self, url: str):
        """
        Looks up the status code of an url, that is definitely broken. If it couldn't find it, it returns -1. 
        :param url:
        :return:
        """
        for element in self.broken_sites:
            if element[2] == url:
                return element[3]
        return -1

    def is_url_already_visited(self, url: str):
        """
        Determines, if the urls has already been visited. 
        :param url:
        :return: Boolean
        """
        if url in self.already_visited:
            return True
        else:
            return False

    def should_url_be_ignored(self, url: str): 
        """
        Determines, wether a given url is one of the urls that should be ignored
        :param url: 
        :return: Boolean
        """
        if self.urls_to_ignore == None: 
            return False 
        else: 
            for ignore_url in self.urls_to_ignore:
                if ignore_url in url: 
                    return True 
            return False

    def safe_as_csv(self):
        """
        Writes the content of "self.broken_sites" to the initially specified output path without determining if there is already a file with the same name. 
        :return: None
        """
        with open(self.output_file, "w") as csvfile:
            writer = csv.writer(csvfile, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
            writer.writerow([self.base_url, "", "", ""])
            writer.writerow(["Origin", "Label", "Link", "Status"])
            for broken_site in self.broken_sites:
                writer.writerow(broken_site)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Finds faulty links on your website. Learn more at: https://github.com/bahe007/tt404")
    parser.add_argument('base_url', type=str,
                        help='The base url where the crawler should start')
    parser.add_argument('--output_csv', type=str, default="tt404_analysis.csv")
    parser.add_argument('--politeness', type=float, default=0.0)
    parser.add_argument("--ignore_urls", type=str, nargs="+")
    parser.add_argument("--ignore_html_classes", type=str, nargs="+")
    parser.add_argument("--ignore_html_ids", type=str, nargs="+")    

    arguments = parser.parse_args()
    
    base_url = arguments.base_url 
    output_csv = arguments.output_csv
    politeness = arguments.politeness
    ignore_urls = arguments.ignore_urls 
    ignore_classes = arguments.ignore_html_classes
    ignore_ids = arguments.ignore_html_ids

    crawler = Crawler(base_url, output_file=output_csv, ignore_urls=ignore_urls, ignore_classes=ignore_classes, ignore_ids=ignore_ids, politeness=politeness)
    crawler.crawl()
    crawler.safe_as_csv()