from transformers import AutoTokenizer, AutoModelForCausalLM
import tensorflow as tf

class Llama7bEmbedding:
    def __init__(self):
        self.tokenizer =  AutoTokenizer.from_pretrained("deerslab/llama-7b-embeddings")
        self.model = AutoModelForCausalLM.from_pretrained("deerslab/llama-7b-embeddings")

    def encode(self, text):
        tokens = self.tokenizer(text, padding=True, truncation=True, return_tensors="tf")
        embeddings = self.model(tokens)[0]
        #return tf.reduce_mean(embeddings, axis=1)

    def predict(self, text):
        embeddings = self.encode(text)
        # Perform inference using the embeddings
        # Return the predicted output
