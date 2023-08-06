import os
import pickle
import nltk
from nltk.stem.lancaster import LancasterStemmer
import numpy
import tflearn
import tensorflow
import random
import json

stemmer = LancasterStemmer()


class ChatBot():
    
    def __init__(self, dataSource, Dev):
        ####Initializations####
        global data
        global words
        global model
        global chatting
        global words
        words = []
        global labels
        labels = []
        global docsX
        docsX = []
        global docsY
        docsY = []
        ####Initializations####

        with open(dataSource) as file:
            data = json.load(file)


        for intent in data["intents"]:
            for pattern in intent["patterns"]:
                tokens = nltk.word_tokenize(pattern)
                words.extend(tokens)
                docsX.append(tokens)
                docsY.append(intent["tag"])

                if intent["tag"] not in labels:
                    labels.append(intent["tag"])

        words = [stemmer.stem(w.lower()) for w in words if w != "?"]
        words = sorted(list(set(words)))

        labels = sorted(labels)

        training = []
        output = []

        out_empty = [0 for _ in range(len(labels))]

        for x, doc in enumerate(docsX):
            bag = []
            tokens = [stemmer.stem(w) for w in doc]
            for w in words:
                if w in tokens:
                    bag.append(1)
                else:
                    bag.append(0)

            output_row = out_empty[:]
            output_row[labels.index(docsY[x])] = 1

            training.append(bag)
            output.append(output_row)

        training = numpy.array(training)
        output = numpy.array(output)

        with open("data.pickle","wb") as model:
            pickle.dump((words, labels, docsX, docsY),model)

        tensorflow.reset_default_graph()
        dnnIn = tflearn.input_data(shape=[None , len(training[0])])
        layer1 = tflearn.fully_connected(dnnIn, 8)
        layer2 = tflearn.fully_connected(layer1, 8)
        layer3 = tflearn.fully_connected(layer2, 8)
        layer4 = tflearn.fully_connected(layer3, 8)
        nNet = tflearn.fully_connected(layer4, len(output[0]), activation = "softmax")
        reggModel = tflearn.regression(nNet)

        self.model = tflearn.DNN(reggModel)
        self.model.fit(training, output, n_epoch = 1000, batch_size=8, show_metric = True)

    def words_list(self, s, words):
        print(words)
        bag = [0 for _ in range(len(words))]

        s_words = nltk.word_tokenize(s)
        s_words = [stemmer.stem(word.lower()) for word in s_words]

        for se in s_words:
            for i, w in enumerate(words):
                if w == se:
                    bag[i] = 1
        if dev:
            print(bag)
        
        return numpy.array(bag)

    def chat(self):
            self.chatting = True
            while self.chatting:
                inp = input("You: ")
                if inp.lower() == "quit":
                    break
                
                res = self.model.predict([self.words_list(inp, words)])
                if dev:
                    print(res)
                res_index = numpy.argmax(res)
                res = ""
                tag = labels[res_index]
                if dev:
                    print(labels)

                for tg in data["intents"]:
                    if tg["tag"] == tag:
                        #print(tg)
                        response_l = tg["responses"]
                        response = random.choice(response_l)
                        print(response)


    def endChat(self):
        self.chatting = False

    

#if __name__ == "__main__":
#    bot = ChatBot("intents.json")
#    bot.chat()
#    bot.endChat()