import urllib.request
from os.path import abspath, dirname
import json

link = "http://api.mediastack.com/v1/news"


def scrap(keyword):
    params = urllib.parse.urlencode({
        #TODO: SET THE KEY
        'access_key': '',
        'keywords': keyword,
        'languages': 'fr,en',
        'limit': 100
    })

    req = urllib.request.Request(link + '?{}'.format(params), headers={'User-Agent' : "Magic Browser", 'Content-Type': 'text/plain;charset=utf-8', 'Accept-Charset' : 'utf-8'})
    page = urllib.request.urlopen(req)

    pretreated_json = json.loads(page.read())['data']

    for element in pretreated_json:
        del element['source']
        del element['image']
        del element['category']

    pretty_json = json.dumps(pretreated_json, indent=4, ensure_ascii=False) 

    with open(f"{dirname(abspath(__file__))}/mediastack-{keyword}.json", 'w', encoding='utf-8') as outfile:
        outfile.write(pretty_json)


while(True):
    keyword = input("Veuillez saisir le mot-clé recherché (CTRL-C pour arrêter le programme): ")
    scrap(keyword)
