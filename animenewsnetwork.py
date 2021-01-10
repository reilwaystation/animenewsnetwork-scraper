import bs4 as bs
from urllib import request
import json
import unidecode

# start with ID number 1
# replace to where you want to start
identifier = 1

# as per January 2021 the last anime id is 4797
# replace the limit to when you want to stop the scraping
limit = 4797
data = {}


def write_json(data):
    with open("animenewsnetwork.json", 'w') as f:
        json.dump(data, f, indent=4)


while identifier < limit:

    try:
        xml = request.urlopen(
            f'https://cdn.animenewsnetwork.com/encyclopedia/api.xml?anime={identifier}').read()
        soup = bs.BeautifulSoup(xml, 'lxml')
        ann = soup.find_all('ann')[0]
        if not ann.find('warning'):
            title = soup.find_all(attrs={"type": "Main title"})
            if title:
                data['title'] = title[0].text

            description = soup.find_all(attrs={"type": "Plot Summary"})
            if description:
                data['description'] = unidecode.unidecode(
                    u'' + description[0].text)

            tags = soup.find_all(attrs={"type": "Themes"})
            if tags:
                data['tags'] = []
                for i in tags:
                    data['tags'].append(i.text)

            genres = soup.find_all(attrs={"type": "Genres"})
            if genres:
                data['genres'] = []
                for i in genres:
                    data['genres'].append(i.text)
                    if tags:
                        data['tags'].append(i.text)

            thumbnail = soup.find_all(attrs={"type": "Picture"})
            if thumbnail:
                data['thumbnail'] = thumbnail[-1].find('img')['src']
            with open("animenewsnetwork.json") as file:
                array = json.load(file)
                array.append(data)
                json.dumps(array)
                write_json(array)
    except:
        print(f'something wrong with = {identifier}')

    identifier = identifier + 1
    print(identifier)
