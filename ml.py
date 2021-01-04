from textblob import TextBlob
import random
from sklearn.feature_extraction.text import TfidfVectorizer
from PyDictionary import PyDictionary

class mls:
    def __init__(self, text):
        self.text = text
        self.blob = TextBlob(text)
        self.dictionary = PyDictionary()
        self.sentences = self.text.split(".")
        self.getTags()

    def getTags(self):
        self.noun = {}
        self.properNoun = {}
        self.adjectives = {}

        for i in self.blob.tags:
            if i[1] == 'NNP':
                if i[0] in self.properNoun.keys():
                    self.properNoun[i[0]] += 1
                else:
                    self.properNoun[i[0]] = 1

            if i[1] == 'NN':
                if i[0] in self.noun.keys():
                    self.noun[i[0]] += 1
                else:
                    self.noun[i[0]] = 1

            if i[1] == 'JJ':
                if i[0] in self.adjectives.keys():
                    self.adjectives[i[0]] += 1
                else:
                    self.adjectives[i[0]] = 1

        self.properNoun = dict(sorted(self.properNoun.items(), key=lambda item: item[1], reverse=True))
        self.noun = dict(sorted(self.noun.items(), key=lambda item: item[1], reverse=True))
        self.adjectives = dict(sorted(self.adjectives.items(), key=lambda item: item[1], reverse=True))

    def getBlanks(self):

        tempSentense = set()
        tempBlanks = []

        for i in list(self.properNoun.keys()) + list(self.noun.keys()):
            for j in self.sentences:
                if i in j and j not in tempSentense:
                    tempSentense.add(j)
                    r1 = {}
                    r1["blank"] = j.replace(i, "_____")
                    r1["answer"] = i

                    tempArr = list(self.properNoun.keys()) + list(self.noun.keys())
                    tempArr.remove(i)

                    r1["option1"] = random.choice(tempArr)
                    tempArr.remove(r1["option1"])

                    r1["option2"] = random.choice(list(self.noun.keys()))
                    r1["option3"] = "None of the above"
                    tempBlanks.append(r1)

        self.blanks = tempBlanks[0]
        return self.blanks

    def getBool(self):
        tempOppo = []
        for i in self.adjectives.keys():
            if len(tempOppo) == 2:
                break
            val = self.dictionary.antonym(i)
            if val is not None:
                tempOppo.append([i, val[0]])

        self.bool = []
        for i in tempOppo:
            for j in self.sentences:
                if i[0] in j:
                    ch = random.choice([0, 1])
                    if ch == 0:
                        self.bool.append({"bool": j, "answer": True})
                    else:
                        self.bool.append({"bool": j.replace(i[0], i[1]), "answer": False})

        return random.choice(self.bool)

    def getResponse(self):
        resp = {"blank": self.getBlanks(), "bool": self.getBool()}
        return resp
