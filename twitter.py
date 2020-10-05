from bs4 import BeautifulSoup as bs
import requests
from tqdm import tqdm


def main():
        for i in tqdm(range(1, 1426)):
            try:
                haberler = open('haberler.txt', 'a+')
                newurl = 'https://www.technopat.net/page/' + str(i)
                html = requests.get(newurl).text
                soup = bs(html, "lxml")
                for haber in range(1, 1428):
                    tags = \
                    soup.findAll("div", class_="jeg_thumb")[haber]
                    for a in tags.find_all('a', href=True):
                        if a['href'] != 'https://www.technopat.net/haber/'\
                        and a['href'] != 'https://www.technopat.net/video/':
                            haberler.writelines(a['href'] + '\n')
                haberler.close()
            except IndexError:
                break

if __name__ == '__main__':
    main()