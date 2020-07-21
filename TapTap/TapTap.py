import requests
from bs4 import BeautifulSoup
from requests.exceptions import RequestException
import pandas as pd
import re

import json

headers = {
    'user-agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.102 Safari/537.36"}

def get_page_index(url):
    try:
        respones = requests.get(url, headers=headers)  # get请求
        if respones.status_code == 200:
            return respones.text
        return None
    except RequestException:
        print("请求有错误")
        return None

def parse_one_page(html):
    soup = BeautifulSoup(html, 'lxml')
    board_wrapper = soup.find_all('dl', class_='board-wrapper')[0]
    board_index = board_wrapper.find_all('dd')
    for link in board_index:
        title = link.find_all('p', class_='name')[0].text
        board_index = link.find_all('i')[0].text
        star = link.find_all('p', class_='star')[0].text.strip()[3:]
        releasetime = link.find_all('p', class_='releasetime')[0].text.strip()[5:]
        score = link.find_all('p', class_='score')[0].text
        print(board_index, title, star, releasetime, score) 


url_download='C:\\Users\\admin\\Desktop\\Luna的取数宝宝\\20200720\\luna0-80000.xlsx'

row_data=pd.read_excel(url_download)

#url_download2='C:\\Users\\admin\\Desktop\\Luna的取数宝宝\\20200720\\luna80000-200000.xlsx'

#row_data2=pd.read_excel(url_download2)

del row_data['Unnamed: 0']

row_data.rename(columns={'app':'app_id'},inplace=True)

row_data['app_name']=''

list_app=[]

for i in range(10000,20000):
    dic={}
    id_num=row_data['app_id'][i]
    url='https://www.taptap.com/app/{}'.format(id_num)
    
    html = get_page_index(url)

    soup = BeautifulSoup(html, 'lxml')
    soup1=soup.find_all(class_='main-header-text')[0]
    
    #app_id
    dic['app_id']=str(id_num)
    
    #appname
    name_content=soup1.find('h1').contents[0].string
    name=''
    name=name.join(name_content).rstrip()
    dic['app_name']=name
    
    #creater_info
    try:
        content1=soup1.find_all(class_='header-text-author')
        for j in range(len(content1)):
            info=content1[j].findAll('span')
            if(len(info)==0):
                continue
            dic_name=''.join(info[0].contents[0].string)
            dic_name=dic_name.replace(': ','')
            
            dic_info=''.join(info[1].contents[0].string)
            dic_info=dic_info.replace(': ','')
            dic[dic_name]=dic_info
    except:
        print('creater_info is null')
    
    #user_info
    try:
        content2=soup1.find_all(class_='header-text-download')[0]
        content2=content2.findAll('span')
        for j in range(len(content2)):
            info=content2[j].contents[0]
            
            info=''.join(info)
            info=info.replace(': ','')
            info=info.replace('\n ','').strip()
            
            if(not(bool(re.search(r'\d', info)))):
                continue
            if(bool(re.search(r'¥', info))):
                continue
            
            info=info.split(' 人')
            dic_name=str(info[1])
            dic_info=str(info[0])
            dic[dic_name]=dic_info
    except:
        print('user_info is null')
    
    #score
    try:
        content3=soup1.find_all(class_='app-rating-score')[0].contents
        score=''.join(content3[0])
        dic_name='score'
        dic_info=str(score)
        dic[dic_name]=dic_info
    except:
        print('score is null')
    
    #tag
    try:           
        soup2=soup.find_all(class_='app-tag-body')[0]
        content4=soup2.find_all('a')
        tag_list=''
        for k in content4:
            info=k.string
            info=info.replace('\n ','').strip()
            tag_list=tag_list+str(info)+';'
        dic_name='tag'
        dic_info=tag_list
        dic[dic_name]=dic_info
    except:
        print('tag is null')
    
    #trans_jason
    # new_jdata = json.dumps(dic,ensure_ascii = False, indent = 4)
    list_app.append(dic)
    print(str(i)+str('OK'))
    
    
 
filename = 'C:\\Users\\admin\\Desktop\\Luna的取数宝宝\\20200720\\test2.json'
with open(filename, 'w', encoding = 'UTF-8') as f:
    json.dump(list_app, f, ensure_ascii = False, indent = 2)   

    
df = pd.read_json(filename,encoding="utf-8", orient='records',dtype=False)
df.to_excel('C:\\Users\\admin\\Desktop\\Luna的取数宝宝\\20200720\\taptap_10000_19999.xlsx')       

