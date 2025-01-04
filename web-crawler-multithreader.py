import threading
import requests
from bs4 import BeautifulSoup
from queue import Queue
queue = Queue()
visits = set()
def producer():
    while len(visits) < 60:
        url = queue.get()
        response = requests.get(url)
        soup = BeautifulSoup(response.content, 'html.parser')
        print(f"URL: {url}")
        print(f"This website has {len(soup.find_all('a'))} links")


        for link in soup.find_all('a'):
            http = link.get('href')
            if http and http.startswith('http') and http not in visits:
                with threading.Lock():
                    visits.add(http)
                    queue.put(http)
def crawling():
    queue.put("https://toscrape.com/")
    threads = []
    for x in range(4):
        thread = threading.Thread(target=producer)
        threads.append(thread)
        thread.start()
    for thread in threads:
        thread.join()
def main():
    crawling()
main()