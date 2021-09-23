import requests

class Dictionary:
    def get_synonyms_or_antonyms(self, word, type_of_words):
        if type_of_words not in ["synonyms", "antonyms"]:
            return "Dude! Please give a corrent type of words you want."
        s = requests.get(f"https://tuna.thesaurus.com/pageData/{word}")
        li_1 = [y for x in [s.json()["data"]["definitionData"]["definitions"][0][type_of_words], s.json()["data"]["definitionData"]["definitions"][1][type_of_words]] for y in x]
        li = [y["term"] for y in li_1]
        return li
