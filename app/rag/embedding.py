from sentence_transformers import SentenceTransformer
#get model from https://huggingface.co/intfloat/multilingual-e5-small and save it to the local directory
model = SentenceTransformer('intfloat/multilingual-e5-small', device='cpu', cache_folder='./app/model')
# model = SentenceTransformer('intfloat/multilingual-e5-small')

def get_embedding(text):
    return model.encode(text)