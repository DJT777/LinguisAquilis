import tensorflow as tf
import tensorflow_hub as hub
from tensorflow.keras.optimizers import Adam, SGD
from tensorflow.keras.layers import Dense, Input, BatchNormalization, Dropout, Concatenate
from tensorflow.keras.models import Model, Sequential
import numpy as np
import hnswlib
import json
import pandas as pd


# Path to create recommendation class halted because inner classes cannot inherit outer classes
# thus making it impossible to inherit the create embedding method/function from the outer class
class Recommendation:
    def __init__(self):
        self.query = None
        self.queryLabels = None
        self.registrarData = None
        self.helloWorld = "Hello World"
        print(self.helloWorld)

    # Constructor Pass in a query and the labels returned by useLite's create_embedding() and query_embedding() functions
    def __init__(self, userQueryString, userQueryEmbedding, userQueryLabels, userQueryDistances):
        self.user = None
        self.class_json = open('data.json')
        self.class_data = json.load(self.class_json)
        self.p = hnswlib.Index(space='cosine', dim=512)
        self.p.load_index("./data/indexUSE-trained.bin")
        self.userQueryString = userQueryString
        self.userQueryEmbedding = userQueryEmbedding
        self.userQueryLabels = userQueryLabels
        self.queryDistances = userQueryDistances
        self.recommendations_user_text = []
        self.recommended_majors = []
        labels_to_return = userQueryLabels[0]
        print("Your results for your search of " + self.userQueryString + " returned these results...")
        for index in labels_to_return:
            if self.class_data[index]['course_title'] not in userQueryString:
                self.recommendations_user_text.append(self.class_data[index])
                print(self.class_data[index]['course_title'])
                if self.class_data[index]['course_dept'] not in self.recommended_majors:
                    self.recommended_majors.append(self.class_data[index]['course_dept'])
        self.recommended_major = max(self.recommended_majors)
        # self.helloWorld = "Hello World"
        # print(self.helloWorld)


class useLite:
    name = "Hello World"

    def filter_course(course):
        if (course not in class_data):
            return True
        else:
            return False

    def build_model(self):

        module_url = 'https://tfhub.dev/google/universal-sentence-encoder-large/5'
        embed = hub.KerasLayer(module_url, input_shape=[], dtype=tf.string, trainable=True)

        model = Sequential([
            Input(shape=[], dtype=tf.string),
            embed,
            Dense(256, activation='relu', kernel_regularizer=tf.keras.regularizers.L2(0.01)),
            Dropout(0.2),
            Dense(190, activation='softmax')
        ])
        model.compile(Adam(1e-4), loss='sparse_categorical_crossentropy', metrics=['accuracy'])

        model.load_weights('data/model.h5')

        return model

    def create_embeddings(self, text):

        aux_model = tf.keras.Model(inputs=self.model.inputs,
                                   outputs=self.model.outputs + [self.model.layers[0].output])

        classification, course_embedding = aux_model.predict([text])

        return course_embedding

    def classify(self, text):
        test_pred = self.model.predict([text])
        idx = np.argsort(test_pred, axis=1)[:, -5:]
        idx = np.asarray(idx, dtype=int, order=None)
        for i in idx[0]:
            print(self.majorCodes[i] + " Accuracy: " + str(test_pred[0][i]))

        return self.majorCodes[idx[0][-1]], self.majorDict[self.majorCodes[idx[0][-1]] + " "]

    def query_embedding(self, user_description_embedding, user_description_string):
        labels, distances = self.p.knn_query(user_description_embedding, k=6)
        print(labels)
        recommendation = Recommendation(user_description_string, user_description_embedding, labels, distances)
        print(recommendation.userQueryString)
        self.currentRecommendation = recommendation

        return recommendation

    def __init__(self):
        self.model = self.build_model()
        self.class_json = open('data.json')
        self.class_data = json.load(self.class_json)
        self.majorDict = json.load(open('subjects.json'))
        self.df = pd.read_csv("https://waf.cs.illinois.edu/discovery/course-catalog.csv", )
        self.majorCodes = self.df["Subject"].unique()
        self.p = hnswlib.Index(space='cosine', dim=512)
        self.p.load_index("/content/data/indexUSE-trained.bin")
        self.currentRecommendation = None
        # print(self.name)
        # print("A sample embedding")
        # print(self.sampleEmbedding)



