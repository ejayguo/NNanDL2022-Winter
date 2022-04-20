from re import I
from nltk.corpus import stopwords

import nltk
from nltk.wsd import lesk
from nltk.corpus import wordnet as wn

import sys
sys.path.append('../')
from utils.utils import clean_str, loadWord2Vec  


if len(sys.argv) != 2:
	sys.exit("Use: python remove_words.py <dataset>")

datasets = ['20ng', 'R8', 'R52', 'ohsumed', 'mr', 'supremecourt']
dataset = sys.argv[1]

THRESHOLD_FREQ = 5
MAX_LENGTH_DOC = 50

if dataset not in datasets:
	sys.exit("wrong dataset name")

nltk.download('stopwords')
stop_words = set(stopwords.words('english'))
stop_words.add("footnote")
stop_words.add("mr")
stop_words.add("mrs")
print(stop_words)

# Read Word Vectors
# word_vector_file = 'data/glove.6B/glove.6B.200d.txt'
# vocab, embd, word_vector_map = loadWord2Vec(word_vector_file)
# word_embeddings_dim = len(embd[0])
# dataset = '20ng'

doc_content_list = []
#with open('data/wiki_long_abstracts_en_text.txt', 'r') as f:
with open('../data/corpus/' + dataset + '.txt', 'rb') as f:
    for line in f.readlines():
        doc_content_list.append(line.strip().decode('latin1'))

doc_label_list = []
with open('../data/' + dataset + '.txt', 'rb') as f:
    for line in f.readlines():
        doc_label_list.append(line.strip().decode('latin1'))

word_freq = {}  # to remove rare words

for doc_content in doc_content_list:
    temp = clean_str(doc_content)
    words = temp.split()
    for word in words:
        if word in word_freq:
            word_freq[word] += 1
        else:
            word_freq[word] = 1

clean_docs = []
clean_labels = []
# for doc_content in doc_content_list:
for idx_doc_content in range(len(doc_content_list)):
    doc_content = doc_content_list[idx_doc_content]
    label_line = doc_label_list[idx_doc_content]
    temp = clean_str(doc_content)
    words = temp.split()
    doc_words = []
    for word in words:
        # word not in stop_words and word_freq[word] >= THRESHOLD_FREQ
        if(len(word)<=1):
            continue

        if dataset == 'mr':
            doc_words.append(word)
        elif (word not in stop_words and \
            #   not word.isnumeric() and \
              word_freq[word] >= THRESHOLD_FREQ):
            doc_words.append(word)

    if(len(doc_words)<=MAX_LENGTH_DOC):
        continue

    doc_str = ' '.join(doc_words).strip()

    #if doc_str == '':
        #doc_str = temp
    clean_docs.append(doc_str)
    clean_labels.append(label_line)

print("Num of Docs: " + str(len(clean_docs)))
print("Num of Labels: " + str(len(clean_labels)))

clean_corpus_str = '\n'.join(clean_docs)
clean_labels_str = '\n'.join(clean_labels)

#with open('../data/wiki_long_abstracts_en_text.clean.txt', 'w') as f:
with open('../data/corpus/' + dataset + '.clean.txt', 'w') as f:
    f.write(clean_corpus_str)

with open('../data/' + dataset + '.clean.txt', 'w') as f:
    f.write(clean_labels_str)

#dataset = '20ng'
min_len = 10000
aver_len = 0
max_len = 0 

#with open('../data/wiki_long_abstracts_en_text.txt', 'r') as f:
with open('../data/corpus/' + dataset + '.clean.txt', 'r') as f:
    lines = f.readlines()
    for line in lines:
        line = line.strip()
        temp = line.split()
        aver_len = aver_len + len(temp)
        if len(temp) < min_len:
            min_len = len(temp)
        if len(temp) > max_len:
            max_len = len(temp)

aver_len = 1.0 * aver_len / len(lines)
print('Min_len : ' + str(min_len))
print('Max_len : ' + str(max_len))
print('Average_len : ' + str(aver_len))
