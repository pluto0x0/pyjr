from functools import total_ordering
from sre_constants import SRE_FLAG_UNICODE
import requests
import json
import re

import pprint

pp = pprint.PrettyPrinter(indent=4)

DBfile = 'xjp.json'

res = []


def genDB():
    UA = 'User-Agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10_7_0) AppleWebKit/535.11 (KHTML, like Gecko) Chrome/17.0.963.56 Safari/535.11'
    MAX_PAGE = 200000000

    def getArticle(articleID):
        # print(articleID)
        url = f'http://jhsjk.people.cn/article/{articleID}'
        r = requests.get(url, headers={'User-Agent': UA})

        title = re.search(r'<h1>(.*?)</h1>', r.text, re.S).group(1)
        try:
            total = re.search(
                r'<div class="d2txt_con clearfix">\s*<p>(.*?)</p>\s*</div>',
                r.text, re.S).group(1)
            paras = re.findall(r'<p[^>]*>[\s]*(.+?)[\s]*</p>', total, re.S)
            paras = list(
                filter(
                    lambda x: len(x),
                    map(lambda x: re.sub('</?[^>]+>', '', x).strip('　'),
                        paras)))
        except AttributeError:
            paras = ['']
        # pp.pprint(paras)
        return {'articleid': articleID, 'title': title, 'paras': paras}

    page = 0
    res.clear()
    while True:
        url = f'http://jhsjk.people.cn/testnew/result?keywords=&isFuzzy=0&searchArea=0&year=0&form=0&type=0&page={page}&origin=%E5%85%A8%E9%83%A8&source=2'
        # url = 'http://myip.ipip.net'
        r = requests.get(url, headers={'User-Agent': UA})
        data = r.json()['list']
        if data == [] or page > MAX_PAGE:
            break

        for i in data:
            res.append(getArticle(i['article_id']))
            print('.', end='')

        print(page, 'OK')
        page += 1

    with open(DBfile, 'w', encoding='utf8') as ff:
        ff.write(json.dumps(res, ensure_ascii=False))


genDB()

'''
def loadDB():
    with open(DBfile, 'r', encoding='utf8') as ff:
        res = json.loads(ff.read())


def search(text, inTitle=False):
    
    for i in res:
        if inTitle:
            


def load():
    with open(DBfile, 'r', encoding='utf8') as inf:
        res = json.loads(inf.read())

if __name__ == '__main__':
    load()
'''
