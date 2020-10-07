import concurrent.futures
import requests
from tqdm import tqdm
from bs4 import BeautifulSoup as bs
import csv


def load_url(url, timeout):
    response = requests.get(url, timeout=timeout)
    return response.text


def main():
    with concurrent.futures.ThreadPoolExecutor(max_workers=35) as executor:
        haberler = open('haberler.txt', 'r')
        future_to_url = {executor.submit(load_url, url, 15): url.strip() for url in
                         haberler.readlines()}
        for future in tqdm(concurrent.futures.as_completed(future_to_url)):
            try:
                url = future_to_url[future]
                html = future.result()
                content_table = get_data(html, url)
                write_data(content_table)
            except Exception as exc:
                print('%r generated an exception: %s' % (url, exc))
        haberler.close()


def get_data(html, url):
    # date format: dd-mm-yyyy
    parsed_url = url.split('/')
    date = parsed_url[4] + '-' + parsed_url[5] + '-' + parsed_url[3]
    try:
        soup = bs(html, "lxml")
        # title
        title = soup.findAll("h1", class_="jeg_post_title")[0].text
        # body text
        body_text = soup.findAll("div", class_="content-inner")[0].text.split('Etiketler:')[0]

        return [url, date, title, body_text]

    except IndexError:
        return [url, date, 'no data', 'no data']


def write_data(data):
    csv_file = open('icerik.csv', 'a+', newline='')
    header = ['URL', 'DATE', 'TITLE', 'TEXT']
    writer = csv.DictWriter(csv_file, fieldnames=header)
    writer.writeheader()
    writer.writerow({'URL': data[0],
                     'DATE': data[1],
                     'TITLE': data[2],
                     'TEXT': data[3]})

    csv_file.close()


if __name__ == '__main__':
    main()


# from bs4 import BeautifulSoup as bs
# from tqdm import tqdm
# import aiohttp
# import asyncio
# import csv
#
# async def fetch(session, url):
#     async with session.get(url) as response:
#         return await response.text()
#
#
# async def main():
#     async with aiohttp.ClientSession() as session:
#         haberler = open('haberler.txt', 'r')
#         csv_file = open('icerik.csv', 'a+', newline='')
#         header = ['URL', 'DATE', 'TITLE', 'TEXT']
#         writer = csv.DictWriter(csv_file, fieldnames=header)
#         writer.writeheader()
#         for haber in tqdm(haberler.readlines()):
#             url = haber.strip()
#             content_table = get_data(await fetch(session, url), url)
#
#
#
# def get_data(html, url):
#     # date
#     parsed_url = url.split('/')
#     date = parsed_url[5] + '/' + parsed_url[4] + '/' + parsed_url[3]
#     try:
#         soup = bs(html, "lxml")
#         # title
#         title = soup.findAll("h1", class_="jeg_post_title")[0].text
#         # body text
#         body_text = soup.findAll("div", class_="content-inner")[0].text.split('Etiketler:')[0]
#
#         return [url, date, title, body_text]
#
#     except IndexError:
#         return [url, date, 'no data', 'no data']
#
#
# if __name__ == '__main__':
#     loop = asyncio.get_event_loop()
#     loop.run_until_complete(main())
