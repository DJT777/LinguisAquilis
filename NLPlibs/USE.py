from absl import logging

import tensorflow as tf

import tensorflow_hub as hub
from tensorflow.python.ops.numpy_ops import np_config
import matplotlib.pyplot as plt
import numpy as np
import os
import pandas as pd
import re
import seaborn as sns
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity

np_config.enable_numpy_behavior()


class USE:
    def __init__(self, model_url):
        self.model = hub.load('/home/dylan/Desktop/repos/CS478-LinguisAquilis/models/USE')
        self.type = 'USE'


    def embed(self, text):
        returned_list = []
        output = self.model(text)
        #output = output.detach().cpu().numpy()
        print(output)
        returned_list.append(output)
        return returned_list

    def compare(self, input_embedding, dict_list):
        # Compare the input embedding with the 'USE_embedding' key in each dictionary
        similarities = []
        input_embedding = np.array(input_embedding)
        for i, dictionary in enumerate(dict_list):
            use_embedding = np.array(dictionary['USE_embedding'])
            similarity = cosine_similarity(input_embedding.reshape(-1, 512), use_embedding.reshape(-1, 512))[0][0]
            print(similarity)
            similarities.append((i, similarity))

        # Sort the similarities in descending order
        sorted_similarities = sorted(similarities, key=lambda x: x[1], reverse=True)

        # Return the sorted similarities
        return sorted_similarities



