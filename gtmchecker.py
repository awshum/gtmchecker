import csv
import requests
from bs4 import BeautifulSoup

def check_url(url, container_id):
    response = requests.get(url, headers={'Connection': 'close'})
    soup = BeautifulSoup(response.content, 'lxml')
    script_tags = soup.find('head').find_all(lambda tag: container_id in tag.text)
    noscript_tags = soup.find('body').find_all('noscript')
    row = [url]
    print('Checking URL:', url)
    head = ''.join(str(script_tags))
    if container_id in head:
        row.append('TRUE')
    else:
        row.append('FALSE')
    body = ''.join(str(noscript_tags))
    if container_id in body:
        row.append('TRUE')
    else:
        row.append('FALSE')
    return row

def main():
    filename = input('Where is the file with urls? ')
    container_id = input('What is the GTM container id? ')
    urls = []
    with open(filename, 'r') as f:
        data = f.readlines()
        for line in data:
            urls.append(line.rstrip('\n'))
    rows = []
    for url in urls:
        rows.append(check_url(url, container_id))
    f = open('gtmchecker.csv', 'w')
    with f:
        writer = csv.writer(f)
        writer.writerow(['URL Crawled', 'Installed in Head', 'Installed in Body'])
        writer.writerows(rows)

if __name__ == "__main__":
    main()
