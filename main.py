import urllib.request
from urllib.parse import urlsplit, urlunsplit, urljoin, urlparse
import re
from multiprocessing import Process


# initializing parameters
# parser = argparse.ArgumentParser(description="Sitemap generator")
# parser.add_argument('--url', action="store", default="", help="For example https://www.finstead.com")
# parser.add_argument('--exclude', action="store", default="", help="regex pattern to exclude. For example 'symbol/info' will exclude https://www.finstead.com/symbol/info/ORCL")
# parser.add_argument('--no-verbose', action="store_true", default="", help="print verbose output")
# parser.add_argument('--output', action="store", default="sitemap.xml", help="File path for output, if file exists it will be overwritten"), exclude=args.exclude, no_verbose=args.no_verbose
# # parsing parameters
# args = parser.parse_args()
class urlparser:
    def __init__(self,url,exclude = None,no_verbose = False  ):
        self.url = self.normalize(url)
        self.host = urlparse(self.url).netloc
        self.exclude = exclude
        self.no_verbose = no_verbose
        self.visited_links = [self.url]
        self.found_links = []


    def normalize(self,url):
        scheme, netloc, path, qs, anchor = urlsplit(url)
        return urlunsplit((scheme, netloc, path, qs, anchor))


    def is_internal(self,url):
        host = urlparse(url).netloc
        return host == self.host or host == ''


    def is_url(self,url):
        scheme, netloc, path, qs, anchor = urlsplit(url)
        if url != '' and scheme in ['http', 'https', '']:
            return True
        else:
            False

    def find(self,url):
        print(url)
        try:
            response = urllib.request.urlopen(url)

        except:
            print('404 Error' )
            return
        page = str(response.read())
        pattern = '<a [^>]*href=[\'|"](.*?)[\'"].*?>'
        found_links = re.findall(pattern,page )
        links = []
        for link in found_links:
            is_url = self.is_url(link)
            if is_url:
                is_internal = self.is_internal(url)
                if is_internal:
                    self.add(link, links, self.exclude)
                    self.add(link, self.found_links, self.exclude)
        for link in links:
            if link not in self.visited_links:
                link = self.normalize(link)
                self.visited_links.append(link)
                self.find(urljoin(self.url,link))


    def start(self):
        self.find(self.url)
        return self.found_links


    def add(self, link,link_list,eclude_pattern = None ):
        link = self.normalize(link)
        if link:
            notinlist = link not in link_list
            exclude = False
            if eclude_pattern :
                exclude = re.search(eclude_pattern,link)
            if notinlist and not exclude:
                link_list.append(link)






import urllib.request
from urllib.parse import urlsplit, urlunsplit, urljoin, urlparse
import re
import datetime
import sqlite3

class Crawler:

    def __init__(self, url , exclude=None, no_verbose=False):
        self.url = self.normalize(url)

        self.host = urlparse(self.url).netloc
        self.exclude = exclude
        self.no_verbose = no_verbose
        self.found_links = []
        self.visited_links = [self.url]

    def start(self):
        self.crawl(self.url)

        return self.found_links

    def crawl(self, url):

        print("Parsing " + url)
        try:
            response = urllib.request.urlopen(url)
        except:
            print('404 error')
            return

        page = str(response.read())

        pattern = '<a [^>]*href=[\'|"](.*?)[\'"].*?>'

        found_links = re.findall(pattern, page)
        links = []

        for link in found_links:
            is_url = self.is_url(link)

            if is_url:
                is_internal = self.is_internal(link)

                if is_internal:
                    self.add_url(link, links, self.exclude)
                    self.add_url(link, self.found_links, self.exclude)

        for link in links:
            if link not in self.visited_links:
                link = self.normalize(link)

                self.visited_links.append(link)
                self.crawl(urljoin(self.url, link))

    def add_url(self, link, link_list, exclude_pattern=None):
        link = self.normalize(link)

        if link:
            not_in_list = link not in link_list

            excluded = False

            if exclude_pattern:
                excluded = re.search(exclude_pattern, link)

            if not_in_list and not excluded:
                link_list.append(link)

    def normalize(self, url):
        scheme, netloc, path, qs, anchor = urlsplit(url)
        return urlunsplit((scheme, netloc, path, qs, anchor))

    def is_internal(self, url):
        host = urlparse(url).netloc
        return host == self.host or host == ''

    def is_url(self, url):
        scheme, netloc, path, qs, anchor = urlsplit(url)

        if url != '' and scheme in ['http', 'https', '']:
            return True
        else:
            return False
def multy(*func):
    tmp = []
    for i in func:
        p = Process(target=i)
        p.start()
        tmp.append(p)

    for t in tmp :
        t.join()







a = open('saitmap.xml','w')
a.write('<?xml version="1.0" encoding="UTF-8"?>\n\t<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">')


url = 'https://www.avalonmebel.ru'
url2 = 'https://www.google.com'
crawler1 = Crawler(url2)
crawler = Crawler(url)
multy(crawler1.start(),crawler.start())
start = datetime.datetime.now()
links = crawler.start()
end = datetime.datetime.now()
time = end - start
print(time)
print(len(links))
for i in links:
    a.write('\n\t\t<url>\n\t\t\t<loc>\n\t\t\t\t{}{}/\n\t\t\t</loc>\n\t\t</url>'.format(url,i))
a.write('</urlset>')

sqlite_connection = sqlite3.connect('test2.db')
cursor = sqlite_connection.cursor()
a = url
b = str(time)
c = str(len(links))
d = 'saitmap.xml'

with sqlite_connection:
    try:
        create_table = '''CREATE TABLE test_table(
          url TEXT NOT NULL,
          time TEXT NOT NULL,
          qty  TEXT NOT NULL,
          name TEXT NOT NULL);'''

        cursor.execute(create_table)
    except:
        pass
    insert = '''INSERT INTO test_table
    (url,time,qty,name)VALUES(?,?,?,?)
                    '''
    cursor.execute(insert, [a, b, c, d])


#
# import sqlite3
# db = sqlite3.connect('server.db')
# sql = db.cursor()
# with db:
#     try:
#         create_table = '''CREATE TABLE users (
#                        login TEXT NOT NULL,
#                        password TEXT NOT NULL,
#                        cash TEXT NOT NULL);'''
#         db.execute(create_table)
#     except:
#         pass

    # user_login = input('Login:')
    # user_password = input('password:')
    # user_cash = input('cash:')
    # db.execute('SELECT login FROM users ')
    #
    #
    # sql.execute( "INSERT INTO users VALUES (?,?,?)",[user_login,user_password,user_cash])

