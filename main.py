import requests
from bs4 import BeautifulSoup
import csv
import json
from  collections import namedtuple

KL_NEW_URL = "https://www.klwines.com/Products?&filters=sv2_206!4!90$eq$1$True$ff-90-1--$&limit=50&offset=0&orderBy=60%20asc,search.score()%20desc&searchText="
URL_FILENAME = "kl-search.txt"
KL_URL = "https://www.klwines.com/"

Result = namedtuple('Result', ['product', 'url'])

def get_soup_results():
    html = requests.get(KL_NEW_URL, headers = {'User-Agent' : 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.54 Safari/537.36'}).text
    search_soup = BeautifulSoup(html, 'html.parser')
    items = search_soup.find_all("div", class_="tf-product clearfix")
    results = []
    for item in items:
        a = item.find("a")
        product = a.contents[0].strip()
        url = KL_URL + a['href']
        result = Result(product, url)
        results.append(result)
    return results


def write_results(results):
    with open(URL_FILENAME, 'w') as file:
        for result in results:
            serialized_result = json.dumps(result._asdict())
            file.write(serialized_result + "\n")

def compare_items(results):
    new_items = []
    try:
        with open(URL_FILENAME, 'r') as file:
            serialized_items = file.read().splitlines()
            previous_items = [Result(**json.loads(item)) for item in serialized_items]

            for result in results:
                if result not in previous_items:
                    new_items.append(result)
    except IOError:
        print('This is the first search')

    return new_items


if __name__ == '__main__':
    results = get_soup_results()
    write_results(results)
    new_items = compare_items(results)
    print(new_items)
