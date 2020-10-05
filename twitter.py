from bs4 import BeautifulSoup as bs
import requests
from tqdm import tqdm
import aiohttp
import asyncio

async def fetch(session, url):
    async with session.get(url) as response:
        return await response.text()

async def main():
    async with aiohttp.ClientSession() as session:
            for i in tqdm(range(1, 1428)):
                try:
                    haberler = open('haberler.txt', 'a+')
                    newurl = 'https://www.technopat.net/page/' + str(i)
                    html = await fetch(session, newurl)
                    soup = bs(html, "lxml")
                    for haber in range(21):
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
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
