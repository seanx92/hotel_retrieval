from nltk.corpus import wordnet as wn

class MyWordNet(object):

    def __init__(self):
        self.wn_catogories = [wn.synset('clean.a.01'), wn.synset('service.n.01'), wn.synset('value.n.02'), 
                        wn.synset('sleep.n.01'), wn.synset('location.n.01'), wn.synset('room.n.01')]

if __name__ == '__main__':
    # wordnet = MyWordNet()
    # dog = wn.synset('dog.n.01')
    # cat = wn.synset('cat.n.01')
    # print(dog.path_similarity(cat))

        


