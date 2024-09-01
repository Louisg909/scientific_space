import numpy as np
import torch
import struct

class SciBERT:
    def __init__(self, reduction_model=None):
        from transformers import AutoTokenizer, AutoModel
        self.tokenizer = AutoTokenizer.from_pretrained("allenai/scibert_scivocab_uncased")
        self.model = AutoModel.from_pretrained("allenai/scibert_scivocab_uncased")
        self.reduction_model = reduction_model # XXX placeholder for future integration (after I have established a model and I want to add new papers to database)

    def embed(self, text: str, length=512) -> np.ndarray:
        tokens = self.tokenizer(text, return_tensors='pt', padding=True, truncation=True, max_length=length)
        # Disable gradient calculations as we're only performing inference
        with torch.no_grad():
            outputs = self.model(**tokens)
        
        embedding = outputs.last_hidden_state[0, 0, :].numpy()
        if len(embedding.shape) != 1:
            raise ValueError(f"Embedding has an invalid shape: {embedding.shape}. Expected shape is (X,).")
        return embedding
    
    def add_embedding(self, paper_tuple):
        text = f'{paper_tuple[1]}: \n{paper_tuple[2]}'
        embedding = convert_to_binary(self.embed(text))
        return tuple(embedding if i == 6 else paper_tuple[i] for i in range(len(paper_tuple)))


