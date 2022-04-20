import numpy as np
import textacy.datasets

data_dir = './sc'
ds = textacy.datasets.SupremeCourt(data_dir)

ds.download()
print(ds.info)

# for text in ds.texts(limit=1):
    
#     print(text, end="\n\n")
#     print("------------------------------------------")
#     print(type(text))
#     text_x = text.replace('\n', '')
#     print(text_x)

dataset_name = 'supremecourt'
sentences = []
labels = []
meta_data_list = []
train_or_test_list = ['train', 'test']

idx = 0
PROB_TEST = 0.8

# for text_raw, meta_raw in ds.records(limit=1000):
for text_raw, meta_raw in ds.records():
    # print("------------------------------------------")
    # print(meta, end="\n\n")
    # print("\n{} ({})\n{}".format(meta["case_name"], meta["decision_date"], text[:500]))
    # print(text_raw)
    label = str(meta_raw['issue_area'])

    if(label == '-1' or label == '14'):
        continue

    text = text_raw.replace('\n', '')
    # print(text)
    
    idx_end = text.find("[Footnote")
    if(idx_end != -1):
        text_no_footnote = text[:idx_end]
        sentences.append(text_no_footnote)
    else:
        sentences.append(text)

    type = train_or_test_list[0]

    prob_test = np.random.uniform()
    if(prob_test >= PROB_TEST):
        type = train_or_test_list[1]
    
    meta = str(idx) + '\t' + type + '\t' + label

    meta_data_list.append(meta)

    if(label not in labels):
        labels.append(label)

    idx += 1



meta_data_str = '\n'.join(meta_data_list)

f = open('data/' + dataset_name + '.txt', 'w')
f.write(meta_data_str)
f.close()

corpus_str = '\n'.join(sentences)

f = open('data/corpus/' + dataset_name + '.txt', 'w')
f.write(corpus_str)
f.close()