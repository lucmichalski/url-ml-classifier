import pandas as pd
import numpy as np
import re
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfTransformer
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report, accuracy_score

random_state = 47
np.random.seed(seed=random_state)


df = pd.read_csv('./dmoz.csv', header=None, names=['url', 'category'])

df = df.dropna()

print('Data set len: ', len(df))

print(df.head())


dict_cat = {
    'Adult': 0,
    'Arts': 1,
    'Business': 2,
    'Computers': 3,
    'Games': 4,
    'Health': 5,
    'Home': 6,
    'Kids': 7,
    'News': 8,
    'Recreation': 9,
    'Reference': 10,
    'Science': 11,
    'Shopping': 12,
    'Society': 13,
    'Sports': 14
}

def to_category_id(item):
    return dict_cat[item]


df['cat_id'] = df['category'].apply(to_category_id)
print(df.head())


def remove_special_char(item):
    return re.sub(r'\W+', '', item)


regex_replace_http = r'(www[0-9][.])'


def replace_http(item):
    item_r = item.replace('http://', '').replace('https://', '').replace('www.', '')
    return re.sub(regex_replace_http, '', item_r)

def only_char(item):
    return re.sub('[^A-Za-z]+', '', item)


df['n_url'] = df['url'].apply(replace_http)


df['norm_url'] = df['n_url'].apply(remove_special_char)
df['url_text'] = df['n_url'].apply(only_char)

print(df.head())

X = df['url_text']
Y = df['cat_id']

count_vectorizer = CountVectorizer(analyzer='char', ngram_range=(3,3)).fit(X)
print('Length of vocabulary: ', len(count_vectorizer.vocabulary_))
urls_tf = count_vectorizer.transform(X)

print('TF shape: ', urls_tf.shape)

print('Data set shape: ', urls_tf.shape)
print('First item: ', urls_tf.getrow(0).toarray())

print('Labels shape: ', Y.shape)

#%%

url_train,url_test,label_train,label_test = train_test_split(urls_tf, Y, test_size=0.3)

X = None
Y = None
urls_tf = None
data_set = None
df = None

url_train = url_train[:600000]

url_train = None
label_train = None

print('Teste shape: ', url_test.shape)
print('Labels teste shape: ',label_test.shape)
print('Data set teste shape: ', url_test.shape)

#%%

print('\n\n================== Starting testing ==================\n\n')

from sklearn.svm import SVC
import datetime

C = 5.5
gamma = 0.05
max_iter = 100

print('C: ', C)
print('Gamma: ', gamma)
print('Max iter: ', max_iter)

print('Start: ', datetime.datetime.now())

model = SVC(C=C, gamma=gamma,random_state=random_state,max_iter=max_iter)
model.fit(url_train,label_train)

print('Finish: ', datetime.datetime.now())

print('Finish training')

predictions = model.predict(url_test)

print(classification_report(label_test, predictions))

np.save('./resultados/label_600k_OnlyTri.npy',np.array(label_test))
np.save('./resultados/saida_600k_OnlyTri.npy',np.array(predictions))