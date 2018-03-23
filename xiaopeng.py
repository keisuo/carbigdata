# coding=utf-8
# !/usr/bin/python
import requests
from  bs4 import BeautifulSoup
import json

import jieba
from wordcloud import WordCloud,ImageColorGenerator
import numpy as np
from PIL import Image
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfTransformer

import matplotlib.pyplot as plt

urls = [
'http://app.peopleapp.com/Api/600/LiveApi/newLiveRoom?articleId=1096381&city=%E5%B9%BF%E5%B7%9E%E5%B8%82&citycode=020&device=e415fd64-9fa1-3442-8bff-0d8ce41e487b&device_model=Redmi%20Pro&device_os=Android%206.0&device_product=Xiaomi&device_size=1080*1920&device_type=1&district=%E5%A4%A9%E6%B2%B3%E5%8C%BA&fake_id=7227487&id=0&interface_code=621&latitude=23.118633&longitude=113.351061&province=%E5%B9%BF%E4%B8%9C%E7%9C%81&province_code=1521788816000&sort_flag=1&type=0&user_id=0&version=6.2.1&securitykey=b596d74ff778cb93f1bb1659388790e9',
'http://app.peopleapp.com/Api/600/LiveApi/newLiveRoom?articleId=1096381&city=%E5%B9%BF%E5%B7%9E%E5%B8%82&citycode=020&device=e415fd64-9fa1-3442-8bff-0d8ce41e487b&device_model=Redmi%20Pro&device_os=Android%206.0&device_product=Xiaomi&device_size=1080*1920&device_type=1&district=%E5%A4%A9%E6%B2%B3%E5%8C%BA&fake_id=7227487&id=24496&interface_code=621&latitude=23.118633&longitude=113.351061&province=%E5%B9%BF%E4%B8%9C%E7%9C%81&province_code=1521788831000&sort_flag=1&type=0&user_id=0&version=6.2.1&securitykey=8525cb10223613766a6ea225f1b1b018',
'http://app.peopleapp.com/Api/600/LiveApi/newLiveRoom?articleId=1096381&city=%E5%B9%BF%E5%B7%9E%E5%B8%82&citycode=020&device=e415fd64-9fa1-3442-8bff-0d8ce41e487b&device_model=Redmi%20Pro&device_os=Android%206.0&device_product=Xiaomi&device_size=1080*1920&device_type=1&district=%E5%A4%A9%E6%B2%B3%E5%8C%BA&fake_id=7227487&id=24507&interface_code=621&latitude=23.118633&longitude=113.351061&province=%E5%B9%BF%E4%B8%9C%E7%9C%81&province_code=1521788839000&sort_flag=1&type=0&user_id=0&version=6.2.1&securitykey=a66e417831f6333476ef5c184be15770',
'http://app.peopleapp.com/Api/600/LiveApi/newLiveRoom?articleId=1096381&city=%E5%B9%BF%E5%B7%9E%E5%B8%82&citycode=020&device=e415fd64-9fa1-3442-8bff-0d8ce41e487b&device_model=Redmi%20Pro&device_os=Android%206.0&device_product=Xiaomi&device_size=1080*1920&device_type=1&district=%E5%A4%A9%E6%B2%B3%E5%8C%BA&fake_id=7227487&id=24517&interface_code=621&latitude=23.118633&longitude=113.351061&province=%E5%B9%BF%E4%B8%9C%E7%9C%81&province_code=1521788843000&sort_flag=1&type=0&user_id=0&version=6.2.1&securitykey=4a1375b89877d010bc713a89021a69ee'
]
user_agent = "Mozilla/5.0 (Windows NT 10.0; WOW64; rv:52.0) Gecko/20100101 Firefox/52.0"
headers = {'user-agent': user_agent}

wens = []
das = []
for url in urls:
    r = requests.get(url, headers = headers)
    data = json.loads(r.content)
    for comment in data['data']:
        tcomment= comment['comment_content'].strip()
        if tcomment.startswith('主持人'):
            wens.append(tcomment)
        else:
            das.append(tcomment)

# 写入文件
with open('./data/wens.txt', 'w', encoding='utf-8') as f:
    f.write(" ".join(wens))
with open('./data/das.txt', 'w', encoding='utf-8') as f:
    f.write(" ".join(das))

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

# Images 读取背景图片
color_mask = np.array(Image.open(r"./dict/v.jpg"))
image_colors = ImageColorGenerator(color_mask)

# 设置词云
wc = WordCloud(background_color="white",  # 设置背景颜色
               mask=color_mask,  # 设置背景图片
               max_words=200,  # 设置最大显示的字数
               # stopwords = "", #设置停用词
               font_path=r"C:\Windows\Fonts\msyh.ttf",
               # 设置中文字体，使得词云可以显示（词云默认字体是“DroidSansMono.ttf字体库”，不支持中文）
               max_font_size=60,  # 设置字体最大值
               random_state=30,  # 设置有多少种随机生成状态，即有多少种配色方案
               )

# SKLearn TFIDF
vectorizer = CountVectorizer()
transformer = TfidfTransformer()

# 分析问得问题
sentences = [" ".join([word for word in jieba.cut(open('./data/wens.txt', 'rb').read().decode('utf-8')) if word not in STOP_WORDS])]
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
wc.to_file('./data/wens.jpg')
# 分析回答内容
sentences = [" ".join([word for word in jieba.cut(open('./data/das.txt', 'rb').read().decode('utf-8')) if word not in STOP_WORDS])]
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
wc.to_file('./data/das.jpg')
