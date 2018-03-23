# coding=utf-8
# !/usr/bin/python
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from bs4 import BeautifulSoup
import time
import random


class Answer():
    author = None
    content = None
    images = None

    def log(self):
        print(self.author,self.content,self.images)

    def __init__(self,author,content,images):
        self.author=author
        self.content=content
        self.images =images

class Question():
    href = None
    title = None
    answers = None
    def __init__(self,href,title):
        self.href=href
        self.title=title
        self.answers = []
    def appendAnswer(self,answer):
        self.answers.append(answer)


class ZhihuSpider():
    question = None
    driver = None
    def __init__(self,questionId):
        self.driver = webdriver.Chrome(executable_path=r"D:\Development\chromedriver\chromedriver.exe")
        self.question = questionId
    def spider(self):
        # 1.爬取互联网汽车精华问题
        carUrl="https://www.zhihu.com/topic/"+self.question+"/top-answers"
        self.driver.get(carUrl)
        print(self.driver.title)
        self.scroll()
        # 2.等待滑到最下面
        time.sleep(120)
        hrefinfos=self.driver.find_elements_by_xpath("//h2[@class='ContentItem-title']//a[contains(@href,'question') or contains(@href,'zhuanlan.zhihu.com')]")
        hrefs= []
        zhuanlanhrefs=[]
        for info in hrefinfos:
            href = info.get_attribute('href');
            if 'zhuanlan'in href:
                zhuanlanhrefs.append(href)
            else:
                hrefs.append(href[0:(href.find('answer')-1)])

        # 3.问题详情页详情页(专题页略过)
        questions = []
        hrefs = list(set(hrefs))
        for href in hrefs:
            self.driver.get(href)
            print(href,self.driver.title)
            question = Question(href,self.driver.title)
            self.scroll()
            # 等待滑到最下面
            time.sleep(60)
            # 找到所有的展开阅读全文
            readbuttons= self.driver.find_elements_by_css_selector("button[class='Button ContentItem-rightButton Button--plain'][type='button']")
            for button in readbuttons:
                #driver.execute_script("arguments[0].click();", element)
                button.send_keys(Keys.SPACE)
                time.sleep(5)
            html = self.driver.page_source
            # 爬取内容
            soup= BeautifulSoup(html,'lxml')
            storys =soup.find_all('div',{'class':'List-item'})
            # 爬取所有回答内容
            for story in storys:
                try:
                    nameLabel = story.find('div',{'itemprop':'author'}).find('meta',{'itemprop':'name'})
                    name = nameLabel['content']
                    rich = story.find('span', {'class': 'RichText CopyrightRichText-richText'})
                    images = []
                    if rich.find('img'):
                       imgs = rich.find_all('img')
                       for img in imgs:
                           images.append(img['src'])
                    storyText = rich.get_text()
                    strimages = ""
                    if len(images)>0:
                        strimages = ",".join(images)
                    answer = Answer(str(name),repr(storyText),strimages)
                    answer.log()
                    question.appendAnswer(answer)
                except Exception as ex:
                    print(ex)
            questions.append(question)

        #写入文件
        with open("./data/"+self.question + '.txt', 'w', encoding='utf-8') as f:
            for question in questions:
                href=question.href
                title=question.title
                answers=question.answers
                for answer in answers:
                    msg = '\''+href +'\'`\''+ title+'\'`\''+answer.author +'\'`'+answer.content+'`\''+answer.images+'\'\n'
                    f.write(msg)
        print('That is all')

    def scroll(self):
        waitSecond=random.randint(1,10)*1000
        steps = [100,110,120,130,140,150,160,170,180,190,200,210,220,230,240,250,260,270,280,290,300]
        step = random.choice(steps)
        script= """
                   (function () {
                       var y = document.body.scrollTop;
                       var step = $Step;
                       window.scroll(0, y);
                       function f() {
                           if (y < document.body.scrollHeight) {
                               y += step;
                               window.scroll(0, y);
                               setTimeout(f, 50);
                           }
                           else {
                               window.scroll(0, y);
                               document.title += "scroll-done";
                           }
                       }
                       setTimeout(f, $WaitSecond);
                   })();
                   """
        script = script.replace('$Step',str(step))
        script = script.replace('$WaitSecond',str(waitSecond))
        self.driver.execute_script(script)
    def __del__(self):
        self.driver.close()

if __name__=="__main__":
    spider=ZhihuSpider('20033948')
    spider.spider()








