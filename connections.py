# -*- coding: utf-8 -*-
"""
Created on Tue Feb 07 11:00:00 2023

@author: jhutchison

"""

# %% Packages
""" Third party and local imports """

import pathlib

from transformers import AutoTokenizer, AutoModel
import torch
import numpy as np
from sklearn.cluster import KMeans
from scipy.spatial.distance import cosine


# %% Functions
""" Define functions """

def get_word_embedding(word):
    """Get the embedding of a single word."""
    inputs = tokenizer(word, return_tensors="pt")
    outputs = model(**inputs)
    return outputs.last_hidden_state.mean(dim=1).squeeze()

def calculate_similarity(word1, word2):
    """Calculate cosine similarity between two words."""
    embedding1 = get_word_embedding(word1)
    embedding2 = get_word_embedding(word2)
    return 1 - cosine(embedding1.detach().numpy(), embedding2.detach().numpy())


# %% Variables
""" Set script (global) variables """

path_data = pathlib.Path("data/")


# %% Main
""" Display task data """

if __name__ == "__main__":
    # print("logger update here, main complete")

    # Load a pre-trained model and tokenizer
    model_name = "bert-base-uncased"
    tokenizer = AutoTokenizer.from_pretrained(model_name)
    model = AutoModel.from_pretrained(model_name)

    # Example words
    words = ["apple", "banana", "orange", "car", "bike", "train", "joy", "happiness", "sadness", "anger"]
    words = [
    "travel",
    "cheers",
    "frasier",
    "poetry",
    "whooping",
    "euphoria",
    "felciity",
    "huge",
    "ficition",
    "consturcution",
    "big",
    "great",
    "glee",
    "giant",
    "paper",
    "humor",
    ]

    # Embedding the words
    word_embeddings = np.array([get_word_embedding(word).detach().numpy() for word in words])

    # Calculate similarities (Example)
    similarity_matrix = np.array([[calculate_similarity(w1, w2) for w2 in words] for w1 in words])

    # Initial clustering (Example with K-means)
    num_clusters = 4  # Assuming we need to form 4 groups
    kmeans = KMeans(n_clusters=num_clusters, random_state=0).fit(word_embeddings)
    clusters = kmeans.labels_

    # Show the clusters
    clustered_words = {i: [] for i in range(num_clusters)}
    for word, cluster in zip(words, clusters):
        clustered_words[cluster].append(word)

    clustered_words

