import concurrent.futures
import requests
from tqdm import tqdm
from bs4 import BeautifulSoup as bs

URLS = []

for i in range(1, 1428):
    URLS.append('http://technopat.net/page/' + str(i))


# Retrieve a single page and report the URL and contents
def load_url(url, timeout):
    response = requests.get(url, timeout=timeout)
    return response.text


# We can use a with statement to ensure threads are cleaned up promptly
def main():
    with concurrent.futures.ThreadPoolExecutor(max_workers=10) as executor:
        # Start the load operations and mark each future with its URL
        haberler = open('haberler.txt', 'a+')
        future_to_url = {executor.submit(load_url, url, 15): url for url in
                         URLS}
        for future in tqdm(concurrent.futures.as_completed(future_to_url)):
            try:
                url = future_to_url[future]
                html = future.result()
                soup = bs(html, "lxml")
                for haber in range(21):
                    tags = \
                        soup.findAll("div", class_="jeg_thumb")[haber]
                    for a in tags.find_all('a', href=True):
                        if a['href'] != 'https://www.technopat.net/haber/' \
                                and \
                                a['href'] != 'https://www.technopat.net/video/':
                            haberler.writelines(a['href'] + '\n')
            except Exception as exc:
                print('%r generated an exception: %s' % (url, exc))
        haberler.close()


if __name__ == '__main__':
    main()
