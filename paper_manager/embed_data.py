import numpy as np
import torch
import struct


def update_scibert(table='papers'):
    from .commands import DatabaseManager
    scibert = SciBERT()
    with DatabaseManager() as db:
        db.update(table, scibert.add_embedding, "embedding = X''")

class SciBERT:
    def __init__(self, reduction_model=None):
        from transformers import AutoTokenizer, AutoModel
        self.tokenizer = AutoTokenizer.from_pretrained("allenai/scibert_scivocab_uncased")
        self.model = AutoModel.from_pretrained("allenai/scibert_scivocab_uncased")
        self.reduction_model = reduction_model # XXX placeholder for future integration (after I have established a model and I want to add new papers to database)

    def embed(self, text: str) -> np.ndarray:
        tokens = self.tokenizer(text, return_tensors='pt', padding=True, truncation=True, max_length=512)
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


def convert_to_binary(embedding: torch.Tensor or np.ndarray) -> bytes:
    """ Convert a PyTorch tensor or numpy array embedding to a binary string (bytes).  """
    return struct.pack(f'{len(embedding)}f', *embedding)

import struct
import numpy as np

def convert_from_binary(binary_string: bytes) -> np.ndarray:
    """ Convert a binary string (bytes) back to a numpy array embedding.  """
    num_floats = len(binary_string) // struct.calcsize('f')
    return np.array(struct.unpack(f'{num_floats}f', binary_string))

def translate(input_data: (torch.Tensor or str)) -> (str or torch.Tensor):
    if isinstance(input_data, bytes):
        return convert_from_binary(input_data)
    return convert_to_binary(input_data)

if __name__=='__main__':
    text = 'Hello there margret'
    bert = SciBERT()
    embeding = bert.embed(text)
    print(embeding)
    ## Example tensor
    #tensor = torch.rand(1, 768)
    #print(tensor)
    #binary = translate(tensor)
    #print(binary)
    #print(type(binary))
    #tensor2 = translate(binary)
    #print(tensor2)
    



"""



-0.662
0.386
0.779
-0.740
-0.594
0.271
-0.501
-1.026
0.248
0.589
0.117
-0.603












"""
