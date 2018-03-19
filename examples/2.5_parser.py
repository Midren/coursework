from bs4 import BeautifulSoup
from collections import defaultdict
import json
import urllib.request
import nltk
import re

def write_to_json(idioms_list):
    with open("idioms.json", "w") as f:
        print(json.dumps(idioms_list), file=f)

def handle_idiom_name(idiom_name):
    idiom_name = re.sub("something", "_aw", idiom_name)
    idiom_name = re.sub("someone", "_aw", idiom_name)
    idiom_name = re.sub("somebody", "_aw", idiom_name)
    # tokens_lst = nltk.word_tokenize(idiom_name)
    return idiom_name

def get_idioms_to_json():
    all_idioms = []
    for let in range(ord("a"), ord("z")+1):
        page = 1
        while(True):
            print(chr(let), page)
            url = "https://www.usingenglish.com/reference/idioms/" + chr(let) +\
                  ".html?page=" + str(page)
            r = urllib.request.urlopen(url)
            soup = BeautifulSoup(r, "html.parser")
            i_html = soup.find("dl", id="expandable")
            idioms = []
            for idiom, definition in zip(i_html.find_all("dt"), \
                    i_html.find_all("dd")):
                idioms.append({"idiom_name" :
                    handle_idiom_name(idiom.a.get_text().strip().lower()),
                               "definition":
                    definition.get_text().strip().lower()})
            if len(idioms) == 0:
                break
            all_idioms.extend(idioms)
            page += 1
    write_to_json(all_idioms)


get_idioms_to_json()

with open("idioms.json") as f:
    idioms = {idiom["idiom_name"]: idiom["definition"] for idiom in json.loads(f.read().strip())}

print([nltk.word_tokenize(word) for word in idioms.keys()])
