import gensim.downloader as api
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
import nltk
from nltk.tokenize import word_tokenize

# Download NLTK tokenizer if not available
#inltk.download('punkt')

# Load pre-trained Word2Vec model (Google News or another)
print("Loading Word2Vec model...")
model = api.load("word2vec-google-news-300")  # 300-dimensional vectors

# Function to compute sentence vector
def sentence_vector(sentence, model):
    words = word_tokenize(sentence.lower())  # Tokenize and lowercase
    word_vectors = [model[word] for word in words if word in model]  # Get vectors
    if not word_vectors:  # Handle case where no words are found
        return np.zeros(model.vector_size)
    return np.mean(word_vectors, axis=0)  # Average word vectors

# Example sentences
sentence1 = "The cat is sitting on the mat."
sentence2 = "A dog is barking loudly."

# Compute sentence embeddings
vector1 = sentence_vector(sentence1, model)
vector2 = sentence_vector(sentence2, model)

# Compute cosine similarity
similarity = cosine_similarity([vector1], [vector2])[0][0]

# Print result
print(f"Cosine Similarity: {similarity:.4f}")