# coding=utf-8
# !/usr/bin/python
import pandas as pd
import re
import jieba.analyse
from wordcloud import WordCloud,ImageColorGenerator
import numpy as np
from PIL import Image
import copy
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfTransformer

import matplotlib.pyplot as plt

df = pd.read_csv(r"./data/20033948.txt",sep="`",names=['href','title','author','content','images'],header = None)
df = pd.DataFrame({'content':df['title'] + ' ' + df['content']})

#过滤HTML
df['content']=df.apply(lambda x: re.sub('<[^>]+>','',x['content'].replace("&lt;","<").replace("&gt;",">")),axis=1)

# 停用词
stopwordfile=r"./dict/hagongda.txt"
STOP_WORDS = set((
    "the", "of", "is", "and", "to", "in", "that", "we", "for", "an", "are",
    "by", "be", "as", "on", "with", "can", "if", "from", "which", "you", "it",
    "this", "then", "at", "have", "all", "not", "one", "has", "or", "that"
))
content = open(stopwordfile, 'rb').read().decode('utf-8')
for line in content.splitlines():
    STOP_WORDS.add(line)

#分析每个回答
df['content']=df.apply(lambda x:" ".join([word for word in jieba.cut(x['content']) if word not in STOP_WORDS]) ,axis=1)
df = df.reset_index()
df['idx']=df.index

# Images 读取背景图片
color_mask = np.array(Image.open(r"./dict/v.jpg"))
image_colors = ImageColorGenerator(color_mask)

# 设置词云
wc = WordCloud(background_color="white",  # 设置背景颜色
               mask=color_mask,  # 设置背景图片
               max_words=500,  # 设置最大显示的字数
               # stopwords = "", #设置停用词
               font_path=r"C:\Windows\Fonts\msyh.ttf",
               # 设置中文字体，使得词云可以显示（词云默认字体是“DroidSansMono.ttf字体库”，不支持中文）
               max_font_size=60,  # 设置字体最大值
               random_state=30,  # 设置有多少种随机生成状态，即有多少种配色方案
               )

#计算每个回答TF-IDF
xiaopengdf = copy.deepcopy(df[df['content'].str.contains('小鹏')])
xiaopengdf = xiaopengdf.reset_index()
xiaopengdf['idx']=xiaopengdf.index

vectorizer = CountVectorizer()
sentences = xiaopengdf['content']
X = vectorizer.fit_transform(sentences)
words = vectorizer.get_feature_names()

transformer = TfidfTransformer()
tfidf = transformer.fit_transform(X)

wordstfidfs = {}
sentencesidfs = {}
for i in range(len(sentences)):
    sentence_word_tfidf={}
    for j in range(len(words)):
        if tfidf[i,j] > 0:
            sentence_word_tfidf[words[j]]=float(tfidf[i,j])
            wordstfidfs[words[j]]=float(tfidf[i,j])
    sentencesidfs[i]=sentence_word_tfidf

xiaopengdf['words'] = xiaopengdf.apply(lambda x: sentencesidfs[x['idx']],axis=1)

# 生成词
wc.generate_from_frequencies(wordstfidfs)
# 展示词云图
plt.figure()
plt.imshow(wc.recolor(color_func=image_colors),interpolation="bilinear")
plt.axis("off")
#plt.show()
wc.to_file(r'./wordcloud/wordcloud.jpg')


#计算每个回答TF-IDF
sentences = [" ".join(df['content'])]
X = vectorizer.fit_transform(sentences)
words = vectorizer.get_feature_names()
tfidf = transformer.fit_transform(X)
wordstfidfs = {}
sentencesidfs = {}
for i in range(len(sentences)):
    sentence_word_tfidf={}
    for j in range(len(words)):
        if tfidf[i,j] > 0:
            sentence_word_tfidf[words[j]]=float(tfidf[i,j])
            wordstfidfs[words[j]]=float(tfidf[i,j])
    sentencesidfs[i]=sentence_word_tfidf

# 生成词
wc.generate_from_frequencies(wordstfidfs)
# 展示词云图
plt.figure()
plt.imshow(wc.recolor(color_func=image_colors),interpolation="bilinear")
plt.axis("off")
#plt.show()
wc.to_file(r'./wordcloud/wordcloud2.jpg')