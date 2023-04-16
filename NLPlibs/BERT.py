import torch
from transformers import AutoTokenizer, AutoModel


class BERT:
    def __init__(self, model_name):
        self.tokenizer = AutoTokenizer.from_pretrained(model_name)
        self.model = AutoModel.from_pretrained(model_name)
        self.model.eval()

    def encode(self, text):
        tokens = self.tokenizer(text, padding=True, truncation=True, return_tensors="pt")
        with torch.no_grad():
            embeddings = self.model(**tokens)[0]
        return embeddings.mean(dim=1)

    def predict(self, text):
        embeddings = self.encode(text)
        # Perform inference using the embeddings
        # Return the predicted output
