import requests
from collections import defaultdict
import json


def get_app_id_key():
    """
    Get app_id and app_key for this app
    """
    app_id = '0dd8f390'
    app_key = '1671423a9398f671e334350676749918'
    return app_id, app_key


def get_oxf_definitions(word):
    """
    Get definations of word from Oxford API
    """
    app_id, app_key = get_app_id_key()
    url = "https://od-api.oxforddictionaries.com:443/api/v1/entries/en/" + word
    r = requests.get(url, headers={"app_id": app_id, "app_key": app_key})
    word_definition_dict = defaultdict(list)
    for lexical_category in json.loads(r.text)["results"][0]["lexicalEntries"]:
        for definition in lexical_category["entries"][0]["senses"]:
            # Using try-except because some words don't have examples
            try:
                word_definition_dict[
                    lexical_category["lexicalCategory"]].append({
                        "definition": definition["definitions"][0],
                        "example": definition["examples"][0]["text"]
                })
            except KeyError:
                word_definition_dict[
                    lexical_category["lexicalCategory"]].append({
                        "definition": definition["definitions"][0],
                        "example": None
                })

    return word_definition_dict


def get_lemmas(word):
    """
    Get all lemmas of a word from Oxford API
    """
    app_id, app_key = get_app_id_key()
    url = "https://od-api.oxforddictionaries.\
com:443/api/v1/inflections/en/" + word
    ret = requests.get(url, headers={"app_id": app_id, "app_key": app_key})
    possible_lemmas = defaultdict(list)
    for entry in json.loads(ret.text)["results"][0]["lexicalEntries"]:
        for lemma in entry["inflectionOf"]:
            possible_lemmas[entry["lexicalCategory"]].append(lemma["text"])
    return possible_lemmas


def get_lexical_categories():
    """
    Get English lexical categories
    """
    app_id, app_key = get_app_id_key()
    url = "https://od-api.oxforddictionaries.com:443/api/v1/\
lexicalcategories/en"
    ret = requests.get(url, headers={"app_id": app_id, "app_key": app_key})
    return json.loads(ret.text)["results"]
