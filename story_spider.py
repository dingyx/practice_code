import requests
import os
from bs4 import BeautifulSoup


def get_story_info(url, file):
    res = requests.get(url)
    res.encoding = 'utf-8'
    if res.status_code == 200:
        print("request success:"+url+"\n")
        print(res.text)
        file.write(res.text)
    else:
        print("request fail:"+url+"\n")


def main():

    # 创建一个文件 写入 Hello World
    file = open('C:/Users/edong-1/Desktop\story.txt', 'w', encoding='utf-8')
    # 2 - 12200
    for num in range(2, 4):
        get_story_info("http://www.gushi365.com/info/%s.html" % num, file)
        file.flush()


if __name__ == "__main__":
    main()
