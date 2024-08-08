import numpy as np
import torch
import struct


def update_scibert(table='papers'):
    from .commands import db
    bert = SciBERT()
    with db() as d_b:
        d_b.edit(table, bert.add_embedding, lambda paper : paper[6]==b'')

class SciBERT:
    def __init__(self, reduction_model=None):
        from transformers import AutoTokenizer, AutoModel
        # Load SciBERT model and tokenizer
        self.tokenizer = AutoTokenizer.from_pretrained("allenai/scibert_scivocab_uncased")
        self.model = AutoModel.from_pretrained("allenai/scibert_scivocab_uncased")
        self.reduction_model = None # TODO - implement way to give a basic reduction model that all the embedded vectors will be reduced by.

    def embed(self, text: str) -> torch.Tensor:
        tokenized = self.tokenizer(text, return_tensors="pt", padding=True, truncation=True, max_length=512)
        with torch.no_grad():
            outputs = self.model(**tokenized)
        return outputs.last_hidden_state[:, 0, :].squeeze().numpy() # squeeze removes batch dimension
    
    def add_embedding(self, paper_tup):
        text = f'{paper_tup[1]}: \n{paper_tup[2]}'
        embedding = translate(self.embed(text))
        return (paper_tup[i] if i!=6 else embedding for i in range(len(paper_tup)))


def embedding_to_binary(embedding: torch.Tensor or np.ndarray) -> bytes:
    """
    Convert a PyTorch tensor or numpy array embedding to a binary string (bytes).

    Args:
    - embedding (torch.Tensor or np.ndarray): The embedding to convert.

    Returns:
    - bytes: The binary string (bytes) representation of the embedding.
    """
    if isinstance(embedding, torch.Tensor):
        # Convert tensor to numpy array and flatten
        embedding = embedding.numpy().flatten()
    elif isinstance(embedding, np.ndarray):
        # Flatten numpy array if not already flattened
        embedding = embedding.flatten()

    return struct.pack(f'{len(embedding)}f', *embedding)

def binary_to_embedding(binary_string: bytes) -> np.ndarray:
    """
    Convert a binary string (bytes) back to a numpy array embedding.

    Args:
    - binary_string (bytes): The binary string representation of the embedding.

    Returns:
    - np.ndarray: The reconstructed embedding numpy array.
    """
    # Calculate the number of floats
    num_floats = int(len(binary_string) / struct.calcsize('f'))
    
    # Unpack the binary string into a numpy array
    unpacked_array = struct.unpack(f'{num_floats}f', binary_string)
    
    # Convert the list to a numpy array and reshape it to [1, 768]
    return np.array(unpacked_array).reshape(1, 768)


def translate(inputt:(torch.Tensor or str)) -> (str or torch.Tensor):
    if isinstance(inputt, bytes):
        return binary_to_embedding(inputt)
    return embedding_to_binary(inputt)

if __name__=='__main__':
    # Example tensor
    tensor = torch.rand(1, 768)
    print(tensor)
    binary = translate(tensor)
    print(binary)
    print(type(binary))
    tensor2 = translate(binary)
    print(tensor2)
    

