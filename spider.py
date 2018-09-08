import requests
import os
from bs4 import BeautifulSoup


headers = {
    'accept': 'application/json, text/plain, */*',
    'accept-encoding': 'gzip, deflate, br',
    'accept-language': 'zh-CN,zh;q=0.9,en-US;q=0.8,en;q=0.7,und;q=0.6',
    'cookie': 'wluuid=WLGEUST-6111380A-0ADF-C74D-4954-87F200ADFF2A; _ga=GA1.3.140875095.1535956804; _ba=BA0.2-20180903-51751-5vt5FTA6p2R8eZreB1dz; bad_ide7dfc0b0-b3b6-11e7-b58e-df773034efe4=306962d1-af44-11e8-903c-77e237499e3f; weilisessionid=6223b5a9a4ef68630ecc52648f92b478; _gid=GA1.3.553211351.1536215141; accessId=e7dfc0b0-b3b6-11e7-b58e-df773034efe4; pageViewNum=1; nice_ide7dfc0b0-b3b6-11e7-b58e-df773034efe4=af1e9901-b19d-11e8-903c-77e237499e3f; webp_enabled=1',
    'referer': 'https://stock.tuchong.com/free/search/?term=%E9%A3%8E%E6%99%AF',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.81 Safari/537.36',
    '/x-requested-with': 'XMLHttpRequest'
}


# 根据关键字获取image_id
def get_image_id(term, page):
    try:
        print('获取图片ID.....')
        url = 'https://stock.tuchong.com/api/free/search/?term=' + term + '&size=200&page=' + str(page)
        req = requests.get(url, headers=headers)
        if req.status_code == 200:
            # file = open('C:/Users/edong-1/Desktop\log.txt', 'w')
            # file.write(req.text)
            json_image_id = req.json()
            parse_json(json_image_id)
    except ConnectionError:
        return None


# 解析包含image id 的 json
def parse_json(json_image_id):
    print('解析包含 image id json.....')
    hits = json_image_id.get('data').get('hits')
    print(hits)
    if hits:
        print('解析 hit 获取 image id')
        for item in hits:
            id = item.get('imageId')
            get_image_res(id)


# 根据image id 获取图片资源
def get_image_res(id):
    if id:
        try:
            print('拼接图片访问页面url')
            url = 'https://stock.tuchong.com/free/image/?imageId='+id
            req = requests.get(url, headers=headers)
            if req.status_code == 200:
                parse_image_url(req.text)
        except ConnectionError:
            return None


#  解析HTML拿到图片URL
def parse_image_url(html):
    if html:
        print('解析图片页面html')
        soup = BeautifulSoup(html)
        divs = soup.find_all("div", class_="image-cover")
        file_path = 'D:/temp/picture/'
        if not os.path.exists(file_path):
            os.makedirs(file_path)
        for div in divs:
            url = "http:"+div.img['src']
            down_image(url, file_path)


# 根据URL下载图片
def down_image(url, file_path):
    path = file_path+url.split('/')[-1]
    print(url+' - - - '+path)
    response = requests.get(url)
    with open(path, "wb") as file:
        file.write(response.content)


# 爬图虫网图片
def main():
    term = input("输入要搜索的内容:")
    get_image_id(term, 1)


if __name__ == "__main__":
    main()
