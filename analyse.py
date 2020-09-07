#%%
from crawl import crawl

import ktrain
from loguru import logger
import matplotlib.pyplot as plt
import numpy as np
import os
import seaborn as sns
import tensorflow as tf
from tensorflow.python.keras import backend as K
import yaml
#%%
logger.info('Loading predictor')
bert_topic = ktrain.load_predictor('models/bert_20ng/trained_bert_4epochs_2e-2')
#%%
ARTICLE1 = "Google_2_en.yml"
ARTICLE2 = "Google_9_en.yml"

with open(f"articles/{ARTICLE1}") as f:
    article1 = yaml.load(f)
with open(f"articles/{ARTICLE2}") as f:
    article2 = yaml.load(f)
# %%
inp = bert_topic.model.input
outs = bert_topic.model.layers[-2].output

functor = K.function([inp, K.symbolic_learning_phase()], outs)

#%%
embeddings1 = []

for p in article1['paragraphs']:
    preproc = bert_topic.preproc.preprocess(p)
    out = functor([preproc, True])
    embeddings1.append(out.prod(axis=0))

embeddings2 = []

for p in article2['paragraphs']:
    preproc = bert_topic.preproc.preprocess(p)
    out = functor([preproc, True])
    embeddings2.append(out.prod(axis=0))

similarities = np.zeros([len(embeddings1), len(embeddings2)])

for idx, embed_x in enumerate(embeddings1):
    for idy, embed_y in enumerate(embeddings2):
        # if embed_x.shape != (768,) or embed_y.shape != (768,):
        #     continue
        similarities[idx, idy] = tf.losses.cosine_similarity(embed_x, embed_y).numpy()

#%%
sns.heatmap(-similarities)
plt.savefig('results.png')
# %%
with open('results.txt', 'w+') as f:
    for idy, idx in enumerate(similarities.argmin(axis=0)):
        print(article2['paragraphs'][idy], file=f)
        print(article1['paragraphs'][idx], file=f)
        print(file=f)
# %%
