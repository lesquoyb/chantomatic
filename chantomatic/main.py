import re


class Markov:

    def __init__(self):
        self.bigrams = {}
        self.transitionMatrix = {}

    def generateTransitionMatrix(self):
        for word in self.bigrams.keys():
            self.transitionMatrix[word] = {}
            for w in self.bigrams[word].keys():
                total = 0.0
                p = 0
                for k in self.bigrams[word]:
                    total += self.bigrams[word][k]
                    if w == k:
                        p = self.bigrams[word][k]
                self.transitionMatrix[word][w] = p/total

    def getProbability(self, word, knowing):
        if knowing not in self.bigrams or word not in self.bigrams[knowing]: #si le mot n'est pas dans l'espace d'état on retourne 0
            return 0
        return self.transitionMatrix[knowing][word]

    def sentenceProbability(self, sentence, knowing):
        words = [word.upper() for word in self.split(sentence)]
        if not knowing:
            k = "."
            start = 0
        else:
            k = words[0]
            start = 1

        prob = 1
        for word in words[start:]:
            prob *= self.getProbability(word.upper(), k)
            k = word.upper()
        return prob

    def parse(self, file):

        f = open(file, "r", encoding="latin1").read()
        #f = "bonjour comment ca va bonjour ca va salut ca va bien salut comment ca va bonjour"
        words = self.split(f)
        words.insert(0, ".")
        self.bigrams[words[-1].upper()] = {".": 1}
        for i, word in enumerate(words[1:]):
                word = word.upper()
                prev = words[i].upper()
                if prev in self.bigrams:
                    if word in self.bigrams[prev]:
                        self.bigrams[prev][word] += 1
                    else:
                        self.bigrams[prev][word] = 1
                else:
                    self.bigrams[prev] = {word: 1}
        self.generateTransitionMatrix()

    def split(self, sentence):
        return [x for x in re.split('[?*#<>()!.,\\n\\r\\t \\x96]', sentence) if x != '']

    def musicGen(self, startingWord=None, endingWord=None):

        import random
        sentence = ""
        prev = random.Random().choice([w for w in self.transitionMatrix.keys()]) if not startingWord else startingWord
        last = random.Random().choice([w for w in self.transitionMatrix.keys()]) if not endingWord else endingWord
        while True:
            p = random.random()
            s = 0
            for w in self.transitionMatrix[prev].keys():
                s += self.transitionMatrix[prev][w]
                if p < s:
                    sentence += w + " "
                    prev = w
                    if w == last:
                        return sentence
                    break
        return sentence
if __name__ == "__main__":
    pretexte = "bonjour comment ca va bonjour ca va salut ca va bien salut comment ca va bonjour"
    m = Markov()
    m.parse("../texteTest/Beyonce.txt")
    #print(m.transitionMatrix)
    #print(m.sentenceProbability("oh i asked you", True))
    print(m.musicGen())

