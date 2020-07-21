import requests
import pandas as pd
from requests.exceptions import RequestException

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

        
url='https://www.taptap.com/app/200000'
html = get_page_index(url)

luna=pd.DataFrame(columns = ['app'])

url='https://www.taptap.com/app/{}'
for i in range(200000):
    url_test=url.format(i)
    html = get_page_index(url_test)
    if(html!=None):
        new_i=pd.DataFrame({'app':i},index=[0])
        luna=luna.append(new_i,ignore_index=True)
        print(str(i)+'OK')
    else:
        print(str(i)+'NO')
